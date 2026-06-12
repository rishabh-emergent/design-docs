# GTM Plan — "Launch and run your AI product on Emergent"

**Owner:** Rishabh · **Status:** Draft v1 (2026-06-12) · pairs with [09-flagship-prd.md](09-flagship-prd.md)

## 1. Positioning

**Category claim:** *Emergent is where you launch — and run — your AI product.* One prompt → working app + agent + hosting + LLM key + payments. No competitor owns the post-deploy "operate" layer (07 §1); 5/6 have managed keys (parity via FF2), 0/6 have WhatsApp channels, end-user billing rails, or checkpointed generation.

**Narrative beats (all evidence-backed):**
1. "From idea to live AI product in under an hour" — LifeScore: PRD-paste → deployed in 53 min, $35.
2. "One bill, no API keys" — universal key vs the two-bill anxiety every agent platform creates.
3. "OpenClaw, but hosted and safe" — capture the 247K-star wave; we already rank for "what is OpenClaw" → add *Deploy your own, no setup, no leaked keys* CTA.
4. "Your AI app's first 10 real users" — S4 honesty: deploy is the start; analytics + share moments get you adopted.

## 2. Audiences & channels

| Audience | Size | Channel | Play |
|---|---|---|---|
| Engaged-not-deployed AI builders (in-product) | 57K/mo | Ship Loop surfaces (F1/F2/F4) | the flagship itself is the campaign |
| Stuck high-spend builders | ~top-200 list queryable | lifecycle email + design-partner invites | "we built the thing you were missing" — 20-partner beta |
| AI-intent signups (acquisition) | 390K/qtr first-prompt-AI; converts 1.66× | SEO template pages ("Build an AI ebook generator / WhatsApp AI agent / Claude-wrapper SaaS"), template gallery, launch video | Starter Kits = landing pages; AI-intent is the premium segment to bid for |
| Production-app operators | 412 apps ≥50 calls/day (62% custom domains) | direct outreach (beta list from proxy×deployer join) | FF2 beta + case studies (smart-photo-tools, agri-fintech) |
| Geo/device focus | Desktop-first; IN+US/CA/AU/UK/PK/UAE over-index; mobile AI-intent converts 1.9× ratio-wise | paid + content localization later (FR/PT lead non-EN at ~15%) | EN-first launch; pt-BR/id localization experiment Q4 |

## 3. Launch sequencing

- **Wk 0–2 (pre):** design-partner beta (20 stuck builders + 4 seed users); proxy-ETL live; baseline dashboard snapshot.
- **Wk 3 (Ship Loop GA):** in-product only — no external noise for a funnel feature; weekly experiment readouts.
- **Wk 6–8 (Starter Kits launch = the public moment):** template gallery + 3 SEO pages + launch video ("idea → live AI SaaS in 1 hour", reuse LifeScore pattern) + X thread + OpenClaw capture page CTA + Product Hunt-style placement. Creator/affiliate angle: boilerplate market charges $199–$999 for what kits include free — that's the hook.
- **Wk 10+ (Operate beta):** FF2 to the 412-app list; publish 2 case studies; "one bill, no API keys" pricing page update; AI Builder plan experiment starts.

## 4. Pricing & packaging moves

1. **Ship-it pack** (in Ship Loop) — one-time, project-scoped; price ≈ 150–200 ECU tier.
2. **AI Builder plan** ~250–300 ECU + runtime allowance ("ship one AI app/month") — fills the measured 100-vs-199 ECU gap; experiment-gated, offered at first-topup and post-first-conversion (20.5% of AI-first converters top up within 30d — the window opens immediately).
3. **Auto-topup** opt-in at first topup (78.6% of AI revenue is repeated $20 topups — convert friction to commitment).
4. **Runtime inference**: pass-through pricing (parity), monetize via plan allowance + wallet share.
5. **White-label** on Pro+ (policy decision: honor-system now, enforced later).

## 5. Success metrics & cadence

North star **Weekly Shipped AI Apps**; supporting: engaged→deployed %, pack attach, template-start share, runtime-key enablement, S4 organic rate (quarterly Mongo probe), AI-builder bad-churn %. Weekly readout vs kill criteria (ADR 0001); monthly VoC refresh; quarterly segment re-sizing (filter v2 with OpenClaw exclusion).

## 6. Dependencies & risks

- Finance: whale-margin review before any consumption-stimulating expansion; refund-policy sign-off.
- Data: churn-classification pipeline is stale (no data past 2026-02-25) — fix before churn guardrails go live.
- Brand risk on "OpenClaw" association — position as *hosted alternative*, never imply affiliation.
- Support readiness: Starter Kits launch will shift ticket mix toward Stripe/WhatsApp setup — prep macros + playbook links.
