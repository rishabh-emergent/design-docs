#!/usr/bin/env python3
"""
Pilot harness — call Exa Research + Perplexity Deep Research in parallel for N integrations.
Mirrors the exact prompt templates in llm-proxy-service/pkg/tools/{exa,perplexity}/client.go.
"""
import concurrent.futures as cf
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# ---- Keys ----
def _gcloud_secret(name, project):
    out = subprocess.run(
        ["gcloud", "secrets", "versions", "access", "latest", "--secret", name, "--project", project],
        capture_output=True, text=True, check=True
    )
    return out.stdout.strip()

EXA_KEY = os.environ.get("EXA_API_KEY") or _gcloud_secret("EXA_API_KEY", "emergent-default")
PPLX_KEY = os.environ.get("PERPLEXITY_API_KEY") or _gcloud_secret("PERPLEXITY_API_KEY", "emergent-default")

# ---- Prompts — VERBATIM from server-tools source ----
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


def integration_prompts(integ):
    stack = ", ".join(integ["tech_stack"])
    sys_p = SYSTEM_TEMPLATE.format(stack=stack)
    # Augment user prompt with the eval constraint snippet (so research backend
    # sees the same context it'd see in real prod — INTEGRATION/CONSTRAINTS shape).
    user_p = USER_TEMPLATE.format(query=integ["query"], stack=stack) + "\n\n" + integ["constraints"].strip()
    return sys_p, user_p


def _post(url, headers, body, timeout=600):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _get(url, headers, timeout=60):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


# ---- Exa Research API: POST /research/v1 + poll ----
def call_exa(integ):
    sys_p, user_p = integration_prompts(integ)
    instructions = sys_p + "\n\n" + user_p
    t0 = time.time()
    try:
        status, body = _post(
            "https://api.exa.ai/research/v1",
            {"x-api-key": EXA_KEY, "Content-Type": "application/json"},
            {"instructions": instructions, "model": "exa-research-pro"},
            timeout=120,
        )
        if status >= 300:
            return {"provider": "exa", "ok": False, "error": f"start http {status}", "raw": body, "latency_s": time.time() - t0}
        rid = body.get("researchId")
        if not rid:
            return {"provider": "exa", "ok": False, "error": "no researchId", "raw": body, "latency_s": time.time() - t0}
        # Poll
        deadline = time.time() + 600  # 10 min max
        while time.time() < deadline:
            time.sleep(5)
            s, poll = _get(f"https://api.exa.ai/research/v1/{rid}", {"x-api-key": EXA_KEY})
            st = poll.get("status")
            if st in ("completed", "failed", "canceled"):
                content = (poll.get("output") or {}).get("content", "")
                cost = (poll.get("costDollars") or {}).get("total")
                return {
                    "provider": "exa",
                    "ok": st == "completed",
                    "research_id": rid,
                    "status": st,
                    "content": content,
                    "cost_dollars": cost,
                    "latency_s": time.time() - t0,
                    "instructions": instructions,
                    "raw_terminal": poll,
                }
        return {"provider": "exa", "ok": False, "error": "timeout", "research_id": rid, "latency_s": time.time() - t0, "instructions": instructions}
    except Exception as e:
        return {"provider": "exa", "ok": False, "error": str(e), "latency_s": time.time() - t0, "instructions": instructions}


