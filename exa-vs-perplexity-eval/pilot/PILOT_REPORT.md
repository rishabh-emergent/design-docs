# Exa vs Perplexity — Pilot Results

## TL;DR

- **Verdict: `MIXED_RUN_FULL_EVAL`**
- Sample: 29 integrations (paired Exa + Perplexity playbooks)
- Win rates: Exa = **86%**, Perplexity = **0%**, Tie = **14%**
- Wall-clock: 1280s (21.3 min)
- Cost: Exa = $21.73, Perplexity ≈ $8.70 (estimated)

## Stage 1 — Generation stats

| Provider | OK count | Avg latency (s) | Avg playbook chars |
|---|---|---|---|
| exa | 29/29 | 209.8 | 20067 |
| perplexity | 29/29 | 212.5 | 68546 |

## Stage 1 — Judge (Claude Opus 4.7, absolute Shape A)

### Per-dimension averages (1-5 scale)

| Dimension | Exa avg | Perplexity avg | Δ (Exa − Pplx) |
|---|---|---|---|
| correctness_and_freshness | 3.24 | 3.34 | -0.1 |
| executability | 2.69 | 2.52 | 0.17 |
| completeness | 3.93 | 3.34 | 0.59 |
| citation_anchoring | 4.31 | 1.79 | 2.52 |

### Per-integration pairwise

| ID | Integration | Exa scores (C&F/EX/CP/CT) | Pplx scores | Winner | Tie rule | Both broken? |
|---|---|---|---|---|---|---|
| I01 | Stripe Payment Element (one-time + sub) | 4/4/5/5 | 4/3/4/2 | **exa** | single_dim_ge_2 | False |
| I02 | Lemon Squeezy hosted checkout | 3/2/4/5 | 2/1/1/1 | **exa** | single_dim_ge_2 | True |
| I03 | Stripe Connect Express | 4/3/4/5 | 3/2/3/2 | **exa** | single_dim_ge_2 | False |
| I04 | PhonePe PG v2 UPI | 3/3/4/5 | 4/3/3/2 | **exa** | single_dim_ge_2 | False |
| I05 | Paytm All-in-One Web SDK | 2/2/3/4 | 4/2/3/1 | **exa** | single_dim_ge_2 | True |
| I06 | Xendit virtual account | 2/2/3/3 | 2/2/3/2 | **TIE** | within_noise | True |
| I07 | Flutterwave Standard (Nigeria) | 3/4/5/4 | 4/3/4/2 | **exa** | single_dim_ge_2 | False |
| I08 | MercadoPago Checkout Pro (LatAm) | 4/4/5/5 | 3/2/3/2 | **exa** | single_dim_ge_2 | False |
| I09 | Clerk clerkMiddleware (nextjs) | 4/3/4/5 | 3/2/3/2 | **exa** | single_dim_ge_2 | False |
| I10 | Supabase auth v2 | 4/3/5/5 | 4/4/5/2 | **exa** | single_dim_ge_2 | False |
| I11 | Auth0 New Universal Login + RBAC | 2/2/3/5 | 4/2/3/2 | **exa** | single_dim_ge_2 | True |
| I12 | Better-Auth social + magic link (nextjs) | 3/3/4/4 | 2/2/3/1 | **exa** | single_dim_ge_2 | True |
| I13 | Instagram Login Business (Graph) | 3/3/3/5 | 4/4/5/2 | **exa** | single_dim_ge_2 | False |
| I14 | WhatsApp Cloud API + webhook | 4/2/4/4 | 4/2/3/2 | **exa** | single_dim_ge_2 | False |
| I15 | Discord OAuth2 + bot slash command | 3/2/4/3 | 4/3/3/2 | **TIE** | zero_sum | False |
| I16 | Telegram Bot inline keyboard + webhook | 4/2/4/4 | 4/3/4/2 | **exa** | single_dim_ge_2 | False |
| I17 | OpenAI Responses API + SSE | 3/3/4/4 | 2/2/3/1 | **exa** | single_dim_ge_2 | True |
| I18 | Anthropic Messages + tool_use + cache_control | 2/2/3/3 | 2/2/3/2 | **TIE** | within_noise | True |
| I19 | ElevenLabs websocket streaming TTS | 4/3/4/3 | 3/2/3/2 | **exa** | aggregate | False |
| I20 | Solana @solana/web3.js v2 transfer | 2/2/3/3 | 2/1/2/2 | **exa** | aggregate | True |
| I21 | wagmi v2 + viem connect + sign (nextjs) | 2/2/3/3 | 3/2/3/2 | **TIE** | within_noise | True |
| I22 | Alchemy NFT API v3 owned NFTs | 4/2/4/5 | 3/3/4/2 | **exa** | single_dim_ge_2 | False |
| I23 | Mapbox GL JS v3 + Directions | 4/3/4/5 | 3/2/3/2 | **exa** | single_dim_ge_2 | False |
| I24 | Google Maps Places API (New) | 3/3/4/5 | 4/4/5/1 | **exa** | single_dim_ge_2 | False |
| I25 | Cloudflare R2 presigned PUT | 4/4/5/5 | 4/3/4/2 | **exa** | single_dim_ge_2 | False |
| I26 | UploadThing v6 file upload (nextjs) | 4/2/4/5 | 4/3/3/2 | **exa** | single_dim_ge_2 | False |
| I27 | PostHog flags + capture | 3/3/4/5 | 4/3/4/1 | **exa** | single_dim_ge_2 | False |
| I28 | Mixpanel /import + Query API | 3/2/4/4 | 4/3/3/2 | **exa** | single_dim_ge_2 | False |
| I29 | Open-Meteo forecast + historical | 4/3/4/4 | 4/3/4/2 | **exa** | single_dim_ge_2 | False |

## Verdict math

- Exa wins: 25/29 = 86%
- Perplexity wins: 0/29 = 0%
- Ties: 4/29 = 14%
- Any Exa playbook with correctness ≤ 2: True
- Any Perplexity playbook with correctness ≤ 2: True

**Decision rule applied:**
Inconclusive signal at pilot scale → expand to full 28-integration eval before deciding.

## Pilot caveats

- Single judge model (Opus 4.7) — full eval should use Opus + GPT-5 ensemble.
- `docs_unavailable=true` — judge applied LONG-TAIL HANDLING (internal-consistency-only scoring) instead of comparing to fetched official docs. Full eval pre-fetches docs per integration.
- No position swap (each playbook judged once absolute, pairwise computed locally). Position bias not measured at pilot scale.
- Stage 2 (end-to-end smoke tests on real APIs) not run. Verdict score formula `0.7*stage2 + 0.3*stage1` not computable; pilot uses stage1 only as directional signal.
