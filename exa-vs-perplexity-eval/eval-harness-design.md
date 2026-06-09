# Exa vs Perplexity Integration Playbook Eval — Design

## TL;DR

We run a two-stage eval (LLM-judge on 28 paired playbooks + end-to-end smoke-test on 7 randomized Stage-2 cases + 5 no-playbook baselines + 3 idempotence repeats) to decide whether to switch the `integration_playbook_expert_v2` tool from Perplexity sonar-deep-research to Exa Research Pro. The verdict is a single pre-registered formula `verdict_score = 0.7 * stage2_success_rate + 0.3 * judge_pairwise_winrate` with four possible outcomes (Ship Exa / Stay Perplexity / Inconclusive / Experimental Split) — no post-hoc category carve-outs allowed. Realistic single-run cost is ~$145–205 with a hard global abort at $200, no headroom for re-runs without fresh budget approval.

---

## 1. What We're Measuring (and Not)

**The decision is "works", not "reads well."** A playbook with hallucinated SDK methods can read fluently and score high on every readability axis while burning 3–10 agent iterations in prod before it converges (or fails). The three concrete divergences we've observed between "reads well" and "works":

1. **Hallucinated SDK methods** — `stripe.checkout.create_session()` looks right; the real method is `stripe.checkout.Session.create()`.
2. **Stale package versions** — playbook says `pip install supabase==1.x` with v1 syntax but pypi only has v2.
3. **Missing env-var glue** — playbook documents 5 API keys but the agent's `.env` template only gets 3 because two were buried in prose.

**Consequences for the design:**
- Stage 2 (real sandbox + real third-party API round-trip) is weighted **70%** of the verdict. Judge is **30%** and is reporting-only on dimension scores.
- Judge dimension scores never enter the verdict math — only `judge_pairwise_winrate` does.
- The judge sees a normalized, blinded playbook with a deterministically pre-fetched official-docs URL in context, so its freshness scoring isn't gated by Claude's training cutoff (same blindspot as the consumer agent).
- The cache layer **must miss** on every eval integration. ~45% of fallback calls in prod are actually mis-classified cached entries; if we picked any of those, both backends would return identical cached content and the eval would say nothing.

**Out of scope:**
- expo and nextjs stacks beyond a 3-pair cross-stack smell-test (Supabase, Stripe, OpenAI). Verdict is FastAPI+React-primary; nextjs/expo behavior gets a separate eval if the FastAPI+React verdict is unclear.
- Pricing/latency wars (reported separately, never combined with quality).
- Fixing the classifier-OTHER mislabeling bug (~45% of fallback calls). The eval is gated against this issue via cache-miss verification, but doesn't fix it. Mentioned in the writeup as a "bigger lever" follow-up.

---

## 2. Stage 1 — LLM-as-Judge Pairwise + Absolute

### 2.1 Integration Set

**28 primary integrations + 3 cross-stack nextjs pairs + 5 no-playbook baselines + 3 idempotence repeats + 5 dual-judge collusion checks + 5-prompt ambiguous-prompt mini-study.** Stratification matches 7-day prod fallback volume with deliberate over-weighting of regional/long-tail (anti-Western-bias).

#### Stratum counts
| Stratum | Count | Why |
|---|---|---|
| payments-global | 3 | Stripe well-cached; tests edges (Lemon Squeezy, Connect Express) |
| payments-regional | 5 | PhonePe, Paytm, Xendit, Flutterwave, MercadoPago — long-tail freshness |
| auth | 4 | Clerk freshness, Supabase auth, Auth0, Better-Auth |
| social/messaging | 4 | Instagram (highest prior-prod volume), WhatsApp, Discord, Telegram |
| AI/ML providers | 3 | OpenAI Responses, Anthropic, ElevenLabs |
| web3 | 3 | Solana web3.js v2, wagmi v2, Alchemy NFT v3 |
| geo/maps | 2 | Places (New), Mapbox v3 |
| storage | 2 | R2, UploadThing v6 |
| analytics | 2 | PostHog, Mixpanel |
| weather/data | 1 | Open-Meteo |
| **Total** | **28** | |

#### Full primary 28 table

