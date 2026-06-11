#!/usr/bin/env python3
"""
Replay the SAME 5 real prod tool inputs through the Exa Agent API, using the
exact endpoint + config shared by the Exa team:

  POST https://api.exa.ai/agent/runs
  Headers: x-api-key, Exa-Beta: agent-2026-05-07
  Body:    {"query": "...", "effort": "medium"}
  Poll:    GET https://api.exa.ai/agent/runs/{id} until status not in (queued, running)
  Output:  run.output.text (playbook), run.output.grounding (citations), run.costDollars

Prompt construction mirrors our tool's provider-agnostic build: the same
Integration_Playbook_Expert system template + user template (with {query} and
{stack}) concatenated into the single `query` field.
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

OUT = Path(__file__).parent / "samples_exa"
OUT.mkdir(exist_ok=True)


def _gcloud_secret(name, project):
    return subprocess.run(
        ["gcloud", "secrets", "versions", "access", "latest", "--secret", name, "--project", project],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


EXA_KEY = os.environ.get("EXA_API_KEY") or _gcloud_secret("EXA_API_KEY", "emergent-default")
BASE = "https://api.exa.ai/agent/runs"
BETA_HEADER = "agent-2026-05-07"
EFFORT = "medium"
POLL_INTERVAL_S = 5
MAX_WAIT_S = 900


def _req(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "x-api-key": EXA_KEY,
        "Exa-Beta": BETA_HEADER,
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(r, timeout=180) as resp:
        return resp.status, json.loads(resp.read().decode())


def run_sample(s):
    stack = ", ".join(s["tech_stack"])
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(stack=stack)
    user_prompt = USER_PROMPT_TEMPLATE.format(query=s["query"], stack=stack)
    query = system_prompt + "\n\n" + user_prompt
    body = {"query": query, "effort": EFFORT}

    print(f"[{s['id']}] starting run...", flush=True)
    t0 = time.time()
    try:
        status, run = _req("POST", BASE, body)
        run_id = run.get("id")
        polls = 0
        while run.get("status") in ("queued", "running"):
            if time.time() - t0 > MAX_WAIT_S:
                raise TimeoutError(f"exceeded {MAX_WAIT_S}s (status={run.get('status')})")
            time.sleep(POLL_INTERVAL_S)
            _, run = _req("GET", f"{BASE}/{run_id}")
            polls += 1
    except Exception as e:
        latency = time.time() - t0
        print(f"[{s['id']}] FAILED after {latency:.1f}s: {e}", flush=True)
        (OUT / f"{s['id']}.json").write_text(json.dumps({"sample": s["id"], "error": str(e), "latency_s": latency}, indent=2))
        return

    latency = time.time() - t0
    record = {
        "sample_id": s["id"],
        "agent_input": s["query"],
        "tech_stack": s["tech_stack"],
        "request": {
            "url": BASE,
            "method": "POST",
            "headers": {
                "x-api-key": "exa-REDACTED-MOCK-KEY",
                "Exa-Beta": BETA_HEADER,
                "Content-Type": "application/json",
            },
            "body": body,
            "polling": f"GET {BASE}/{{id}} every {POLL_INTERVAL_S}s until status not in (queued, running)",
        },
        "latency_s": round(latency, 1),
        "polls": polls,
        "response": run,
    }
    (OUT / f"{s['id']}.json").write_text(json.dumps(record, indent=2))
    out = run.get("output") or {}
    text = out.get("text", "") or ""
    grounding = out.get("grounding")
    cost = run.get("costDollars")
    print(f"[{s['id']}] {run.get('status')} {latency:.1f}s  cost={json.dumps(cost) if not isinstance(cost,(int,float)) else f'${cost}'}  text={len(text)} ch  grounding={'yes' if grounding else 'none'}", flush=True)


def main():
    todo = [s for s in SAMPLES if not (OUT / f"{s['id']}.json").exists()]
    print(f"Replaying {len(todo)} samples via Exa Agent API (effort={EFFORT})...")
    with cf.ThreadPoolExecutor(max_workers=5) as ex:
        list(ex.map(run_sample, todo))
    print("Done.")


if __name__ == "__main__":
    main()
