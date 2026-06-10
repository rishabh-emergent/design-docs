#!/usr/bin/env python3
"""Generate PERPLEXITY_TRACE.md — a single self-contained, externally-shareable doc.

Per sample, inlines:
  - the agent's tool input (verbatim)
  - the exact Perplexity API request (mock key)
  - measured latency / cost / tokens
  - the EXACT tool output returned to our agent (playbook content with the
    Sources list appended — byte-identical to what the production MCP layer
    hands back, before the {"content", "cost"} JSON wrapper)

No internal file paths / repo names / service names / job IDs.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
SAMPLES_DIR = HERE / "samples"

ORDER = [
    ("sample-1-stripe-expo", "Stripe checkout — mobile (Expo React Native) school-fee app"),
    ("sample-2-google-drive", "Google Drive CSV upload — FastAPI backend"),
    ("sample-3-jwt-auth-expo", "Custom JWT auth — mobile (Expo React Native)"),
    ("sample-4-jwt-otp-roles-expo", "JWT + mocked OTP + roles — mobile (Expo React Native)"),
    ("sample-5-paypal-web", "PayPal checkout — web (FastAPI + React) store"),
]

FENCE = "`" * 5  # outer fence must exceed any ``` inside playbook content


def load(sid):
    p = SAMPLES_DIR / f"{sid}.json"
    return json.loads(p.read_text()) if p.exists() else None


def fmt_money(x):
    return f"${x:.5f}".rstrip("0").rstrip(".") if x is not None else "—"


def tool_output(resp):
    """Reconstruct the exact string the MCP layer returns to the agent:
    content + "\n\n---\nSources:\n1. <url>\n..." (verbatim production logic)."""
    out = resp["choices"][0]["message"]["content"]
    citations = resp.get("citations", [])
    if citations:
        out += "\n\n---\nSources:\n"
        for i, c in enumerate(citations, 1):
            out += f"{i}. {c}\n"
    return out


def sample_section(idx, title, d):
    req = d["request"]
    resp = d["response"]
    usage = resp.get("usage", {})
    cost = usage.get("cost", {})
    final_output = tool_output(resp)
    query = req["body"]["messages"][1]["content"]
    # Recover the agent's raw tool input: strip the fixed prefix/suffix of the user template.
    agent_input = d.get("agent_input")
    citations = resp.get("citations", [])

    lines = []
    lines.append(f"## Sample {idx}: {title}")
    lines.append("")
    lines.append("| | |")
    lines.append("|---|---|")
    lines.append(f"| HTTP status | {d['http_status']} |")
    lines.append(f"| **Latency** | **{d['latency_s']} s** |")
    lines.append(f"| **Total cost (from Perplexity's `usage.cost`)** | **{fmt_money(cost.get('total_cost'))}** |")
    lines.append(f"| Cost breakdown | input {fmt_money(cost.get('input_tokens_cost'))} · output {fmt_money(cost.get('output_tokens_cost'))} · citation {fmt_money(cost.get('citation_tokens_cost'))} · reasoning {fmt_money(cost.get('reasoning_tokens_cost'))} · search {fmt_money(cost.get('search_queries_cost'))} |")
    lines.append(f"| Tokens | prompt {usage.get('prompt_tokens'):,} · completion {usage.get('completion_tokens'):,} · citation {usage.get('citation_tokens'):,} · reasoning {usage.get('reasoning_tokens'):,} |")
    lines.append(f"| Search queries run by Perplexity internally | {usage.get('num_search_queries')} |")
    lines.append(f"| Playbook length | {len(resp['choices'][0]['message']['content']):,} chars |")
    lines.append(f"| Citations | {len(citations)} |")
    lines.append("")

    lines.append("### Input — what our agent asked the tool (verbatim)")
    lines.append("")
    lines.append("```")
    lines.append(agent_input)
    lines.append("```")
    lines.append("")

    lines.append("### Exact API request sent to Perplexity")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps({
        "url": req["url"],
        "method": req["method"],
        "headers": req["headers"],
        "body": req["body"],
    }, indent=2, ensure_ascii=False))
    lines.append("```")
    lines.append("")

    lines.append(f"### Exact output returned to our agent (verbatim, {len(final_output):,} chars)")
    lines.append("")
    lines.append("This is the complete tool result the coding agent receives — the playbook exactly as Perplexity wrote it, with the citation URLs appended as a `Sources:` list by our tool layer. (It is then wrapped as `{\"content\": \"<below>\", \"cost\": 1.5}` — the `1.5` is an internal billing unit, unrelated to the Perplexity dollar cost.)")
    lines.append("")
    lines.append(f"{FENCE}markdown")
    lines.append(final_output)
    lines.append(FENCE)
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main():
    samples = []
    for sid, title in ORDER:
        d = load(sid)
        if d:
            samples.append((sid, title, d))

    lat = [d["latency_s"] for _, _, d in samples]
    costs = [d["response"]["usage"]["cost"]["total_cost"] for _, _, d in samples]
    chars = [len(d["response"]["choices"][0]["message"]["content"]) for _, _, d in samples]
    cits = [len(d["response"].get("citations", [])) for _, _, d in samples]
    n = len(samples)

    summary_rows = []
    for i, (sid, title, d) in enumerate(samples, 1):
        u = d["response"]["usage"]
        summary_rows.append(
            f"| {i} | {title} | {d['latency_s']} s | {fmt_money(u['cost']['total_cost'])} | "
            f"{len(d['response']['choices'][0]['message']['content']):,} ch | {len(d['response'].get('citations', []))} | {u['num_search_queries']} |"
        )

    doc = HEADER_TEMPLATE.format(
        n=n,
        summary_rows="\n".join(summary_rows),
        avg_lat=f"{sum(lat)/n:.1f}",
        avg_cost=f"${sum(costs)/n:.3f}",
        avg_chars=f"{int(sum(chars)/n):,}",
        avg_cits=f"{sum(cits)/n:.0f}",
    )

    body = "".join(sample_section(i, title, d) for i, (sid, title, d) in enumerate(samples, 1))

    out = doc + body + FOOTER
    (HERE / "PERPLEXITY_TRACE.md").write_text(out)
    print(f"PERPLEXITY_TRACE.md written: {len(out):,} chars, {n} samples inlined")


HEADER_TEMPLATE = """# How we call Perplexity today — exact production trace

