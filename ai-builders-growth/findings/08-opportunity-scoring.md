# Phase 8 — Opportunity Scoring & Portfolio Decision

**Date:** 2026-06-12 · **Inputs:** findings 00–07 (all phases) · **Decision record:** [adr/0001-flagship-bet.md](../adr/0001-flagship-bet.md)

## 0. Scoring frame

- **Reach** = users/projects touched per quarter (from Phase 1/3 cohort sizes).
- **Impact** = conservative incremental revenue per quarter at maturity, anchored on the Phase 5 measured deltas: engaged→deployed is worth **$192.77/user (90d)**, causal share assumed 30% → **~$58/converted user**; deployers are the $206.71/90d segment. Strategic value noted separately where revenue isn't the right lens.
- **Confidence** = strength/convergence of evidence (0–1).
- **Effort** = from the codebase feasibility audit (07 §4): S ≈ ≤1 eng-month, M ≈ 2–3, L ≈ 6+.
- Funnel anchors (per month, May 2026): 123.9K new AI builders → 57.4K engaged-not-deployed → 3.2K deployed ≤30d (engaged→deployed ≈ 7.3% incl. the deployed). Death valley = $10–25 band. Zero-balance window = 1.9h.

## 1. The full scored longlist (22 candidates)

| # | Candidate | Track | Reach /qtr | Conserv. $ impact /qtr | Conf. | Effort | RICE verdict |
|---|---|---|---|---|---|---|---|
| 15 | **First-build return loop** ("your app is ready" push/email + live preview + one-tap next action) | Funnel | ~170K engaged users | part of Ship Loop ↓ | 0.8 | **S** | ⭐ flagship component |
| 16 | **Ship-it credit pack** (project-scoped ~150–200 ECU offer at zero-balance, >$10 sunk) | Funnel/pricing | ~90K zero-balance engaged | part of Ship Loop ↓ | 0.8 | **S/M** | ⭐ flagship component |
| 18 | **Deploy preflight + auto-refund on failed deploy** (env/LLM-key checks, prod-parity, smoke test) | Funnel | ~21K deploying projects | part of Ship Loop ↓ | 0.8 | **M** | ⭐ flagship component |
| 22 | **Price-to-finish meter** ("~70% of the way to live; est. N ECU to deployable") | Funnel | all engaged AI projects | part of Ship Loop ↓ | 0.7 | **S** | ⭐ flagship component |
| — | **→ SHIP LOOP bundle (15+16+18+22)** | — | 170K/qtr | **$500K/qtr conserv. ($2M/yr); $1.66M/qtr upper** | 0.75 | ~1 squad-qtr | **FLAGSHIP** |
| 1 | **AI Product Starter Kits** — 3 templates: Claude-wrapper SaaS (multi-tenant auth+Stripe+credits+chat UI+metering), AI Generator w/ credits+paywall+checkpointing, WhatsApp AI agent | T1 | 18K adopters (15% of new AI builders) | $80–150K/qtr + SEO acquisition upside | 0.65 | **S–M** (content-shaped; env_resolver auto-provisions LLM key) | **FAST-FOLLOW 1** |
| 7 | **Universal-key runtime productization** — model picker in built app, key-health at deploy, per-app usage dashboard, auto-topup | T3/T4 | 21K deploys + 4.6K prod apps | $200–400K/qtr at maturity (runtime GMV 2–3× from $350K/qtr base) + **parity: table stakes at 5/6 competitors** | 0.6 | **M** (rails exist: llmrouter, wallets, budget endpoints) | **FAST-FOLLOW 2** |
| 17 | **"AI Builder" plan** (~250–300 ECU + runtime allowance, sized "ship 1 AI app/mo") + auto-topup | Pricing | 24K topup users + 75K subscribed AI builders | $150–300K/qtr (topup→MRR conversion) | 0.6 | M (packaging) | parallel pricing track |
| 3 | Playbook discovery/surfacing (91 exist; show before users ask) | T2 | all builders | modest direct ($1.50/use attach) + success-rate lift | 0.7 | **S** | quick win, do alongside |
| 21 | Iteration punch-list nudge after first build (3 concrete improvements) | Funnel | ~120K first builds | folded into Ship Loop v2 | 0.6 | S | v2 |
| 19 | "Ship now, iterate after" plateau nudge ($25–200 zone) | Funnel | ~26K plateau projects | folded into Ship Loop v2 | 0.6 | S | v2 |
| 11 | App analytics dashboard ("N signups this week") + S4 tracking | T4 | ~21K deployed/qtr | retention of $206/user segment; S4 lift | 0.55 | M | Q4; pairs w/ operate |
| 9 | Checkpointed-generation playbook pattern (checkpoint rows + resume endpoint) | T3 | generator segment (23.5% of AI) | trust/churn protection (58% of bad churn = cost/value incl. wasted generations) | 0.6 | **S** (playbook) | bundle into Generator template |
| 4 | WhatsApp/Telegram managed channel connector | T2 | 200K task mentions; agent templates dependency | enables FF1 agent template; competitor white space (0/6) | 0.55 | M | with FF1 |
| 12 | White-label tier ("remove Emergent branding") | T4 | small organic ask (3/400) | near-free margin on Pro+ | 0.5 | **S** (policy; enforced=M) | opportunistic |
| 8 | Auth+billing+credits preset (standalone block) | T3 | broad | superseded — ship *inside* Starter Kits first | 0.6 | M | inside FF1 |
| 14 | Resellable end-user credit packs (builder charges their customers) | T4 | 4.6K prod apps today | strategic moat (0/6 competitors); small near-term GMV | 0.5 | M/L | Q1-2027, after FF2 |
| 20 | Ask-human UX overhaul (batch approvals, don't-ask-again) | UX | 37.5% of HITL volume | cost reduction + completion; hard to size | 0.5 | M | UX roadmap |
| 10 | RAG/KB block | T3 | 6% of segment, high engagement | small | 0.5 | S/M | template add-on |
| 6 | AI-media bundle packaging | T2 | 40K mentions | small | 0.5 | S | playbook surfacing covers |
| 5 | Transactional email default | T2 | 282K mentions | reliability/支持 cost ↓ | 0.6 | S | inside Starter Kits |
| 2 | Full agent-template gallery (10 archetypes, heartbeat, hosted-OpenClaw positioning) | T1 | proven by OpenClaw wave (~100K installs in Mar) | acquisition + segment growth | 0.55 | M–L | Q4 expansion of FF1 |
| 13 | Operate dashboard ETL (proxy logs → BigQuery daily aggregates) | infra | prerequisite | enables FF2 + analytics | 0.9 | **S** | do immediately |

## 2. Counter-evidence stress-test of the top picks (step 102)

**Ship Loop** — what argues against it:
- *"63% never return" might mean low intent, not a missing loop* → mitigated: these users spent $10–100 and answered the questionnaire; 83.8% were at zero balance — the loop + pack attacks both reasons. Risk priced into the 30% causal assumption.
- *Deployers self-select; +5pp may not be achievable* → that's why the experiment gate exists (kill criteria below). Even +1.5pp clears cost.
- *Topups mostly precede deploy (73.5%)* → fine: the Ship Loop monetizes by extending paying journeys; the pack targets exactly the zero-balance moment payers already use (median 1.9h decision).
- *Whale-margin alert* → Ship Loop creates mid-size deployers, not whales; deployment debit is charged on success. Net positive for margin discipline (auto-refund kills a churn driver worth more than the refunded credits).

**Starter Kits** — counter-evidence:
- *Template-share of demand unproven on Emergent* → actually proven twice: OpenClaw wave (mass install behavior) + LifeScore PRD→deploy in 53 min. Risk is discovery, not demand → gallery placement + SEO pages are part of the plan.
- *Templates may cannibalize build spend (fewer ECU per app)* → deployers' 90d revenue is 80.6% topups on *continued* iteration; faster first success → more reach into the $206 segment. Accept lower per-build burn for higher completion.

**Universal-key runtime** — counter-evidence:
- *Operate base is tiny (4.6K apps, no whales)* → true; that's why it's FF2 not flagship, sized as parity + retention with modest GMV expectations. The 5-day log retention ETL (#13) must land first.
- *Runtime mix skews to cheap non-Claude models* → pass-through pricing (industry norm) still earns wallet share; visibility/control is the value, not margin on tokens.

## 3. Portfolio decision (step 103)

| Slot | Bet | Quarterly impact (conservative) | Kill criteria (4–6 wk experiment) |
|---|---|---|---|
| **FLAGSHIP** | **Ship Loop** — return loop + ship-it pack + deploy preflight/auto-refund + price-to-finish meter | **~$500K/qtr** at +5pp engaged→deployed (upper $1.66M/qtr); plus support-ticket and bad-churn reduction | Kill/iterate if engaged→deployed lift < **+1.5pp** or pack attach < **3%** of zero-balance engaged users |
| **FAST-FOLLOW 1** | **AI Product Starter Kits** (3 templates: Claude-wrapper SaaS, AI Generator w/ checkpointed jobs, WhatsApp AI agent) | $80–150K/qtr + acquisition (AI-intent converts 1.66×; SEO "build an AI ___" pages) | Kill if template-start share < **5%** of new AI builders or template deploy-rate < **2×** baseline after 6 wks |
| **FAST-FOLLOW 2** | **Universal-key runtime productization** (model picker, key health, usage dashboard, auto-topup) — prereq: proxy-log ETL | $200–400K/qtr at maturity + competitive parity | Re-scope if <**15%** of new deploys enable the runtime key or runtime GMV growth < **+25%**/qtr |
| Parallel | **AI Builder plan + auto-topup** (pricing experiment, last-but-one-digit cohorts) | $150–300K/qtr | Standard guardrails: no net MRR loss, churn neutral |
| Immediate S-items | Proxy-log ETL · playbook surfacing · white-label policy call | enablers / near-free margin | — |

**Combined conservative run-rate at maturity: ~$3.7–5.4M/yr incremental**, before acquisition upside and support/churn savings.

Sequencing logic: Ship Loop attacks the *quantified* leak now with S/M effort; Starter Kits grow the segment and make first sessions succeed (49% of churner cancels are ≤7d from first AI job); runtime productization converts "deployed" into "operated" and closes the table-stakes gap — together they ladder to the positioning **"Emergent is where you launch and run AI products."**

## 4. What we explicitly do NOT do (and why)

- **No standalone checkpointed-jobs platform primitive** (the only Large) — playbook pattern inside the Generator template first; revisit if template telemetry shows checkpoint failures persist.
- **No fork-flow investment** — H9 rejected; iteration is in-job.
- **No model-choice UX work** — model mix identical AI vs non-AI; not a differentiator.
- **No whale-acquisition features** until finance clears the $2.39M-consumed/$547K-paid margin question (05 §5).
- **No "pause-retention" discounts for shipped builders** — deployers churn slightly *more* post-ship; expansion hooks (2nd project, custom domain, operate rails) are the right motion.
