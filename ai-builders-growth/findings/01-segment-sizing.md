# Phase 1 — Segment Sizing: the AI-builder economy on Emergent

**Date:** 2026-06-12 · **Window:** 90 days (2026-03-14 → 2026-06-12) unless noted · **Classification:** keyword filter v1 (LLM calibration pending, steps 13–14) · Raw data: [raw-phase01-sweep.md](raw-phase01-sweep.md)

## Headline

> **AI builders are ~16% of projects but ~28–54% of platform spend, convert to paid at 1.66× the rate of other builders, deploy 1.7× more often, and are 100% of the most expensive whale tail. The segment's *share* is flat for 12 months — the opportunity is not riding a wave, it's fixing a leaky, expensive funnel: only 3.0% of AI projects ever deploy, and the ones that do cost a median $111 (11.8× the median non-deployed AI project).**

## 1. Platform context (90d)

- 4,693,212 jobs · 3,174,166 users · 4,545,588 projects · **$151.67M total attributed ECU-value consumption**.
- Platform peaked Mar 2026 (1.87M jobs) / Apr 2026 (1.25M users); May 2026 = 1.30M jobs / 994k users; June pacing ≈ flat vs May.
- Job mix: fullstack builder ~31%, general agent ~22%, Expo mobile ~22%, landing page ~10%, wingman 2.5%.

## 2. How big is the AI segment? (H1: ❓ big but NOT growing as share)

| Metric (90d) | AI-candidate | Share |
|---|---|---|
| Jobs | 867,042 / 4.69M | **18.5%** |
| Users | 600,993 / 3.17M | **18.9%** |
| Projects | 747,632 / 4.55M | **16.4%** |
| Signups whose *first prompt* is AI | 389,391 / 3.97M | 9.8% (14.1% of job creators) |

- Monthly AI share has been **stable in a 14.6–21.8% band since Jun 2025** — no organic growth trend. Absolute volume grows only with the platform.
- Keyword composition: generic "ai" 39.2%, "agent(s)" 35.0%, gpt/openai 11.1%, claude/gemini 8.8%, chatbot 5.6%, voice/tts 13.2%, rag/embeddings 1.6%, image-gen 1.3%. (Two largest buckets are noisy → true share likely lower; calibration pending.)

## 3. Spend: AI builds are the expensive tail (H1-spend: ✅)

| Cost metric per job (90d) | AI | non-AI | Ratio |
|---|---|---|---|
| median | $9.94 | $6.54 | 1.5× |
| p75 | $26.60 | $10.11 | 2.6× |
| p90 | **$152.41** | $16.69 | **9.1×** |
| p99 | $1,324 | $202 | 6.6× |
| mean | $89.80 | $19.50 | 4.6× |

- Job-level spend split: AI = **$77.47M (51.1%)** of $151.67M from 18.5% of jobs.
- Project-level bracket (fork-text bias, see Phase 0): root-task basis **$41.9M / 27.6%** (floor) ↔ any-job basis **$82.2M / 54.2%** (ceiling). The ~$40M gap lives in ~33K long fork chains where AI gets *added to mature projects* — AI is also an expansion behavior, not only a day-one intent.
- Top-10 AI whale projects each burned **$56K–$85K** in 90d (AI communication coach, bitcoin decision engine, arxiv ranking, creator-ops SaaS, gym-maintenance SaaS, Quran memorization w/ AI recitation, AI learning companion). One single job ran 49,704 steps / 11.73B prompt tokens / $57,595.

## 4. Conversion: AI intent = premium acquisition (H3: ✅)

- 24h signup→paid: **AI-first-prompt 8.8%** vs non-AI job creators 5.3% (**1.66×**) vs no-job 1.4%; platform baseline 4.5%.
- AI-first users are 9.8% of signups but **19.4% of all 24h conversions**.
- Context cuts: Desktop converts 6.9% vs Mobile Web 3.1% / Mobile App 2.6%; India = 40.3% of signups at 2.4% conv; US = 7.8% of signups at 11.5%.

## 5. Build→deploy funnel: the cliff (H2 at deploy stage: ❌ refuted — AI deploys MORE)

| 90d projects (root in window) | AI | non-AI |
|---|---|---|
| Projects | 708,023 | 3,811,014 |
| **Deployed (S3)** | 21,265 = **3.0%** | 67,448 = 1.8% |
| Custom domain among deployed | 22.4% | 21.0% |