# ---- Perplexity: POST /chat/completions (sonar-deep-research) ----
def call_perplexity(integ):
    sys_p, user_p = integration_prompts(integ)
    t0 = time.time()
    try:
        # sonar-deep-research can take 60-300s. Generous timeout.
        status, body = _post(
            "https://api.perplexity.ai/chat/completions",
            {"Authorization": f"Bearer {PPLX_KEY}", "Content-Type": "application/json"},
            {
                "model": "sonar-deep-research",
                "messages": [
                    {"role": "system", "content": sys_p},
                    {"role": "user", "content": user_p},
                ],
            },
            timeout=900,
        )
        if status >= 300:
            return {"provider": "perplexity", "ok": False, "error": f"http {status}", "raw": body, "latency_s": time.time() - t0}
        choices = body.get("choices") or []
        content = choices[0]["message"]["content"] if choices else ""
        return {
            "provider": "perplexity",
            "ok": True,
            "content": content,
            "citations": body.get("citations", []),
            "usage": body.get("usage", {}),
            "model": body.get("model", "sonar-deep-research"),
            "latency_s": time.time() - t0,
            "system_prompt": sys_p,
            "user_prompt": user_p,
            "raw": body,
        }
    except urllib.error.HTTPError as e:
        return {"provider": "perplexity", "ok": False, "error": f"http {e.code} {e.read()[:300]!r}", "latency_s": time.time() - t0}
    except Exception as e:
        return {"provider": "perplexity", "ok": False, "error": str(e), "latency_s": time.time() - t0}


def run_one(integ):
    """Fire both providers in parallel for a single integration."""
    fp = RESULTS / f"{integ['id']}.json"
    if fp.exists():
        existing = json.loads(fp.read_text())
        # Skip only if BOTH providers succeeded previously.
        if existing.get("exa", {}).get("ok") and existing.get("perplexity", {}).get("ok"):
            print(f"[{integ['id']}] {integ['name']} — SKIP (already complete)", flush=True)
            return existing
    print(f"[{integ['id']}] {integ['name']} — starting both providers...", flush=True)
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        fut_exa = ex.submit(call_exa, integ)
        fut_pplx = ex.submit(call_perplexity, integ)
        exa = fut_exa.result()
        pplx = fut_pplx.result()

    out = {
        "integration": integ,
        "exa": exa,
        "perplexity": pplx,
        "ts": int(time.time()),
    }
    fp = RESULTS / f"{integ['id']}.json"
    fp.write_text(json.dumps(out, indent=2))
    print(
        f"[{integ['id']}] done. exa={'OK' if exa.get('ok') else 'FAIL'} ({exa.get('latency_s', 0):.1f}s, {len(exa.get('content', ''))} ch) | "
        f"pplx={'OK' if pplx.get('ok') else 'FAIL'} ({pplx.get('latency_s', 0):.1f}s, {len(pplx.get('content', ''))} ch)",
        flush=True,
    )
    return out


def load_integrations(path=None):
    import yaml  # delayed import in case host lacks it
    p = Path(path) if path else (ROOT / "integrations.yaml")
    with open(p) as f:
        return yaml.safe_load(f)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    integs = load_integrations(path)
    print(f"Loaded {len(integs)} integrations. Starting {len(integs)*2} parallel API calls (bounded concurrency 4)...", flush=True)
    t0 = time.time()
    # Each call_pair already runs 2 providers in parallel.
    # Bound integration-level concurrency to 4 → max 8 outbound HTTP calls in flight.
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(run_one, integs))
    elapsed = time.time() - t0
    summary = {
        "elapsed_s": elapsed,
        "n_integrations": len(integs),
        "by_provider": {
            "exa": {
                "ok": sum(1 for r in results if r["exa"].get("ok")),
                "avg_latency_s": sum(r["exa"].get("latency_s", 0) for r in results) / len(results),
                "avg_chars": sum(len(r["exa"].get("content", "")) for r in results) / len(results),
                "total_cost_dollars": sum(r["exa"].get("cost_dollars", 0) or 0 for r in results),
            },
            "perplexity": {
                "ok": sum(1 for r in results if r["perplexity"].get("ok")),
                "avg_latency_s": sum(r["perplexity"].get("latency_s", 0) for r in results) / len(results),
                "avg_chars": sum(len(r["perplexity"].get("content", "")) for r in results) / len(results),
            },
        },
    }
    (RESULTS / "_run_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n=== Stage 1 done ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
