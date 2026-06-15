# Phase 4b — Top-Issue Audit & Root-Cause Validation (120 high-spend AI jobs)

**Date:** 2026-06-15 · **Cohort:** 120 jobs classified "AI Products & Agents" (`icp_classification.verticals_classification_v2`, confidence >0.95, non-expo), each >200 ECU since 2026-06-09. · **Method:** bulk-fetched intent + 3,625 HITL messages + 1,907 error signals + integration counts → 120 parallel audit agents → deterministic aggregation → code-level root-cause against `app-builder` base template + `cortex/prompts`. · Raw: workflow `wf_1951cf39-da1`.

## 0. Outcome baseline (alarming)

- **Only 4/120 jobs (3.3%) shipped clean.** 115 partial, 1 stalled.
- **The agent introduced at least one of its own errors in 116/120 (96.7%).**
- User frustration ≥ level 2 in **72/120 (60%)**, maxed (3) in 7.

## 1. Issue ranking (by # jobs affected)

| Rank | Issue | Jobs | % | Sev-wt |
|---|---|---|---|---|
| 1 | **AGENT_FALSE_COMPLETION** | 68 | **56.7%** | 153 |
| 2 | **GEN_RELIABILITY** | 53 | **44.2%** | 126 |
| 3 | UI_UX_CHURN | 48 | 40.0% | 82 |
| 4 | INT_OTHER_FAILURE | 43 | 35.8% | 96 |
| 5 | INSTRUCTION_BURDEN | 42 | 35.0% | 80 |
| 6 | DEPLOY_PROD_PARITY | 32 | 26.7% | 73 |
| 7 | COST_FRUSTRATION | 30 | 25.0% | 60 |
| 8 | AGENT_REGRESSION | 29 | 24.2% | 66 |
| 9 | AGENT_LOOP | 29 | 24.2% | 64 |
| 10 | LONGRUN_TIMEOUT | 24 | 20.0% | 57 |
| 11 | INT_RATELIMIT_SESSION_BUG | 23 | 19.2% | 48 |
| 12 | ENV_INFRA_ERROR | 23 | 19.2% | 45 |
| 13 | AGENT_IGNORED_INSTRUCTION | 23 | 19.2% | 42 |
| 14 | AUTH_ISSUE | 20 | 16.7% | 44 |
| 15 | INT_UNIVERSAL_KEY_UNSUPPORTED | 20 | 16.7% | 40 |
| 16 | TESTING_BLIND | 20 | 16.7% | 40 |
| 17 | PLATFORM_CAPABILITY_MISMATCH | 18 | 15.0% | 40 |
| — | INT_KEY_MISCONFIG_RUNTIME | 14 | 11.7% | 31 |
| — | INT_STRIPE_TESTLIVE | 13 | 10.8% | 34 |

**By _primary_ (biggest-per-job) issue:** GEN_RELIABILITY 20, AGENT_FALSE_COMPLETION 13, INT_OTHER_FAILURE 10, AGENT_LOOP 8, DEPLOY_PROD_PARITY 8, INT_STRIPE_TESTLIVE 8.

**Attribution:** agent-behavior is the *primary* failure in ~55% of jobs; integration/external ~23%; deploy/prod-parity ~10%; platform/cost/timeout ~12%. Even when the trigger is external, the *unrecoverable* mode is usually the agent declaring success anyway.

---

## 2. THE ROOT CAUSE (validated against code) — the Definition-of-Done is blind to the product's core

The #1 and #2 issues (false completion 57% + gen-reliability 44%) are one defect. The agent declares "100% PASS" while the core feature is broken **because the platform's definition of "done" never executes the core feature.**

### 2a. What the builder treats as "done" — `prompts/prompts/fullstack_opus_4_8.md`
- L62: *"Finish task if testing via testing agent has already passed."*
- L67: *"Testing agent is a MUST before finishing the task and declaring success."*
- L88: *"Call `deployment_agent` for a health check. Once it returns passing, you MUST call the `finish` tool."*
- Speed bias that pushes premature finish: L60 *"don't invoke testing multiple times before the first finish… show early results"*; L65 *"Prioritize finishing the task quickly over getting stuck in a finesse loop"*; L67 *"finish… to provide an AHA moment quickly."*

→ **Completion = "testing-agent passed" + "deploy health-check passed."** The entire bar is delegated to the testing agent.

### 2b. What the testing agent actually verifies — `prompts/prompts/deep_testing_backend_v2.md` / `testing_agent_v4_sonnet_4_6.md`
- It asserts **HTTP status codes + JSON response shape on CRUD/auth endpoints** (testing_agent_v4 L249–350: 200+token, 201+fields, persisted, 404 after delete).
- It is **explicitly told NOT to test the things AI products are made of:**
  - `deep_testing_backend_v2.md:55,139,177` — **"DO NOT test frontend / UI integration."**
  - `deep_testing_backend_v2.md:140` — **DO NOT test "Features involving hardware components like audio/ video."**
  - `deep_testing_backend_v2.md:357–359` — for "LLM or any third-party integration not working," it only **"Inform if any piece of code is `mocked`"** — it does not run the real generation.

→ For an AI product whose core value is *generate a video / image / song / answer / place a trade*, the testing agent checks that `POST /generate` returns `200 + a job id` and calls it **PASS** — while the actual downstream generation fails or returns garbage. The main agent sees "100% PASS," is told it **MUST** finish, and declares success on a broken core.

