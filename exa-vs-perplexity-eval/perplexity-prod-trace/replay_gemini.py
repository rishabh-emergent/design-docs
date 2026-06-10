#!/usr/bin/env python3
"""
Replay the SAME 5 real prod tool inputs through the Gemini research path,
byte-identical to our server-tools implementation (llm-proxy-service PR #348):

- Model: gemini-3.1-pro-preview
- Tools: google_search grounding enabled
- generationConfig: responseMimeType text/plain, maxOutputTokens 8192
- systemInstruction = same Integration_Playbook_Expert template ({stack} joined)
- user content     = same user prompt template ({query} + {stack})
- NOT sent: temperature, topP, topK (prod sends none)

Prod note: the service tries Vertex AI first, then the direct Gemini API —
identical model + request semantics. This replay uses the direct API.

Cost: Gemini returns exact token counts (usageMetadata) but no dollar cost.
Dollar figures = exact tokens x published rates ($2/1M input, $12/1M output)
+ $0.014/call google_search grounding fee ($14/1k grounded prompts).
"""
import concurrent.futures as cf
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from replay import SAMPLES, SYSTEM_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE

OUT = Path(__file__).parent / "samples_gemini"
OUT.mkdir(exist_ok=True)


def _gcloud_secret(name, project):
    return subprocess.run(
        ["gcloud", "secrets", "versions", "access", "latest", "--secret", name, "--project", project],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or _gcloud_secret("GEMINI_API_KEY", "emergent-default")
MODEL = "gemini-3.1-pro-preview"
INPUT_PER_M, OUTPUT_PER_M, GROUNDING_PER_CALL = 2.00, 12.00, 0.014


def run_sample(s):
    stack = ", ".join(s["tech_stack"])
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(stack=stack)
    user_prompt = USER_PROMPT_TEMPLATE.format(query=s["query"], stack=stack)
    body = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "tools": [{"googleSearch": {}}],
        "generationConfig": {"responseMimeType": "text/plain", "maxOutputTokens": 8192},
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key=GEMINI-REDACTED-MOCK-KEY"
    real_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_KEY}"

    print(f"[{s['id']}] firing...", flush=True)
    t0 = time.time()
    req = urllib.request.Request(real_url, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            status = resp.status
            response_body = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        latency = time.time() - t0
        print(f"[{s['id']}] FAILED after {latency:.1f}s: {e}", flush=True)
        (OUT / f"{s['id']}.json").write_text(json.dumps({"sample": s["id"], "error": str(e), "latency_s": latency}, indent=2))
        return

    latency = time.time() - t0
    cand = response_body.get("candidates", [{}])[0]
    content = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
    gm = cand.get("groundingMetadata", {}) or {}
    citations = []
    for ch in gm.get("groundingChunks", []) or []:
        uri = (ch.get("web") or {}).get("uri")
        if uri and uri not in citations:
            citations.append(uri)
    usage = response_body.get("usageMetadata", {}) or {}
    in_tok = usage.get("promptTokenCount", 0)
    out_tok = usage.get("candidatesTokenCount", 0)
    token_cost = (in_tok / 1e6) * INPUT_PER_M + (out_tok / 1e6) * OUTPUT_PER_M
    total_cost = token_cost + GROUNDING_PER_CALL

    record = {
        "sample_id": s["id"],
        "agent_input": s["query"],
        "tech_stack": s["tech_stack"],
        "request": {"url": url, "method": "POST",
                    "headers": {"Content-Type": "application/json"}, "body": body},
        "http_status": status,
        "latency_s": round(latency, 1),
        "computed_cost": {
            "input_tokens_cost": round((in_tok / 1e6) * INPUT_PER_M, 5),
            "output_tokens_cost": round((out_tok / 1e6) * OUTPUT_PER_M, 5),
            "grounding_fee": GROUNDING_PER_CALL,
            "total_cost": round(total_cost, 5),
            "basis": "exact usageMetadata tokens x published rates ($2/1M in, $12/1M out) + $0.014 grounding fee",
        },
        "citations_extracted": citations,
        "response": response_body,
    }
    (OUT / f"{s['id']}.json").write_text(json.dumps(record, indent=2))
    print(f"[{s['id']}] OK {latency:.1f}s  cost=${total_cost:.4f}  content={len(content)} ch  citations={len(citations)}  tokens in/out={in_tok}/{out_tok}", flush=True)


def main():
    todo = [s for s in SAMPLES if not (OUT / f"{s['id']}.json").exists()]
    print(f"Replaying {len(todo)} samples via Gemini ({MODEL}, google_search grounding)...")
    with cf.ThreadPoolExecutor(max_workers=5) as ex:
        list(ex.map(run_sample, todo))
    print("Done.")


if __name__ == "__main__":
    main()
