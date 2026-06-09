#!/usr/bin/env python3
"""
Fourth arm: Gemini 3.1 Pro Preview + Google Search Grounding.

Mirrors llm-proxy-service/pkg/gemini/research.go (xtools PR #19 port):
- Model: gemini-3.1-pro-preview
- Tools: googleSearch grounding enabled
- maxOutputTokens: 8192
- Returns synthesized markdown + citations from GroundingMetadata
"""
import concurrent.futures as cf
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def _gcloud_secret(name, project):
    return subprocess.run(
        ["gcloud", "secrets", "versions", "access", "latest", "--secret", name, "--project", project],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


GEMINI_KEY = _gcloud_secret("GEMINI_API_KEY", "emergent-default")
MODEL = "gemini-3.1-pro-preview"
MAX_OUTPUT_TOKENS = 8192

# Gemini 3 pricing (per Manish/Sachin's doc):
INPUT_PER_M = 2.00
OUTPUT_PER_M = 12.00
GROUNDING_PER_CALL = 0.014  # $14/1K grounded prompts

SYSTEM_TEMPLATE = """You are Integration_Playbook_Expert, responsible for creating detailed integration guides.
Research and provide a complete integration playbook for the requested technology that includes:

1. Installation instructions
2. API key setup & security best practices
3. Complete code examples for this tech stack: {stack}
4. Testing procedures
5. Common pitfalls and how to avoid them

Format your response in a structured, step-by-step guide that a developer can follow.
Include all necessary code samples.
If the integration involves API keys, include instructions on where to get them."""

USER_TEMPLATE = "Create a detailed integration playbook for {query} in {stack} application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."


def call_gemini(integ):
    stack = ", ".join(integ["tech_stack"])
    sys_prompt = SYSTEM_TEMPLATE.format(stack=stack)
    user_prompt = USER_TEMPLATE.format(query=integ["query"], stack=stack) + "\n\n" + integ["constraints"].strip()

    body = {
        "systemInstruction": {"parts": [{"text": sys_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "tools": [{"googleSearch": {}}],
        "generationConfig": {
            "responseMimeType": "text/plain",
            "maxOutputTokens": MAX_OUTPUT_TOKENS,
        },
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_KEY}"

    t0 = time.time()
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=300) as resp:
            api = json.loads(resp.read().decode("utf-8"))

        # Parse response
        candidates = api.get("candidates", [])
        if not candidates:
            return {"provider": "gemini_31", "ok": False, "error": "no candidates", "raw": api, "latency_s": time.time() - t0}
        cand = candidates[0]
        parts = cand.get("content", {}).get("parts", [])
        content = "".join(p.get("text", "") for p in parts).strip()

        # Citations from groundingMetadata
        gm = cand.get("groundingMetadata", {}) or {}
        chunks = gm.get("groundingChunks", []) or []
        citations = []
        for ch in chunks:
            web = ch.get("web") or {}
            uri = web.get("uri")
            if uri:
                citations.append(uri)
        citations = list(dict.fromkeys(citations))  # dedupe preserving order

        usage = api.get("usageMetadata", {}) or {}
        in_tok = usage.get("promptTokenCount", 0)
        out_tok = usage.get("candidatesTokenCount", 0)
        total_tok = usage.get("totalTokenCount", 0)
        token_cost = (in_tok / 1_000_000) * INPUT_PER_M + (out_tok / 1_000_000) * OUTPUT_PER_M
        total_cost = token_cost + GROUNDING_PER_CALL

        return {
            "provider": "gemini_31",
            "ok": True,
            "content": content,
            "citations": citations,
            "n_citations": len(citations),
            "latency_s": time.time() - t0,
            "model": MODEL,
            "usage": {"input_tokens": in_tok, "output_tokens": out_tok, "total_tokens": total_tok},
            "cost_breakdown": {
                "tokens_dollars": round(token_cost, 4),
                "grounding_dollars": GROUNDING_PER_CALL,
                "total_dollars": round(total_cost, 4),
            },
            "system_prompt": sys_prompt,
            "user_prompt": user_prompt,
        }
    except urllib.error.HTTPError as e:
        return {"provider": "gemini_31", "ok": False, "error": f"http {e.code} {e.read()[:400]!r}", "latency_s": time.time() - t0}
    except Exception as e:
        return {"provider": "gemini_31", "ok": False, "error": str(e), "latency_s": time.time() - t0}


def run_one(integ):
    fp = RESULTS / f"{integ['id']}.json"
    if not fp.exists():
        print(f"[{integ['id']}] WARN — base results not present; skipping", flush=True)
        return None
    existing = json.loads(fp.read_text())
    if existing.get("gemini_31", {}).get("ok"):
        print(f"[{integ['id']}] {integ['name']} — SKIP (gemini_31 already done)", flush=True)
        return existing
    print(f"[{integ['id']}] {integ['name']} — running Gemini 3.1 Pro + Grounding...", flush=True)
    r = call_gemini(integ)
    existing["gemini_31"] = r
    fp.write_text(json.dumps(existing, indent=2))
    cost = (r.get("cost_breakdown") or {}).get("total_dollars", 0) if r.get("ok") else 0
    cit = r.get("n_citations", 0)
    print(
        f"[{integ['id']}] done. status={'OK' if r.get('ok') else 'FAIL'} "
        f"({r.get('latency_s', 0):.1f}s, {len(r.get('content', ''))} ch, {cit} cit, ${cost:.3f})",
        flush=True,
    )
    if not r.get("ok"):
        print(f"   error: {r.get('error', '')[:200]}", flush=True)
    return existing


def main():
    import yaml
    path = sys.argv[1] if len(sys.argv) > 1 else "integrations_full.yaml"
    with open(ROOT / path) as f:
        integs = yaml.safe_load(f)
    print(f"Loaded {len(integs)} integrations. Running Gemini 3.1 Pro + Grounding (bounded concurrency 8)...", flush=True)
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(run_one, integs))
    elapsed = time.time() - t0
    completed = [r for r in results if r and r.get("gemini_31", {}).get("ok")]
    total_cost = sum((r["gemini_31"]["cost_breakdown"]["total_dollars"]) for r in completed)
    total_chars = sum(len(r["gemini_31"]["content"]) for r in completed)
    total_latency = sum(r["gemini_31"]["latency_s"] for r in completed)
    summary = {
        "elapsed_s": elapsed,
        "n_integrations": len(integs),
        "n_ok": len(completed),
        "avg_latency_s": total_latency / len(completed) if completed else 0,
        "avg_chars": total_chars / len(completed) if completed else 0,
        "total_cost_dollars": round(total_cost, 3),
        "avg_cost_dollars": round(total_cost / len(completed), 4) if completed else 0,
    }
    (RESULTS / "_gemini_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n=== Gemini 3.1 Pro + Grounding arm done ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