**The corpus confirms the mechanism exactly:**
| Job | "Verified" by testing | Reality (user) |
|---|---|---|
| 23034b1f | "iteration_30: 100% PASS, Non-401 errors: 0" | buttons "NOT FOUND on page" |
| 2772d736 | song object renders | MiniPlayer "displays a song but never plays it" |
| 0e541f0c | endpoint returns success | trades "placed" never reached Capital.com |
| 208e05d2 | `POST` returns 200 | "Sora 2 returned no video bytes" |
| 54e643e4 | API responds | RAG "throwing wrong answers always" |

### 2c. Why the scaffold doesn't catch it — base template
`app-builder/templates/farm/backend/server.py` is **75 lines with no LLM/generation code and no golden-path test** — it ships `emergentintegrations==0.1.0` in requirements and nothing else. There is no reference "core-feature smoke test," so verification falls entirely to the testing agent, which is carved out of exactly this surface.

**Root cause, one sentence:** *the platform defines "done" as backend-CRUD tests + a deploy health check, but the testing agent is explicitly forbidden from exercising the frontend, audio/video, and real third-party generation — i.e., the core of every AI product — so the agent systematically certifies a broken core as "100% PASS."*

---

## 3. Secondary roots for the other top issues (validated)

**GEN_RELIABILITY (44%) & INT_OTHER_FAILURE (36%) — generation has no reliability or coverage floor.**
- Services that actually carry the core feature are uncovered third-party generators: in evidence, **fal.ai ×8, HeyGen ×5, ElevenLabs ×5, Veo ×4, Runway ×4, Wan ×3, Sora, GPT-Image, Kling**, plus WhatsApp ×9 / Resend ×8 / Stripe ×8 for outbound.
- The **universal key cannot serve any of these** — it is hardcoded to `[Claude, OpenAI, Gemini]` (`integration-proxy/core/llmkey/manager.go:24-32`; non-allowed providers rejected with `ErrInvalidProvider`, `update.go:26`). So image/video/voice products **must BYO a fal.ai/Kling/HeyGen/ElevenLabs/Runway key**, which then fails at runtime (out-of-funds, `downstream_service_unavailable`) and the testing agent can't see it.
- The generation playbooks (`prompts/playbooks/*_GENERATION_PLAYBOOK*.md`, `LLM_INTEGRATION_CHAT_*`) contain **no output-validation, no provider-health preflight, and no 429/backoff/retry/timeout/cleanup** (grep across all LLM playbooks = 0 rate-limit/retry hits). Hence LONGRUN_TIMEOUT (20%), INT_RATELIMIT_SESSION_BUG (19%), and stuck-generation credit burns.

**INT_UNIVERSAL_KEY_UNSUPPORTED (17%) & INT_KEY_MISCONFIG_RUNTIME (12%)** — direct consequence of the 3-provider universal key: anything else forces a BYO key, and the flow doesn't validate that key at paste time, so it fails only at runtime in the deployed app.

**INT_STRIPE_TESTLIVE (11%, but #6 *primary*)** — payments are disproportionately fatal (block revenue, noticed instantly). Test-vs-live key + unwired plan IDs/webhooks are never validated before checkout ships (246ba7cf: "couldn't start checkout," billing.py 502; 4ca85e97: live Razorpay key, plan IDs never wired, 5xx).

**UI_UX_CHURN (40%) + INSTRUCTION_BURDEN (35%) + AGENT_LOOP (24%)** — no loop-breaker and no constraint-pinning. The agent re-litigates pinned user constraints every turn (47f476f9 user prefaced 15+ turns with "Do not build any new capability"; 53e35e06 refused to remove "Made with Emergent" across 7 requests) and grinds identical verification failures (06afa21b: ~13 consecutive screenshot scroll-geometry checks, never converged). Speed bias (§2a) co-exists with non-convergence — finish-fast where it shouldn't, grind where it should stop and ask.

---

## 4. Fixes, ranked by jobs helped (each tied to its root)

1. **Real Definition-of-Done gate (helps ~68 + 53 + 29 + 20 jobs).** The main agent may not emit `finish`/"PASS" until the testing agent has **executed the actual core-feature user path and asserted real output** — click play → assert audio plays; generate → assert non-empty, well-formed bytes; place trade → assert external order id; RAG → assert the expected chunk. **Remove the blanket "DO NOT test audio/video / frontend" carve-out for AI-core features** (`deep_testing_backend_v2.md:140,139`); at minimum assert output existence + provider health even if quality is user-judged. Re-run the prior feature's smoke before declaring done (kills AGENT_REGRESSION). *This is the single highest-leverage change in the corpus.*
2. **Core-feature golden-path smoke + provider-health preflight in the scaffold (helps ~53 + 43).** Ship a generation smoke harness in the base template; before claiming the core works and before every ship, run the real pipeline once and detect provider-down/out-of-funds, surfacing a distinct "provider blocked — action needed" status instead of generic success.
3. **Generation-reliability playbook section (helps ~24 + 23).** Add mandatory timeout + bounded retry/backoff + job-status polling + stale-job cleanup/refund to every generation playbook; centralize a throttled client pattern.
4. **Universal-key coverage check + BYO-key live validation (helps ~20 + 14 + 13).** When the requested provider isn't in `[claude, openai, gemini]`, warn early and guide the BYO-key path; validate the pasted key (and Stripe test-vs-live + plan-id/webhook wiring) at paste time, before checkout/generation can ship.
5. **Loop governor + constraint pinning (helps ~48 + 42 + 29, plus COST_FRUSTRATION 30).** Detect N identical edits/verification failures with no state change → stop-and-ask or switch strategy; pin persistent user constraints so they aren't re-litigated.

Fixes 1–2 alone attack the issues present in the majority (false completion 56.7%) and plurality-of-primary (gen-reliability) of jobs and are the difference between today's **3.3% clean-ship rate** and a trustworthy one.
