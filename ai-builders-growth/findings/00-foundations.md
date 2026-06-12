# Phase 0 — Foundations: what we can measure, and how

**Date:** 2026-06-12 · **Source:** workflow `wf_66554e4b-ed7` (13 agents, prod Redash/BigQuery + deployer MCP). Raw outputs: [raw-phase01-sweep.md](raw-phase01-sweep.md)

## Measurement decisions (canonical, use everywhere)

1. **Job cost** = `SUM(trajectories_full_view.value_in_usd) GROUP BY job_id`.
   `jobs_full_view.total_credits_deducted_for_task` is **dead** — 0 for *all* 1.3M May-2026 jobs; 20/20 sampled jobs disagree. Trajectory coverage: 99.6% of jobs have positive cost; no duplicate trajectory ids (278.6M rows checked).
2. **HITL count** = trajectory rows where `human_message IS NOT NULL`.
   `user_messages_array` carries forward across steps and **over-counts ~7×** — do not use.
3. **Job `status` is unreliable** (all 17 seeds read `IN_PROGRESS` regardless of reality). Outcomes must be derived from deployments + activity, never status.
4. **Keyword filter v1 has a structural bias:** fork-job `task` text contains agent-generated handoff prose that mentions "agent"/"AI" → **92.3% of fork jobs** get flagged vs **15.7% of root jobs**. Therefore:
   - User/project-level AI classification → use **root-job task** (trustworthy floor).
   - Job-level spend attribution → bracketed estimate (root-task basis = floor, any-job basis = ceiling).
   - LLM calibration (plan steps 13–14) is mandatory before headline numbers are finalized.
   - Noisiest keyword buckets: generic `ai` (39.2% of matches) and `agent(s)` (35.0%).
5. **`error_message` is sparsely populated** (0 errors across all 17 seeds; platform step-level error rate ~0.02%). It captures infra failures, not build-quality failures. Friction analysis needs complementary signals (HITL content, support tickets, abandonment).

## What the Integration Proxy DB actually is (DS 18)

**Not** a request log — an integration **registry + metering store** (15 tables). No per-request rows, no error rates. What it gives us:

| Signal | Numbers (as of 2026-06-12) |
|---|---|
| Universal LLM keys issued (LiteLLM, 1/user) | 2,120,408 users; **357,989 paid-active** vs 1,751,641 free-active; allowed providers ≈ always `[claude, openai, gemini]` |
| **LiteLLM topups** (deployed apps consuming LLM via universal key — the strongest "production AI app" signal) | 90d: 56,752 entries / 348,394 ECU / **3,626 distinct users**; 30d: 2,239 users; modal topup 5 ECU |
| Stripe app integrations (`app_integrations` = 100% stripe) | 131,767 apps all-time; 39,042 last 90d |
| Tigris object storage | 95,370 users provisioned; 56,689 stored >0 GB last 30d |
| Push notifications (SuprSend, since 2026-05-22) | 352 apps — nascent |

For call-level LLM usage/errors → LLM Proxy Postgres (DS 9) or `credit_ledger.reference_type='UNIVERSAL_KEY'`.

## End-user adoption (S4) is measurable — proven live

Pipeline: `job_id → app_name` via `analytics.deployer_db_data` → `mcp__deployer__run_mongo_query(app_name)`; each app has one DB named `{app_name}-test_database`. Verified on 3 seed apps in prod:

| App (seed) | Result |
|---|---|
| `team-chat-workspace` (onebrain.team, custom domain) | **64 end-users** (63 email-verified), signups still arriving the morning of analysis; 164 chat messages — genuine third-party adoption |
| `personal-growth-lab-2` | 2 users, both `t***@lifescore.app` within 2 min — builder self-test (⇒ need own-account filter) |
| `ebook-ai-craft` | No `users` collection (auth-less app) → fall back to activity docs (3 ebooks) |

**Rules for Phase 3 scale-up:** redact PII server-side inside the Mongo `$project` (pattern validated); classify self-test accounts (same-domain emails, burst creation); auth-less apps need activity-document fallback.

## Gaps register

- No end-user telemetry inside deployed apps beyond their Mongo (no pageview data for builders' apps). Mongo counts + litellm topups + Stripe integration are our S4/S5 proxies.
- `value_in_usd` (ECU value) vs what users actually *paid* are different things — whale platform consumption can exceed revenue paid (top-50 whales: $4.65M 90d consumption vs ~$1.08M lifetime revenue; seed cohort: $61k vs $24k). **Open finance question** (scaling factors, bonus credits, plan economics) — flagged for Phase 5, do not conflate consumption with revenue in any headline.
- Support analytics only ≥ 2026-01-10. PostHog identity stitching incomplete for blocked trackers.
- `fork_chain` only holds forked jobs; ~96.9% of jobs are their own root (forking is rare and concentrated in `fork_fullstack_prompt_*` templates).
