# Phase 5 — Builder Economics & the Revenue Impact Model

**Date:** 2026-06-12 · **Source:** workflow `wf_aaf70c79-b23`. Raw: [raw-phase37-sweep.md](raw-phase37-sweep.md)

## 1. LTV by segment (first root job Jan–Mar 2026; revenue in following 90d)

| Segment | N | Mean 90d rev | % paying | Topup share |
|---|---|---|---|---|
| **(a) AI builder, deployed ≤30d** | 9,522 | **$206.71** | **87.1%** | 80.6% |
| (b) AI engaged ≥$10, not deployed | 112,306 | $13.94 | 17.4% | 71.2% |
| (c) AI shallow | 258,315 | $1.94 | 3.7% | — |
| (d) non-AI deployed ≤30d | 40,130 | $160.77 | 85.7% | 81.2% |
| (e) non-AI engaged | 498,036 | $8.97 | 12.5% | — |

- **Revenue delta (a)−(b): $192.77/user.** AI deployers also out-earn non-AI deployers by +29%.
- **Causality nuance:** 73.5% of deployers' first topups happen *before* first deploy → deployment monetizes by **extending an already-paying journey** (post-deploy iteration, hosting, runtime), not by triggering first purchase. The topup-after-deploy flow (26.5%) is the genuinely incremental path.

## 2. The impact model (plan step 80)

May 2026 produced **57,401 new engaged-not-deployed AI builders** (of 123,929 new AI builders; only 3,199 deployed ≤30d).

| Scenario (engaged→deployed conversion lift) | Upper bound (full delta) | Conservative (30% causal) |
|---|---|---|
| +5pp | $553K / monthly cohort (90d rev) | **$166K** (~$2.0M annualized) |
| +10pp | $1.107M | **$332K** (~$4.0M annualized) |
| +20pp | $2.213M | $664K (~$8.0M annualized) |

Even the conservative +5pp case clears the build cost of deploy-completion features. **Ship behind an experiment to measure the true causal share.**

## 3. Pricing & packaging evidence

- AI builders subscribe at **2.2×** the non-AI rate (17.1% vs 7.7%), skew 2× to Pro, and revenue/user is **5.7×** ($40.17 vs $7.06). But 82.9% still unsubscribed.
- **78.6% of AI-builder revenue arrives as topups** — median $20, ~11 purchases per topping-up user: repeated paywall hits, not committed plans. Auto-topup / usage-commit / bigger bundles at first-topup moment converts friction into MRR.
- **The plan-fit gap:** median deployed AI project = 199.4 ECU vs Standard 100 ECU/mo vs Pro 750. **A ~250–300 ECU "AI Builder" tier sized to "ship one AI project per month" fills a real hole in the lineup.**
- **Expansion window opens immediately:** 20.5% of AI-first 24h-converters top up within 30d (49× non-converters) — surface upgrades right after first payment.
- Free-tier AI funnel: 40% of AI root jobs run on free prompts, deploying at 0.67% vs 4.66% paid (7×) — 207K attempts/quarter for a deploy-gated upsell ("your agent works — ship it live with X ECU included").

## 4. The "operate" business today (LLM-proxy runtime forensics)

Runtime universal-key calls are **identifiable and growing** (~563K calls/day, +10% over 4 days), but build-time testing dominates: the persistent production cohort is **~4,634 recurring apps**, median 10 calls/day; only ~412 apps ≥50 calls/day, ~113 ≥100/day, busiest = 336/day; zero 429s; runtime model mix skews cheap (gemini-flash + gpt-5-nano = 66%).

- **It's a long tail, not whales** → operate pricing = flat fee or generous included tier, not usage-tiered whale pricing.
- Of the top-60 persistent apps: 85% deployed, **62% custom domains, 58% AI** — the serious-operator beta list is generatable today (proxy logs × deployer join).
- Blockers found: **proxy log retention is ~5 days** → ship a daily aggregate ETL (app × day × model × calls × errors) to BigQuery before building any operate analytics.
- Value props the data supports: visibility (per-app usage/spend dashboards), control (model switching, budget caps), per-end-user keys for resellers. Reliability is *not* the pain (0 rate-limit hits).

## 5. Whale margin alert (finance escalation)

Top-20 users by 90d consumption: **$2.39M internal trajectory value vs $547K lifetime revenue collected (23%)**. Every one is underwater on internal-value terms; worst case $158.8K consumed vs $7.96K paid. `value_in_usd` is internal metering value, not COGS — **finance must confirm actual COGS per metered dollar before any growth push that manufactures more whales.** Guardrails (rate limits / enterprise contracts >$80K consumption) should accompany whale-creating features.
