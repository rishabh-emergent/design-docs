#!/usr/bin/env python3
"""
Third arm: Exa /search (semantic neural search) → Claude Haiku 4.5 synthesis.

Two-step pipeline:
  1. POST api.exa.ai/search with useAutoprompt=true, numResults=15, contents={text,highlights}
  2. Pass retrieved sources to Claude Haiku 4.5 with the SAME
     Integration_Playbook_Expert system prompt + integration constraints

Mirrors the architecture described in Manish/Sachin's eval doc and the two-step
approach we discussed earlier in this session. Cost: Exa $7/1k searches + $1/1k pages
+ Claude Haiku ($0.80/1M input, $4.0/1M output).
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

def _gcloud_secret(name, project):
    out = subprocess.run(
        ["gcloud", "secrets", "versions", "access", "latest", "--secret", name, "--project", project],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()

EXA_KEY = os.environ.get("EXA_API_KEY") or _gcloud_secret("EXA_API_KEY", "emergent-default")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY") or _gcloud_secret("ANTHROPIC_API_KEY", "emergent-default")
HAIKU_MODEL = "claude-haiku-4-5-20251001"
HAIKU_INPUT_PER_M  = 0.80
HAIKU_OUTPUT_PER_M = 4.00

# Same prompts as Perplexity / Exa Research arms — VERBATIM from server-tools source.
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


def _post_json(url, headers, body, timeout=120):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def exa_search(query, num_results=15, timeout=60):
    """Exa /search — semantic neural search. Returns top-N URLs + text + highlights."""
    body = {
        "query": query,
        "numResults": num_results,
        "type": "neural",
        "useAutoprompt": True,
        "contents": {
            "text": {"maxCharacters": 8000},
            "highlights": {"numSentences": 5, "highlightsPerUrl": 3},
            "summary": True,
        },
    }
    status, body = _post_json(
        "https://api.exa.ai/search",
        {"x-api-key": EXA_KEY, "Content-Type": "application/json"},
        body,
        timeout=timeout,
    )
    return status, body


def format_search_results(exa_resp, max_chars_per_result=4000):
    """Build a single context string from Exa /search results."""
    results = exa_resp.get("results", [])
    blocks = []
    for i, r in enumerate(results, 1):
        url = r.get("url", "")
        title = r.get("title", "")
        published = r.get("publishedDate", "")
        summary = r.get("summary", "")
        highlights = r.get("highlights", []) or []
        text = (r.get("text") or "")[:max_chars_per_result]
        block = f"[Source {i}] {title}\nURL: {url}"
        if published:
            block += f"\nPublished: {published}"
        if summary:
            block += f"\nSummary: {summary}"
        if highlights:
            block += "\nKey highlights:\n- " + "\n- ".join(highlights[:5])
        if text:
            block += f"\n\nContent:\n{text}"
        blocks.append(block)
    return "\n\n---\n\n".join(blocks), [r.get("url", "") for r in results]


def haiku_synthesize(sys_prompt, user_prompt, search_context):
    """Call Claude Haiku 4.5 with retrieved sources."""
    user_msg = f"""{user_prompt}

You have access to the following web sources retrieved via search. Use them to construct an accurate, current playbook. Cite sources inline as [N] (matching source numbers below).

================================================================================
RETRIEVED SOURCES
================================================================================
{search_context}
================================================================================