- The 1.7× AI deploy lift **holds within every top-10 template** (not composition).
- Template matters hugely: paid fullstack opus_4_7 deploys at 11.1%; free tiers 0.2–0.7%; general_agent 0.2–0.4%.
- **Cost of success:** deployed AI projects median **$111.47** (p75 $397.68, mean $661) vs non-deployed AI median $9.43 → reaching S3 takes ~12× median investment. Combined with §3: the AI funnel is *pay-heavily-to-succeed*; most users stop long before.

## 6. Whales (the "big jobs" you asked about)

- Top-100 projects by 90d cost: combined **$5.57M** (range $40.3K–$158.7K each). **28/100 are AI** by root-task → 27.8% of whale spend.
- Top-50 users by spend: $4.65M combined consumption; 10/50 (root-basis floor) to 42/50 (job-basis ceiling) are primarily-AI builders; lifetime revenue paid by these 50 ≈ $1.08M — **consumption ≫ revenue, finance check flagged** (Phase 5).
- Top whale: user `21e6b39e…` (Poland), $171K consumption, $40K revenue paid.

## 7. Universal LLM key (H6: ✅ correlation)

- 90d: 123,104 users / 2.99M ECU / 408K transactions (1.5% of all debit ECU; 3.9% of LLM-active users).
- **50.9% of universal-key users are AI-candidate builders vs 18.9% baseline → 2.9× enrichment.** The key reaches exactly the target segment.
- But adoption is **broad-and-shallow**: median 5 ECU / 1 transaction per user in 90d. Weekly users declined from 15.5K (Mar) to 7–9K (Jun) while ECU/user doubled.
- Post-deploy production inference (LiteLLM topups): only **3,626 users in 90d** vs 21,265 newly-deployed AI projects → the "operate your AI app" rail is nearly unmonetized today. 357,989 users hold paid universal keys.

## 8. Seeds vs baseline (your 17 sample jobs)

- All 17 are single-job projects (no forks). Total cost $2,264; median $60; one outlier $1,227 (team-chat-workspace → onebrain.team, 48 HITLs, 27.9 hrs).
- **4/17 deployed (23.5%)** — ~8× the 3.0% AI baseline (your picks skew successful); 1 custom domain.
- onebrain.team already has **64 real end-users** in its Mongo within ~48h of deploy → S4 happens fast when it happens.
- Seed users: 16/17 paying but median LTV $5.24 (5 are $1 intro offers); top-4 hold 98.5% of cohort LTV; **topups = 94.1% of cohort revenue**; 17/17 active in the last 14 days; cohort consumed $61K in 90d vs $24.3K lifetime revenue.

## 9. Errors (Phase-4 preview)

- AI jobs are **not** more error-prone per step (0.0195% vs 0.0209%) but hit ≥1 error 2.6× more often per job because they run 2.8× longer (129.7 vs 45.9 steps/job).
- Top signatures: generic "Internal server error" (38% of AI error steps), Cloud Build failures, env restart/fetch failures — **infra, not model**. Most AI-relevant: context-limit errors (616 steps / 238 jobs).

## 10. Strategic implications (feeding Phases 2–8)

1. **Don't bet on segment-share growth; bet on success-rate growth.** Share is flat; spend and conversion premium are real. Moving S2→S3 for AI projects is the revenue lever (model in step 80).
2. **The funnel cliff is the product brief:** 97% of AI projects never deploy, and success costs ~$111+ median. Premade blocks/templates that compress iterations directly attack both abandonment and cost-to-success.
3. **Operate-rails white space:** 21K AI deploys/90d but only 3.6K apps consuming production LLM via us — key management, metering, billing for builders' own end-users is nearly untouched monetization.
4. **AI-intent users are premium acquisition** — GTM should bid for them explicitly (landing pages, templates gallery SEO: "build an AI ___").
5. **Whale economics need a margin check** before we celebrate the tail (consumption vs revenue gap).
6. **Mobile + India gap:** the largest signup pools convert worst; AI-builder GTM aimed at desktop/US/UK/EU pros likely outperforms.

## Open items to finish Phase 1

- Steps 13–14: LLM classification of stratified sample → calibrated share + sub-category taxonomy (chat-wrapper / generator / agent / RAG / AI-feature / voice).
- Step 16 by sub-category (is *agent* demand growing inside flat AI share? — H8).
- Step 18–19 geo/device for AI builders specifically; step 23 fork-depth AI vs non-AI.