| # | Stratum | Name | Stage-2 eligible? | Freshness | Constraint snippet |
|---|---|---|---|---|---|
| 1 | payments-global | Stripe Payment Element + one-time + subscription | YES | HIGH | "Template stack: FastAPI+React. Use case: SaaS app with BOTH one-time digital product purchase AND monthly subscription billing, both via Stripe Payment Element (NOT legacy Card Element). Requirements: (a)(b)(c). Use stripe-python>=8.0 and @stripe/stripe-js latest. Webhook handler for invoice.paid AND payment_intent.succeeded." |
| 2 | payments-global | Lemon Squeezy hosted checkout + signed webhook | candidate | MED | "Template stack: FastAPI+React. Use case: One-time digital product purchase via Lemon Squeezy hosted checkout with signed webhook verification on order_created. Requirements: (a)(b)(c). lemonsqueezy.py current." |
| 3 | payments-global | Stripe Connect Express | candidate | MED | "Template stack: FastAPI+React. Use case: Marketplace where sellers onboard via Stripe Connect Express, and the platform takes 10% application_fee on each PaymentIntent. Requirements: (a)(b)(c). stripe-python>=8.0." |
| 4 | payments-regional | PhonePe PG v2 UPI (India) | candidate | HIGH | "Template stack: FastAPI+React. Use case: Indian B2C UPI payment via PhonePe Payment Gateway v2 (the post-2024 API, NOT deprecated v1). Requirements: (a)(b)(c). Include X-VERIFY checksum header generation." |
| 5 | payments-regional | Paytm All-in-One Web SDK | candidate | MED | "Template stack: FastAPI+React. Use case: Paytm Payment Gateway All-in-One Web checkout for INR e-commerce cart. Requirements: (a)(b)(c). Server-side initiate-transaction; JS bridge on frontend." |
| 6 | payments-regional | Xendit virtual account (Indonesia) | candidate | MED | "Template stack: FastAPI+React. Use case: Indonesian virtual-account creation via Xendit with callback handler for payment confirmation. Requirements: (a)(b)(c). xendit-python current." |
| 7 | payments-regional | Flutterwave Standard (Nigeria) | candidate | MED | "Template stack: FastAPI+React. Use case: Flutterwave Standard checkout for Nigerian NGN cards + mobile money with transaction verification on redirect. Requirements: (a)(b)(c). rave-python current." |
| 8 | payments-regional | MercadoPago Checkout Pro (LatAm) | candidate | MED | "Template stack: FastAPI+React. Use case: Argentinian ARS payment via MercadoPago Checkout Pro with webhook for payment.updated. Requirements: (a)(b)(c). mercadopago-python current." |
| 9 | auth | Clerk clerkMiddleware + useUser | candidate | HIGH | "Template stack: nextjs (App Router). Use case: Clerk-based email + Google OAuth sign-in using clerkMiddleware from @clerk/nextjs current (NOT the deprecated authMiddleware). Requirements: (a)(b)(c). Protect /dashboard route." |
| 10 | auth | Supabase auth v2 — FastAPI+React | candidate, **STAGE-2** | HIGH | "Template stack: FastAPI+React. Use case: Supabase email/password auth using @supabase/supabase-js v2.x (NOT v1's signIn). Requirements: (a)(b)(c). FastAPI verifies JWT with project JWT secret." |
| 11 | auth | Auth0 New Universal Login + RBAC | candidate | LOW | "Template stack: FastAPI+React. Use case: Auth0 New Universal Login with Google + email-password, plus RBAC via Auth0 permissions claim in the access token. Requirements: (a)(b)(c)." |
| 12 | auth | Better-Auth social + magic link | candidate | HIGH | "Template stack: nextjs (App Router). Use case: better-auth social (Google) + magic-link email auth using the better-auth current release (not next-auth, not Auth.js). Requirements: (a)(b)(c)." |
| 13 | social/msg | Instagram Login Business (Graph) | candidate | HIGH | "Template stack: FastAPI+React. Use case: Login with Instagram for a Business/Creator account via Instagram Login (Instagram Graph API), scopes `instagram_business_basic` and `instagram_business_content_publish`. NOT the deprecated Instagram Basic Display API. Requirements: (a)(b)(c)." |
| 14 | social/msg | WhatsApp Cloud API send + webhook | candidate | MED | "Template stack: FastAPI+React. Use case: Send WhatsApp template message via WhatsApp Cloud API (NOT On-Premises API), receive delivery webhook with verified X-Hub-Signature-256. Requirements: (a)(b)(c)." |
| 15 | social/msg | Discord OAuth2 + bot slash command | candidate | LOW | "Template stack: FastAPI+React. Use case: Discord OAuth2 login (scopes 'identify guilds'), AND a bot that registers a guild-scoped slash command via the application commands REST endpoint. Requirements: (a)(b)(c)." |
| 16 | social/msg | Telegram Bot inline keyboard + webhook | candidate | LOW | "Template stack: FastAPI backend. Use case: Telegram bot with inline keyboard buttons, served via webhook (NOT long-polling). Verify update via secret token header. Requirements: (a)(b)(c)." |
| 17 | AI/ML | OpenAI Responses API + SSE | candidate, **STAGE-2** | HIGH | "Template stack: FastAPI+React. Use case: OpenAI Responses API (the newer endpoint, NOT Chat Completions) with server-sent-events streaming to the React client, displaying token-by-token output AND final usage block (input/output/cache tokens). Requirements: (a)(b)(c)." |
| 18 | AI/ML | Anthropic Messages + tool_use + cache_control | candidate | MED | "Template stack: FastAPI backend. Use case: Anthropic Messages API with tool_use, prompt-caching via cache_control on system + tools, and streaming. Requirements: (a)(b)(c). anthropic-python current." |
| 19 | AI/ML | ElevenLabs websocket streaming TTS | candidate | MED | "Template stack: FastAPI+React. Use case: ElevenLabs realtime websocket TTS streaming PCM to a browser AudioContext (NOT the simple HTTP endpoint). Requirements: (a)(b)(c)." |
| 20 | web3 | Solana @solana/web3.js v2 transfer | candidate | HIGH | "Template stack: FastAPI backend (server-signed) + React. Use case: Send a SOL transfer transaction using @solana/web3.js >=2.0 (functional/tree-shakable API with createSolanaRpc, NOT v1's new Connection). Requirements: (a)(b)(c)." |
| 21 | web3 | wagmi v2 + viem connect + sign | candidate | HIGH | "Template stack: nextjs (App Router) + wagmi v2 + viem. Use case: Connect MetaMask, read user's USDC balance on Base, sign an arbitrary message. NOT wagmi v1. Requirements: (a)(b)(c)." |
| 22 | web3 | Alchemy NFT API v3 owned NFTs | candidate | MED | "Template stack: FastAPI backend. Use case: Use Alchemy NFT API v3 (NOT v2) to list NFTs owned by an Ethereum address, including media URLs and floor price. Requirements: (a)(b)(c)." |
| 23 | geo/maps | Mapbox GL JS v3 + Directions API | candidate | MED | "Template stack: FastAPI+React. Use case: Mapbox GL JS v3 map with a route drawn via the Mapbox Directions API between two clicked points. Use the new session-token billing approach. Requirements: (a)(b)(c)." |
| 24 | geo/maps | Google Maps Places API (New) | candidate | HIGH | "Template stack: FastAPI+React. Use case: Address autocomplete using Google Maps Places API (New) — v1 endpoint at places.googleapis.com/v1/places:autocomplete, NOT the legacy Places API. Requirements: (a)(b)(c)." |
| 25 | storage | Cloudflare R2 presigned PUT | non-Stage-2 | LOW | "Template stack: FastAPI+React. Use case: Direct-from-browser upload to Cloudflare R2 via presigned PUT URL minted by FastAPI using boto3 with R2 endpoint. NOT S3. Requirements: (a)(b)(c)." |
| 26 | storage | UploadThing v6 file upload | non-Stage-2 | MED | "Template stack: nextjs (App Router). Use case: UploadThing v6 for image uploads with size + mime validation server-side. NOT v5. Requirements: (a)(b)(c)." |
| 27 | analytics | PostHog flags + capture | non-Stage-2 | LOW | "Template stack: FastAPI+React. Use case: PostHog JS in React (event capture + feature flag check) AND posthog-python in FastAPI for server-side identify on /signup. Requirements: (a)(b)(c)." |
| 28 | analytics | Mixpanel /import + Query API | non-Stage-2 | LOW | "Template stack: FastAPI backend. Use case: Server-side event ingestion to Mixpanel /import (NOT /track), plus daily cohort export via Mixpanel Query API. Requirements: (a)(b)(c)." |
| 29 | weather | Open-Meteo forecast + historical | non-Stage-2 | LOW | "Template stack: FastAPI+React. Use case: Hourly forecast + last-7-days historical temperature for a user-entered city via Open-Meteo (free, no key). NOT OpenWeather. Requirements: (a)(b)(c)." |

#### Constraint snippet schema (verbatim, all 28)

```
Template stack: {stack}.
Use case: {persona_use_case}.
Requirements:
  (a) Include all required env vars in a .env.example block.
  (b) Use exact pip/npm package names with specific versions (>= or pinned).
  (c) Include a single working end-to-end example with no placeholder TODOs or "..." comments.
{freshness_anchor_clause_or_blank}
{security_clause_if_applicable}
```

NO inline `(eval-run-...)` suffix in the prompt. Cache-bust is via the `X-Eval-Run-ID` HTTP header on the MCP call (Phase A verification confirms cache key includes header before run; Phase B inline-suffix validation only if header is dropped from cache key).

#### Cross-stack pairs (3 additional nextjs runs)

| Pair | Topic | FastAPI version | nextjs constraint snippet |
|---|---|---|---|
| CS-A | Supabase auth | #10 | "Template stack: nextjs (App Router, SSR). Use case: Supabase email/password auth with @supabase/ssr (the new package, NOT auth-helpers-nextjs which is deprecated). Cookie-based session. Requirements: (a)(b)(c)." |
| CS-B | Stripe Payment Element | #1 | "Template stack: nextjs (App Router). Use case: SaaS app with one-time AND subscription billing via Stripe Payment Element using @stripe/stripe-js latest and stripe Node SDK current, Route Handlers for server actions. Requirements: (a)(b)(c)." |
| CS-C | OpenAI Responses + SSE | #17 | "Template stack: nextjs (App Router). Use case: OpenAI Responses API with SSE streaming to client component via Route Handler, displaying token-by-token output AND final usage block. Requirements: (a)(b)(c)." |

Pre-registered cross-stack rule: 3/3 pairs agree → directional signal; 2/3 or 1/3 → "cross-stack inconclusive, separate eval required."

#### Stage-2 selection (deterministic, seed `20260609`)

```python
import random
SEED = 20260609
STRATA_FOR_STAGE2 = {
  "payments-global":   [1, 2, 3],
  "payments-regional": [4, 5, 6, 7, 8],
  "auth":              [9, 10, 11, 12],
  "social/msg":        [13, 14, 15, 16],
  "AI/ML":             [17, 18, 19],
  "web3":              [20, 21, 22],
  "geo/maps":          [23, 24],
}
rng = random.Random(SEED)
stage2_picks = {k: rng.choice(v) for k, v in STRATA_FOR_STAGE2.items()}
# Pre-computed (frozen before any backend call):
# {'payments-global': 2, 'payments-regional': 7, 'auth': 10,
#  'social/msg': 13, 'AI/ML': 17, 'web3': 20, 'geo/maps': 24}
```

**Stage-2 picks: integrations #2, #7, #10, #13, #17, #20, #24** (7 cases). Storage/analytics/weather excluded (no clear single-call assertion within budget caps).

#### Backup pool (15)

