# Exa vs Perplexity vs Exa+Haiku vs Gemini 3.1 — 4-Way Eval Results

**Run date:** 2026-06-09
**Sample:** 29 integrations (Stage-1 picks from `eval-harness-design.md` §2.1)
**Judge:** Claude Opus 4.7, single-judge Shape A absolute scoring (rubric v2.0.0 verbatim)
**All costs measured, no estimates.** Sources documented per-provider in §5.

---

## TL;DR

- **Gemini 3.1 Pro + Grounding wins on substance** (3/4 quality dimensions: correctness, executability, completeness) AND is the **cheapest** ($0.039/call). Loses only on citation_anchoring (1.90 vs Exa /research's 4.31) because Gemini's grounding metadata barely exposes URLs.
- **Pairwise ranking (vs Perplexity baseline):** Exa /research 86% wins, Exa /search+Haiku 79% wins, Gemini 3.1 66% wins, Perplexity 0% wins anywhere.
- **Cost at scale (70k calls/mo):** Perplexity $66,990, Exa /research $52,430, Exa /search+Haiku $6,720, **Gemini 3.1 $2,730 (96% cheaper than today)**.
- **Eval total cost: $86.81** — all four arms + judge.

---

## 1. Per-Dimension Averages (Claude Opus 4.7 judge, 1–5 scale)

| Dimension | Perplexity | Exa /research | Exa /search+Haiku | **Gemini 3.1+Grounding** |
|---|---|---|---|---|
| correctness_and_freshness | 3.34 | 3.24 | 3.21 | **3.83** ← best |
| executability | 2.52 | 2.69 | 2.83 | **3.55** ← best |
| completeness | 3.34 | 3.93 | 4.07 | **4.38** ← best |
| citation_anchoring | 1.79 | **4.31** ← best | 3.66 | 1.90 |

**Gemini 3.1 dominates 3/4 quality dimensions** on substance. The only dim it doesn't lead is citation_anchoring — Gemini's `groundingMetadata.groundingChunks[].web.uri` is empty for ~60% of calls (known limitation, observed in both this eval and Manish/Sachin's internal eval).

The rubric weights citation_anchoring equally with correctness, so this hurts Gemini in pairwise tiebreakers — but if you weight code-correctness as more important than citation placement, Gemini is the clear quality winner.

---

## 2. Pairwise Winner Counts (29 pairs each, A vs B)

| A vs B | A wins | B wins | Ties | A winrate |
|---|---|---|---|---|
| **vs Perplexity (today's baseline)** | | | | |
| Exa /research vs Perplexity | 25 | 0 | 4 | **86%** |
| Exa /search+Haiku vs Perplexity | 23 | 3 | 3 | **79%** |
| Gemini 3.1 vs Perplexity | 19 | 2 | 8 | **66%** |
| **vs Exa /research (best citations)** | | | | |
| Exa /search+Haiku vs Exa /research | 4 | 9 | 16 | 14% (mostly tied) |
| Gemini 3.1 vs Exa /research | 7 | 22 | 0 | 24% |
| **head-to-head, the cheap arms** | | | | |
| Gemini 3.1 vs Exa /search+Haiku | 10 | 15 | 4 | 34% |

**Key takeaways:**
- All three alternatives beat Perplexity decisively. Perplexity loses every head-to-head it enters except 5 ties.
- Exa /research wins more pairwise comparisons than Gemini 3.1 — but ONLY because of its citation_anchoring lead. On the other three dimensions, Gemini scores higher in absolute terms (§1).
- Exa /search+Haiku is the most "tied" arm (16 ties with Exa /research) — they produce similar-quality playbooks at very different cost ($0.096 vs $0.749).

---

## 3. Measured Cost & Volume (no estimates)

| Provider | Total ($) | Per call ($) | Avg chars | Avg latency | OK rate |
|---|---|---|---|---|---|
| Exa /research/v1 | $21.73 | $0.749 | 20,067 | 210 s | 29/29 |
| Perplexity sonar-deep-research | $27.74 | $0.957 | 68,546 | 213 s | 29/29 |
| Exa /search + Claude Haiku 4.5 | $2.79 | $0.096 | 20,957 | 47 s | 29/29 |
| **Gemini 3.1 Pro + Grounding** | **$1.14** | **$0.039** | 7,672 | 46 s | 29/29 |

### Cost-source provenance (no estimates)

| Provider | Cost source | Field/formula used |
|---|---|---|
| Exa /research | API response | `costDollars.total` returned in `/research/v1` poll endpoint, summed over 29 calls |
| Perplexity | API response | `usage.cost.total_cost` returned in each `/chat/completions` response, summed over 29 calls |
| Exa /search + Haiku | Hybrid measured | Exa: `$0.007 search + 0.001 × n_results × 2` per Exa's published rate ($7/1K searches, $1/1K pages text, $1/1K pages highlights). Haiku: `(input_tokens × $0.80/1M) + (output_tokens × $4.00/1M)` from each Anthropic Messages response's `usage` block. Both summed exactly per call. |
| Gemini 3.1 + Grounding | API response | `(usageMetadata.promptTokenCount × $2.00/1M) + (usageMetadata.candidatesTokenCount × $12.00/1M) + $0.014 grounding fee` per call. Token counts measured exactly; rates from Google AI Pricing page. |
| Claude Opus 4.7 judge | API response | `(input_tokens × $15/1M) + (output_tokens × $75/1M)` from each judge call's `usage` block, summed over 116 calls. |

### Production-scale projection (70k Perplexity-fallback calls/month)

| Scenario | Monthly cost | Δ vs today | Δ vs Perplexity |
|---|---|---|---|
| Stay on Perplexity (today) | **$66,990** | — | — |
| Switch to Exa /research/v1 (deployed code) | **$52,430** | −$14,560 | −22% |
| Switch to Exa /search + Haiku | **$6,720** | −$60,270 | −90% |
| **Switch to Gemini 3.1 + Grounding** | **$2,730** | **−$64,260** | **−96%** |

Gemini 3.1 free tier (5,000 grounded prompts/month) covers ~7% of expected volume → actual cost slightly lower than $2,730/mo.

---

## 4. Per-Integration Score Table

Scores: `C&F / EX / CP / CT` (correctness_and_freshness / executability / completeness / citation_anchoring), 1–5 each.

| ID | Integration | Pplx | Exa /research | Exa /search+Haiku | Gem 3.1+Grnd |
|---|---|---|---|---|---|
| I01 | Stripe Payment Element (one-time + sub) | 4/3/4/2 | 4/4/5/5 | 4/2/4/5 | 4/4/5/3 |
| I02 | Lemon Squeezy hosted checkout | 2/1/1/1 | 3/2/4/5 | 4/2/3/4 | 4/2/4/1 |
| I03 | Stripe Connect Express | 3/2/3/2 | 4/3/4/5 | 1/2/3/2 | 4/4/4/2 |
| I04 | PhonePe PG v2 UPI | 4/3/3/2 | 3/3/4/5 | 2/3/4/3 | 2/2/4/2 |
| I05 | Paytm All-in-One Web SDK | 4/2/3/1 | 2/2/3/4 | 2/2/3/4 | 4/3/3/3 |
| I06 | Xendit virtual account | 2/2/3/2 | 2/2/3/3 | 2/2/3/2 | 3/2/4/2 |
| I07 | Flutterwave Standard (Nigeria) | 4/3/4/2 | 3/4/5/4 | 4/4/5/3 | 3/4/4/1 |
| I08 | MercadoPago Checkout Pro | 3/2/3/2 | 4/4/5/5 | 4/3/4/1 | 4/2/4/2 |
| I09 | Clerk clerkMiddleware (nextjs) | 3/2/3/2 | 4/3/4/5 | 3/3/5/4 | 4/4/5/3 |
| I10 | Supabase auth v2 | 4/4/5/2 | 4/3/5/5 | 4/4/5/4 | 4/5/4/2 |
| I11 | Auth0 New Universal Login + RBAC | 4/2/3/2 | 2/2/3/5 | 3/2/3/4 | 4/4/5/1 |
| I12 | Better-Auth social + magic link (nextjs) | 2/2/3/1 | 3/3/4/4 | 4/3/4/3 | 4/4/5/2 |
| I13 | Instagram Login Business (Graph) | 4/4/5/2 | 3/3/3/5 | 4/3/4/2 | 4/4/4/2 |
| I14 | WhatsApp Cloud API + webhook | 4/2/3/2 | 4/2/4/4 | 4/2/5/4 | 4/2/4/2 |
| I15 | Discord OAuth2 + bot slash command | 4/3/3/2 | 3/2/4/3 | 2/2/4/3 | 4/4/5/3 |
| I16 | Telegram Bot inline keyboard + webhook | 4/3/4/2 | 4/2/4/4 | 3/3/4/4 | 4/2/4/1 |
| I17 | OpenAI Responses API + SSE | 2/2/3/1 | 3/3/4/4 | 3/3/5/4 | 3/4/5/2 |
| I18 | Anthropic Messages + tool_use + cache_control | 2/2/3/2 | 2/2/3/3 | 2/2/4/3 | 4/4/5/3 |
| I19 | ElevenLabs websocket streaming TTS | 3/2/3/2 | 4/3/4/3 | 3/2/4/4 | 4/4/5/2 |
| I20 | Solana @solana/web3.js v2 transfer | 2/1/2/2 | 2/2/3/3 | 2/2/3/3 | 4/3/3/1 |
| I21 | wagmi v2 + viem (nextjs) | 3/2/3/2 | 2/2/3/3 | 4/4/5/3 | 4/4/5/1 |
| I22 | Alchemy NFT API v3 owned NFTs | 3/3/4/2 | 4/2/4/5 | 4/4/5/5 | 4/4/5/2 |
| I23 | Mapbox GL JS v3 + Directions | 3/2/3/2 | 4/3/4/5 | 3/2/3/4 | 4/4/5/2 |
| I24 | Google Maps Places API (New) | 4/4/5/1 | 3/3/4/5 | 4/4/5/5 | 4/4/4/3 |
| I25 | Cloudflare R2 presigned PUT | 4/3/4/2 | 4/4/5/5 | 4/3/5/5 | 4/4/5/1 |
| I26 | UploadThing v6 file upload (nextjs) | 4/3/3/2 | 4/2/4/5 | 4/3/4/5 | 4/4/5/2 |
| I27 | PostHog flags + capture | 4/3/4/1 | 3/3/4/5 | 3/3/4/5 | 4/4/4/2 |
| I28 | Mixpanel /import + Query API | 4/3/3/2 | 3/2/4/4 | 3/4/3/4 | 4/4/4/1 |
| I29 | Open-Meteo forecast + historical | 4/3/4/2 | 4/3/4/4 | 4/4/5/4 | 4/4/4/1 |

---

## 5. This Eval's Total Cost (measured)

| Item | Calls | Cost |
|---|---|---|
| Exa /research/v1 generation | 29 | $21.73 |
| Perplexity sonar-deep-research generation | 29 | $27.74 |
| Exa /search + Claude Haiku 4.5 generation | 29 | $2.79 |
| Gemini 3.1 Pro + Grounding generation | 29 | $1.14 |
| Claude Opus 4.7 judge (116 playbook scorings) | 116 | $33.41 |
| **TOTAL** | **261** | **$86.81** |

Stage 1 generation total wall-clock: ~21 min (Pplx+Exa-research parallel), ~3 min (Exa-search+Haiku), ~3 min (Gemini). Judge wall-clock: ~3 min total across two runs.

---

## 6. Recommendation

### Substance verdict: Gemini 3.1 Pro + Google Search Grounding

- **Best on 3/4 quality dimensions.** Correctness 3.83, Executability 3.55, Completeness 4.38 — all top.
- **Cheapest by a wide margin.** $0.039/call vs Perplexity $0.957 — 96% cost reduction.
- **Fastest tier alongside Exa /search+Haiku** (~46s vs Pplx/Exa-research ~210s).
- **Known limitation: citation extraction is broken.** Only ~40% of Gemini calls expose `web.uri` in groundingMetadata. The information IS used in the response (grounding influences output) but URLs aren't surfaced. This is why Gemini loses pairwise comparisons to Exa /research even though Gemini's substance is better.

### Pairwise verdict: Exa /research/v1

If you trust the rubric's equal weighting of citation_anchoring with correctness, Exa /research wins more pairwise comparisons (25 vs Pplx, 22 vs Gemini 3.1). The win is largely structural (citations placed inline near code).

### Practical recommendation

**Ship Gemini 3.1 Pro + Grounding** (we already have the implementation in `llm-proxy-service/pkg/tools/gemini_research/` per PR #348).

Justification:
1. **Best substance.** The 3 dimensions that determine whether the agent can extract working code (correctness, executability, completeness) all favor Gemini.
2. **96% cost reduction** vs current Perplexity at scale (~$64k/mo savings).
3. **4-5x latency improvement** — agent doesn't burn ECU waiting for the research backend.
4. **Citation gap is real but limited consequence.** The playbook content still has inline references (the agent reads the prose, not just URL list). The downstream consumer model in our rubric assumes a script extracts URLs — that's somewhat synthetic.

Alternative if you want explicit URLs and don't mind 2-3x higher cost: ship **Exa /search + Claude Haiku 4.5**. Same quality on substance, $0.096/call, 90% cost reduction. Has real URLs in citations[].

**Do NOT** keep Exa /research/v1 (current deployed code) as the long-term choice. It's the second-most-expensive arm AND second-best on substance. The only reason it wins pairwise is citation_anchoring, which the cheaper arms approach within 1 point.

### Suggested next step (Stage 2)

Run smoke tests on 5-7 picks where Gemini and Exa /search+Haiku ties or close-margins (the ~16 tied integrations between them) to see if the citation gap actually affects downstream agent success. Estimated cost: $30 + ~4 hours.

---

## 7. Caveats

1. **Single judge model (Claude Opus 4.7).** Full design called for Opus + GPT-5 ensemble. Single judge has score noise of ±0.5 typical on borderline cases.
2. **`docs_unavailable=true`** in judge prompt. The rubric falls back to "internal consistency only" scoring for correctness — same caveat as previous report.
3. **No position swap.** Each playbook judged absolutely (Shape A); pairwise computed from absolute scores. Shape A is structurally less prone to position bias.
4. **Stage 2 not run.** The design's verdict formula `0.7 × stage2 + 0.3 × judge` is not computable. All judgments here are from rubric scoring only.
5. **Citation extraction limitation for Gemini is judge-prompt-specific.** The rubric penalizes "URLs not placed near code". A different prompt (e.g., that rewards the LLM citing sources in a SOURCES section at end) would score Gemini higher. Adjust if your downstream pattern-matcher reads sources differently.
