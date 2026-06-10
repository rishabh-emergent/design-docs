# How Emergent calls Perplexity today — exact trace (INTERNAL version)

> **⚠️ For external sharing use [`PERPLEXITY_TRACE.md`](./PERPLEXITY_TRACE.md)** — single self-contained file with all 5 samples fully inlined and internal paths/job-IDs scrubbed. This README is the internal companion (keeps prod job IDs + source file paths for traceability).

**Purpose:** Reference showing exactly how our `integration_playbook_expert_v2` tool calls Perplexity in production — request construction, settings, prompts, and real measured outputs (latency + cost + full responses).

**Method:** We pulled 5 real production tool inputs (from jobs that ran in the last few hours and hit the Perplexity fallback in prod — 4 on the expo template, 1 on the main web template), then replayed them through the byte-identical request construction our production Go service uses. Every number below is measured, not estimated. Full raw request/response JSON for each sample is in [`samples/`](./samples/).

**No assumptions were made.** Prompt templates are verbatim copies from production source (`llm-proxy-service/pkg/tools/perplexity/client.go`), tech-stack values are verbatim from the template registry (`emergent/agents/service/templates/config.yaml`), and the inputs are verbatim agent tool calls from production trajectories.

---

## 1. Where the Perplexity call sits

```
Coding agent (Claude Opus 4.7, orchestrated by our Temporal service)
    │  calls MCP tool: integration_playbook_expert_v2
    │  input: free-text "INTEGRATION: ... CONSTRAINTS: ..." block
    ▼
server-tools (Go MCP server)
    │  1) POST {EA}/api/v1/knowledge/check  {query, run_id, user_id, env_image}
    │     → LLM classifier matches query against our verified-playbook DB
    │
    ├─ knowledge_found = true  → return cached verified playbook (NO Perplexity call)
    │
    └─ knowledge_found = false → response carries tech_stack[] for the job's template
           │
           ▼
       POST https://api.perplexity.ai/chat/completions   ← THE CALL DOCUMENTED HERE
```

- Volume on the Perplexity fallback path: **~16.3k calls measured over a 7-day production window ≈ ~70k calls/month**.
- The fallback fires when the classifier returns `OTHER` (no verified playbook matches the query).

## 2. The exact API call

### Request

```
POST https://api.perplexity.ai/chat/completions
Authorization: Bearer pplx-REDACTED-MOCK-KEY
Content-Type: application/json
```

```json
{
  "model": "sonar-deep-research",
  "messages": [
    { "role": "system", "content": "<SYSTEM PROMPT — see §3>" },
    { "role": "user",   "content": "<USER PROMPT — see §3>" }
  ]
}
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
| HTTP timeout | 25 minutes | shared Go `http.Client` (`internal/mcpserver/registry.go`) |
| Retries | **none** — single attempt | no retry loop at any layer of this path |
| Connection | keep-alive pool (MaxIdleConns 100, MaxIdleConnsPerHost 10) | |

The body contains **only** `model` and `messages`. Everything else is Perplexity's default behavior.

## 3. Prompt construction

Both prompts are assembled in Go (`pkg/tools/perplexity/client.go`). Two inputs vary per call:

- `{query}` — the agent's tool input, embedded **whole and unmodified** (the entire `INTEGRATION: ... CONSTRAINTS: ...` block, newlines included)
- `{stack}` — `strings.Join(tech_stack, ", ")`, where `tech_stack` comes from the EA knowledge-check response for the job's template

### System prompt (verbatim template)

```
You are Integration_Playbook_Expert, responsible for creating detailed integration guides.
Research and provide a complete integration playbook for the requested technology that includes:

1. Installation instructions
2. API key setup & security best practices
3. Complete code examples for this tech stack: {stack}
4. Testing procedures
5. Common pitfalls and how to avoid them