| ID | Stratum | Name | Replaces |
|---|---|---|---|
| B1–B2 | payments-global | Square Web Payments / Adyen Drop-in | 1, 2, 3 |
| B3–B4 | payments-regional | Razorpay / dLocal | 4–8 |
| B5–B6 | auth | NextAuth v5 / WorkOS AuthKit | 9–12 |
| B7–B8 | social/msg | Twilio Verify / Slack Bolt | 13–16 |
| B9–B10 | AI/ML | Gemini streaming / Replicate polling | 17–19 |
| B11–B12 | web3 | thirdweb v5 / Helius RPC | 20–22 |
| B13 | storage | Supabase Storage v2 | 25, 26 |
| B14 | analytics | Plausible Events | 27, 28 |
| B15 | weather | NOAA NWS | 29 |

#### Cache-miss pre-flight (T-24h AND T-0, all 43 items)

```python
# preflight.py
import httpx, json, datetime
EA_CHECK = "https://api.emergentagent.com/api/v1/knowledge/check"
PRIMARY = json.load(open("integration_set.v2.primary.json"))  # 28
BACKUPS = json.load(open("integration_set.v2.backups.json"))  # 15

def cache_hit(name: str, template: str) -> bool:
    r = httpx.post(EA_CHECK, json={"integration": name, "template": template}, timeout=30)
    r.raise_for_status()
    return r.json().get("verified_playbook") is not None

def preflight_all(items, label):
    return {it["id"]: cache_hit(it["name"], it["stack"]) for it in items}

def resolve(primary, backups, hits_t24, hits_t0):
    final, used, drift = [], set(), []
    for item in primary:
        if hits_t24[item["id"]] != hits_t0[item["id"]]:
            drift.append((item["id"], hits_t24[item["id"]], hits_t0[item["id"]]))
        if hits_t0[item["id"]]:
            sub = next((b for b in backups
                        if b["category"] == item["category"]
                        and b["id"] not in used
                        and not hits_t24[b["id"]] and not hits_t0[b["id"]]), None)
            if sub is None:
                raise RuntimeError(f"No clean backup for stratum {item['category']}")
            used.add(sub["id"]); sub["replaces"] = item["id"]
            final.append(sub)
        else:
            final.append(item)
    return final, drift

if __name__ == "__main__":
    hits_t24 = preflight_all(PRIMARY + BACKUPS, "T-24h")
    hits_t0  = preflight_all(PRIMARY + BACKUPS, "T-0")
    final, drift = resolve(PRIMARY, BACKUPS, hits_t24, hits_t0)
    if len(drift) > 5:
        raise RuntimeError(f"Cache drift too high: {len(drift)} items flipped in 24h")
    out = f"integration_set.resolved.{datetime.date.today():%Y%m%d}.json"
    json.dump({"final": final, "drift_log": drift}, open(out, "w"), indent=2)
```

**Fallback if `/knowledge/check` is template-agnostic:** runtime latency-based detector — any tool response with latency <2s flagged as suspected cache hit and replaced from backup.

### 2.2 Judge Rubric & Prompt

**Two-judge ensemble: GPT-5 and Claude Opus 4.7 at 50/50 with disagreement-as-signal (no weighted averaging). Temperature 0. Per-dimension scores reported as `(claude_score, gpt_score)` tuples; never collapsed into a composite that enters the verdict math.**

#### Verbatim judge system prompt

```
You are an expert code-review judge for integration playbooks generated by AI research tools.

RUBRIC VERSION: 2.0.0 (locked 2026-06-04). Emit this version string in your output. If you are reading any other version in this prompt, STOP and refuse to score.

================================================================================
THE CONSUMER (read this carefully — it is NOT what you think)
================================================================================

These playbooks are NOT consumed by an LLM agent that can "figure things out". They are extracted by a DETERMINISTIC PATTERN-MATCHING SCRIPT into:
- A list of pip/npm install commands (from ```bash fenced blocks).
- A .env template (from KEY=VALUE lines in code blocks or explicit env-var lists).
- One or more code files (from ```python, ```typescript, ```javascript, ```tsx, ```jsx fenced blocks, written to disk verbatim).
- A test command (from a ```bash block following a "## Test" or similar header).

Then the extracted artifacts are EXECUTED UNCHANGED. There is no LLM in the loop between extraction and execution. There is no "the agent will figure that out". Ambiguity = failure. Every minute the downstream agent spends fixing a playbook bug costs the user real money (ECU) and burns iteration budget (5 iterations max before the agent gives up).

You are NOT scoring how well YOU could use this playbook. You are scoring how well a SED/AWK SCRIPT could extract correct, runnable code from this playbook.

================================================================================
WHAT YOU WILL RECEIVE
================================================================================

You will receive ONE of two prompt shapes:

SHAPE A — ABSOLUTE SCORING (one playbook only):
  - INTEGRATION, TEMPLATE STACK, CANONICAL CONSTRAINTS
  - OFFICIAL DOCS REFERENCE: <URL + first 8k tokens of fetched content>
  - PLAYBOOK: <text, stylistic fingerprints normalized>
  - Score this ONE playbook on four dimensions. No pairwise output.

SHAPE B — PAIRWISE WINNER (scores only, no playbook text):
  - PLAYBOOK A SCORES, PLAYBOOK B SCORES, DETERMINISTIC FLAGS for each.
  - You DO NOT see the playbook text. Compute pairwise winner FROM THE SCORES AND FLAGS ONLY.

================================================================================
ANTI-BIAS DISCIPLINE
================================================================================

1. LENGTH IS NOT QUALITY. Duplicated content = NEGATIVE on completeness.
2. CITATION COUNT IS NOT QUALITY. Score OFFICIAL-DOCS RATIO, not count.
3. POSITION BIAS. Each pair is re-sent with positions swapped.
4. SELF-RECOGNITION. Pattern-match against OFFICIAL DOCS REFERENCE, not against "this sounds well-written".
5. SIMULATION BIAS. Do NOT think "I could figure that out from context". The extractor cannot.
6. AUTHORITY-SOUNDING TONE. "According to the latest documentation..." with no link is filler.

================================================================================
SCORING — FOUR ORTHOGONAL DIMENSIONS, EACH 1–5
================================================================================

DIM 1: CORRECTNESS_AND_FRESHNESS  (merges API surface + freshness — they are not separable)
5 = Every SDK method, REST endpoint, scope, version matches OFFICIAL DOCS REFERENCE. Honest "as of YYYY-MM" within 18 months and consistent with docs scores 5.
4 = One minor inaccuracy (optional param renamed); core path correct.
3 = Happy path matches docs; one supporting call (webhook sig, refund) stale or absent from docs.
2 = Primary SDK method wrong (renamed, removed, hallucinated). Extractor writes it; runtime hits AttributeError or 404.
1 = Core integration FABRICATED. Endpoints don't exist in docs at all.

DETERMINISTIC AUGMENTATION (harness pre-grep, attached to your prompt):
  STRIPE_PYTHON: stripe.checkout.Session.create CURRENT, stripe.checkout.session.create (lowercase) DEPRECATED
  STRIPE_NODE:   stripe.checkout.sessions.create CURRENT, stripe.checkout.Sessions.create DEPRECATED
  SUPABASE_JS:   supabase.auth.signInWithPassword CURRENT, supabase.auth.signIn DEPRECATED
  SUPABASE_JS:   supabase.auth.signInWithOAuth CURRENT, supabase.auth.signIn({provider}) DEPRECATED
  CLERK_NEXTJS:  clerkMiddleware CURRENT, withClerkMiddleware DEPRECATED, authMiddleware DEPRECATED
  CLERK_REACT:   useUser().user.primaryEmailAddress.emailAddress CURRENT, useUser().user.email DEPRECATED
  INSTAGRAM:     scope instagram_business_basic CURRENT, user_profile/user_media (Basic Display) DEPRECATED (sunset 2024-12-04)
  INSTAGRAM:     graph.instagram.com/v21.0 CURRENT, graph.facebook.com/v12.0 DEPRECATED
  SOLANA_WEB3:   createSolanaRpc() CURRENT v2, new Connection() DEPRECATED (v1)
  HUBSPOT:       /crm/v3/objects/contacts CURRENT, /contacts/v1/contact DEPRECATED
  HUBSPOT:       hubspot.crm.contacts.basicApi.create CURRENT, hubspot.contacts.create DEPRECATED
  TWILIO_PYTHON: Client(account_sid, auth_token).messages.create CURRENT, TwilioRestClient DEPRECATED
  SPOTIFY:       PKCE flow CURRENT for SPAs, response_type=token (implicit) DEPRECATED

