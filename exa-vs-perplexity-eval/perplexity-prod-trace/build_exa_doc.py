#!/usr/bin/env python3
"""Generate EXA_TRACE.md — single shareable doc: how we call the Exa Agent API
for the same integration-playbook tool, with the SAME 5 real prod inputs
replayed, plus a 3-way comparison (Exa / Gemini / Perplexity, identical inputs)."""
import json
from pathlib import Path

HERE = Path(__file__).parent
EXA = HERE / "samples_exa"
GEM = HERE / "samples_gemini"
PPLX = HERE / "samples"

ORDER = [
    ("sample-1-stripe-expo", "Stripe checkout — mobile (Expo React Native) school-fee app"),
    ("sample-2-google-drive", "Google Drive CSV upload — FastAPI backend"),
    ("sample-3-jwt-auth-expo", "Custom JWT auth — mobile (Expo React Native)"),
    ("sample-4-jwt-otp-roles-expo", "JWT + mocked OTP + roles — mobile (Expo React Native)"),
    ("sample-5-paypal-web", "PayPal checkout — web (FastAPI + React) store"),
]
FENCE = "`" * 5


def load(d, sid):
    p = d / f"{sid}.json"
    return json.loads(p.read_text()) if p.exists() else None


def exa_citations(run):
    cits, seen = [], set()
    for g in (run.get("output") or {}).get("grounding") or []:
        for c in g.get("citations", []):
            u = c.get("url")
            if u and u not in seen:
                seen.add(u)
                cits.append(u)
    return cits


def tool_output(run):
    out = (run.get("output") or {}).get("text", "")
    cits = exa_citations(run)
    if cits:
        out += "\n\n---\nSources:\n"
        for i, c in enumerate(cits, 1):
            out += f"{i}. {c}\n"
    return out


def fmt_money(x):
    return f"${x:.5f}".rstrip("0").rstrip(".")


def gem_content(gem):
    cand = gem["response"]["candidates"][0]
    return "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))


def main():
    rows, sections, comp_rows = [], [], []
    e_lat, e_cost, e_chars = [], [], []

    for i, (sid, title) in enumerate(ORDER, 1):
        d = load(EXA, sid)
        if not d or "response" not in d:
            continue
        run = d["response"]
        text = (run.get("output") or {}).get("text", "")
        cits = exa_citations(run)
        cost = run["costDollars"]
        usage = run.get("usage", {})
        e_lat.append(d["latency_s"]); e_cost.append(cost["total"]); e_chars.append(len(text))

        rows.append(f"| {i} | {title} | {d['latency_s']} s | {fmt_money(cost['total'])} | {len(text):,} ch | {len(cits)} | {usage.get('searches', '?')} |")

        gem = load(GEM, sid)
        pplx = load(PPLX, sid)
        if gem and pplx:
            p_cost = pplx["response"]["usage"]["cost"]["total_cost"]
            comp_rows.append(
                f"| {i} | {d['latency_s']} / {gem['latency_s']} / {pplx['latency_s']} s | "
                f"{fmt_money(cost['total'])} / {fmt_money(gem['computed_cost']['total_cost'])} / {fmt_money(p_cost)} | "
                f"{len(text):,} / {len(gem_content(gem)):,} / {len(pplx['response']['choices'][0]['message']['content']):,} ch | "
                f"{len(cits)} / {len(gem.get('citations_extracted', []))} / {len(pplx['response'].get('citations', []))} |"
            )

        out = tool_output(run)
        sec = []
        sec.append(f"## Sample {i}: {title}")
        sec.append("")
        sec.append("| | |")
        sec.append("|---|---|")
        sec.append(f"| Run status / stop reason | `{run.get('status')}` / `{run.get('stopReason')}` |")
        sec.append(f"| **Latency** | **{d['latency_s']} s** (incl. {d.get('polls','?')} polls at 5 s) |")
        sec.append(f"| **Total cost (from Exa's `costDollars`)** | **{fmt_money(cost['total'])}** |")
        sec.append(f"| Cost breakdown | agentCompute {fmt_money(cost.get('agentCompute', 0))} · search {fmt_money(cost.get('search', 0))} |")
        sec.append(f"| Usage | agentComputeUnits {usage.get('agentComputeUnits')} · searches {usage.get('searches')} |")
        sec.append(f"| Playbook length | {len(text):,} chars |")
        sec.append(f"| Citations (real doc URLs from `output.grounding`) | {len(cits)} |")
        sec.append("")
        sec.append("### Input — what our agent asked the tool (verbatim, same as the Perplexity/Gemini traces)")
        sec.append("")
        sec.append("```")
        sec.append(d["agent_input"])
        sec.append("```")
        sec.append("")
        sec.append("### Exact API request sent to Exa")
        sec.append("")
        sec.append("```json")
        sec.append(json.dumps({
            "url": d["request"]["url"],
            "method": d["request"]["method"],
            "headers": d["request"]["headers"],
            "body": d["request"]["body"],
            "polling": d["request"]["polling"],
        }, indent=2, ensure_ascii=False))
        sec.append("```")
        sec.append("")
        sec.append(f"### Exact output returned to our agent (verbatim, {len(out):,} chars)")
        sec.append("")
        sec.append("The playbook exactly as Exa Agent wrote it (`output.text`), with the grounding citation URLs appended as a `Sources:` list by our tool layer. Wrapped as `{\"content\": \"<below>\", \"cost\": 1.5}` (internal billing unit, unrelated to the Exa dollar cost).")
        sec.append("")
        sec.append(f"{FENCE}markdown")
        sec.append(out)
        sec.append(FENCE)
        sec.append("")
        sec.append("---")
        sec.append("")
        sections.append("\n".join(sec))

    n = len(e_lat)
    doc = HEADER.format(
        n=n,
        summary_rows="\n".join(rows),
        comp_rows="\n".join(comp_rows),
        avg_lat=f"{sum(e_lat)/n:.1f}",
        avg_cost=f"${sum(e_cost)/n:.3f}",
        avg_chars=f"{int(sum(e_chars)/n):,}",
    )
    (HERE / "EXA_TRACE.md").write_text(doc + "".join(sections) + FOOTER)
    print(f"EXA_TRACE.md written, {n} samples")