Format your response in a structured, step-by-step guide that a developer can follow.
Include all necessary code samples.
If the integration involves API keys, include instructions on where to get them.
```

### User prompt (verbatim template)

```
Create a detailed integration playbook for {query} in {stack} application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise.
```

Note: because `{query}` is a multi-line block, the assembled user prompt reads like
*"Create a detailed integration playbook for INTEGRATION: Stripe payment integration … CONSTRAINTS: … in expo react native, mongodb database, react native web application. Include all necessary…"* — the full agent message is inlined mid-sentence.

### `tech_stack` values per template (exact, from template registry)

| Template (env image) | `tech_stack` |
|---|---|
| `fastapi_react_mongo_shadcn_base_image` (main web template) | `["reactjs frontend with shadcn", "fastapi backend", "mongodb database"]` |
| `expo_mongo_base_image` (mobile) | `["expo react native", "mongodb database", "react native web"]` |
| `nextjs_mongo_shadcn_base_image` | `["nextjs fullstack", "mongodb database", "shadcn ui"]` |
| `fastapi_react_mongo_base_image` | `["reactjs frontend", "fastapi backend", "mongodb database"]` |
| Fallback if template lookup fails | `["Python", "FastAPI"]` |

Samples 1–4 below ran on `expo_mongo_base_image`, so `{stack}` = `expo react native, mongodb database, react native web`. Sample 5 ran on `fastapi_react_mongo_shadcn_base_image`, so `{stack}` = `reactjs frontend with shadcn, fastapi backend, mongodb database`.

## 4. The 5 samples — real prod inputs, measured results

Each sample is a **real production tool input** (verbatim, from a job in the last few hours that hit the Perplexity fallback), replayed with the exact construction above. Full request + response JSON per sample in [`samples/`](./samples/).

| # | Sample | Prod job | Latency | Total cost | Output | Citations | Search queries |
|---|---|---|---|---|---|---|---|
| 1 | Stripe checkout (Expo school-fee app) | `5573afd7-c9dc…` | **258.3 s** | **$0.837** | 67,943 ch | 42 | 50 |
| 2 | Google Drive CSV upload (FastAPI) | `7abb5ac8-1f08…` | **321.2 s** | **$0.943** | 90,197 ch | 48 | 50 |
| 3 | Custom JWT auth (Expo + FastAPI + Mongo) | `dc6c8b51-79c3…` | **261.7 s** | **$0.916** | 67,328 ch | 41 | 50 |
| 4 | JWT + mocked OTP + roles (Expo) | `da83523f-7735…` | **317.9 s** | **$1.257** | 77,531 ch | 50 | 59 |
| 5 | PayPal checkout (web dropshipping store) | `30cd3e24-f9d2…` | **229.6 s** | **$1.047** | 63,374 ch | 50 | 60 |
| | **Average** | | **277.7 s (4.6 min)** | **$1.000** | 73,274 ch | 46 | 54 |

### Cost composition (from Perplexity's own `usage.cost` field)

| Sample | input | output | citation | **reasoning** | **search** | total |
|---|---|---|---|---|---|---|
| 1 | $0.00046 | $0.10798 | $0.04094 | $0.43766 | $0.25000 | $0.83704 |
| 2 | $0.00051 | $0.14414 | $0.04544 | $0.50285 | $0.25000 | $0.94294 |
| 3 | $0.00051 | $0.10977 | $0.05750 | $0.49826 | $0.25000 | $0.91603 |
| 4 | $0.00053 | $0.13248 | $0.06797 | $0.76137 | $0.29500 | $1.25735 |
| 5 | $0.00039 | $0.10578 | $0.05405 | $0.58689 | $0.30000 | $1.04711 |

→ ~**56% of cost is hidden reasoning tokens** (146k–254k per call), ~**26% is search queries** (50–60 searches per call at $5/1k).

### Token usage (from `usage`)

| Sample | prompt | completion | citation tokens | reasoning tokens |
|---|---|---|---|---|
| 1 | 230 | 13,498 | 20,470 | 145,885 |
| 2 | 254 | 18,018 | 22,718 | 167,616 |
| 3 | 254 | 13,721 | 28,749 | 166,085 |
| 4 | 267 | 16,560 | 33,983 | 253,791 |
| 5 | 195 | 13,222 | 27,027 | 195,629 |

## 5. Sample 1 in full — exact assembled request

This is the byte-exact request body sent for sample 1 (only the API key is mocked). The other three differ only in the `{query}` portion of the user message.

```json
{
  "model": "sonar-deep-research",
  "messages": [
    {
      "role": "system",
      "content": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
    },
    {
      "role": "user",
      "content": "Create a detailed integration playbook for INTEGRATION: Stripe payment integration for Expo React Native mobile app + FastAPI backend. Use case: students/parents pay school registration fee for pondok pesantren (Islamic boarding school). Need test mode payment with checkout session. CONSTRAINTS: Mobile app uses Expo SDK 54, no login (registration ID based), Stripe test keys available in pod environment. in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
    }
  ]
}
```

### Response shape (sample 1; identical structure across all 4)

```json
{
  "id": "0dd8a3aa-1175-4378-bae3-6761683d52f1",
  "model": "sonar-deep-research",
  "object": "chat.completion",
  "created": 1781083466,
  "usage": {
    "prompt_tokens": 230,
    "completion_tokens": 13498,
    "total_tokens": 13728,
    "citation_tokens": 20470,
    "num_search_queries": 50,
    "reasoning_tokens": 145885,
    "cost": {
      "input_tokens_cost": 0.00046,
      "output_tokens_cost": 0.10798,
      "citation_tokens_cost": 0.04094,
      "reasoning_tokens_cost": 0.43766,
      "search_queries_cost": 0.25,
      "total_cost": 0.83704
    }
  },
  "citations": ["https://stripe.com", "https://stripe.com/payments/checkout", "..."],
  "search_results": [
    {
      "title": "Stripe | Financial Infrastructure to Grow Your Revenue",
      "url": "https://stripe.com",
      "snippet": "Stripe is a financial services platform that helps...",
      "source": "web"
    }
  ],
  "choices": [
    {
      "index": 0,
      "finish_reason": "stop",
      "message": { "role": "assistant", "content": "# Stripe Checkout Integration Playbook for an Expo React Native + FastAPI + MongoDB Registration App\n\n..." },
      "delta": { "role": "assistant", "content": "" }
    }
  ]
}
```

- `choices[0].message.content` is one long markdown report (68k–90k characters in our samples) with **inline numeric citation markers** (`[4]`, `[13]`, `[39]`, …) that index into the `citations` array.
- `citations` is a flat array of URL strings; `search_results` carries the same URLs with title + snippet.
- Full content for every sample is in the JSON files — nothing trimmed.

### Output opening lines (one per sample, verbatim)

1. `# Stripe Checkout Integration Playbook for an Expo React Native + FastAPI + MongoDB Registration App`
2. `# Integration Playbook: Google Drive CSV Export with a FastAPI Backend and Expo React Native / React Native Web Clients`
3. `# End-to-End Integration Playbook for JWT-Based Email/Password Authentication with Expo React Native (SDK 54), FastAPI, and MongoDB`
4. `# End-to-end Integration Playbook: JWT Authentication between an Expo React Native App and a FastAPI + MongoDB Backend`
5. `# Integration Playbook: PayPal Checkout for a React (shadcn) + FastAPI + MongoDB Dropshipping Store`