**Purpose:** Reference for the Exa team showing exactly how our integration-playbook tool calls Perplexity in production — request construction, settings, prompts — with {n} fully-inlined real samples (measured latency + cost + the complete output our agent receives).

**Method:** We took {n} real production tool inputs (from jobs in the last few hours that hit the Perplexity research path) and replayed them through the byte-identical request construction our production service uses. Every number is measured, not estimated. The prompt templates below are verbatim copies of our production code; the inputs are verbatim agent tool calls from production.

---

## 1. Where the Perplexity call sits

```
Coding agent (Claude Opus 4.7)
    |  calls tool: integration_playbook_expert_v2
    |  input: free-text "INTEGRATION: ... CONSTRAINTS: ..." block
    v
Our tool server
    |  1) internal knowledge-base check: an LLM classifier matches the query
    |     against our DB of pre-verified playbooks
    |
    |- match found  -> return cached verified playbook (NO Perplexity call)
    |
    \\- no match     -> the check also returns the job's tech_stack[]
           |
           v
       POST https://api.perplexity.ai/chat/completions   <- THE CALL DOCUMENTED HERE
```

- Volume on this research path: **~16.3k calls measured over a 7-day production window ≈ ~70k calls/month**.

## 2. The exact API call

```
POST https://api.perplexity.ai/chat/completions
Authorization: Bearer pplx-REDACTED-MOCK-KEY
Content-Type: application/json
```

```json
{{
  "model": "sonar-deep-research",
  "messages": [
    {{ "role": "system", "content": "<SYSTEM PROMPT - see section 3>" }},
    {{ "role": "user",   "content": "<USER PROMPT - see section 3>" }}
  ]
}}
```

### Settings — complete list

| Setting | Value | Notes |
|---|---|---|
| Model | `sonar-deep-research` | hardcoded |
| `temperature` | **not sent** | Perplexity default applies |
| `max_tokens` | **not sent** | Perplexity default applies |
| `top_p` / `top_k` | **not sent** | |
| `stream` | **not sent** (non-streaming) | |
| `search_domain_filter` / `search_recency_filter` | **not sent** | |
| `web_search_options` | **not sent** | |
| HTTP timeout | 25 minutes | |
| Retries | **none** — single attempt | |

The body contains **only** `model` and `messages` — everything else is Perplexity's default behavior.

## 3. Prompt construction

Two inputs vary per call:

- `{{query}}` — the agent's tool input, embedded **whole and unmodified** (the entire `INTEGRATION: ... CONSTRAINTS: ...` block, newlines included)
- `{{stack}}` — comma-joined `tech_stack` of the job's project template

### System prompt (verbatim template)

```
You are Integration_Playbook_Expert, responsible for creating detailed integration guides.
Research and provide a complete integration playbook for the requested technology that includes:

1. Installation instructions
2. API key setup & security best practices
3. Complete code examples for this tech stack: {{stack}}
4. Testing procedures
5. Common pitfalls and how to avoid them

Format your response in a structured, step-by-step guide that a developer can follow.
Include all necessary code samples.
If the integration involves API keys, include instructions on where to get them.
```

### User prompt (verbatim template)

```
Create a detailed integration playbook for {{query}} in {{stack}} application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise.
```

Because `{{query}}` is a multi-line block, the assembled user prompt inlines the full agent message mid-sentence (see each sample's exact request below).

### `tech_stack` values per project template (exact)

| Project template | `tech_stack` |
|---|---|
| Web (main) | `["reactjs frontend with shadcn", "fastapi backend", "mongodb database"]` |
| Mobile | `["expo react native", "mongodb database", "react native web"]` |
| Next.js | `["nextjs fullstack", "mongodb database", "shadcn ui"]` |
| Web (legacy) | `["reactjs frontend", "fastapi backend", "mongodb database"]` |
| Fallback | `["Python", "FastAPI"]` |

## 4. What we do with the response

1. Take `choices[0].message.content` as-is (markdown with inline numeric citation markers like `[4]`, `[13]` that index into the `citations` array).
2. Append the citations as a plain `Sources:` list (exact format visible at the end of every sample output below).
3. Wrap into the tool result: `{{"content": "<playbook + sources>", "cost": 1.5}}` (internal billing unit, unrelated to the Perplexity dollar cost).

The coding agent reads the playbook prose + inline code blocks and writes the integration.

## 5. Samples — summary

| # | Sample | Latency | Total cost | Playbook | Citations | Searches |
|---|---|---|---|---|---|---|
{summary_rows}

**Averages:** latency **{avg_lat} s**, cost **{avg_cost}/call**, playbook **{avg_chars} chars**, **{avg_cits} citations**.

From a separate 29-integration run with the same construction: avg 212.5 s, avg $0.957/call, avg 68,546 chars, 29/29 success. At ~70k research calls/month, the current Perplexity path costs **~$67k/month**.

---

"""

FOOTER = """## Notes

- The API key in all request dumps above is mocked (`pplx-REDACTED-MOCK-KEY`); everything else is byte-exact.
- Cost figures come from the `usage.cost` object Perplexity returns in each response.
"""


if __name__ == "__main__":
    main()