If a deprecated trap match is detected by the harness, score CORRECTNESS_AND_FRESHNESS no higher than 2. This overrides your own judgment.

LONG-TAIL HANDLING (if docs_unavailable=true):
Score based on internal consistency only — version claims, self-consistency of method names across the playbook. Inconsistent + no version = 1. Consistent + version claimed = 4.

DIM 2: EXECUTABILITY  (extractor-runs-it + sandbox-feasibility)
5 = All blocks syntactically valid; all symbols defined/imported; SANDBOX_FEASIBLE.
4 = One trivial fix (missing import).
3 = 1–2 non-obvious fixes.
2 = Multiple fixes OR sandbox-infeasible pattern (ngrok, brew install, /etc/hosts, sudo apt).
1 = Pseudo-code with placeholders; multiple sandbox blockers.

Harness greps for: ngrok|serveo|localtunnel|cloudflared tunnel|brew install|sudo apt|sudo yum|edit /etc/hosts|expose localhost publicly|register a domain|purchase an SSL cert. Match caps EXECUTABILITY at 2.

DIM 3: COMPLETENESS  (six pieces in extractable form)
(a) API keys with explicit acquisition (URL + menu); (b) install commands in ```bash; (c) env var template with EXACT names; (d) backend code in fenced blocks; (e) frontend code in fenced blocks; (f) runnable test command.
5 = All six present, extractable, no conflicting samples, no env-vars-in-prose. INFEASIBILITY ESCAPE VALVE: if integration is genuinely infeasible AND playbook says so structurally (reasoning + alternative + redirect), score 5.
4 = Five of six fully; one light.
3 = Four; one critical missing.
2 = Three; major gap.
1 = ≤2 pieces.

If env_vars_listed and env_vars_referenced disagree, cap COMPLETENESS at 3.

DIM 4: CITATION_ANCHORING
5 = Official docs URL (per canonical list) placed near relevant code; no fabricated URLs.
4 = Official + 1-2 third-party, all at end only.
3 = Mostly third-party + 1 official.
2 = Only third-party/blog.
1 = None or fabricated URLs.

Canonical official docs domains (from eval_official_docs.json):
- Stripe: docs.stripe.com
- Supabase: supabase.com/docs
- Instagram: developers.facebook.com/docs/instagram-platform
- Clerk: clerk.com/docs
- OpenAI: platform.openai.com/docs
- Anthropic: docs.anthropic.com
- HubSpot: developers.hubspot.com
- Solana web3: solana-labs.github.io/solana-web3.js or docs.solana.com
- Spotify: developer.spotify.com/documentation
- PhonePe: developer.phonepe.com
- Paytm: business.paytm.com/docs
- Xendit: developers.xendit.co
- Twilio: twilio.com/docs
- Auth0: auth0.com/docs
- AWS S3: docs.aws.amazon.com/s3
- Mapbox: docs.mapbox.com

================================================================================
PAIRWISE WINNER JUDGMENT (Shape B only)
================================================================================

Compute: winner ∈ {A, B, TIE}, winner_confidence ∈ {low, medium, high}, decisive_dimensions, both_broken, rationale.

TIE RULES (symmetric within-noise):
- TIE if sum of |dim_diff| across all four dims ≤ 2 AND no single dim differs by ≥ 2.
- If a single dim differs by ≥ 2, that dim alone decides.
- both_broken=true if EITHER playbook has correctness_and_freshness ≤ 2 (not requiring both — surfaces asymmetric-broken cases).

================================================================================
OUTPUT FORMAT
================================================================================

Emit ONE JSON object. rubric_version is mandatory. Field order is LOAD-BEARING: absolute scores BEFORE pairwise output. Score each playbook independently first; only after both score blocks are complete should you determine the pairwise winner from the scores.
```

#### Output schemas

**Shape A (absolute scoring, one playbook):**
```json
{
  "rubric_version": "2.0.0",
  "shape": "absolute",
  "integration": "<string>",
  "template_stack": "fastapi-react | expo | nextjs",
  "playbook_id": "<opaque>",
  "scores": {
    "correctness_and_freshness": <int 1-5>,
    "executability": <int 1-5>,
    "completeness": <int 1-5>,
    "citation_anchoring": <int 1-5>
  },
  "evidence": {
    "correctness_and_freshness": "<1-2 sentences citing exact method/endpoint vs OFFICIAL DOCS REFERENCE>",
    "executability": "<did fenced blocks parse? undefined symbols? sandbox-infeasible?>",
    "completeness": "<which of 6 pieces present/missing; env-var match; duplicate content noted>",
    "citation_anchoring": "<official docs URLs per canonical list; placement near code or only at end>"
  },
  "deterministic_flags_observed": {
    "freshness_traps_matched_deprecated": ["<pattern>"],
    "freshness_traps_matched_current": ["<pattern>"],
    "sandbox_infeasibility_patterns": ["<pattern>"],
    "env_var_listed_vs_referenced_mismatch": <bool>,
    "official_docs_url_cited": <bool>,
    "infeasibility_escape_valve_applied": <bool>
  },
  "length_tokens_estimate": <int>,
  "rubric_notes": "<edge-case notes>"
}
```

**Shape B (pairwise from scores only):**
```json
{
  "rubric_version": "2.0.0",
  "shape": "pairwise",
  "integration": "<string>",
  "position_variant": "AB | BA",
  "winner": "A | B | TIE",
  "winner_confidence": "low | medium | high",
  "decisive_dimensions": ["correctness_and_freshness", ...],
  "both_broken": <bool>,
  "within_noise_threshold_applied": <bool>,
  "rationale": "<1-3 sentences citing specific score diffs and deterministic flags>"
}
```

#### Anchor table (single source of truth)

| Dim | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|
| correctness_and_freshness | All methods/endpoints/scopes match docs; honest dated claim within 18mo, verified | One minor param rename | Happy path right, one supporting call stale | Primary SDK method wrong/hallucinated; or freshness trap hit | Core fabricated; package not on PyPI/npm |
| executability | All code parses; sandbox-feasible; all symbols defined or in listed packages | One trivial fix (missing import) | 1-2 non-obvious fixes | Multiple fixes; OR sandbox-infeasible pattern (ngrok etc.) | Pseudo-code/placeholder; multiple sandbox blockers |
| completeness | All 6 pieces extractable; env-var-listed = env-var-referenced; no duplicate restatement | 5 of 6; one light | 4 of 6; OR env-var mismatch | 3 of 6; major gap | ≤2 of 6 |
| citation_anchoring | Official docs URL per canonical list, placed near code; no broken URLs | Official + 1-2 third-party, at end only | Mostly third-party + 1 official | Only third-party | None or fabricated |

#### Anti-bias mechanics (caller-side)

1. **Normalization** (replaces token-stripping as blinding): collapse `[1][2][3]` to `[N]`; strip markdown `---`; normalize "Sources:"/"References:"/"Citations:" → "References:"; strip "According to recent sources..." / "To integrate X you'll need to..." openers; strip "Powered by Exa" / "via Perplexity" / model preambles via regex `(?i)(perplexity|sonar(-deep-research)?|exa(-research(-pro)?)?|powered by exa|via perplexity|generated at:.*|model:.*)`.
2. **Pre-fetch official docs** per integration; first 8k tokens of cleaned-HTML body, cached per run.
3. **Position swap** on every pairwise call (AB and BA per judge = 4 votes per pair).
4. **Self-consistency check**: 3 random pairs run twice per judge. If any |score_run1 - score_run2| > 1 on any dim → PAUSE eval, investigate noise floor.
5. **Stylistic-fingerprint calibration**: 2-3 calibration pairs with content reformatted into the other tool's style; the resulting `formatting_delta_per_dim` is the floor — headline differences must exceed it to be claimed as real signal.
6. **Log everything** to `eval_runs/{run_id}/judge_calls.jsonl`: model name+version, temperature, rubric_version, system prompt hash, user prompt, raw JSON, latency, tokens, cache status.

#### Human spot-check triggers (any one fires)