## 6. What we do with the response

In the MCP layer (`pkg/tools/perplexity/tool.go`), before the playbook is handed back to the coding agent:

1. Take `choices[0].message.content` as-is.
2. Append the citations as a plain list:
   ```
   \n\n---\nSources:\n1. https://stripe.com\n2. https://stripe.com/payments/checkout\n...
   ```
3. Wrap into the MCP tool result: `{"content": "<playbook + sources>", "cost": 1.5}` (the `1.5` is an internal billing unit, unrelated to the Perplexity dollar cost).

The coding agent then reads the playbook prose + inline code blocks and writes the integration. (Side note from our trace analysis: agents consume the prose/code but in practice never fetch the citation URLs.)

## 7. Wider measured aggregates

From a separate 29-integration head-to-head we ran against the same API with the same construction (full data in [`../pilot/`](../pilot/)):

| Metric | Value (n=29) |
|---|---|
| Avg latency | 212.5 s |
| Avg cost per call | $0.957 (sum $27.74, from `usage.cost.total_cost`) |
| Avg output length | 68,546 chars |
| Success rate | 29/29 |

At ~70k fallback calls/month, the current Perplexity path costs **≈ $67k/month**.

## 8. Files in this folder

```
perplexity-prod-trace/
├── README.md                          ← this doc (internal version)
├── PERPLEXITY_TRACE.md                ← SHAREABLE single-file version (all samples inlined, internals scrubbed)
├── replay.py                          ← the replay harness (exact prod construction)
├── build_doc.py                       ← generates PERPLEXITY_TRACE.md from samples/
├── replay_log.txt                     ← run log
└── samples/
    ├── sample-1-stripe-expo.json      ← full request + full response + timing (89 KB)
    ├── sample-2-google-drive.json     ← (116 KB)
    ├── sample-3-jwt-auth-expo.json    ← (89 KB)
    ├── sample-4-jwt-otp-roles-expo.json ← (104 KB)
    └── sample-5-paypal-web.json       ← web-stack sample (78 KB)
```

Each sample JSON contains: the prod job id + original prod call timestamp, the exact request (URL, headers with mocked key, full body), HTTP status, measured latency, and the complete unmodified Perplexity response.
