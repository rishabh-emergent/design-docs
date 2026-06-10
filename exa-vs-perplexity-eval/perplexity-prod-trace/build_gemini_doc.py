#!/usr/bin/env python3
"""Generate GEMINI_TRACE.md — single shareable doc: how we call Gemini for the same
integration-playbook tool, with the SAME 5 real prod inputs replayed, plus a
side-by-side comparison against the Perplexity numbers (same inputs)."""
import json
from pathlib import Path

HERE = Path(__file__).parent
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


def content_of(gem):
    cand = gem["response"]["candidates"][0]
    return "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))


def tool_output(gem):
    out = content_of(gem)
    cits = gem.get("citations_extracted", [])
    if cits:
        out += "\n\n---\nSources:\n"
        for i, c in enumerate(cits, 1):
            out += f"{i}. {c}\n"
    return out


def fmt_money(x):
    return f"${x:.5f}".rstrip("0").rstrip(".")


def main():
    rows, sections, comp_rows = [], [], []
    g_lat, g_cost, g_chars = [], [], []

    for i, (sid, title) in enumerate(ORDER, 1):
        gem = load(GEM, sid)
        pplx = load(PPLX, sid)
        if not gem or "response" not in gem:
            continue
        content = content_of(gem)
        usage = gem["response"].get("usageMetadata", {})
        cost = gem["computed_cost"]
        cits = gem.get("citations_extracted", [])
        g_lat.append(gem["latency_s"]); g_cost.append(cost["total_cost"]); g_chars.append(len(content))

        rows.append(f"| {i} | {title} | {gem['latency_s']} s | {fmt_money(cost['total_cost'])} | {len(content):,} ch | {len(cits)} |")

        if pplx:
            p_u = pplx["response"]["usage"]
            p_content_len = len(pplx["response"]["choices"][0]["message"]["content"])
            comp_rows.append(
                f"| {i} | {gem['latency_s']} s / {pplx['latency_s']} s | "
                f"{fmt_money(cost['total_cost'])} / {fmt_money(p_u['cost']['total_cost'])} | "
                f"{len(content):,} / {p_content_len:,} ch |"
            )

        sec = []
        sec.append(f"## Sample {i}: {title}")
        sec.append("")
        sec.append("| | |")
        sec.append("|---|---|")
        sec.append(f"| HTTP status | {gem['http_status']} |")
        sec.append(f"| **Latency** | **{gem['latency_s']} s** |")
        sec.append(f"| **Total cost (computed)** | **{fmt_money(cost['total_cost'])}** |")
        sec.append(f"| Cost breakdown | input {fmt_money(cost['input_tokens_cost'])} · output {fmt_money(cost['output_tokens_cost'])} · grounding fee {fmt_money(cost['grounding_fee'])} |")
        sec.append(f"| Tokens (exact, from `usageMetadata`) | prompt {usage.get('promptTokenCount', 0):,} · output {usage.get('candidatesTokenCount', 0):,} · total {usage.get('totalTokenCount', 0):,} |")
        sec.append(f"| Playbook length | {len(content):,} chars |")
        sec.append(f"| Citation URLs surfaced in grounding metadata | {len(cits)} |")
        sec.append("")
        sec.append("### Input — what our agent asked the tool (verbatim, same as the Perplexity trace)")
        sec.append("")
        sec.append("```")
        sec.append(gem["agent_input"])
        sec.append("```")
        sec.append("")
        sec.append("### Exact API request sent to Gemini")
        sec.append("")
        sec.append("```json")
        sec.append(json.dumps({
            "url": gem["request"]["url"],
            "method": "POST",
            "headers": gem["request"]["headers"],
            "body": gem["request"]["body"],
        }, indent=2, ensure_ascii=False))
        sec.append("```")
        sec.append("")
        out = tool_output(gem)
        sec.append(f"### Exact output returned to our agent (verbatim, {len(out):,} chars)")
        sec.append("")
        if cits:
            sec.append("Includes the `Sources:` list our tool layer appends when grounding metadata surfaces URLs. Wrapped as `{\"content\": \"<below>\", \"cost\": 1.5}` (internal billing unit).")
        else:
            sec.append("No citation URLs were surfaced in grounding metadata for this call, so no `Sources:` list is appended — the playbook below is the complete tool output. Wrapped as `{\"content\": \"<below>\", \"cost\": 1.5}` (internal billing unit).")
        sec.append("")
        sec.append(f"{FENCE}markdown")
        sec.append(out)
        sec.append(FENCE)
        sec.append("")
        sec.append("---")
        sec.append("")
        sections.append("\n".join(sec))

    n = len(g_lat)
    doc = HEADER.format(
        n=n,
        summary_rows="\n".join(rows),
        comp_rows="\n".join(comp_rows),
        avg_lat=f"{sum(g_lat)/n:.1f}",
        avg_cost=f"${sum(g_cost)/n:.4f}",
        avg_chars=f"{int(sum(g_chars)/n):,}",
    )
    (HERE / "GEMINI_TRACE.md").write_text(doc + "".join(sections) + FOOTER)
    print(f"GEMINI_TRACE.md written, {n} samples")