Now produce the integration playbook. Be specific (exact package versions, real endpoint URLs from the sources, exact env var names). Include code that compiles. End with a SOURCES section listing each [N] URL used."""

    body = {
        "model": HAIKU_MODEL,
        "max_tokens": 8000,
        "system": sys_prompt,
        "messages": [{"role": "user", "content": user_msg}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        api = json.loads(resp.read().decode("utf-8"))
    text = "".join(b.get("text", "") for b in api.get("content", []) if b.get("type") == "text").strip()
    return text, api.get("usage", {})


def call_exa_search_arm(integ):
    """Run the two-step pipeline for one integration."""
    stack = ", ".join(integ["tech_stack"])
    sys_prompt = SYSTEM_TEMPLATE.format(stack=stack)
    user_prompt = USER_TEMPLATE.format(query=integ["query"], stack=stack) + "\n\n" + integ["constraints"].strip()
    # Build a search query oriented toward official-docs retrieval.
    search_query = f"{integ['query']} {stack} integration setup guide official documentation"

    t0 = time.time()
    try:
        t_search0 = time.time()
        status, search_resp = exa_search(search_query)
        t_search = time.time() - t_search0
        if status >= 300:
            return {"provider": "exa_search_haiku", "ok": False, "error": f"search http {status}", "latency_s": time.time() - t0, "raw_search": search_resp}
        search_context, urls = format_search_results(search_resp)
        if not urls:
            return {"provider": "exa_search_haiku", "ok": False, "error": "no search results", "latency_s": time.time() - t0}

        t_syn0 = time.time()
        synthesized, usage = haiku_synthesize(sys_prompt, user_prompt, search_context)
        t_syn = time.time() - t_syn0

        # Cost calculation
        in_tok = usage.get("input_tokens", 0)
        out_tok = usage.get("output_tokens", 0)
        haiku_cost = (in_tok / 1_000_000) * HAIKU_INPUT_PER_M + (out_tok / 1_000_000) * HAIKU_OUTPUT_PER_M
        # Exa /search: $7/1K searches = $0.007 per search.
        # Pages with text content: $1/1K = $0.001 each. Highlights: $1/1K = $0.001 each.
        n_results = len(search_resp.get("results", []))
        exa_cost = 0.007 + n_results * 0.001 + n_results * 0.001  # search + text + highlights
        total_cost = haiku_cost + exa_cost

        return {
            "provider": "exa_search_haiku",
            "ok": True,
            "content": synthesized,
            "citations": urls,
            "latency_s": time.time() - t0,
            "latency_search_s": t_search,
            "latency_synth_s": t_syn,
            "search_query_used": search_query,
            "n_search_results": n_results,
            "haiku_usage": usage,
            "cost_breakdown": {
                "exa_search_dollars": round(exa_cost, 4),
                "haiku_dollars": round(haiku_cost, 4),
                "total_dollars": round(total_cost, 4),
            },
            "system_prompt": sys_prompt,
            "user_prompt": user_prompt,
        }
    except urllib.error.HTTPError as e:
        return {"provider": "exa_search_haiku", "ok": False, "error": f"http {e.code} {e.read()[:300]!r}", "latency_s": time.time() - t0}
    except Exception as e:
        return {"provider": "exa_search_haiku", "ok": False, "error": str(e), "latency_s": time.time() - t0}


def run_one(integ):
    fp = RESULTS / f"{integ['id']}.json"
    if not fp.exists():
        print(f"[{integ['id']}] WARN — base results not present; skipping", flush=True)
        return None
    existing = json.loads(fp.read_text())
    if existing.get("exa_search_haiku", {}).get("ok"):
        print(f"[{integ['id']}] {integ['name']} — SKIP (exa_search_haiku already done)", flush=True)
        return existing
    print(f"[{integ['id']}] {integ['name']} — running Exa /search + Haiku...", flush=True)
    r = call_exa_search_arm(integ)
    existing["exa_search_haiku"] = r
    fp.write_text(json.dumps(existing, indent=2))
    cost = (r.get("cost_breakdown") or {}).get("total_dollars", 0) if r.get("ok") else 0
    print(
        f"[{integ['id']}] done. status={'OK' if r.get('ok') else 'FAIL'} "
        f"({r.get('latency_s', 0):.1f}s, {len(r.get('content', ''))} ch, ${cost:.3f})",
        flush=True,
    )
    return existing


def main():
    import yaml
    path = sys.argv[1] if len(sys.argv) > 1 else "integrations_full.yaml"
    with open(ROOT / path) as f:
        integs = yaml.safe_load(f)
    print(f"Loaded {len(integs)} integrations. Running Exa /search + Haiku arm (bounded concurrency 8)...", flush=True)
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(run_one, integs))
    elapsed = time.time() - t0
    completed = [r for r in results if r and r.get("exa_search_haiku", {}).get("ok")]
    total_cost = sum((r["exa_search_haiku"]["cost_breakdown"]["total_dollars"]) for r in completed)
    total_chars = sum(len(r["exa_search_haiku"]["content"]) for r in completed)
    total_latency = sum(r["exa_search_haiku"]["latency_s"] for r in completed)
    summary = {
        "elapsed_s": elapsed,
        "n_integrations": len(integs),
        "n_ok": len(completed),
        "avg_latency_s": total_latency / len(completed) if completed else 0,
        "avg_chars": total_chars / len(completed) if completed else 0,
        "total_cost_dollars": round(total_cost, 3),
        "avg_cost_dollars": round(total_cost / len(completed), 4) if completed else 0,
    }
    (RESULTS / "_exa_search_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n=== Exa /search + Haiku arm done ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
