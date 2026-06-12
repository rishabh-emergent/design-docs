# ADR 0001 — Flagship growth bet: the Ship Loop

**Status:** Proposed (awaiting Rishabh ratification) · **Date:** 2026-06-12 · **Deciders:** Rishabh (owner), Claude (research)

## Context

11-phase research program (findings 00–08) on AI-product builders (~12% of root projects, ~28% of spend root-basis, 1.66× conversion). The single quantified funnel leak: **57.4K users/month reach "engaged" (≥$10 invested) on an AI project and never deploy**; deployers monetize at $206.71/90d vs $13.94 (engaged). Death mechanics measured: 63% never return after the kickoff questionnaire; 83.8% die at zero credit balance (decision window 1.9h); deploy failures are the #1 support cluster and charge-on-failure is the top churn quote.

## Decision

Build the **Ship Loop** as the flagship: (1) first-build **return loop** (push/email "your app is ready" + live preview + one-tap next action), (2) **ship-it credit pack** (project-scoped ~150–200 ECU offer at zero-balance for projects >$10 sunk, framed as progress preservation), (3) **deploy preflight + auto-refund on failed deploys** (env/LLM-key checks, prod-parity, smoke test), (4) **price-to-finish meter**. Fast-follows: AI Product Starter Kits (3 templates), Universal-key runtime productization (after proxy-log ETL). Parallel: AI Builder plan pricing experiment.

## Alternatives considered

- **Templates-first flagship** — strong evidence (OpenClaw wave, boilerplate WTP, LifeScore) but un-quantified revenue path vs Ship Loop's measured $192.77/user delta; demoted to fast-follow 1.
- **Operate-rails-first** — biggest strategic white space but tiny current base (4.6K prod apps, median 10 calls/day) and blocked on log ETL; demoted to fast-follow 2.
- **Agent-platform pivot** — organic agent-building demand flat (H8); template-mediated demand served via Starter Kits/gallery instead.

## Consequences & guardrails

- Experiment-gated (conversion cohorts = last-but-one user-id digit): kill/iterate if engaged→deployed lift < +1.5pp or pack attach < 3%.
- Auto-refund reduces short-term deploy revenue; accepted — it defuses the most-quoted grievance and protects the $206/user segment.
- North star: **Weekly Shipped AI Apps**; guardrails: 24h conversion, support-ticket volume in deploy clusters, bad-churn rate, gross margin per finance review.
- Finance dependency: whale-margin review (top-20 consumed $2.39M vs $547K paid) before any feature that manufactures heavy consumption.