(a) <3 of 4 pairwise votes agree.
(b) Cross-model split: both Claude votes disagree with both GPT votes.
(c) Within-judge position-swap instability.
(d) Judge correctness_and_freshness disagrees with deterministic freshness_traps grep.
(e) Judge citation_anchoring ≥ 4 but `official_docs_url_in_playbook=false`.

Estimated spot-check load at n=28: ~30–40% of pairs = 8–12 items, one afternoon for rishabh.

#### Human ground-truth anchor protocol

Before LLM judge runs on full n=28, rishabh hand-grades FIRST 5 integrations (one per category + one wildcard) against the rubric. Then LLM judges run on the same 5. Compare:
- Per-dim: |human - judge|. If MAD > 0.8 on any dim → re-anchor the rubric wording before proceeding.
- Pairwise: if <4 of 5 winners agree → eval is too noisy. Stop and debug.

### 2.3 Harness Plumbing

```
mono/tools/eval/exa-perplexity/
├── README.md                       # VPN, PROXY_API_KEY, slack-checkin, k8s job alt
├── pyproject.toml                  # httpx, pyyaml, tenacity, python-dotenv, pydantic, asyncpg
├── .env.example                    # SERVER_TOOLS_URL, PROXY_API_KEY, EA_BASE_URL, LLM_PROXY_DB_*
├── integrations.yaml               # 28 + 3 nextjs + reserve
├── harness.py                      # CLI: full / --dry-run / --smoke-subset / --resume
├── mcp_client.py                   # MCP HTTP JSON-RPC; sends ONLY {"query": ...}
├── mcp_probe.py                    # /healthz + tools/list pre-run validation
├── cache_preflight.py              # EA /api/v1/knowledge/check, same X-Emergent-Base-URL as tool
├── parse_envelope.py               # json.loads(content[0].text) + split "---\nSources:\n"
├── quality_check.py                # thin/refused/non-english filters
├── render.py                       # render_query(integration) -> {"query": <pinned string>}
├── persistence.py                  # atomic write; resume via file-existence (NO manifest)
├── cost.py                         # projection + running-total watchdog + envelope cost
├── backfill_cost.py                # post-run SQL on llm_proxy_db.llm_logs_partitioned by X-Run-ID
├── judge_order.py                  # seeded RNG -> judge_order.json
├── schema.py                       # pydantic CallResult, RunMeta, QuarantineRow
├── scripts/survival_probe.sh       # bulk preflight read-only probe of all slugs
├── k8s/eval-harness-job.yaml       # in-cluster Job for clean PROXY_API_KEY access
├── tests/
│   ├── test_parse_mcp_payload.py   # fixtures {content, cost} envelope shape
│   ├── test_render_query.py        # asserts ONLY 'query' key emitted
│   └── test_resume.py
└── results/<run_id>/
    ├── run_meta.json
    ├── judge_order.json
    ├── <slug>__exa.json
    ├── <slug>__perplexity.json
    ├── quarantine/<slug>__cache_hit.json | __thin_content.json
    └── bonus/classifier_mislabels.jsonl   # only if --collect-mislabels
```

#### Key code: `render.py`

```python
import hashlib, json

def render_query(integration: dict) -> dict:
    """SINGLE source of truth. Returns the EXACT params dict sent to BOTH tools.

    pkg/tools/{exa,perplexity}/tool.go MCPTool() accepts ONLY 'query'.
    tech_stack is CLASSIFIER OUTPUT in agents.go, not input.
    Stack is pinned by EMBEDDING it in the query string itself —
    same string the EA classifier embeds for cache lookup.
    """
    return {"query": integration["query"]}

def params_sha256(params: dict) -> str:
    return hashlib.sha256(
        json.dumps(params, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
```

#### Key code: `parse_envelope.py`

```python
import json, re

CITATIONS_SPLIT = re.compile(r"\n\n---\nSources:\n", re.MULTILINE)
CITATION_LINE   = re.compile(r"^(\d+)\.\s+(.+?)\s*$", re.MULTILINE)

def parse_mcp_payload(raw: dict) -> tuple[str, list[dict], float | None]:
    """Real wire shape (pkg/tools/exa/tool.go MCPExecute lines 269-274):
       result.content[0] = {"type":"text", "text": json.dumps({"content": <prose+sources>, "cost": <float>})}
    """
    result = raw.get("result") or {}
    content_blocks = result.get("content") or []
    if not content_blocks or content_blocks[0].get("type") != "text":
        return "", [], None
    envelope_text = content_blocks[0].get("text", "")
    try:
        envelope = json.loads(envelope_text)
    except json.JSONDecodeError:
        return envelope_text, [], None
    full = envelope.get("content", "")
    cost = envelope.get("cost")
    parts = CITATIONS_SPLIT.split(full, maxsplit=1)
    if len(parts) == 2:
        prose, sources_block = parts[0], parts[1]
        citations = [
            {"n": int(m.group(1)), "url": m.group(2).strip()}
            for m in CITATION_LINE.finditer(sources_block)
        ]
    else:
        prose, citations = full, []
    return prose, citations, (float(cost) if cost is not None else None)
```

#### Key code: `mcp_client.py`

```python
import time, uuid, httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

HEADER_RUN_ID         = "X-Run-ID"
HEADER_USER_ID        = "X-User-ID"
HEADER_ENV_IMAGE      = "X-Env-Image"
HEADER_BASE_URL       = "X-Emergent-Base-URL"
HEADER_PROXY_API_KEY  = "X-Emergent-Proxy-Api-Key"
HEADER_EVAL_RUN_ID    = "X-Eval-Run-ID"   # cache-bust

class TransientError(Exception): pass

class MCPClient:
    def __init__(self, *, server_tools_url, proxy_api_key, ea_base_url, user_id, env_image,
                 eval_run_id, timeout_s: float = 900.0):
        self._http = httpx.AsyncClient(timeout=timeout_s, base_url=server_tools_url)
        self._proxy_api_key = proxy_api_key
        self._ea_base_url   = ea_base_url
        self._user_id       = user_id
        self._env_image     = env_image
        self._eval_run_id   = eval_run_id

    async def aclose(self): await self._http.aclose()

    def headers(self, request_id: str) -> dict:
        return {
            HEADER_RUN_ID: request_id, HEADER_USER_ID: self._user_id,
            HEADER_ENV_IMAGE: self._env_image, HEADER_BASE_URL: self._ea_base_url,
            HEADER_PROXY_API_KEY: self._proxy_api_key,
            HEADER_EVAL_RUN_ID: self._eval_run_id,
            "Content-Type": "application/json",
        }

    @retry(
        retry=retry_if_exception_type(TransientError),
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=4, min=4, max=32),  # 4s, 16s
        reraise=True,
    )
    async def call_tool(self, tool_name: str, query: str) -> dict:
        request_id = str(uuid.uuid4())
        body = {"jsonrpc":"2.0","id":request_id,"method":"tools/call",
                "params":{"name":tool_name,"arguments":{"query": query}}}
        t0 = time.monotonic()
        try:
            r = await self._http.post("/mcp/v1/", json=body, headers=self.headers(request_id))
        except (httpx.ConnectError, httpx.ReadError, httpx.RemoteProtocolError) as e:
            raise TransientError(f"network: {e}") from e
        latency_ms = int((time.monotonic() - t0) * 1000)
        if r.status_code in (429, 502, 503, 504):
            raise TransientError(f"http {r.status_code}: {r.text[:200]}")
        r.raise_for_status()
        payload = r.json()
        payload["_request_id"] = request_id
        payload["_latency_ms"] = latency_ms
        payload["_image_sha"]  = r.headers.get("X-Image-Tag", "")
        return payload
```

#### Key code: `mcp_probe.py` (pre-run validation, NEW)

