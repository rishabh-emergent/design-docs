# Exa vs Perplexity — Full 29-Integration Eval Results

**Run date:** 2026-06-09
**Methodology:** Live API calls (Exa Research Pro `/research/v1` + Perplexity `sonar-deep-research`) → Claude Opus 4.7 single-judge (Shape A absolute, rubric v2.0.0 verbatim from `eval-harness-design.md`) → pairwise winners computed locally per the TIE RULES.

---

## TL;DR

- **Exa wins 25/29 pairs (86%). Perplexity wins 0/29 (0%). Ties 4/29 (14%).**
- BUT — drill into the dimensions: **on correctness_and_freshness alone, Perplexity is marginally better** (10 head-to-head wins vs 9, 10 ties). Exa's overall victory is driven by **citation_anchoring**, where it leads 4.31 vs 1.79 on a 1-5 scale.
- **Cost: $54.11 total** for full run — measured: Exa $21.73, **Perplexity $27.74** (from `usage.cost.total_cost` field — Pplx is 21.7% MORE expensive than Exa per call, NOT cheaper), Judge $4.64 est. Stage 1 wall-clock: 21.3 min.
- **Verdict (qualified): SHIP EXA**, with caveats — the win is structural (better citation placement, less verbose, more complete playbook structure), not code-correctness. Both providers under-perform on actual correctness (~3.2 avg / 5), meaning Stage 2 smoke tests will still find broken code regardless of provider.

---

## 1. Pairwise Results (29 integrations)

### Winner counts
| Winner | Count | % |
|---|---|---|
| **Exa** | **25** | **86%** |
| Perplexity | 0 | 0% |
| Tie | 4 | 14% |

### Per-integration scores

Score format: `C&F / EX / CP / CT` (Correctness_and_Freshness / Executability / Completeness / Citation_anchoring), each 1-5.

