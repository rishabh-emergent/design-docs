# AI Builders Growth — Master Research Plan

**Owner:** Rishabh (PM/builder) + Claude (research execution)
**Started:** 2026-06-12
**Mission:** Increase adoption, experience, and retention of users building **AI products and AI agents** on Emergent. Decide which feature project(s) to build (agent templates, premade integrations, premade AI-product features), build them, and take them to market.
**Scope-equivalent:** ~3 months of dedicated PM research, compressed into a phased, data-driven program.

---

## 0. Context & Working Hypotheses

Emergent users describe apps in natural language; agents build and deploy them. A growing segment of users is building **AI products** — apps whose core value is itself an LLM/AI feature (chatbots, AI SaaS, generators, copilots, agents). The 17 seed jobs confirm this: AI ebook generators, AI astrology platform, AI career navigator, AI image retouching SaaS, "VORTEX AI" all-in-one AI platform, AI financial modeling, multi-user shared LLM chat, etc.

**Hypotheses to test (H1–H10):**
- **H1:** AI-product jobs are a large and growing share of platform jobs and an outsized share of credit spend.
- **H2:** AI-product jobs fail/stall more often than CRUD apps (LLM key setup, streaming, rate limits, integration complexity).
- **H3:** Users building AI products have higher willingness-to-pay (they intend to monetize) → higher LTV if they succeed.
- **H4:** Most AI products on Emergent re-implement the same 6–10 building blocks by hand (chat UI, RAG, key management, usage metering, multi-model routing, image gen, voice, agent loops) — premade blocks would compress time-to-value dramatically.
- **H5:** "Success" (deployed + real end-users in the app's MongoDB + custom domain) strongly predicts builder retention and topups.
- **H6:** The Emergent Universal LLM Key is a major activation lever for AI builds (no API key friction), and its absence/limits is a major churn/friction source.
- **H7:** A meaningful share of HITL messages on AI jobs are repeated requests for the same missing primitives (integrations, templates) — i.e., a ranked feature backlog already exists in our data.
- **H8:** Agent-builder demand (multi-step agents, automations, schedulers, integrations like WhatsApp/Telegram/email) is rising faster than chat-wrapper demand.
- **H9:** Fork-chain length (iteration count) on AI jobs is higher than non-AI; cost-per-successful-AI-app is the #1 hidden churn driver.
- **H10:** Competitors (Lovable, Bolt, Replit, v0, Base44) are weak on *operating* AI products post-deploy (keys, metering, billing, evals) — that's our differentiation window.

---

## 1. Data Assets (validated 2026-06-12)

| Asset | Access | Use |
|---|---|---|
| `analytics.jobs_full_view` (BigQuery DS 7) | ✅ Redash | All jobs: task text, prompt_name, chat_mode, user, cost field (NOTE: `total_credits_deducted_for_task` is often 0 → compute cost from trajectories) |
| `analytics.trajectories_full_view` (partitioned, needs `created_at` filter) | ✅ | Per-step cost (`value_in_usd`), tokens, HITL messages (`user_messages_array`), errors, agent names |
| `analytics.fork_chain` | ✅ | Project lineage; jobs→projects rollup |
| `credits_db.credit_ledger` (partitioned) | ✅ | True ECU spend by reference_type (LLM_CALL, DEPLOYMENT…) |
| `analytics.user_revenue_events`, `subscription_events`, `cancellation_snapshots`, `predict_churn.churn_reason_classifications` | ✅ | LTV, conversion, churn segmentation |
| `analytics.conversions_dataset` | ✅ | Signup→paid funnel w/ `prompt_type` of first job |
| `analytics.deployer_db_data` | ✅ | Deployments, custom domains = success signals |
| `analytics.signups_raw_dataset`, `person_first_event`, `posthog.events_full_view` (partitioned) | ✅ | Acquisition, device, geo, behavioral events |
| `support_analytics.conversation_state_segments_latest` (≥2026-01-10) | ✅ | Support tickets by cluster, job_id in custom_fields |
| `hitl.IntentClassificationEvent` | ✅ | Bug vs feedback density |
| Integration Proxy DB (Redash DS 18) | ✅ schema TBD | Which 3rd-party integrations user apps actually call |
| LLM Proxy DB (DS 9), Cortex DB (DS 14), agent-service-prod (DS 10), Deployer (DS 5) | ✅ | Raw prod lookups when BigQuery lags |
| `mcp__deployer__run_mongo_query` + `fetch_app_details` | ✅ | **End-user adoption inside deployed apps** (users collection of app's Mongo) |
| `cortex_debugger` MCP | ✅ | Per-job forensics: sessions, messages, tool calls, cost |
| user-jobs MCP | ✅ | Job + user quick lookups |
| Web research | ✅ | Competitive intel |

**Data quality rules:** partition filters mandatory on trajectories/posthog/credit_ledger; exclude internal users (`%emergent.sh`, test user `90e9d382-…`); jobs vs projects = `COALESCE(fork_chain.first_job_id, job.id)`; job `status` is unreliable (seed jobs all read IN_PROGRESS) → define outcomes from deployments/activity, not status.

---

## 2. Key Definitions (to be locked in Phase 0)

- **AI-product job:** task text indicates the *app being built* has AI/LLM functionality (not merely built *by* AI). Detection: keyword heuristic → LLM classifier with rubric (see Step 12–15).
- **AI-builder (user):** user with ≥1 AI-product project.
- **Project:** root job + all forks (`first_job_id`).
- **Build success ladder (S0–S5):** S0 created → S1 preview loaded → S2 agent finished w/o abandon → S3 deployed → S4 has real end-users (≥3 non-owner users in app Mongo / traffic) → S5 monetizing (Stripe/PayPal integration live or custom domain + users).
- **Builder retention:** user creates ≥1 job in month M+1 (and separately: keeps active subscription).
- **TTV (time-to-value):** signup→first deploy; prompt→preview; prompt→working AI feature.

---

## 3. The 118-Step Research Program

### PHASE 0 — Foundations, definitions, instrumentation audit (Steps 1–10) — "Week 1"

1. ✅ Inventory data sources; validate Redash/BigQuery/MCP access. *(done 2026-06-12)*
2. ✅ Validate the 17 seed jobs exist; pull task text, users, prompt types. *(done; all AI products)*
3. Lock the **AI-product taxonomy v1** (categories below, Step 13) and the S0–S5 success ladder; write `01-definitions.md`.
4. Build the **keyword pre-filter** (AI/GPT/Claude/chatbot/agent/LLM/RAG/generate/voice/copilot/etc. in task text, multilingual: EN/ES/PT/IT/FR/ID/HI) and measure its hit-rate on seeds (target: ≥16/17).
5. Validate cost computation: `SUM(trajectories.value_in_usd)` per job vs `credit_ledger` DEBITs for 20 random jobs; pick canonical method.
6. Verify Integration Proxy DB schema (DS 18): what tables exist, what's logged per call (provider, app, job, status).
7. Verify app-Mongo end-user counting via `deployer run_mongo_query` on 3 seed apps; define the "real end-users" heuristic (exclude owner email, test users).
8. Verify deployments join: seed jobs → `deployer_db_data` rows; document the job→app_name mapping path.
9. Audit PostHog events available for builder UX funnels (preview_event, deploy_click, chat_message_sent, integration-related events if any).
10. Write Phase 0 memo `findings/00-foundations.md`: what we can/can't measure; gaps list (e.g., no end-user telemetry inside deployed apps → proxy via Mongo).

### PHASE 1 — Segment sizing: how big is the AI-builder economy? (Steps 11–25) — "Weeks 1–2"

11. Pull 90-day job universe: volume, users, projects, spend by `prompt_name` and `chat_mode`.
12. Run keyword pre-filter over 90-day tasks → AI-candidate share by week.
13. **LLM-classify a stratified sample (~1,500–3,000 jobs)** into taxonomy: (a) chat-wrapper/assistant, (b) AI-SaaS generator (ebooks/images/video/content), (c) agent/automation (multi-step, tools, schedulers), (d) RAG/knowledge app, (e) AI feature inside non-AI app, (f) voice/calls, (g) not-AI. Capture confidence + secondary labels.
14. Calibrate keyword filter precision/recall against LLM labels; produce corrected segment-share estimate ±CI.
15. Estimate **share of platform credit spend** attributable to AI-product jobs (join classification → cost).
16. Trend analysis: AI-product share of new projects by month since 2025-06 (sample per month) — growing or flat? (tests H1, H8 split by sub-category).
17. Revenue overlay: AI-builders' share of subscription revenue + topups vs other builders.
18. Geo/language split of AI builders (seeds show IT, FR, ID, EN — multilingual matters for GTM).
19. Device split (Mobile App vs Desktop) for AI builders — mobile builders may need different UX.
20. First-job analysis: what % of *new signups'* first prompts are AI products? (acquisition framing; `conversions_dataset.prompt_type` + own classification).
21. Conversion overlay: signup→paid conversion rate for AI-first-prompt users vs others (tests H3).
22. Model mix on AI jobs (opus/sonnet, thinking mode) and cost/job distributions (p25/50/75/95) AI vs non-AI.
23. Fork-chain depth & iteration counts AI vs non-AI (tests H9).
24. Identify **whales**: top 200 users by 90-day spend; classify how many are AI builders; list top 100 highest-spend AI projects for Phase 2/3 deep-dives.
25. Write `findings/01-segment-sizing.md` with the "AI-builder economy" headline numbers (TAM-on-platform).

### PHASE 2 — Seed + whale job forensics (Steps 26–40) — "Weeks 2–3"

26. For each of the 17 seed jobs: full metadata, fork chain, total cost, duration, deploy status, HITL count.
27. For each seed job: trajectory narrative — what was built, which integrations attempted, where the agent struggled (errors, retries, long tool loops).
28. Extract every **integration touched or requested** across seeds (LLM providers, Stripe/PayPal, image gen, TTS, email, WhatsApp…), and whether it used Emergent universal key vs user's own key.
29. Extract every **premade-feature gap**: things users asked for that the agent hand-rolled (auth, credits system, admin panel, chat UI, PDF export, payments).
30. Check each seed app's deployment + app-Mongo for end-user signups (S4 check) + custom domains (S5).
31. Pull each seed user's profile: signup date, plan, LTV, total projects, still-active?
32. Classify each seed's outcome on S0–S5 ladder; note the blocking step.
33. Repeat 26–32 (lighter, batched) for **top-50 highest-spend AI projects** from Step 24 ("big jobs").
34. Repeat for a **random-100 AI projects** sample (unbiased view, not just whales).
35. Specifically mine for **agent-builder jobs** (sub-category c): what agent patterns do users want (schedulers, scrapers, social bots, email agents, multi-agent)?
36. Measure per-seed/per-whale **time-to-first-preview** and **prompt→deploy** durations.
37. Quantify HITL repair loops: % of HITL messages that are bug-fix requests vs new features (join `hitl.IntentClassificationEvent`).
38. Identify the 10 most common *technical failure signatures* in AI jobs (from trajectory errors + cortex_debugger spot-checks on ~10 jobs).
39. Cross-reference seed/whale users with support tickets (by email) — what did they file?
40. Write `findings/02-job-forensics.md`: per-cohort narratives + the integration/feature gap longlist (input to Phase 8).

### PHASE 3 — Cohorts & success metrics at scale (Steps 41–58) — "Weeks 3–5"

41. Build the **master cohort table** (BigQuery SQL, materialized as a saved Redash query): one row per AI project with: user, category, start date, cost, iterations, deploy flag, custom-domain flag, HITL count, duration, model, outcome ladder stage.
42. Compute S0→S1→S2→S3 funnel conversion for AI vs non-AI projects (the **build funnel**).
43. For deployed AI apps: sample ≥100 apps' Mongo databases for end-user counts → S4 rate; distribution of end-users per app (how many AI apps have >10, >100, >1000 real users?).
44. S5: which deployed AI apps added payments (Stripe key acknowledgement in deployments, task mentions, integration proxy calls)?
45. Define cohorts by **spend tier**: small (<5 ECU), mid (5–25), large (25–100), whale (>100) — distribution of outcomes per tier ("do bigger spends succeed more?").
46. Define cohorts by **category** (taxonomy a–f): success rates, spend, retention per category → which AI product types succeed today and which burn credits and fail.
47. Define cohorts by **start month**: are newer AI cohorts more successful (platform improving) or less?
48. Builder retention curves: M1/M2/M3 job-creation retention by category × outcome stage (tests H5 — does shipping S3/S4 retain builders?).
49. Subscription churn overlay: cancellation rate within 30/60d for AI builders whose flagship project stalled at S1/S2 vs shipped S3+.
50. Topup behavior: do AI builders top-up more after reaching S3 (deployed)? Causality direction check via event ordering.
51. Cost-of-success: median ECU from prompt→S3 per category (the "price of an AI app" today) — and the failure tax (spend on projects that never deploy).
52. Iteration economics: cost per fork-level; identify the "death valley" iteration count where users abandon.
53. Quantify **multi-project behavior**: % of AI builders who start a 2nd project within 30d (expansion signal).
54. Referral/virality check: do successful AI builders refer more (signups_raw_dataset.invited_by)?
55. Compare AI builders on Free vs paid plans: free-plan AI build attempts that died from credit exhaustion (overdraft/balance-zero events near abandonment).
56. Weekly active AI-builders time series (the north-star candidate metric) + its decomposition (new vs retained).
57. Sensitivity checks: re-run key cuts excluding bots/internal, and excluding $0-cost jobs.
58. Write `findings/03-cohorts-success.md` with the **AI Builder Funnel dashboard spec** (Redash) + headline: where the funnel leaks.

### PHASE 4 — Friction & failure driver analysis (Steps 59–72) — "Weeks 5–7"

59. Error taxonomy: cluster trajectory `error_message` strings on AI jobs (top 30 signatures, frequency × cost burned).
60. LLM-key friction: count AI jobs where user had to paste/provision an external API key; measure drop-off around those steps (tests H6).
61. Universal-key usage: credit_ledger `UNIVERSAL_KEY` debits — adoption, spend, and retention of users using it vs own keys.
62. Integration failure rates from Integration Proxy DB: per-provider error rates, latency, which providers users attempt most and fail most.
63. Streaming/timeout issues specific to AI apps (21-min sync timeout, long-running generations) — from errors + support tickets.
64. Deployment friction for AI apps: deploy failure rate vs non-AI (env vars, key injection, websockets).
65. Preview friction: preview_event gaps on AI jobs (AI features often need backend keys → broken previews?).
66. Cost-shock analysis: HITL/support complaints mentioning credits/cost on AI jobs; spend spikes preceding abandonment.
67. Mobile-builder friction: AI builds started on mobile app — completion gap vs desktop.
68. Agent-loop quality: on agent/automation jobs (category c), how often does the built agent actually run on schedule/webhook vs remain demo-ware? (envcore/cortex checks on sampled apps).
69. Support-ticket clustering for AI builders (cluster field + LLM-cluster subjects) — top 10 themes.
70. Churn-reason mining: `churn_reason_classifications` for churned AI builders; bad-churn reasons ranked.
71. Synthesis: rank the **top 12 frictions** by (users affected × spend burned × churn correlation).
72. Write `findings/04-friction-failures.md`.

### PHASE 5 — Builder economics & monetization (Steps 73–82) — "Weeks 7–8"

73. LTV by builder segment (category × success stage): subscription + topup revenue per user, 90-day and lifetime.
74. Payback framing: revenue per AI builder vs credits cost-to-serve (gross-margin proxy per segment).
75. Price-sensitivity probes: conversion by plan tier among AI builders; which tier do successful AI builders sit on?
76. Expansion revenue: upgrade rates after S3/S4 milestones.
77. The "operator" opportunity: deployed AI apps' ongoing usage → would builders pay for hosted inference, key management, usage-based billing rails? Estimate from app activity (deployments billing + integration calls).
78. End-user monetization patterns: of S5 apps, what do they charge end-users (mine task text/HITL for pricing mentions — e.g., seed job with $8/week PayPal paywall)?
79. Whale interviews-by-proxy: reconstruct 10 whale journeys end-to-end (timeline: signup→builds→payments→today) as case studies.
80. Model the revenue impact of moving funnel conversion: +10pp S2→S3 on AI jobs = $X MRR (from cohort LTV deltas).
81. Identify the 20 highest-potential *currently-stuck* builders (high spend, S2-stalled, active sub) — candidate design partners for new features.
82. Write `findings/05-builder-economics.md`.

### PHASE 6 — Voice of customer at scale (Steps 83–90) — "Weeks 8–9"

83. Mine ALL HITL messages on AI jobs (sampled ~5k) with an LLM for: explicit feature requests, integration requests, frustration signals; produce ranked request table (tests H7).
84. Mine support tickets (≥2026-01-10) from AI builders similarly.
85. Mine churn reasons free-text for AI builders.
86. Mine task prompts for **named external tools** (n8n, Zapier, WhatsApp, Telegram, Notion, Shopify, etc.) → demand map for premade integrations.
87. Mine for **named model/providers** (GPT-5.2, Nano Banana, Kokoro, ElevenLabs, etc.) → universal-key coverage gaps.
88. Public-web VoC: what do Emergent users say on X/Reddit/Discord about building AI apps on Emergent vs alternatives (sample).
89. Consolidate into a **demand-ranked backlog**: feature/integration × request frequency × requester spend-weight.
90. Write `findings/06-voice-of-customer.md`.

### PHASE 7 — Competitive & market intelligence (Steps 91–97) — "Week 9"

91. Deep teardown: Lovable, Bolt.new, Replit Agent, v0, Base44, Firebase Studio — their AI-app-building affordances (AI templates, LLM key handling, AI SDK integrations, agent builders).
92. Adjacent: agent-builder platforms (LangGraph Cloud/Platform, n8n, Make, Lindy, Relevance AI, Vapi for voice) — what primitives they offer that our users hand-roll.
93. AI-SaaS-starter ecosystem scan (boilerplates people pay for: chat UI kits, RAG starters, credit-billing kits) — proves willingness-to-pay for premade blocks.
94. Pricing scan: how competitors price AI usage (BYOK vs bundled inference) — informs universal-key strategy.
95. Identify 3 strategic gaps where Emergent can be first/best (hypothesis: "build AND operate AI products end-to-end").
96. SWOT + positioning draft for "Emergent = the place to launch AI products".
97. Write `findings/07-competitive-landscape.md`.

### PHASE 8 — Opportunity synthesis & feature scoring (Steps 98–105) — "Week 10"

98. Consolidate opportunity longlist from Phases 2,4,6,7 (expect 25–40 candidates).
99. Group into 4 strategy tracks: **(T1) Agent/AI templates**, **(T2) Premade integrations** (model providers, channels, payments), **(T3) AI-product building blocks** (chat UI, RAG, metering/billing, evals, key mgmt), **(T4) Operate/GTM rails for builders' own products** (analytics, end-user auth, monetization).
100. Score all candidates: RICE (reach from Phase 3 cohort sizes, impact from funnel-leak economics in Step 80, confidence from VoC strength, effort with eng input).
101. Map each candidate to the exact funnel leak + cohort it fixes; kill anything that doesn't map.
102. Stress-test top 5 with counter-evidence sweep (adversarial pass over our own data).
103. Pick **1 flagship project + 2 fast-follow features**; write decision memo with kill-criteria.
104. Validate technical feasibility of top picks against the mono codebase (templates system, integration-proxy, playbooks, deployer) — effort sizing with file-level pointers.
105. Write `findings/08-opportunity-scoring.md` + ADR `adr/0001-flagship-bet.md`.

### PHASE 9 — PRD, build plan, GTM (Steps 106–112) — "Weeks 11–12"

106. Full PRD for the flagship (problem, users from Step 81 list, UX flows, requirements, success metrics, rollout flags).
107. Eng design doc: architecture, services touched, template/playbook/prompt changes, integration-proxy additions, milestones.
108. Experiment design: A/B plan (cohort rules per knowledge base: conversion → last-but-one digit), guardrail metrics.
109. GTM strategy: positioning, launch narrative ("ship your AI product in a day"), channels (in-product template gallery, lifecycle emails to stuck-builders list from Step 81, X/launch video, SEO templates pages, affiliate/community), pricing/packaging decision (incl. universal-key bundling).
110. Design-partner program: recruit 10–20 from Step 81 list; feedback loop plan.
111. Launch checklist + success dashboard spec (north star: weekly shipped AI apps / weekly active AI builders).
112. Write `09-flagship-prd.md`, `10-gtm-plan.md`.

### PHASE 10 — Measurement & iteration loop (Steps 113–118) — "Ongoing"

113. Stand up the AI-Builder Funnel dashboard (Redash) with weekly snapshots.
114. Define the experiment readout protocol (weekly) + kill/scale criteria per feature.
115. Post-launch cohort tracking: do feature-adopters ship/retain more (vs matched controls)?
116. VoC re-run cadence: monthly HITL/support mining refresh to catch new demand.
117. Quarterly re-run of segment sizing (Phase 1) to track AI-builder share trend.
118. Retro memo: which hypotheses H1–H10 held, which died; update strategy.

---

## 4. Operating Notes

- **Artifacts:** every phase ends with a findings doc in `findings/`; decisions become ADRs in `adr/`; the README indexes everything.
- **Method bar:** every quantitative claim gets a query snippet committed alongside it (reproducibility); every LLM classification gets a rubric + sampled-accuracy check; adversarial verification pass before any number goes in a headline.
- **Sequencing:** Phases 1–3 are the critical path; 4–7 parallelize; 8+ gated on 1–7.
- **Session plan:** this is a multi-session program. Each session: pick next steps from this plan, execute, write findings, commit, update README status table.

## 5. Status Tracker

| Phase | Status | Findings doc |
|---|---|---|
| 0 Foundations | ✅ done 2026-06-12 (steps 1–10; step 7 validated live on 3 apps) | `findings/00-foundations.md` |
| 1 Segment sizing | 🟡 mostly done (steps 11,12,15,17²,20,21,22,24 done; 13–14 LLM calibration, 16 sub-category trend, 18–19, 23 remain) | `findings/01-segment-sizing.md` |
| 2 Job forensics | ⚪ | |
| 3 Cohorts & success | ⚪ | |
| 4 Friction | ⚪ | |
| 5 Economics | ⚪ | |
| 6 VoC | ⚪ | |
| 7 Competitive | ⚪ | |
| 8 Scoring | ⚪ | |
| 9 PRD + GTM | ⚪ | |
| 10 Measurement | ⚪ | |
