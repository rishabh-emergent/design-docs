# Phase 2 — Job Forensics: what AI builders actually build, where money dies, and what they keep asking for

**Date:** 2026-06-12 · **Source:** workflow `wf_29190caa-2ed` (8 agents). Raw outputs + SQL: [raw-phase02-sweep.md](raw-phase02-sweep.md) · Calibration corrections to Phase 1 included here (§1).

## 1. Calibrated segment size (closes plan steps 13–14)

Hand-classification of 620 root-job tasks (250 keyword-matched + 250 non-matched + 120 random-matched):

| Measure | Value |
|---|---|
| Keyword filter **precision** | 59.6% (250-sample) / 55.0% (120-sample) → working band **55–60%**; whale roots 67.9% |
| Keyword filter **recall miss** (false negatives among non-matched) | 3.2% (CI 1.6–6.2%) — mostly non-English "IA", "Al" typo, implicit AI |
| **Corrected true AI-product share of root projects** | **~11–14.5%** (formula: 0.157·P + 0.843·0.032) — call it **~1 in 8 projects** |
| Corrected whale-AI spend (28 flagged → 19 confirmed) | **$1.13M / 90d in top-100 alone** (72.7% of flagged) |

False-positive patterns (now documented for filter v2): meta-references to the builder itself (~28/101), branding-only "AI" (~18), game-NPC "AI" (~10), builder-as-assistant tasks (~8), word collisions (French *j'ai*, Italian *ai*, RAG=red/amber/green) (~14).

**Sub-category mix among true AI products (n=149):** ai-feature **35.6%**, generator-SaaS **23.5%**, agent-automation 20.8% (inflated — see §2), chat-assistant 11.4%, RAG 6.0%, voice 2.7%.

## 2. The OpenClaw/MoltBot discovery (H8 verdict — and the biggest strategic signal so far)

Monthly classification (360 jobs, Jan–Jun 2026) shows agent-automation share spiking 9% → 43% → 53% (Jan→Feb→Mar) then collapsing to 7% by June. The spike was **a wave of copy-paste "OpenClaw / MoltBot Installation" template prompts** — users mass-deploying a prebuilt open-source personal AI agent (peak ~100K matched root jobs in March at sampled rate; 18/20 of March's category-C sample; one of Rishabh's 17 seeds is this pattern).

- **H8 organic verdict: NOT supported.** Organic from-scratch agent demand is flat at 5–14% of AI products (~7–20K root projects/month).
- **But the wave is direct, observed evidence that users deploy prebuilt agent templates en masse when one exists.** Demand for *agents* is real; demand for *building them from scratch* is not. This is the strongest data point yet for the **agent-template track (T1)**.
- Caveat: the install jobs themselves are low-value to us as jobs (median $0.58, 0 HITL, 0 deploys) — the lesson is distribution power of templates, not the install jobs' economics.

## 3. Whale forensics (19 confirmed-AI projects, $40K–$159K each)

**What whales build:** NOT toy chatbots. By spend: **agent-automation #1** — 7 projects / $408K (36%): LLM-tournament paper ranker (kurate.org), creator-outreach autopilot (ChamsPilot), managed agent-hosting SaaS (ObeGee), market-sensing agent, AI trading platform, Gmail-RFQ sales agent + WhatsApp bot (1buy.ai), job-application automation. Then ai-feature $250K, chat-assistant $200K, **voice $110K** (Quran recitation-following hifzly.net; real-time sales-call copilot reppx.ai), generator $108K, doc-AI $48K.

**Outcomes:** 15/19 deployed, 9/19 custom domains. **Two of the biggest agent-automation whales ship OFF-platform** (own VPS / DigitalOcean) — they use Emergent as their dev team and export to self-managed infra, pasting server shell output back into HITL. An "export/operate on your own infra" story is a real retention surface.

**What burned their money (HITL evidence):** (1) huge volumes of pure approval round-trips ("yes", "proceed" — RealTalk burned $85K/330 jobs/5,280 HITLs and never deployed); (2) real-time voice debugging (streaming STT, mic permissions, model conversion); (3) data-pipeline persistence ("series disappeared after restart"); (4) LLM cost confusion (user disputing per-call Opus pricing); (5) auth/email plumbing; (6) asset-pipeline ops; (7) endless UI nits on huge codebases.

## 4. Random-120 sample: where the money dies (unbiased view)

- True-AI deploy rate 3/66 = 4.5% — consistent with the 3.0% population number.
- **Engagement hierarchy:** chat-assistants go deepest (median $59, 8 HITLs, 2/7 deployed); generator-SaaS and ai-feature apps stall early (median ~$10, 1 HITL, 0% deployed).
- **The death valley:** 37/63 dead projects die in the **$2–25 "one default session" band** — after the first real job, before any deploy. 16/63 die under $2 (instant abandonment). Top 9 burners (≥$50) hold 65% of dead spend.
- Payments are almost absent in practice (1 mention) despite many paywall/credit business models in the same tasks — users *plan* monetization and never reach it.

## 5. HITL demand mining (400 messages tagged, from a 2.76M-message / 248K-user population, May–Jun 2026)

Tag mix: clarification/approvals **37.5%** (the ask-human loop itself is a major cost+UX surface — one user: *"I thought I didn't have a choice… do I have to start all over?"*), new-feature 19.5%, bug-fix 18.3%, styling 12.8%, deployment-help 7.8%, integration-config 3.8%.

**Ranked integration asks:** ① LLM provider/keys & model choice (~18) ② payments — Stripe test→live trap, Paystack, IAP (~12) ③ transactional email (~9) ④ Google auth (~7) ⑤ WhatsApp (~5) ⑥ GitHub sync (~4) ⑦ Twilio/SMS (~3).
**Ranked hand-rolled features:** auth/roles (~12), admin panels (~8), mobile/app-store packaging (~7), billing/credits/paywall (~6), notifications (~6), exports (~6), multi-language (~4), chat/voice UI (~4), **white-labeling — "remove Emergent branding" (3 distinct users; monetizable upgrade)**.

Signature pain quotes: deployed app failing with `OPENAI_API_KEY` not configured; *"I don't have any API key"* (Hindi); *"whatever is free or cheapest, maybe give a provider picker in my app's dashboard"* (Indonesian); *"only one song in three renders… not going to make much money on this site"* — **generator reliability = the builder's revenue**.

## 6. Named-tools demand map (all 4.52M root jobs, 90d)

| Service | Mentions (all jobs) | AI share |
|---|---|---|
| email/SMTP generic | 281,900 | 37.9% |
| **WhatsApp** | 200,562 | 25.9% |
| Instagram | 138,012 | — |
| Firebase | 96,206 | — |
| OpenAI/GPT | 83,341 | ~100% |
| MongoDB | 70,035 | — |
| **Stripe** | 58,883 | 56.3% |
| Supabase | 56,520 | — |
| Google login/OAuth | 45,473 | 64.6% |
| Claude | 39,239 | ~100% |
| Razorpay | 27,837 | 48.6% |
| AI-media long tail (ElevenLabs, Whisper, DALL-E, Runway, Flux, Sora, Suno…) | ~40,242 combined | 60–99% |
| n8n+Zapier+Make | 6,854 | 78.5% |
| Vector DBs | 5,411 | 72.4% |

LLM providers combined = **154K mentions**. Highest-AI-share services (vector DBs, n8n/Zapier, Clerk, Twilio, Slack) mark pure AI-builder demand.

## 7. Success-case narratives (the 4 deployed seeds)

- **onebrain.team ($1,227, 1,101 steps, 48 HITLs, ~28h):** a developer driving the agent like a contracted team; built a full multi-tenant Claude-wrapper SaaS. **80% of cost = context-heavy edit loop on a growing monolith** (execute_bash $350, view_file $284…). Costliest phases were all commodity SaaS plumbing: token metering $100, image+vision $92, Stripe $70, memory $67, invitations $64 — **~$400+ was boilerplate a template would have included.** Stripe webhook-secret misconfig caused a paid-but-not-upgraded emergency.
- **ebook-ai-craft ($84, 9 HITLs):** sustained fight with **long-form generation reliability** — incoherence after ch.4 (context windowing), 3 failed runs, *"credits consumed but no ebook"* (trust-destroying), prod-only timeout failures. The user effectively invented the missing primitive themselves: **checkpointed, resumable, queued AI generation jobs**. 5 of 9 HITLs were this.
- **personal-growth-lab-2 ($35, 53 min, zero errors):** PRD-paste → deployed AI assessment generator in under an hour. **The success pattern to productize and market.** User manually invoked "Call Deployer Agent and Run Health Check" — should be a button.
- **weekly-music-app ($44):** actually a borderline non-AI paywall site; 3 of 6 HITLs were a non-technical user hunting for their zip/access codes — artifact retrieval UX, not code.

## 8. Emerging feature shortlist (input to Phase 8 scoring — evidence-tagged)

| # | Candidate | Track | Evidence |
|---|---|---|---|
| 1 | **AI-product templates**: Claude-wrapper SaaS (multi-tenant auth+billing+metering+chat UI), viral AI assessment/score, AI generator w/ credits+paywall | T1 | onebrain $400 boilerplate; LifeScore <1h success; generator stall stats (§4); OpenClaw wave distribution proof (§2) |
| 2 | **Checkpointed AI-generation job primitive** (queue, resume, per-chapter context, prod-parity timeouts) | T3 | ebook-ai-craft; "1 song per 3 renders"; generator-SaaS = 23.5% of segment |
| 3 | **LLM key & model-picker block** (universal-key default, provider picker for the *end-user app*, runtime key health check) | T2/T3 | #1 HITL integration ask; `OPENAI_API_KEY` prod failures; 154K provider mentions; universal-key 2.9× AI-enrichment (Phase 1) |
| 4 | **Auth + billing + credits preset** (Google OAuth, Stripe live-mode guided setup w/ webhook verification, credits wallet) | T3 | every confirmed-AI whale; Stripe test→live trap; 45K OAuth + 59K Stripe mentions |
| 5 | **Channel connector pack: WhatsApp/Telegram/IG-DM (+Twilio)** | T2 | 200K WhatsApp mentions; 4 whale projects; chatbot categories A/C need channels |
| 6 | **Outbound-agent block** (email autopilot w/ dedupe, caps, logs; scheduled ingestion w/ persistence) | T1/T3 | ChamsPilot/1buy.ai/NdorFlow whales; data-persistence HITL pain |
| 7 | **Real-time voice pipeline block** (streaming STT/TTS) | T3 | 2 voice whales = $110K hand-rolled; fragmented voice mentions in random sample |
| 8 | **Transactional email block** (Resend/SendGrid preset) | T2 | 282K mentions; "no one got emails?" |
| 9 | **White-label / remove-branding upgrade** | T4 | 3 organic HITL requests; monetizable |
| 10 | **AI-media bundle** (image+TTS+STT+video behind universal key) | T2 | 40K long-tail mentions, 60–99% AI share |
| 11 | **RAG/KB block** (vector DB + doc Q&A) | T3 | 5.4K vector mentions @72% AI share; whale Qdrant; RAG=6% of segment but high engagement |
| 12 | Ask-human UX overhaul (batch approvals, "don't ask again") | UX | 37.5% of HITL volume is approvals; RealTalk $85K burn |
| 13 | Pre-deploy health-check button | UX | LifeScore user invoked it by name |
| 14 | Export/operate-on-own-infra story | T4 | 2 whale agent businesses self-host but keep paying for the agent |

## 9. Hypothesis scoreboard update

| Hypothesis | Status |
|---|---|
| H1 (big share, growing) | Big in spend ✅, share flat ❌; calibrated ~12% of projects |
| H2 (AI fails to deploy more) | ❌ refuted (1.7× higher deploy rate) |
| H3 (higher willingness-to-pay) | ✅ (1.66× conversion) |
| H4 (same blocks re-implemented) | ✅✅ strongly confirmed — §5/§7 name the exact blocks |
| H6 (universal key = activation lever) | ✅ correlation + #1 HITL ask |
| H7 (HITL = ranked backlog) | ✅ confirmed — §5 is that backlog |
| H8 (agent demand rising) | ❌ organic; ✅ template-mediated (OpenClaw wave) |
| H5, H9, H10 | open → Phases 3, 5, 7 |
