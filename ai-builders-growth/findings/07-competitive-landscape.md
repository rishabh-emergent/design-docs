# Phase 7 — Competitive & Market Intelligence (mid-2026)

**Date:** 2026-06-12 · **Source:** workflow `wf_aaf70c79-b23` web research (sources cited in raw doc). Raw: [raw-phase37-sweep.md](raw-phase37-sweep.md). Includes codebase feasibility notes (§4).

## 1. App-builder competitors: AI-product affordances

| Capability | Lovable | Bolt.new | Replit | v0/Vercel | Base44 | Firebase Studio |
|---|---|---|---|---|---|---|
| Managed LLM key for built app's runtime | ✅ auto `LOVABLE_API_KEY`, provider cost | ❌ BYOK | ✅ 300+ models, public API price | ✅ AI Gateway, no markup, $5/mo free | ✅ InvokeLLM, credit-metered | ✅ AI Logic, billed to user's GCP |
| Integration marketplace | Stripe/Connect, Clerk, ElevenLabs, Twilio (most polished) | DIY via Supabase | Stripe auto-wired at publish, RevenueCat | Marketplace integrations | basics | Google ecosystem |
| Agent templates | nascent | ❌ | ✅ Agent 3: Slack/Telegram/scheduled | "coming 2026" | ❌ | 60+ generic templates |
| WhatsApp channel | ❌ (Twilio DIY) | ❌ | ❌ (Slack/Telegram only) | ❌ | ❌ | ❌ |
| End-user billing rails for builder's customers | ❌ (stops at Stripe wiring) | ❌ | ❌ | ❌ | closest (credits not resellable) | ❌ |
| Checkpointed long-generation | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Verdicts:** (a) **Managed runtime LLM keys are now table stakes** — 5 of 6 ship it; Emergent's universal key needs urgent *productization parity* (we have the rails — §4). (b) **The "operate your AI product" layer is unclaimed by everyone**: nobody offers end-user metering + resellable credits + billing for the builder's own customers. (c) **WhatsApp-as-deploy-target is an open lane** (0 of 6). (d) Checkpointed generation is unclaimed messaging space.

## 2. Agent platforms & the OpenClaw lesson

Market layers: workflow incumbents (n8n €24–800/mo, 10K+ templates, >75% now LLM-using; Zapier; Make) · agent-employee platforms (Lindy $19–200/mo, 1,000+ templates; Relevance 400+ templates) · dev infra (LangGraph, CrewAI to $60K+/yr) · voice vertical (Vapi/Retell, $0.13–0.31/min all-in).

**OpenClaw** (the thing our users mass-installed, ~100K jobs in March): fastest-growing OSS repo ever (247K stars by Mar 2026) — a self-hosted personal agent driven through **WhatsApp/Telegram/Slack/iMessage**, with a skills marketplace, cron + proactive "heartbeat" loops. It proved: **chat-app-as-UI is the killer agent distribution surface, and proactive triggers make agents feel alive.** It also became 2026's first agent security crisis (≈12% of marketplace skills malicious, 7.1% leak credentials) with self-managed LLM bills of $5–$3,600/mo. → **"OpenClaw, but hosted and safe"** is a ready-made positioning; Emergent already ranks for "what is OpenClaw" (emergent.sh/learn/what-is-openclaw).

**Boilerplate market** proves one-time WTP of **$199–$999** for exactly the blocks our users hand-roll (auth, Stripe, credits, chat UI, RAG) — ShipFast, SaaS Pegasus, supastarter, Makerkit.

**Proven agent-template archetypes** (paid demand on ≥1 platform): email triage · doc-QA/RAG support bot · WhatsApp/Telegram support agent · outreach autopilot · voice receptionist · social/content repurposer · meeting scheduler-recap · lead-research agent · personal heartbeat assistant · data-analyst chat.

## 3. Strategic gaps where Emergent can be first/best (H10 ✅)

1. **One prompt → operated AI product**: app + agent + hosting + universal LLM key + billing in one place (today this takes an n8n sub + a $300 boilerplate + Vercel + per-provider keys).
2. **The operate layer**: end-user metering, resellable credit packs, per-app usage dashboards — no competitor does it; our integration-proxy already has 7 billing tables live (§4).
3. **Channel-native agents**: managed WhatsApp numbers + templates + webhooks; "one bill, no API keys" pricing wedge vs everyone's two-bill anxiety.

## 4. Feasibility notes against the monorepo (input to Phase 8 sizing)

| Candidate | Effort | Existing leverage found |
|---|---|---|
| AI-SaaS templates (Claude-wrapper, generator+credits) | **S** (content-shaped) | Template registry + snapshots exist; `env_resolver_config` already auto-provisions per-user `EMERGENT_LLM_KEY` — the hard part on any other platform |
| Premade integrations surfacing | **S** | **91 playbooks already shipped** (incl. BAILEYS_WHATSAPP, TWILIO_SMS, RESEND_EMAIL, 20+ LLM/media variants) with per-use pricing (~$1.50) — largely a *discovery/packaging* problem, an under-marketed moat |
| Universal-key runtime for deployed apps (model picker, key health, usage UI) | **M** (highest-leverage) | integration-proxy has litellm key issuance, llmrouter proxy, auto-topup wallets, budget endpoints, 7 billing tables — needs public app-facing API + drop-in UI block |
| Checkpointed long-generation primitive | **L** (only true Large) | Nothing exists for user apps; scope down to a playbook pattern (checkpoint rows + resume endpoint) first |
| White-label | **S** (policy decision) | Badge is client-side HTML (already removable); *enforced* white-label needs server-side injection — decide honor-system vs enforced |
| Ask-human/approval for end-user apps | S (playbook) / M (hosted API) | Full platform-side HITL stack exists; zero end-app primitive |

Correction from code: suprsend isn't in the codebase (comms = RudderStack→MoEngage); integration-proxy providers confirmed: litellm, stripe, tigris, ecubilling.