HEADER = """# How we call the Exa Agent API for the same playbook tool — exact trace

**Purpose:** Companion to the Perplexity and Gemini traces. We have implemented an Exa-backed variant of the same integration-playbook tool using the **Exa Agent API** endpoint and config shared by the Exa team. This doc shows exactly how we call it, with the **same {n} real production inputs** replayed — measured latency, billed cost, and complete outputs — for a like-for-like 3-way comparison.

**Method:** Same {n} verbatim production tool inputs as the other traces, replayed through the byte-identical request construction of our Exa implementation. The prompt text is IDENTICAL to the Perplexity/Gemini paths (same system + user templates, same tech_stack injection), sent as the Agent API's single `query` field.

---

## 1. The exact API call

```
POST https://api.exa.ai/agent/runs
x-api-key: exa-REDACTED-MOCK-KEY
Exa-Beta: agent-2026-05-07
Content-Type: application/json
```

```json
{{
  "query": "<SAME SYSTEM PROMPT + blank line + SAME USER PROMPT as the other traces>",
  "effort": "medium"
}}
```

Then poll until the run reaches a terminal status:

```
GET https://api.exa.ai/agent/runs/{{id}}     (same headers, every 5 s)
```

### Settings — complete list

| Setting | Value | Notes |
|---|---|---|
| Endpoint | `POST /agent/runs` + `GET /agent/runs/{{id}}` polling | async run model |
| `effort` | `medium` | flat-priced $0.10/call |
| Beta header | `Exa-Beta: agent-2026-05-07` | |
| `outputSchema` | **not sent** | defaults to text output |
| Poll interval / max wait | 5 s / 10 min | |
| Retries | **none** — single run | |

### Prompts

Identical text to the Perplexity trace (section 3 there) — the `Integration_Playbook_Expert` system template with `{{stack}}` and the user template with `{{query}}` embedded whole, concatenated into the single `query` field.

### Cost basis

Exa returns the actual billed cost in every run (`costDollars`) — **flat $0.10 total on every one of our calls**, split into `agentCompute` + `search` components. No estimation needed.

### What we do with the response

1. Take `output.text` as-is (the playbook markdown).
2. Harvest unique citation URLs from `output.grounding[].citations[].url` — these are **real, checkable doc-page links** (e.g. `docs.stripe.com/...`, `docs.expo.dev/...`), present on every call.
3. Append them as the same `Sources:` list format; wrap as `{{"content": ..., "cost": 1.5}}` (internal billing unit).

## 2. Samples — summary (same {n} inputs as the other traces)

| # | Sample | Latency | Billed cost | Playbook | Citation URLs | Searches run |
|---|---|---|---|---|---|---|
{summary_rows}

**Averages:** latency **{avg_lat} s**, cost **{avg_cost}/call (flat)**, playbook **{avg_chars} chars**.

## 3. Three-way comparison — identical inputs (Exa / Gemini / Perplexity)

| # | Latency (s) | Cost | Playbook (chars) | Citation URLs |
|---|---|---|---|---|
{comp_rows}

Reading: each cell is `Exa / Gemini / Perplexity`.

---

"""

FOOTER = """## Notes

- The API key in all request dumps is mocked (`exa-REDACTED-MOCK-KEY`); everything else is byte-exact.
- Exa costs are the actual billed amounts returned in `costDollars`; Perplexity costs are from its `usage.cost`; Gemini costs are computed from exact token counts x published rates (it returns no dollar figure).
"""


if __name__ == "__main__":
    main()
