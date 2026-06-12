# Phase 3 — Cohorts & Success: shipping is the hinge of the whole business

**Date:** 2026-06-12 · **Source:** workflow `wf_aaf70c79-b23`. Raw: [raw-phase37-sweep.md](raw-phase37-sweep.md)

## 1. H5 verdict: shipping predicts retention & revenue (✅ for retention/revenue, ❌ for sub-churn)

Cohort: 392,152 users whose first AI root job was Feb–Mar 2026. Outcome of that first project within 30d:

| Group (30d outcome) | N (%) | Job ret. d31–60 | Job ret. d61–90 | Paying d31–90 | Mean rev d31–90 | 2nd project ≤30d |
|---|---|---|---|---|---|---|
| **Deployed** | 7,908 (2.0%) | **20.4%** | 14.7% | **44.1%** | **$134.70** | 44.4% |
| Engaged not deployed (≥$10) | 100,636 (25.7%) | 10.3% | 7.0% | 11.5% | $18.36 | 18.0% |
| Shallow (<$10) | 283,608 (72.3%) | 7.0% | 4.6% | 3.7% | $4.72 | 35.4% (restarts) |

- Deployers retain 2× engaged and 3× shallow; pay at **3.8×** the engaged rate.
- **Anti-finding:** deployers cancel subscriptions slightly *more* within 60d (5.7% vs 3.7%, small n) — "mission accomplished" churn. Deployment is a monetization/retention lever, not a churn-prevention pitch.
- Correlational (deployers self-select: mean 30d project cost $404 vs $45) — causal share addressed in the impact model (05).

## 2. Death-valley mechanics (n=338,195 AI projects, Apr 1–May 15)

Deploy rate by spend band: <$2 → 0.04% · $10–25 → **1.1%** · $25–100 → 10.6% · $200–350 → 28.9% · >$500 → 52.4%.

- **The cliff is $10–25** (93K projects, 28% of all AI roots): the marginal-dollar curve jumps **~16×** between $10–15 and $25–50. One more meaningful iteration (~$10–25, ~3–5 HITLs) is worth more than anything else in the funnel.
- **Why engaged projects die (read 30 last-messages):** 63% end on a scoping answer or bare "proceed" — the user answered the kickoff questionnaire, let the agent build, and **never came back to see the result**. 23% feature-fatigue mid-iteration, 10% unresolved bugs, **0% mention credits** (stated-reason view; see 04 for the balance-data view).
- 87.6% of died-engaged projects were active a single calendar day.
- **~90% of death-valley users leave the platform entirely** (only 11% start another project within 14d). Win-back must resume the *existing* project (preview + chat + remaining credits), not prompt a fresh start.

## 3. S4 — first-ever measurement: do deployed AI apps get real users?

Sampled 45 deployed AI apps' production MongoDBs (44 measured, 98% coverage):

| Bar | Result |
|---|---|
| Has end-user auth collection | 24/45 (53%) |
| ≥3 registered end-users (S4) | 18/45 (40%) |
| **≥3 users with signups spread >24h (organic bar)** | **8/45 (18%)** |
| Auth apps where all signups in <60 min (self-test burst) | 10/24 (42%) |
| Max users observed | 54 (smart-photo-tools-1); zero apps >100 |
| Deployed but zero databases | 3/45 |

**The growth story currently ends at "deployed," not "adopted."** Auth-less lead-gen apps quietly outperform (one Telegram-bot tool: 2,096 records/30d). Implications: built-in app analytics ("your app got N signups this week"), share/launch moments post-deploy, native waitlist/lead-inbox blocks. Methodology is repeatable → quarterly S4 tracking metric.

## 4. Who the AI builders are (steps 18–19, 22–23)

- **Desktop-first:** 52.3% desktop signups vs 39.9% baseline (+12.4pp); less free-prompt usage (29.3% vs 33.0%).
- **Geo:** India = 50.3% of AI builders by volume; *propensity* over-indexes in AU (24.3%), CA, PK, IN, UAE, US (20–24% of those countries' builders build AI). Indonesia/Brazil/Mexico/Turkey under-index ~2× → localization opportunity. ~15% of organic AI tasks are non-English (FR, PT lead).
- **Model mix mirrors non-AI** (Opus 4.7 38.6%, Sonnet 4.5-thinking 35.4%) — model choice is not the differentiator; workflow is.
- **H9 (forks) rejected:** 98% of $10+ AI projects are single-job — iteration happens *inside* one long job via chat, not via forks. Invest in in-job ergonomics (checkpoints, rollback), not fork flows.
- **Data hygiene:** the OpenClaw template (~15% of AI-candidate sample, incl. prompt-injection attempts) must be excluded by filter v2 before targeting campaigns.

## 5. Adversarial red-team verdicts on Phase 1 headlines

An independent agent re-derived our four headline claims hunting for confounds:

| Claim | Verdict | Honest restatement |
|---|---|---|
| "18.5% of jobs, 51.1% of spend" | **CONFIRMED w/ caveat** | True per-job-task; under root-task rule it's 16%/27.6%. AI jobs are 2.98× longer AND 1.55× costlier per step (~71% of gap = length, 29% = intensity). **Use 16%/~28% externally.** |
| "Deploy 3.0% vs 1.8%" | **CONFIRMED** | Not a paid-mix artifact (AI uses *less* free prompts); within paid prompts 3.97% vs 2.40% (1.65×). |
| "Convert 8.8% vs 5.3%" | **CONFIRMED** | Device confound exists but minor: desktop-only 1.27×, mobile-web ~1.9×; mix-adjusted ~1.55×. Mobile AI-intent users are an underexploited pocket. |
| "Universal-key users 2.9× AI" | **WEAKENED → ~1.8×** | Half the multiplier was an activity artifact. Honest: "among equally active builders, UK users are ~2× as likely to be AI builders." |
