# Phase 4 — Friction & Failure Drivers

**Date:** 2026-06-12 · **Source:** workflow `wf_aaf70c79-b23` (+ error baseline from Phase 1 sweep). Raw: [raw-phase37-sweep.md](raw-phase37-sweep.md)

## 1. Credit exhaustion: the hidden killer of engaged projects (H6 friction side)

Stated last-messages showed 0% credit complaints (03 §2) — but the *balance data* tells the real story:

| Signal | Number |
|---|---|
| Died-engaged AI projects ($10–100, no deploy) whose user hit **zero balance within ±3d of last activity** | **83.8%** (90,948 users) |
| Same for *deployed* AI projects' users | 55.9% (**+27.9pp gap**) |
| AI builders hitting zero who never run another job in 14d | **88.9%** (223K of 251K, Apr–May) |
| Median time from first zero-balance → first topup (payers) | **1.9 hours** (p25 ≈ instant) |
| May first-job AI users exhausting day-1 free credits | 65.6% — and they convert **1.8×** better (7.65% vs 4.15%) |

**Read:** deployers hit zero too — they just pay through it within hours. Non-payers are 89% gone in 14 days. The zero-balance moment is a decisive, fast-closing window: rescue interventions must fire **within hours**. Day-1 free-pool burn is a *qualification* signal — don't throttle it; optimize what happens at the wall (offer + remaining-cost estimate).

**The structural mismatch:** 1 ECU ≈ $1 metered cost (validated). Median deployed AI project = **199.4 ECU lifetime** (p25 110, p90 1,783) + ~50–59 ECU deployment debit, vs **Standard plan = 100 ECU/month**. The entry subscription *guarantees* mid-project exhaustion; even the p25 deployed project overruns a full Standard month.

## 2. Support burden: deployment is the #1 AI-builder pain

AI builders (578K users) filed 21.2% of all support tickets since Mar 1 but **44.9% of "Production Site Errors and Outages"** tickets (2.1× over-index) — and only 3% of account-deletion tickets (they engage, hit walls, churn on cost/quality; recoverable with product fixes). Tagged ticket subjects: deployment 33%, billing/credits 15%, app-broken 13%, refund 13%, integration/keys 5%.

**Most quotable grievance:** *"Charged 50 Credits But Deployment Failed"* — appears in both tickets and churn reasons. Auto-refund on failed deploy (or charge-on-success-only) defuses it.

## 3. Churn reasons (latest classified window 2025-12-01..2026-02-25; pipeline stale after Feb 25 — flagged)

- AI-builder bad-churn 54.9% vs non-AI 50.8% (+4.1pp).
- **58.4% of AI-builder bad churn is cost/value** (pricing perception + token wastage + budget); product quality 19%; onboarding confusion 8%.
- **Timing:** 33% of churning AI builders cancel within 0–1 days of their *first AI job*; 49% within 7 days. **The first AI-build session is make-or-break** — first-run success (pre-wired templates, working LLM-key onboarding) beats any later retention play.

## 4. Infra error signatures (from Phase 1 baseline, 60d)

AI jobs aren't more error-prone per step (0.0195% vs 0.0209%) but hit ≥1 error 2.6× more per job due to length. Top signatures: generic "Internal server error" (38% of AI error steps), Cloud Build failures, env restart/fetch failures, context-limit errors (most AI-specific, 616 steps/238 jobs). One OOM killed a $70 project mid-build.

## 5. Ranked friction list (users affected × spend burned × churn link)

1. **Credit exhaustion mid-build on engaged projects** (83.8% of deaths; 100K+ users/quarter) → ship-it pack + price-to-finish meter (see 05).
2. **First-session failure → 0–7-day churn** (49% of churner cancels) → first-run templates with pre-wired AI integration.
3. **Deployment failures + deploy-fee-on-failure** (#1 ticket cluster; 2.1× over-index) → AI-app deploy preflight (env/LLM-key checks, prod-parity), auto-refund.
4. **Never-returned-to-first-build loop** (63% of engaged deaths) → "your app is ready" return loop + live preview link.
5. **Long-generation reliability** ("credits consumed, no ebook"; context-limit signature) → checkpointed generation pattern.
6. **Plateau feature-fatigue, never launches** ($25–200 zone, 9–13% deploy) → "ship now, iterate after" nudge.
7. **Runtime key misconfiguration in deployed apps** (`OPENAI_API_KEY` errors; 5% of tickets) → key health check at deploy.
8. **Token wastage perception** (58% of bad churn is cost/value) → cost transparency + efficient-retry policies.