| ID | Integration | Exa | Perplexity | Winner | Decisive dim |
|---|---|---|---|---|---|
| I01 | Stripe Payment Element (one-time + sub) | 4/4/5/5 | 4/3/4/2 | **Exa** | citation_anchoring (+3) |
| I02 | Lemon Squeezy hosted checkout | 3/2/4/5 | 2/1/1/1 | **Exa** | citation_anchoring (+4) |
| I03 | Stripe Connect Express | 4/3/4/5 | 3/2/3/2 | **Exa** | citation_anchoring (+3) |
| I04 | PhonePe PG v2 UPI | 3/3/4/5 | 4/3/3/2 | **Exa** | citation_anchoring (+3) |
| I05 | Paytm All-in-One Web SDK ⚠️ Exa broken | 2/2/3/4 | 4/2/3/1 | **Exa** | citation_anchoring (+3) |
| I06 | Xendit virtual account ⚠️ both broken | 2/2/3/3 | 2/2/3/2 | TIE | within_noise |
| I07 | Flutterwave Standard | 3/4/5/4 | 4/3/4/2 | **Exa** | citation_anchoring (+2) |
| I08 | MercadoPago Checkout Pro | 4/4/5/5 | 3/2/3/2 | **Exa** | citation_anchoring (+3) |
| I09 | Clerk clerkMiddleware (nextjs) | 4/3/4/5 | 3/2/3/2 | **Exa** | citation_anchoring (+3) |
| I10 | Supabase auth v2 | 4/3/5/5 | 4/4/5/2 | **Exa** | citation_anchoring (+3) |
| I11 | Auth0 New Universal Login + RBAC ⚠️ Exa broken | 2/2/3/5 | 4/2/3/2 | **Exa** | citation_anchoring (+3) |
| I12 | Better-Auth social + magic link (nextjs) ⚠️ Pplx broken | 3/3/4/4 | 2/2/3/1 | **Exa** | citation_anchoring (+3) |
| I13 | Instagram Login Business (Graph) | 3/3/3/5 | 4/4/5/2 | **Exa** | citation_anchoring (+3) |
| I14 | WhatsApp Cloud API + webhook | 4/2/4/4 | 4/2/3/2 | **Exa** | citation_anchoring (+2) |
| I15 | Discord OAuth2 + bot slash command | 3/2/4/3 | 4/3/3/2 | TIE | within_noise |
| I16 | Telegram Bot inline keyboard + webhook | 4/2/4/4 | 4/3/4/2 | **Exa** | citation_anchoring (+2) |
| I17 | OpenAI Responses API + SSE ⚠️ Pplx broken | 3/3/4/4 | 2/2/3/1 | **Exa** | citation_anchoring (+3) |
| I18 | Anthropic Messages + tool_use + cache_control ⚠️ both broken | 2/2/3/3 | 2/2/3/2 | TIE | within_noise |
| I19 | ElevenLabs websocket streaming TTS | 4/3/4/3 | 3/2/3/2 | **Exa** | aggregate (+4 total) |
| I20 | Solana @solana/web3.js v2 transfer ⚠️ both broken | 2/2/3/3 | 2/1/2/2 | **Exa** | completeness (+1, aggregate) |
| I21 | wagmi v2 + viem (nextjs) ⚠️ Exa broken | 2/2/3/3 | 3/2/3/2 | TIE | within_noise |
| I22 | Alchemy NFT API v3 owned NFTs | 4/2/4/5 | 3/3/4/2 | **Exa** | citation_anchoring (+3) |
| I23 | Mapbox GL JS v3 + Directions | 4/3/4/5 | 3/2/3/2 | **Exa** | citation_anchoring (+3) |
| I24 | Google Maps Places API (New) | 3/3/4/5 | 4/4/5/1 | **Exa** | citation_anchoring (+4) |
| I25 | Cloudflare R2 presigned PUT | 4/4/5/5 | 4/3/4/2 | **Exa** | citation_anchoring (+3) |
| I26 | UploadThing v6 file upload (nextjs) | 4/2/4/5 | 4/3/3/2 | **Exa** | citation_anchoring (+3) |
| I27 | PostHog flags + capture | 3/3/4/5 | 4/3/4/1 | **Exa** | citation_anchoring (+4) |
| I28 | Mixpanel /import + Query API | 3/2/4/4 | 4/3/3/2 | **Exa** | citation_anchoring (+2) |
| I29 | Open-Meteo forecast + historical | 4/3/4/4 | 4/3/4/2 | **Exa** | citation_anchoring (+2) |

---

## 2. Per-Dimension Averages (1-5)

| Dimension | Exa avg | Perplexity avg | Δ (Exa − Pplx) |
|---|---|---|---|
| correctness_and_freshness | 3.24 | 3.34 | **−0.10** |
| executability | 2.69 | 2.52 | +0.17 |
| completeness | 3.93 | 3.34 | +0.59 |
| citation_anchoring | 4.31 | 1.79 | **+2.52** |

**Interpretation:**
- **Correctness:** statistical tie, slight Pplx edge (within noise).
- **Executability:** essentially tied, both barely above "3 = 1-2 non-obvious fixes needed".
- **Completeness:** Exa modestly better — Pplx's 3x verbosity (69k vs 23k chars) didn't translate to more present pieces; judge correctly penalized duplication.
- **Citation_anchoring:** Exa's structural win. Exa places official-docs URLs near relevant code; Perplexity dumps citations at the end or cites only third-party blogs.

---

## 3. Sensitivity Analysis — What if citation_anchoring weren't in the rubric?

Re-running the pairwise winner logic with only `correctness_and_freshness + executability + completeness` (drop citation_anchoring):

| Winner | Count | % |
|---|---|---|
| Exa | 9 | 31% |
| Perplexity | 6 | 21% |
| Tie | 14 | 48% |

**Key insight: without citation_anchoring, the eval is essentially a tie.** Exa's 86% winrate is almost entirely a function of how well it places official-docs URLs. If you don't care about citations, the providers are interchangeable on this rubric.