HEADER = """# How we call Gemini for the same playbook tool — exact trace

**Purpose:** Companion to the Perplexity trace. We have implemented a Gemini-backed variant of the same integration-playbook tool. This doc shows exactly how it calls Gemini, with the **same {n} real production inputs** replayed — measured latency, cost, and complete outputs — so the two providers can be compared like-for-like.

**Method:** Same {n} verbatim production tool inputs as the Perplexity trace, replayed through the byte-identical request construction of our Gemini implementation. The prompt templates are IDENTICAL to the Perplexity path (same system + user templates, same tech_stack injection) — only the provider call differs.

---

## 1. The exact API call

Our service calls Gemini's `generateContent` with the built-in `google_search` grounding tool (it can route via Vertex AI or the direct Gemini API — identical model and request semantics; these samples were measured via the direct API):

```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key=GEMINI-REDACTED-MOCK-KEY
Content-Type: application/json
```

```json
{{
  "systemInstruction": {{ "parts": [ {{ "text": "<SAME SYSTEM PROMPT as the Perplexity trace>" }} ] }},
  "contents": [ {{ "role": "user", "parts": [ {{ "text": "<SAME USER PROMPT as the Perplexity trace>" }} ] }} ],
  "tools": [ {{ "googleSearch": {{}} }} ],
  "generationConfig": {{ "responseMimeType": "text/plain", "maxOutputTokens": 8192 }}
}}
```

### Settings — complete list

| Setting | Value | Notes |
|---|---|---|
| Model | `gemini-3.1-pro-preview` | hardcoded |
| Grounding | `google_search` built-in tool | Gemini runs the searches internally |
| `maxOutputTokens` | 8192 | |
| `responseMimeType` | `text/plain` | |
| `temperature` / `topP` / `topK` | **not sent** | Gemini defaults apply |
| Retries | provider-level fallback only (Vertex → direct API) | no call-level retry |

### Prompts

Identical templates to the Perplexity trace (section 3 there) — same `Integration_Playbook_Expert` system prompt with `{{stack}}`, same user prompt with `{{query}}` embedded whole.

### Cost basis

Gemini returns exact token counts (`usageMetadata`) but no dollar figure. Costs below = exact tokens x published list rates (**$2/1M input, $12/1M output**) + **$0.014/call** google_search grounding fee ($14/1k grounded prompts).

### What we do with the response

1. Concatenate all text parts of the first candidate (the playbook markdown).
2. Extract unique citation URLs from `groundingMetadata.groundingChunks[].web.uri`. In practice Gemini often surfaces few or zero URLs here even though grounding ran (visible from the per-call search activity) — the playbook content itself is still search-grounded.
3. If any URLs were surfaced, append them as the same `Sources:` list format; wrap as `{{"content": ..., "cost": 1.5}}` (internal billing unit).

## 2. Samples — summary (same {n} inputs as the Perplexity trace)

| # | Sample | Latency | Total cost | Playbook | Citation URLs |
|---|---|---|---|---|---|
{summary_rows}

**Averages:** latency **{avg_lat} s**, cost **{avg_cost}/call**, playbook **{avg_chars} chars**.

## 3. Side-by-side vs Perplexity (identical inputs)

| # | Latency (Gemini / Perplexity) | Cost (Gemini / Perplexity) | Playbook (Gemini / Perplexity) |
|---|---|---|---|
{comp_rows}

---

"""

FOOTER = """## Notes

- The API key in all request dumps is mocked (`GEMINI-REDACTED-MOCK-KEY`); everything else is byte-exact.
- Token counts are exact (from Gemini's `usageMetadata`); dollar figures are computed from published list rates as described in section 1.
"""


if __name__ == "__main__":
    main()