```python
import httpx, subprocess

async def assert_server_tools_ready(server_tools_url: str, headers: dict) -> tuple[str, list[str]]:
    async with httpx.AsyncClient(timeout=30.0) as c:
        # /healthz -> X-Image-Tag header
        h = await c.get(f"{server_tools_url}/healthz")
        h.raise_for_status()
        image_sha = h.headers.get("X-Image-Tag", "").strip()
        if not image_sha:
            try:
                image_sha = subprocess.check_output(
                    ["kubectl", "-n", "server-tools", "get", "deploy", "server-tools",
                     "-o", "jsonpath={.spec.template.spec.containers[0].image}"],
                    text=True, timeout=10,
                ).strip()
            except Exception as e:
                raise RuntimeError(
                    f"server_tools_image_sha unobtainable from X-Image-Tag or kubectl: {e}. "
                    "Refusing to run — reproducibility invariant would be violated.")
        # tools/list
        body = {"jsonrpc": "2.0", "id": "probe", "method": "tools/list"}
        r = await c.post(f"{server_tools_url}/mcp/v1/", json=body, headers=headers)
        r.raise_for_status()
        tools = [t["name"] for t in (r.json().get("result") or {}).get("tools", [])]
        required = {"integration_playbook_expert_v2", "integration_playbook_expert_v2_exa"}
        missing = required - set(tools)
        if missing:
            raise RuntimeError(f"tools/list missing required tools: {missing}. Found: {tools}")
        return image_sha, tools
```

#### Concurrency, retries, budget

- **Sequential per integration** (Exa then Perplexity in seeded random order), `integration_sem=2` across integrations. ~25–35 min wall clock for 28 integrations.
- **Retries**: one retry only, 4s/16s exponential backoff. Real flake → fail row with `failure_class='upstream_flake'`, proceed.
- **Cost watchdog**: per-call envelope cost adds to running total; hard abort if cumulative > $200.
- **Cache-miss double check**: preflight `/api/v1/knowledge/check` with same `X-Emergent-Base-URL` as tool call + post-hoc parse for `cost` in knowledge-base price band (0 < cost < 0.10) OR "Source: knowledge_base" marker → quarantine row.

### 2.4 Outputs

Per run at `results/{run_id}/`:
- `run_meta.json` — run_id, started_at, integrations_yaml_sha256, harness_git_commit, server_tools_image_sha, user_id, env_image, verdict_scope, judge_seed, projected/ceiling costs, integration_count, tools_registered, python/httpx versions.
- `judge_order.json` — seeded A/B mapping per slug for blinded pairwise.
- `<slug>__exa.json` + `<slug>__perplexity.json` — full CallResult per pydantic schema.
- `quarantine/` — cache-hit, thin-content, non-english rows excluded from analysis.
- `bonus/classifier_mislabels.jsonl` — opt-in via `--collect-mislabels`, free training data for the classifier-fix lever.

**Verdict dashboard tables** (in order):

**Table 1 — Reliability (FIRST, before any quality):**
| Backend | success | timeout | malformed | empty | http_err | reliability_rate |
|---|---|---|---|---|---|---|
| Exa Research | ?/28 | ? | ? | ? | ? | ? |
| Perplexity sonar-deep | ?/28 | ? | ? | ? | ? | ? |

If reliability_rate gap > 10pp → "stay on more-reliable backend" regardless of quality.

**Table 2 — Stage-1 quality** (per-dim tuples, never composite):
| Integration | C&F (C,G) | Exec (C,G) | Complete (C,G) | Cite (C,G) | Pairwise (4 votes) |

**Table 3 — Stage-2 pass rate** (verdict-relevant):
| Integration | Exa | Perplexity | Baseline (no-playbook) | Lift |

**Table 4 — Both-fail integrations** (route to human-help fallback): integrations where BOTH backends fail any non-`success` outcome. ≥3 both-fail in same stratum = stratum-level routing recommendation.

---

## 3. Stage 2 — End-to-End Smoke Test

### 3.1 Contract

7 Stage-2 cases (pre-randomized from §2.1). Each runs the agent (Claude Opus 4.7) in a sandbox pod with ONLY the candidate playbook (no playbook tools, no `knowledge_check`, no doc-domain egress). All four scoring axes (executability via Stage-2 override + the three judge-scored axes from Stage 1) feed the verdict.

**Per-Stage-2-case budget harness:**
```python
STAGE2_LIMITS = {
  "max_iterations": 10,
  "max_wallclock_s": 600,
  "max_spend_usd": 15.00,  # hard cap
}

def stage2_run(integration, playbook):
    agent = OpusAgent(model="claude-opus-4-7", tools=[execute_bash, ...])
    agent.set_budget(STAGE2_LIMITS)
    agent.system_prompt = f"Implement: {integration.persona}. Playbook follows:\n{playbook}"
    result = agent.run_until_assertion(integration.assertion_fn)
    if result.truncated:
        return Stage2Outcome(
            integration=integration.id,
            outcome="failure_truncated",
            reason=result.truncation_reason,  # "iter_cap" | "time_cap" | "spend_cap"
            iterations_used=result.iterations,
            spend_usd=result.spend,
        )
    return Stage2Outcome(outcome="success" if result.assertion_passed else "failure_assertion",
                        iterations_used=result.iterations, spend_usd=result.spend)
```

**Critical: truncation = failure. Not silent termination.** Mean expected cost $5/case, hard cap $15/case. Total Stage-2 worst-case: 7 × $15 = $105.

**Anti-cheat / egress policy:**
- `EA_VERIFIED_PLAYBOOK_LOOKUP=disabled` env flag on the pod.
- Smoke-test agent variant at `cortex/resources/agents/smoke-test-agent.yaml` (committed, version-pinned, NOT hot-emitted) with `integration_playbook_expert_v2`, `integration_playbook_expert_v2_exa`, `knowledge_check` REMOVED.
- Pod NetworkPolicy: allowlist (third-party target API host + pypi.org/simple + files.pythonhosted.org + registry.npmjs.org + harness control plane). Denylist (docs.stripe.com, developers.facebook.com, developers.google.com, supabase.com/docs, github.com, stackoverflow.com, pypi.org/project pages, npmjs.com/package).
- Monkey-patched `requests`, `httpx`, `urllib3` → log every outbound URL to `egress.log`.
- Pre-flight egress probe: agent runs `curl -sS https://docs.stripe.com`; assert non-zero exit with network-policy denial. Fail-fast cell as `infrastructure_fail` otherwise.
- Pre-flight toolset probe: send agent "list every tool currently available to you, one per line"; assert none of the three forbidden tool names in response.

**Synthetic tool-result injection** (matches prod prompt shape):
```python
pre_populated_turns = [
    {"role": "user", "content": canary.canary_task},
    {"role": "assistant", "content": [
        {"thinking": "Let me retrieve the playbook for {integration_name}."},
        {"tool_use": {
            "id": f"tu_{cell_id}",
            "name": "integration_playbook_expert_v2",
            "input": {"integration": canary.integration_name, "constraints": canary.constraints},
        }},
    ]},
    {"role": "user", "content": [
        {"tool_result": {"tool_use_id": f"tu_{cell_id}", "content": playbook_text_verbatim}},
    ]},
]
# agent resumes from turn 4
```

**Sandbox-onboarding timeline (T-7d):**
- Instant: Stripe test, Supabase test project, Clerk dev, OpenAI key, Solana devnet, Mapbox dev token.
- ~1h: Google Cloud project + Places API enabled.
- 24–72h human turnaround: PhonePe Business sandbox, Instagram Business Meta dev app, WhatsApp Cloud API test number + template approval. Initiate at T-7d. Pre-onboard ALL social/msg integrations as substitution insurance.

### 3.2 Canary Tasks (the 7 Stage-2 cases, persona-aligned with assertions)