**Head-to-head on correctness alone:**
- Pplx beats Exa: 10 integrations
- Exa beats Pplx: 9 integrations
- Tied: 10 integrations

→ Perplexity's correctness is marginally BETTER than Exa's, contrary to the headline winrate.

---

## 4. Broken Cases (Correctness ≤ 2 on at least one side)

Both providers struggle on 9 of 29 integrations (31%):

| Integration | Exa C&F | Pplx C&F | Whose-fault |
|---|---|---|---|
| I02 Lemon Squeezy | 3 | **2** | Pplx-only |
| I05 Paytm | **2** | 4 | Exa-only |
| I06 Xendit | **2** | **2** | both |
| I11 Auth0 | **2** | 4 | Exa-only |
| I12 Better-Auth | 3 | **2** | Pplx-only |
| I17 OpenAI Responses | 3 | **2** | Pplx-only |
| I18 Anthropic Messages | **2** | **2** | both |
| I20 Solana web3.js v2 | **2** | **2** | both |
| I21 wagmi v2 | **2** | 3 | Exa-only |

Exa-only broken: 3 cases (Paytm, Auth0, wagmi v2). Pplx-only broken: 3 cases (Lemon Squeezy, Better-Auth, OpenAI Responses). Both broken: 3 (Xendit, Anthropic Messages, Solana). Roughly symmetric — neither provider has a structural advantage on hard correctness cases.

---

## 5. Volume + Cost Stats (both measured from live API responses)

| Metric | Exa | Perplexity |
|---|---|---|
| OK count | 29/29 | 29/29 |
| Avg latency | 210 s | 212 s |
| Avg playbook chars | **20,068** | 68,546 (3.4x more verbose) |
| **Cost total (measured)** | **$21.73** | **$27.74** |
| **Cost per call** | **$0.749** | **$0.957** |
| Cost delta | — | Perplexity **+21.7%** vs Exa |

**Source of cost numbers:**
- Exa: `costDollars.total` field returned by `/research/v1` poll endpoint, summed across 29 calls.
- Perplexity: `usage.cost.total_cost` field in each `/chat/completions` response, summed across 29 calls.

### Perplexity cost composition (where the $27.74 goes)
| Component | Cost | % |
|---|---|---|
| Reasoning tokens | $15.72 | **56.7%** |
| Search queries (avg 50/call × $5/1k) | $7.16 | 25.8% |
| Output tokens | $3.30 | 11.9% |
| Citation tokens | $1.56 | 5.6% |
| Input tokens | $0.01 | 0.0% |

Perplexity's `sonar-deep-research` does extensive internal "thinking" (reasoning tokens) and runs ~50 searches per call — that's where 82% of its cost lives. Exa's `/research/v1` flat-prices the research task; cheaper in practice.

### Production-scale projection (70k Perplexity-fallback calls/month)
| Scenario | Monthly cost |
|---|---|
| Stay on Perplexity | **$66,990/mo** |
| Switch to Exa | **$52,430/mo** |
| **Savings** | **−$14,560/mo (−22%)** |

Exa is both **better on the rubric** AND **cheaper at scale**.

---

## 6. Caveats

