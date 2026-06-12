# Phase 6 — Voice of Customer (consolidated)

**Date:** 2026-06-12 · Consolidates HITL mining (Phase 2 sweep), support tickets + churn reasons (Phase 3–7 sweep). Raw: [raw-phase02-sweep.md](raw-phase02-sweep.md), [raw-phase37-sweep.md](raw-phase37-sweep.md)

## 1. The demand-ranked backlog (frequency × source)

| Rank | Ask | Evidence (HITL n=400 · tickets n=40 · 4.5M task scan · churn) |
|---|---|---|
| 1 | **LLM provider/keys & model choice** (universal key default, model picker *inside the built app*, runtime key health) | #1 HITL integration topic (~18/400); `OPENAI_API_KEY` prod failures; 154K task mentions of providers; 5% of tickets |
| 2 | **Payments done right** (Stripe test→live trap, Paystack, IAP, Razorpay for India) | ~12/400 HITL; 59K Stripe + 28K Razorpay mentions; whale HITLs (webhook secrets) |
| 3 | **Deployment that doesn't fail or charge on failure** | 33% of tagged AI tickets; "Charged 50 Credits But Deployment Failed"; churn quotes |
| 4 | **Transactional email** ("no one got emails?") | ~9/400; 282K task mentions |
| 5 | **Auth/roles/Google login** | ~12/400 hand-rolled + ~7 integration asks; 45K mentions @64.6% AI share |
| 6 | **WhatsApp/Telegram channels** | ~5/400; 200K WhatsApp mentions; 4 whale projects; OpenClaw virality driver |
| 7 | **Credits/billing systems for the builder's own end-users** | ~6/400 hand-rolled; whale recurrence (learnskill credits, GymFix subs) |
| 8 | **Admin panels / dashboards** | ~8/400 |
| 9 | **Mobile/app-store packaging** (APK, EAS, TestFlight, IAP) | ~7/400 |
| 10 | **Generation reliability for long outputs** ("credits consumed, no ebook"; "1 song per 3 renders — not going to make money") | seed narrative (5/9 HITLs); random-sample stalls |
| 11 | **White-label / remove Emergent branding** | 3 unprompted requests in 400 — monetizable tier feature |
| 12 | Exports (PDF/MP4/code download), multi-language, notifications | ~6/~4/~6 in 400; "how do I download the code?" was a death-valley last message |

## 2. Churn voice (classified window Dec 2025–Feb 2026; pipeline stale after Feb 25 — fix flagged)

- AI-builder bad churn 54.9% (vs 50.8% non-AI). **58.4% of it is cost/value** (pricing perception, token wastage, budget), 19% product quality, 8% onboarding confusion.
- 33% of churning AI builders cancel within 0–1 day of their first AI job; 49% within 7 days.
- Representative quotes: *"50 credits? you gotta be kidding me"* (deploy fee on failure); token-wastage complaints about repeated agent retries.

## 3. The ask-human problem (UX, not feature)

37.5% of HITL volume is approvals/clarifications, and 63% of engaged-project deaths happen **at the scoping answer** — the kickoff questionnaire is where projects go to die. One user verbatim: *"I thought I didn't have a choice… do I have to start all over?"*. Whale case: RealTalk burned $85K across 5,280 HITL approval round-trips and never deployed.

## 4. What this means

The voice data converges with the funnel data on one sentence: **users don't need more building capability — they need the path from "it built" to "it's live, wired to keys/payments/email, and in front of real users" to be premade.** Every top-10 ask is a premade block, integration, or deploy-completion feature; none is "smarter code generation."