| Stage-2 # | Integration | Persona (in constraint snippet) | Assertion (Stage-2 PASS = TRUE) |
|---|---|---|---|
| **2** | Lemon Squeezy | "One-time digital product purchase ... order_created webhook" | Complete sandbox order; receive `order_created` webhook; signature verifies. |
| **7** | Flutterwave Standard | "NGN cards + mobile money with transaction verification on redirect" | Initiate sandbox txn; on redirect, `GET /v3/transactions/:id/verify` returns `status=successful`. |
| **10** | Supabase auth (FastAPI+React) | "Email/password auth ... FastAPI verifies JWT with project JWT secret" | Signup → row in `auth.users`; subsequent JWT decoded by FastAPI returns user_id. |
| **13** | Instagram Login Business | "Login with Instagram for Business/Creator ... scopes instagram_business_basic + instagram_business_content_publish" | OAuth redirect lands on Meta sandbox; token exchange returns `access_token` with expected scopes in `/me` query. |
| **17** | OpenAI Responses + SSE | "SSE streaming ... displaying token-by-token output AND final usage block" | Streamed response yields ≥10 tokens; final SSE event contains `usage` object with `input_tokens`, `output_tokens`, `cache_read_input_tokens` fields. |
| **20** | Solana web3.js v2 | "Send a SOL transfer using @solana/web3.js >=2.0 ... createSolanaRpc" | Devnet transfer returns signature; `getSignatureStatuses` confirms `status='finalized'` within 60s. |
| **24** | Google Places (New) | "Address autocomplete using places.googleapis.com/v1/places:autocomplete" | POST to `/v1/places:autocomplete` with "1600 Amph" returns ≥1 suggestion containing 'Amphitheatre'. |

**No-playbook baseline (per missing concern: lift over baseline)** — 5 random Stage-2 picks (seed `20260609-baseline` → integrations [13, 17, 10, 20, 7]) run through the SAME harness but with `integration_playbook_expert_v2` REPLACED by a generic `web_search` tool (Tavily, $0.005/call). Same persona, same assertion. Verdict table adds "lift over baseline":

| Backend | Stage-2 pass rate | Baseline pass rate (n=5 subset) | Lift |
|---|---|---|---|
| Exa | ?/7 | ?/5 | ? pp |
| Perplexity | ?/7 | ?/5 | ? pp |
| (Baseline) | — | ?/5 | (anchor) |

**If lift < 15pp for both backends:** pre-registered conclusion = "playbook tool is not earning its keep; investigate deprecating it for OTHER traffic."

### 3.3 Success Criteria

**Per-case binary outcome.** Stage-2 PASS iff `agent.run_until_assertion(canary.assertion_fn)` returns `outcome='success'` within (max 10 iterations, max 600s wallclock, max $15 spend). Truncation = `failure_truncated` (NOT silent termination, NOT success).

**Stage-2 overrides EXECUTABILITY axis** for the 7 Stage-2 cases: actual execution outcome replaces judge-scored EXECUTABILITY with ground-truth 1 (truncated/assertion-fail) or 5 (success). Other axes still scored by judge.

**Reliability is INDEPENDENTLY DISQUALIFYING** (Table 1 in verdict). Tool_outcome enum per call: `{success, timeout (>210s), malformed_response, empty_response, http_error}`. If reliability_rate gap > 10pp → stay on more-reliable backend regardless of quality.

---

## 4. Sequencing & Timeline

| When | Event |
|---|---|
| **T-7d** | Sandbox-onboard phase: Stripe test, Supabase test, Clerk dev, Solana devnet, Mapbox dev, Google Places enable. |
| T-7d | Initiate slow-onboarding: PhonePe Business, Instagram Meta dev, WhatsApp test number + template approval (24-72h SLA each). |
| **T-3d** | Server-tools cache-key shape verification (Phase A): does cache key include `X-Eval-Run-ID` header? |
| T-3d | If Phase A reveals header dropped: Phase B suffix-confound validation on 3 integrations. |
| T-3d | Anti-overfit pre-grading: GPT-4o + Claude staleness grade all 28 integrations ($5.60). |
| T-3d | Empirical experiment: confirm `/api/v1/knowledge/check` template-aware or template-agnostic. If latter → enable runtime latency-based cache-hit detector. |
| **T-24h** | First pre-flight on ALL 43 items (28 primary + 15 backup). |
| **T-1d** | Confirm all Stage-2 sandboxes provisioned. Substitute via stratum if not. |
| **T-1d** | **Human ground-truth anchor: rishabh hand-grades 5 integrations against rubric. Run LLM judges on same 5. If MAD > 0.8 on any dim OR <4 of 5 pairwise winners agree → re-anchor rubric or stop and debug.** |
| **T-0** | Second pre-flight on all 43; resolve set; freeze; log drift. |
| T-0 + 0h | Main eval: 28 + 3 cross-stack + 3 idempotence repeats = 34 backend × 2 calls launched (sequential per integration, parallel across via integration_sem=2). |
| T-0 + ~3h | Backend results in; judge LLM runs primary (28 × 2 × 2) + collusion (5 dual-judge) + cross-stack (3). |
| **T-0 + ~6h** | **Operator gate after first 2 canary pairs:** spot-check Exa-vs-Perplexity wire shape for normalization-equivalence; require confirmation before remaining cells dispatch. |
| T-0 + ~6h | Stage-2 + no-playbook baseline runs begin (sequential to respect sandbox concurrency limits, especially Instagram). |
| T-0 + ~24h | Stage-2 complete; verdict assembly. |
| T-0 + ~30h | Ambiguous-prompt mini-study runs (separate, $5). |
| **T-0 + ~36h** | **Final writeup delivered.** |

**Human-in-loop checkpoints:** (1) operator confirms $200 budget pre-launch, (2) rishabh hand-grades 5 calibration integrations at T-1d, (3) operator gate after first 2 canary pairs for normalization sanity, (4) rishabh resolves judge disagreement spot-checks (~8–12 items, one afternoon).

---

## 5. Cost & Compute Budget

| Line item | Calc | Cost (USD) |
|---|---|---|
| Primary 28 × 2 backends × ~$0.40 | 28 × 2 × 0.40 | $22.40 |
| Cross-stack 3 nextjs × 2 backends × $0.40 | 3 × 2 × 0.40 | $2.40 |
| Idempotence 3 × 2 backends × 1 extra × $0.40 | 6 × 0.40 | $2.40 |
| Stage-2 7 cases × $5 mean (worst $15 cap) | 7 × 5 → 7 × 15 | $35 – $105 |
| No-playbook baseline 5 × $5 mean (worst $15) | 5 × 5 → 5 × 15 | $25 – $75 |
| Judge primary 28 × $0.05 (single judge call, cached) | 28 × 0.05 | $1.40 |
| Judge cross-stack 3 × $0.05 | 3 × 0.05 | $0.15 |
| Judge-collusion dual 5 × 2 × $0.05 | 10 × 0.05 | $0.50 |
| Judge self-consistency 3 × 2 × $0.05 | 6 × 0.05 | $0.30 |
| Judge style calibration 3 × 4 × $0.05 | 12 × 0.05 | $0.60 |
| Anti-overfit pre-grading 28 × 2 models × $0.10 | 28 × 2 × 0.10 | $5.60 |
| Ambiguous-prompt mini-study 5 × 2 × $0.40 | 10 × 0.40 | $4.00 |
| Buffer (re-runs of failed calls) | — | $5.00 |
| **TOTAL** | | **$103.85 – $223.85** |

**Realistic expected: ~$145** (Stage-2 and baseline at $5 mean).
**Worst case: ~$224**, ~12% over $200. Pre-registered: if worst-case hit, the report notes "exceeded $200 budget by $X due to Stage-2 cap saturation — this itself is a signal that one or both backends produced agent-iteration-heavy playbooks."

**Global watchdog**: per-cell envelope cost adds to running total; soft abort at $190 (no new dispatches, in-flight finish); hard abort at $200 (SIGTERM in-flight, partial report).

**No headroom for re-runs.** The original "3-runs-headroom" claim from v1 is retracted. A re-run requires fresh budget approval.

---

## 6. Risks & Mitigations