1. **Single judge model (Claude Opus 4.7).** Full design called for Opus + GPT-5 ensemble. Single judge means non-determinism in borderline cases (I13 Instagram flipped from Pplx-win in pilot to Exa-win in full run because Exa's citation_anchoring scored 5 instead of 4 — same playbook content, different judge sampling).
2. **`docs_unavailable=true`** — judge applied LONG-TAIL HANDLING (internal-consistency-only scoring) for correctness, not direct comparison to fetched official docs. Full eval should pre-fetch official docs per integration for harder correctness verification.
3. **No position swap.** Each playbook judged once absolute (Shape A); pairwise computed locally. Position bias not directly measured — though Shape A is structurally less prone to it than Shape B pairwise.
4. **Stage 2 (end-to-end smoke tests) not run.** The design's verdict formula is `0.7 * stage2_success_rate + 0.3 * judge_pairwise_winrate`. We only have the 0.3 piece. Stage 2 is the real test of whether "playbook reads well" translates to "agent produces working code."
5. **Citation_anchoring is doing most of the work.** Per §3, the headline winrate is largely a function of one dimension. If you change rubric weights, the verdict changes.

---

## 7. Recommendation

**Ship Exa, with two qualifications:**

### Why ship Exa
1. **86% pairwise winrate, 0% Pplx wins.** No ambiguity in the rubric's framing.
2. **Structural format quality.** Exa produces shorter playbooks (3.4x less verbose) with inline official-docs citations. Both properties matter for our downstream consumer: the agent has 5 iterations max before giving up, so concise correct playbooks reduce context bloat and burn fewer ECUs.
3. **No correctness regression.** On the core code-correctness dimension, Exa is within 0.10 points of Pplx (3.24 vs 3.34) — statistical tie. Switching does not make code worse.
4. **Both providers under-perform on correctness** (3.24 / 3.34 on 5-scale; executability 2.69 / 2.52). This is independent of which provider we ship — Stage 2 will find bugs either way.

### Qualifications
1. **Run Stage 2 before committing the prod cutover.** Citation quality is a leading indicator but not a guarantee of working code. Spend ~$50 on 7 stage-2 smoke tests (Stripe, Supabase, Instagram, OpenAI Responses, Solana, Google Maps, MercadoPago) before flipping prod traffic. If stage-2 success rates are within 10% of each other, the verdict already favors Exa on both quality AND cost.
2. **Cost is in Exa's favor.** Exa is 21.7% cheaper per call. At 70k calls/month, switching to Exa SAVES ~$14,560/mo. The original motivation for evaluating Exa (cheaper than Perplexity) checks out.

### Hybrid policy is no longer necessary
A previous draft of this report suggested a hybrid (Exa for HIGH-freshness, Pplx for LOW-freshness) to balance "Exa quality" against "Pplx cost". That tradeoff doesn't exist — Exa is cheaper. Use Exa for everything unless Stage 2 surfaces a stack/category where Pplx materially outperforms on code-correctness.

---

## 8. What's in this folder

```
pilot/
├── integrations.yaml          # original 7 pilot integrations
├── integrations_full.yaml     # full 29-integration eval set
├── run_pilot.py               # Stage 1 harness (Exa + Perplexity parallel)
├── judge.py                   # judge harness (Claude Opus 4.7, Shape A)
├── summarize.py               # auto-summary writer
├── PILOT_REPORT.md            # auto-generated 7-integration pilot view
├── FULL_REPORT.md             # this document (29-integration analysis)
├── results/
│   ├── I01.json … I29.json    # per-integration raw playbook outputs
│   ├── _run_summary.json      # Stage 1 wall-clock + cost summary
│   ├── _run_log.txt           # pilot run log
│   └── _run_log_full.txt      # full run log
└── judge_results/
    ├── I01-exa.json … I29-perplexity.json  # per-playbook scores + evidence
    └── _aggregate.json        # pairwise winners + dim averages
```

---

## 9. Cost summary (this eval run)

| Item | Cost | Source |
|---|---|---|
| Exa Research API (29 calls) | $21.73 | measured (`costDollars.total`) |
| Perplexity sonar-deep-research (29 calls) | **$27.74** | measured (`usage.cost.total_cost`) |
| Claude Opus 4.7 judge (58 playbooks) | $4.64 | estimated (output-token × Opus rate) |
| **GRAND TOTAL** | **$54.11** | |

Stage 1 wall-clock: 21.3 min (bounded concurrency 4 at integration level → 8 concurrent HTTP calls). Judge wall-clock: 2 min (concurrency 6, 14-22s per call).
