# PRD — Ship Loop (flagship) + Starter Kits & Runtime Key (fast-follows)

**Owner:** Rishabh · **Status:** Draft v1 (2026-06-12) · **Evidence base:** findings 00–08 · **Decision:** [adr/0001-flagship-bet.md](adr/0001-flagship-bet.md)

---

## 1. Problem

AI-product builders are Emergent's most valuable segment (subscribe 2.2×, revenue/user 5.7×, deploy 1.7×) — but **57K/month reach "engaged" (≥$10 invested) on an AI project and never ship**. Measured death mechanics:
- 63% never return after answering the kickoff questionnaire (the build finishes into silence).
- 83.8% are at zero credit balance within ±3 days of project death; payers decide within ~1.9h; non-payers are 89% gone in 14 days.
- Median deployed AI project costs 199 ECU vs Standard's 100 ECU/month — exhaustion is structural.
- Deploy failures = #1 support cluster for AI builders (2.1× over-index); "charged 50 credits but deployment failed" recurs in tickets and churn.

Deployers pay at 44.1% vs 11.5% and generate $206.71 vs $13.94 (90d). The leak is quantified: **+5pp engaged→deployed ≈ $166K per monthly cohort conservative (~$2M/yr).**

## 2. Goals & non-goals

**North star:** Weekly Shipped AI Apps (deployed AI-candidate projects/week; filter v2 excluding OpenClaw template).
**Goals (90d post-launch):** engaged→deployed +5pp (kill-gate +1.5pp); ship-it pack attach ≥5% of zero-balance engaged (gate 3%); deploy-failure ticket volume −30%; D31–60 builder retention of engaged cohort +2pp.
**Non-goals:** no codegen-quality work; no fork flows; no whale-acquisition mechanics (finance gate); no platform checkpointing primitive (playbook pattern only, in FF1).

## 3. Users

- **Primary:** engaged-not-deployed AI builders (57K/mo; desktop-heavy 52%, India+EN markets, 17% subscribed, median project $10–100).
- **Secondary:** zero-balance moments across all engaged builders; deploying builders hitting preflight.
- **Design partners:** 20 stuck high-spend builders (high spend, S2-stalled, active subscription — list queryable from cohort tables) + the 4 deployed seed users.

## 4. Feature spec — Ship Loop

### F1. First-build return loop (S)
When a build session ends agent-side with no user view within 30/120 min: push (mobile app) + email "**{AppName} is ready** — see it live" → deep link to running preview + 3-button next action: *Looks good → Deploy* / *Fix something* / *Keep building*. Includes one screenshot of the app (existing screenshot tooling). Frequency-capped; suppressed if user returned organically.
- Why: 63% of engaged deaths are never-returned; win-back must resume the *existing* project (90% never start another).

### F2. Ship-it credit pack (S/M)
Trigger: balance ≤0 AND active project with ≥$10 sunk. In-product (and email fallback within the 1.9h window): "**You're ~{pct}% of the way to live.** Est. {N} ECU to deployable + deployment included — one-time pack {price}." Project-scoped framing; 150–200 ECU sizing (covers median remaining build + ~50–59 ECU deploy debit). One per project.
- Why: 83.8% of engaged deaths at zero balance; payers already convert in ~1.9h; median deployed project = 199 ECU vs 100/mo Standard.

### F3. Deploy preflight + auto-refund (M)
Pre-deploy checks for AI apps: env vars/LLM-key presence + live key health-call, prod-vs-preview parity diff (URLs, CORS, websockets), backend smoke test; "Run health check" surfaced as a button (LifeScore user invoked it by name). **Deployment debit auto-refunded on failed deploy** (or charged only on success).
- Why: #1 ticket cluster; `OPENAI_API_KEY`-missing prod failures; most-quoted grievance.

### F4. Price-to-finish meter (S)
Persistent project header element: "est. {N} ECU to deployable" (model from cohort medians by category + remaining steps heuristics), updating as the build progresses; links to F2 when balance is low.
- Why: $111+ median price-of-success arrives as a shock today; 58% of bad churn is cost/value perception.

### v2 (post-gate): iteration punch-list after first build; "ship now, iterate after" plateau nudge; batch-approval ask-human UX.

## 5. Fast-follow specs (summary)

**FF1 — AI Product Starter Kits (S–M, content-shaped):** 3 templates via existing registry + `env_resolver_config` (auto-provisions `EMERGENT_LLM_KEY`): ① Claude-wrapper SaaS (multi-tenant auth, Stripe live-mode guided setup, end-user credits wallet, chat UI, token metering — the $400-boilerplate kill from onebrain); ② AI Generator (credits+paywall+**checkpointed generation playbook**: progress rows + resume endpoint — the ebook-ai-craft fix); ③ WhatsApp AI agent (BAILEYS_WHATSAPP playbook + heartbeat cron — the OpenClaw demand, hosted and safe). Each ships with an SEO landing page ("Build an AI ___").

**FF2 — Universal-key runtime productization (M; prereq: proxy-log daily ETL to BigQuery, S):** key-health at deploy; model picker block for the *built app* (the "give my users a provider picker" ask); per-app usage/spend dashboard; auto-topup. Pass-through pricing (parity with Lovable/Replit/Vercel). Beta list: the ~412 apps ≥50 calls/day.

**Parallel — AI Builder plan:** ~250–300 ECU + runtime allowance, "ship one AI app per month" framing; auto-topup offer at first topup; experiment-gated.

## 6. Experiment design

- Conversion experiments → **last-but-one digit** of user_id (per analytics KB); regression → last digit.
- Ship Loop: F1+F2+F4 as one arm vs control (they compose); F3 ships to 100% (reliability, not conversion).
- Primary metric: engaged→deployed within 30d of first AI root job. Secondary: pack attach, D31–60 retention, revenue/user 90d. Guardrails: 24h conversion, refund volume, support tickets, margin/user (finance).
- Readout weekly; decision at 4–6 weeks against kill criteria (ADR 0001).

## 7. Engineering notes (from feasibility audit, 07 §4)

- F1: notification path exists (RudderStack→MoEngage); needs build-completion event + screenshot attach. Touches: agent-service (event), comms.
- F2: credits system + ledger live; needs offer service + project-progress estimate. Touches: app-service (payments/offers), E1ectron.
- F3: deployment_agent + health-check tooling exist; refund = deployer + ledger policy. Touches: deployer, app-service.
- F4: cohort-median model server-side; UI in E1ectron project header.
- FF1: template registry + snapshots + `code-first-template` skill; zero service changes for template #1.
- FF2: integration-proxy llmrouter/wallets/budget endpoints exist; needs public app-facing API + drop-in UI; ETL from LLM-proxy Postgres (5-day retention!) to BigQuery first.

## 8. Risks

| Risk | Mitigation |
|---|---|
| Return-loop = notification spam | strict caps, suppress-on-organic-return, quality bar (screenshot present) |
| Pack cannibalizes Standard upgrades | track plan-mix guardrail; pack is one-per-project |
| Refund abuse (intentional failed deploys) | refund only on platform-side failure classes |
| Causal share < 30% assumption | experiment gate; even +1.5pp ≈ break-even |
| Whale margin | finance review precedes any consumption-stimulating v2 |

## 9. Measurement (Phase 10 loop)

Weekly dashboard (Redash): Weekly Shipped AI Apps · engaged→deployed by cohort · pack attach/decision-latency · preflight pass rate & refund volume · template-start share & template deploy-rate (FF1) · runtime-key enablement & per-app GMV (FF2) · S4 organic-adoption quarterly probe (Mongo methodology validated) · monthly VoC re-run (HITL mining refresh).