| # | Risk | Mitigation |
|---|---|---|
| 1 | **Judge favors length/citation density → Exa wins on style not substance** | Four orthogonal dimensions (length doesn't help completeness if duplicated). Per-dim scores reported as `(claude, gpt)` tuples — never composite. Stylistic-fingerprint calibration on 3 pairs quantifies the bias floor; headline differences must exceed it. |
| 2 | **Cache contamination (verified playbook → both tools return identical)** | Double-check: pre-flight `/api/v1/knowledge/check` with same `X-Emergent-Base-URL` as tool call + post-hoc parse for KB price band (0 < cost < 0.10) + "Source: knowledge_base" marker → quarantine. Pre-flight ALL 43 items at T-24h AND T-0. Drift >5 items aborts run. |
| 3 | **Smoke test passes hallucinated code (mocks let bad SDK pass)** | Stage-2 hits REAL third-party APIs in test mode. Long-tail (PhonePe, Paytm) uses mitmproxy outbound capture + signature shape verification; fail-closed if no outbound call detected OR if backend returns fabricated 200 with no real provider response. |
| 4 | **Opus self-rescues bad playbooks via doc curling → tools look more equal than they are** | Pod NetworkPolicy denylist on docs.stripe.com, developers.facebook.com, supabase.com/docs, github.com, stackoverflow.com, pypi.org/project, npmjs.com/package. Pre-flight probe: agent runs `curl -sS https://docs.stripe.com`; assert denial. Monkey-patch all Python HTTP libs to log egress URLs. |
| 5 | **Claude judging Claude-consumed playbooks amplifies self-preference bias** | Two-judge ensemble at 50/50 (NOT 60/40 Claude-primary). Disagreement-as-signal: cross-model split (both Claude votes vs both GPT votes) → human spot-check. Deterministic freshness_traps.json grep catches Claude's training-cutoff blind spots on Supabase/Clerk/Instagram/Solana/HubSpot/Stripe. |
| 6 | **Self-reported "low familiarity" is a fig leaf — LLMs hallucinate confidently on long-tail** | Replaced with structural pre-fetched-docs verification: harness fetches canonical official docs URL per integration (eval_official_docs.json) and ships it to judge in context. Judge scores "does playbook describe an API surface consistent with this URL". For genuinely undocumentable integrations: docs_unavailable=true triggers internal-consistency-only fallback. |
| 7 | **Verdict drift between Stage-2 numbers and judge dim scores → louder signal wins** | Pre-registered formula: `verdict_score = 0.7 * stage2_success_rate + 0.3 * judge_pairwise_winrate`. Judge dim scores are REPORTING-ONLY — they explain why, they don't decide the winner. Locked rubric (v2.0.0) with `rubric_version` field in every JSON; any rubric change requires re-run of all prior judged pairs. |

---

## 7. Definition of Done — What Verdict Does This Produce?

**Pre-registered verdict outcomes (locked BEFORE any data collection). Category-conditional verdicts are HYPOTHESIS-GENERATING only.**

```
verdict_score(backend) = 0.7 * stage2_success_rate(backend) + 0.3 * judge_pairwise_winrate(backend)
```

Where:
- `stage2_success_rate(backend)` = fraction of integrations where a real sandbox-agent run using the playbook from `backend` reached a passing state within (max 10 iter, 600s, $15). Binary per integration.
- `judge_pairwise_winrate(backend)` = fraction of pairs where the majority-vote winner across 4 judge votes (post-spot-check resolution) is `backend`. TIE counts 0.5 to each.

**Allowed verdicts:**

| Outcome | Condition |
|---|---|
| **SHIP EXA** | Exa wins on aggregate quality by ≥15pp **AND** reliability gap < 10pp **AND** Stage-2 pass rate gap ≥ 15pp **AND** cross-stack 3/3 agree **AND** median_tokens_to_semantic_pass(exa | pass) ≤ median_tokens(perplexity | pass) * 0.85. |
| **STAY ON PERPLEXITY** | Any of: reliability gap > 10pp favoring Perplexity, OR aggregate quality favors Perplexity by ≥15pp, OR Stage-2 favors Perplexity by ≥15pp, OR Exa Stage-2 below no-playbook baseline. |
| **INCONCLUSIVE — NEED MORE DATA** | Gaps within ±15pp on all axes. |
| **EXPERIMENTAL TRAFFIC SPLIT** | Cross-stack 2/3 agreement, OR judge-collusion bias suspected (4/5 cross-model disagreement) — recommend 20% Exa / 80% Perplexity prod traffic split for 2 weeks with downstream metrics monitored, then re-evaluate. |

**NOT allowed (explicitly retired from the verdict menu):**
- "Ship Exa for category X only" — n per category (3–5) cannot detect a category-level gap at decision-grade power. Any category-level finding is `requires follow-up eval with n ≥ 10 in that category` before influencing prod routing rules.

**Reliability cutoff (independent of quality):** Verdict Table 1 reports reliability rate per backend. **If reliability_rate gap > 10pp → STAY ON the more-reliable backend regardless of quality scores.**

**Both-fail integrations:** Pre-registered sidebar — integrations where BOTH backends fail any non-`success` outcome are logged as "route this category to human-help fallback in prod" candidates. ≥3 both-fail in same stratum = stratum-level routing recommendation (independent of which backend ships).

**Baseline cutoff:** If lift over no-playbook baseline < 15pp for BOTH backends, pre-registered conclusion = "playbook tool is not earning its keep; investigate deprecating it for OTHER traffic." This is a higher-priority finding than the Exa-vs-Perplexity question.

**Backend-failure handling (pre-registered):** Exa polling timeout or Perplexity API error → harness retries once. If still fails after retry, that integration is EXCLUDED from both head-to-head and per-backend Stage-2 success rate denominator. Exclusions reported: "Exa failed to respond on N of 28 (timeout); verdict computed on n=(28-N)."

**Retention policy (for any re-run within 6 months):** 14 integrations carried over from this run (drawn from the 28 whose verified-playbook DB entry was NOT written by this run's caching pipeline post-eval — checked via `/knowledge/check` pre-re-run); 14 freshly drawn from updated backup pool + new candidates. Pre-registered NOW, before any results.

---

## 8. Open Questions

1. **Server-tools cache-key shape (Phase A at T-3d).** Does the cache key for `integration_playbook_expert_v2_exa` include HTTP request headers like `X-Eval-Run-ID`? Needs server-tools team confirmation (or 5-min code read of `pkg/tools/exa/`) before T-3d. Phase B suffix-validation fallback adds 1 day of engineering work if header is not honored.

2. **`/api/v1/knowledge/check` template-awareness.** Empirical experiment at T-3d: call for "Stripe Payment Element" with `template=FastAPI+React` AND `template=nextjs`. If responses differ, check is template-aware (script valid as-is). If identical, add runtime latency-based cache-hit detector (any tool response with latency <2s → flagged, discarded, replaced).

3. **mitmproxy sidecar in deployer image** (blocks long-tail Stage-2). Deployer team has confirmed sidecar support but the eval-specific config (record-only, no MITM cert injection — we DON'T want to break TLS for the agent's outbound calls; just record at the gateway) needs a short PR to the deployer image. ETA 1 day.

4. **Sandbox onboarding ownership.** Who maintains the smoke-test 3rd-party accounts (HARNESS_TEST_EMAIL for Clerk, HARNESS_IG_TEST_USERNAME for Instagram, harness-funded Solana devnet pool addresses, Razorpay/MercadoPago test creds)? Proposal: single `eval-bot@emergent.sh` identity with credentials in 1Password vault `eval-harness-creds`. Needs ops sign-off because Instagram Business sandbox requires Meta dev portal access.

5. **Stage-2 case #13 (Instagram) onboarding fallback.** Meta dev app's 1-tester-at-a-time limit means Instagram serializes (3 runs ≈ 75 min wall). If onboarding fails at T-1d, the substitution algorithm picks #14 WhatsApp or #15 Discord — both with their own sandbox onboarding. Pre-onboard ALL social/msg integrations as insurance (~3h human time, $0).

6. **Judge-collusion escalation path.** If 4/5 cross-model disagreement is observed (Claude vs GPT-4o), verdict is downgraded one level (decision-grade → suggestive) AND a $50 follow-up sub-eval with Gemini 2.0 as third judge is recommended. Confirm this escalation path is acceptable to the operator.

7. **Cross-stack pair CS-C (OpenAI Responses on nextjs Edge).** Should we pin Edge runtime, or relax to just "nextjs App Router" without runtime specifier? Leaning yes — pin the destination, not the runtime — but escalating for confirmation.

8. **Sign-off on the $200 hard-abort and ~1 day of authoring 5 calibration anchor playbooks (rishabh's hand-grading set).** Operator must confirm before kick-off.