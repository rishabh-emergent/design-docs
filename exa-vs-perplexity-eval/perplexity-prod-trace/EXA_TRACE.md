# How we call the Exa Agent API for the same playbook tool — exact trace

**Purpose:** Companion to the Perplexity and Gemini traces. We have implemented an Exa-backed variant of the same integration-playbook tool using the **Exa Agent API** endpoint and config shared by the Exa team. This doc shows exactly how we call it, with the **same 5 real production inputs** replayed — measured latency, billed cost, and complete outputs — for a like-for-like 3-way comparison.

**Method:** Same 5 verbatim production tool inputs as the other traces, replayed through the byte-identical request construction of our Exa implementation. The prompt text is IDENTICAL to the Perplexity/Gemini paths (same system + user templates, same tech_stack injection), sent as the Agent API's single `query` field.

---

## 1. The exact API call

```
POST https://api.exa.ai/agent/runs
x-api-key: exa-REDACTED-MOCK-KEY
Exa-Beta: agent-2026-05-07
Content-Type: application/json
```

```json
{
  "query": "<SAME SYSTEM PROMPT + blank line + SAME USER PROMPT as the other traces>",
  "effort": "medium"
}
```

Then poll until the run reaches a terminal status:

```
GET https://api.exa.ai/agent/runs/{id}     (same headers, every 5 s)
```

### Settings — complete list

| Setting | Value | Notes |
|---|---|---|
| Endpoint | `POST /agent/runs` + `GET /agent/runs/{id}` polling | async run model |
| `effort` | `medium` | flat-priced $0.10/call |
| Beta header | `Exa-Beta: agent-2026-05-07` | |
| `outputSchema` | **not sent** | defaults to text output |
| Poll interval / max wait | 5 s / 10 min | |
| Retries | **none** — single run | |

### Prompts

Identical text to the Perplexity trace (section 3 there) — the `Integration_Playbook_Expert` system template with `{stack}` and the user template with `{query}` embedded whole, concatenated into the single `query` field.

### Cost basis

Exa returns the actual billed cost in every run (`costDollars`) — **flat $0.10 total on every one of our calls**, split into `agentCompute` + `search` components. No estimation needed.

### What we do with the response

1. Take `output.text` as-is (the playbook markdown).
2. Harvest unique citation URLs from `output.grounding[].citations[].url` — these are **real, checkable doc-page links** (e.g. `docs.stripe.com/...`, `docs.expo.dev/...`), present on every call.
3. Append them as the same `Sources:` list format; wrap as `{"content": ..., "cost": 1.5}` (internal billing unit).

## 2. Samples — summary (same 5 inputs as the other traces)

| # | Sample | Latency | Billed cost | Playbook | Citation URLs | Searches run |
|---|---|---|---|---|---|---|
| 1 | Stripe checkout — mobile (Expo React Native) school-fee app | 91.7 s | $0.1 | 10,633 ch | 14 | 9 |
| 2 | Google Drive CSV upload — FastAPI backend | 65.0 s | $0.1 | 12,555 ch | 15 | 9 |
| 3 | Custom JWT auth — mobile (Expo React Native) | 71.8 s | $0.1 | 10,088 ch | 7 | 12 |
| 4 | JWT + mocked OTP + roles — mobile (Expo React Native) | 113.4 s | $0.1 | 13,240 ch | 8 | 6 |
| 5 | PayPal checkout — web (FastAPI + React) store | 50.7 s | $0.1 | 9,125 ch | 16 | 9 |

**Averages:** latency **78.5 s**, cost **$0.100/call (flat)**, playbook **11,128 chars**.

## 3. Three-way comparison — identical inputs (Exa / Gemini / Perplexity)

| # | Latency (s) | Cost | Playbook (chars) | Citation URLs |
|---|---|---|---|---|
| 1 | 91.7 / 35.9 / 258.3 s | $0.1 / $0.04698 / $0.83704 | 10,633 / 10,061 / 67,943 ch | 14 / 0 / 42 |
| 2 | 65.0 / 32.0 / 321.2 s | $0.1 / $0.04653 / $0.94294 | 12,555 / 9,685 / 90,197 ch | 15 / 0 / 48 |
| 3 | 71.8 / 33.0 / 261.7 s | $0.1 / $0.05147 / $0.91603 | 10,088 / 10,700 / 67,328 ch | 7 / 0 / 41 |
| 4 | 113.4 / 36.1 / 317.9 s | $0.1 / $0.0554 / $1.25735 | 13,240 / 11,856 / 77,531 ch | 8 / 0 / 50 |
| 5 | 50.7 / 27.4 / 229.6 s | $0.1 / $0.04279 / $1.04711 | 9,125 / 8,642 / 63,374 ch | 16 / 0 / 50 |

Reading: each cell is `Exa / Gemini / Perplexity`.

---

## Sample 1: Stripe checkout — mobile (Expo React Native) school-fee app

| | |
|---|---|
| Run status / stop reason | `completed` / `schema_satisfied` |
| **Latency** | **91.7 s** (incl. 17 polls at 5 s) |
| **Total cost (from Exa's `costDollars`)** | **$0.1** |
| Cost breakdown | agentCompute $0.055 · search $0.045 |
| Usage | agentComputeUnits 0.55 · searches 9 |
| Playbook length | 10,633 chars |
| Citations (real doc URLs from `output.grounding`) | 14 |

### Input — what our agent asked the tool (verbatim, same as the Perplexity/Gemini traces)

```
INTEGRATION: Stripe payment integration for Expo React Native mobile app + FastAPI backend. Use case: students/parents pay school registration fee for pondok pesantren (Islamic boarding school). Need test mode payment with checkout session. CONSTRAINTS: Mobile app uses Expo SDK 54, no login (registration ID based), Stripe test keys available in pod environment.
```

### Exact API request sent to Exa

```json
{
  "url": "https://api.exa.ai/agent/runs",
  "method": "POST",
  "headers": {
    "x-api-key": "exa-REDACTED-MOCK-KEY",
    "Exa-Beta": "agent-2026-05-07",
    "Content-Type": "application/json"
  },
  "body": {
    "query": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them.\n\nCreate a detailed integration playbook for INTEGRATION: Stripe payment integration for Expo React Native mobile app + FastAPI backend. Use case: students/parents pay school registration fee for pondok pesantren (Islamic boarding school). Need test mode payment with checkout session. CONSTRAINTS: Mobile app uses Expo SDK 54, no login (registration ID based), Stripe test keys available in pod environment. in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise.",
    "effort": "medium"
  },
  "polling": "GET https://api.exa.ai/agent/runs/{id} every 5s until status not in (queued, running)"
}
```

### Exact output returned to our agent (verbatim, 11,420 chars)

The playbook exactly as Exa Agent wrote it (`output.text`), with the grounding citation URLs appended as a `Sources:` list by our tool layer. Wrapped as `{"content": "<below>", "cost": 1.5}` (internal billing unit, unrelated to the Exa dollar cost).

`````markdown
# Stripe Checkout Playbook — Expo React Native + FastAPI + MongoDB + React Native Web

## 1) Install

### Backend (FastAPI)
```bash
pip install fastapi uvicorn stripe motor pydantic-settings python-dotenv
```
Use one MongoDB client/pool per process and keep the MongoDB URI in env vars. MongoDB recommends reusing a single `MongoClient`/pool; default pool size is 100. [MongoDB][FastAPI]

### Mobile + Web (Expo SDK 54)
```bash
npx expo install expo-web-browser expo-linking
```
`expo-web-browser` opens Stripe Checkout in the system browser/custom tab; `expo-linking` handles deep links and URL creation. Add a custom `scheme` in `app.json` for native redirects. [Expo WebBrowser][Expo Linking]

### `app.json`
```json
{
  "expo": {
    "name": "pondok-pay",
    "slug": "pondok-pay",
    "scheme": "pondokpay"
  }
}
```

## 2) API keys + security

### Where to get keys
- **Stripe test secret key**: Stripe Dashboard → Developers → API keys
- **Webhook signing secret**: Stripe Dashboard → Developers → Webhooks, or locally from `stripe listen` output (`whsec_...`) [Stripe Webhooks][Stripe CLI]

### Store as environment variables in the backend pod
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
MONGODB_URI=mongodb+srv://...
PUBLIC_WEB_URL=https://your-web-app.example
APP_SCHEME=pondokpay
REGISTRATION_FEE_IDR=250000
```

### Security rules
- Keep Stripe secret key and webhook secret **server-side only**.
- Never trust the client for the fee amount; derive it from `registration_id`/database.
- Put `registration_id` in `client_reference_id` and `metadata`.
- Use **test keys** in test mode only; rotate and separate test/live secrets.
- Verify every webhook with the raw body + `Stripe-Signature` + webhook secret. Do **not** parse JSON before verification. [Stripe Webhooks]

## 3) Backend implementation (FastAPI + MongoDB)

### `main.py`
```python
import os
from datetime import datetime, timezone
from functools import lru_cache

import stripe
from fastapi import FastAPI, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    MONGODB_URI: str
    PUBLIC_WEB_URL: str
    APP_SCHEME: str = "pondokpay"
    REGISTRATION_FEE_IDR: int = 250000
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
stripe.api_key = settings.STRIPE_SECRET_KEY

mongo = AsyncIOMotorClient(settings.MONGODB_URI)
db = mongo["pondok_pay"]
registrations = db["registrations"]
payments = db["payments"]
processed_events = db["stripe_events"]

app = FastAPI()

class CheckoutReq(BaseModel):
    registration_id: str
    student_name: str | None = None
    platform: str  # "mobile" or "web"

@app.post("/api/payments/checkout-session")
async def create_checkout_session(body: CheckoutReq):
    reg = await registrations.find_one({"registration_id": body.registration_id})
    if not reg:
        raise HTTPException(404, "registration_id not found")

    amount = int(reg.get("fee_idr", settings.REGISTRATION_FEE_IDR))
    success_url = (
        f"{settings.PUBLIC_WEB_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}&registration_id={body.registration_id}"
        if body.platform == "web"
        else f"{settings.APP_SCHEME}://payment/success?session_id={{CHECKOUT_SESSION_ID}}&registration_id={body.registration_id}"
    )
    cancel_url = (
        f"{settings.PUBLIC_WEB_URL}/payment/cancel?registration_id={body.registration_id}"
        if body.platform == "web"
        else f"{settings.APP_SCHEME}://payment/cancel?registration_id={body.registration_id}"
    )

    session = stripe.checkout.Session.create(
        mode="payment",
        origin_context="mobile_app",
        line_items=[{
            "price_data": {
                "currency": "idr",
                "product_data": {"name": "Biaya pendaftaran pesantren"},
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=body.registration_id,
        metadata={
            "registration_id": body.registration_id,
            "student_name": body.student_name or "",
            "purpose": "registration_fee"
        },
    )

    await payments.update_one(
        {"registration_id": body.registration_id},
        {"$set": {
            "registration_id": body.registration_id,
            "stripe_session_id": session.id,
            "status": "pending",
            "amount_idr": amount,
            "updated_at": datetime.now(timezone.utc),
        }},
        upsert=True,
    )
    return {"url": session.url, "session_id": session.id}

@app.post("/api/payments/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()  # raw body required
    sig_header = request.headers.get("stripe-signature")
    if not sig_header:
        raise HTTPException(400, "missing signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except Exception:
        raise HTTPException(400, "invalid signature")

    # idempotency: ignore duplicate events
    if await processed_events.find_one({"id": event["id"]}):
        return {"received": True, "duplicate": True}
    await processed_events.insert_one({"id": event["id"], "type": event["type"]})

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        registration_id = session.get("metadata", {}).get("registration_id") or session.get("client_reference_id")
        if registration_id:
            await payments.update_one(
                {"registration_id": registration_id},
                {"$set": {
                    "status": "paid",
                    "stripe_payment_status": session.get("payment_status"),
                    "stripe_checkout_session_id": session["id"],
                    "paid_at": datetime.now(timezone.utc),
                }},
                upsert=True,
            )
    return {"received": True}
```
Stripe recommends a new Checkout Session per payment attempt, with `mode='payment'`, `line_items`, and a hosted-session redirect URL; for mobile app flows, `origin_context=mobile_app` is supported. [Stripe Checkout]

## 4) Expo React Native + React Native Web client

### Shared payment button
```tsx
import React, { useEffect } from 'react';
import { Alert, Platform, Button, View } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import * as Linking from 'expo-linking';

const API_URL = process.env.EXPO_PUBLIC_API_URL!;

export default function PayFeeButton({ registrationId }: { registrationId: string }) {
  const url = Linking.useURL();

  useEffect(() => {
    if (!url) return;
    const parsed = Linking.parse(url);
    if (parsed.path?.includes('payment/success')) {
      // read session_id / registration_id and refresh payment status
      console.log('Returned from Stripe:', parsed.queryParams);
    }
  }, [url]);

  const startPayment = async () => {
    const res = await fetch(`${API_URL}/api/payments/checkout-session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ registration_id: registrationId, platform: Platform.OS === 'web' ? 'web' : 'mobile' }),
    });
    const data = await res.json();
    if (!res.ok) return Alert.alert('Payment error', data.detail || 'Failed');

    if (Platform.OS === 'web') {
      window.location.href = data.url;
      return;
    }
    await WebBrowser.openBrowserAsync(data.url);
  };

  return <Button title="Pay registration fee" onPress={startPayment} />;
}
```
Use `Linking.createURL()` and a custom app `scheme` for native deep links; Expo Go uses `exp://`, while development/production builds use your custom scheme. [Expo Linking] `expo-web-browser` is the right tool for opening Checkout in a browser, and on web it requires a secure origin when using auth-style flows; for a plain checkout page, `openBrowserAsync` is the simple choice. [Expo WebBrowser]

### Web success page
```tsx
import React from 'react';
import { useLocalSearchParams } from 'expo-router';

export default function PaymentSuccess() {
  const { session_id, registration_id } = useLocalSearchParams();
  return (
    <div>
      <h1>Payment received</h1>
      <p>Registration ID: {registration_id}</p>
      <p>Session: {session_id}</p>
    </div>
  );
}
```

## 5) Testing procedure

1. **Set env vars** in the backend pod: Stripe test secret, MongoDB URI, webhook secret, public web URL. 
2. **Run backend**: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
3. **Forward webhooks locally**:
   ```bash
   stripe listen --forward-to http://localhost:8000/api/payments/stripe-webhook
   ```
   Use the `whsec_...` printed by the CLI for local webhook verification; do not mix it with the dashboard endpoint secret. [Stripe CLI][Stripe Webhooks]
4. **Create a Checkout Session** from the app with a test `registration_id`.
5. **Complete checkout in test mode** and confirm:
   - browser returns to success URL
   - MongoDB payment document changes to `paid`
   - webhook event is stored once (idempotency)
6. **Webhook simulation**: `stripe trigger checkout.session.completed` if you want a fast local event test. [Stripe CLI]
7. **Deep-link test on mobile**: use a development build, not Expo Go, for custom scheme redirects. [Expo Linking]

## 6) Common pitfalls

- **Wrong secret**: dashboard webhook secret vs CLI `whsec_...` are different. [Stripe Webhooks][Stripe CLI]
- **Parsing request body before verification**: breaks signature checks. Keep raw bytes intact. [Stripe Webhooks]
- **Client-controlled amount**: never accept fee amount from the app; derive it server-side from `registration_id`.
- **No custom scheme in Expo**: success redirect won’t come back into the app without a configured `scheme` and a development build. [Expo Linking]
- **Not handling duplicates**: Stripe can retry webhooks; store processed event IDs.
- **Using live keys in test flow**: keep test and live env vars separate.
- **Missing `payment_status` check**: only mark paid from `checkout.session.completed` after webhook verification, not from the client redirect.

If you want, I can turn this into a ready-to-paste repo structure (`backend/`, `mobile/`, `web/`) with filenames.

---
Sources:
1. https://www.mongodb.com/docs/drivers/node/current/connect/mongoclient/
2. https://fastapi.tiangolo.com/advanced/settings/
3. https://docs.expo.dev/linking/into-other-apps/
4. https://docs.expo.dev/versions/latest/sdk/webbrowser/
5. https://docs.stripe.com/api/checkout/sessions/create
6. https://docs.stripe.com/api/checkout/sessions
7. https://docs.stripe.com/webhooks?lang=python&locale=en-GB
8. https://docs.stripe.com/webhooks/quickstart
9. https://docs.stripe.com/cli/listen
10. https://docs.expo.dev/linking/into-your-app/
11. https://docs.expo.dev/versions/latest/sdk/linking/
12. https://www.mongodb.com/docs/drivers/node/current/connect/connection-options/
13. https://fastapi.tiangolo.com/environment-variables/
14. https://docs.stripe.com/webhooks/signature

`````

---
## Sample 2: Google Drive CSV upload — FastAPI backend

| | |
|---|---|
| Run status / stop reason | `completed` / `schema_satisfied` |
| **Latency** | **65.0 s** (incl. 12 polls at 5 s) |
| **Total cost (from Exa's `costDollars`)** | **$0.1** |
| Cost breakdown | agentCompute $0.055 · search $0.045 |
| Usage | agentComputeUnits 0.55 · searches 9 |
| Playbook length | 12,555 chars |
| Citations (real doc URLs from `output.grounding`) | 15 |

### Input — what our agent asked the tool (verbatim, same as the Perplexity/Gemini traces)

```
INTEGRATION: Google Drive API integration for Python FastAPI backend
REQUIREMENTS:
- Upload CSV files to a specific shared Google Drive folder
- Auto-sync functionality for daily/weekly exports
- Real-time sync of time entry data
- User will provide OAuth tokens/credentials
- Need to handle authentication and file upload to shared folder ID
CONSTRAINTS:
- Must work with FastAPI backend
- Need to support automated scheduled uploads
- Handle OAuth2 authentication flow
```

### Exact API request sent to Exa

```json
{
  "url": "https://api.exa.ai/agent/runs",
  "method": "POST",
  "headers": {
    "x-api-key": "exa-REDACTED-MOCK-KEY",
    "Exa-Beta": "agent-2026-05-07",
    "Content-Type": "application/json"
  },
  "body": {
    "query": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them.\n\nCreate a detailed integration playbook for INTEGRATION: Google Drive API integration for Python FastAPI backend\nREQUIREMENTS:\n- Upload CSV files to a specific shared Google Drive folder\n- Auto-sync functionality for daily/weekly exports\n- Real-time sync of time entry data\n- User will provide OAuth tokens/credentials\n- Need to handle authentication and file upload to shared folder ID\nCONSTRAINTS:\n- Must work with FastAPI backend\n- Need to support automated scheduled uploads\n- Handle OAuth2 authentication flow in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise.",
    "effort": "medium"
  },
  "polling": "GET https://api.exa.ai/agent/runs/{id} every 5s until status not in (queued, running)"
}
```

### Exact output returned to our agent (verbatim, 13,624 chars)

The playbook exactly as Exa Agent wrote it (`output.text`), with the grounding citation URLs appended as a `Sources:` list by our tool layer. Wrapped as `{"content": "<below>", "cost": 1.5}` (internal billing unit, unrelated to the Exa dollar cost).

`````markdown
## Google Drive API + FastAPI + Expo/RN/Web + MongoDB Integration Playbook

### 0) What you need from Google
1. **Google Cloud project** → enable **Google Drive API**.
2. **OAuth consent screen** → add scopes and test users.
3. **OAuth client IDs**:
   - **Web client ID** for React Native Web / browser OAuth.
   - **iOS/Android client IDs** for Expo native builds.
4. **Shared folder ID** in the target Shared Drive.

> For this use case, use **OAuth 2.0** (not a simple API key). Drive uploads to shared drives require Drive OAuth scopes and `supportsAllDrives=true` on shared-drive calls [Google Drive API scopes, shared drives, OAuth web-server].

---

## 1) Installation

### FastAPI backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 motor pymongo apscheduler python-dotenv pydantic
```

### Expo React Native / React Native Web
```bash
npx create-expo-app myapp
cd myapp
npx expo install expo-auth-session expo-web-browser expo-secure-store
npm install axios
```

### MongoDB
Use MongoDB Atlas or self-hosted MongoDB. Store secrets in environment variables, never in source control [MongoDB/FastAPI docs].

---

## 2) OAuth setup & security best practices

### Scopes
Use the narrowest scope that still works for your flow. Recommended starting point:
- `https://www.googleapis.com/auth/drive.file` for per-file access
- Use broader `drive` only if you truly need full-drive management [Google Drive scopes]

### OAuth flow
- In Expo/Web, start OAuth with **AuthSession**.
- Request **offline access** (`access_type=offline`) so the backend can refresh tokens without user interaction [Google OAuth web-server].
- Use `state` and PKCE; do **not** embed client secrets in the app [Expo AuthSession, Google OAuth].
- Store refresh tokens **encrypted** in MongoDB and rotate/revoke when disconnected [Google OAuth, MongoDB/FastAPI].

### Expo-specific security notes
- `WebBrowser.maybeCompleteAuthSession()` is required.
- Use `AuthSession.makeRedirectUri()`.
- **Expo Go is not suitable** for production-like OAuth redirect testing; use a Development Build [Expo AuthSession].
- Store native tokens in `expo-secure-store`; on web use secure cookies or backend sessions [Expo auth docs].

---

## 3) Backend architecture

### MongoDB models
Store one integration record per user/account:
```python
# models.py
from datetime import datetime
from pydantic import BaseModel, Field

class GoogleDriveIntegration(BaseModel):
    user_id: str
    access_token_enc: str | None = None
    refresh_token_enc: str | None = None
    expiry: datetime | None = None
    folder_id: str
    shared_drive_id: str | None = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Encryption helper
Use your KMS or app-level encryption (Fernet example shown for brevity):
```python
# crypto.py
from cryptography.fernet import Fernet
import os

fernet = Fernet(os.environ["TOKEN_ENC_KEY"].encode())

def encrypt(v: str) -> str: return fernet.encrypt(v.encode()).decode()
def decrypt(v: str) -> str: return fernet.decrypt(v.encode()).decode()
```

### FastAPI app: OAuth callback, upload, sync
```python
# main.py
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os, csv, io

from crypto import encrypt, decrypt

load_dotenv()
app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = os.environ["GOOGLE_REDIRECT_URI"]
SHARED_FOLDER_ID = os.environ["GOOGLE_SHARED_FOLDER_ID"]

# Replace with real MongoDB access
DB = {}

class OAuthTokenIn(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str | None = None
    expires_in: int | None = None

class UploadRequest(BaseModel):
    user_id: str
    csv_path: str
    filename: str


def drive_client(user_id: str):
    doc = DB.get(user_id)
    if not doc:
        raise HTTPException(404, "integration not connected")
    creds = Credentials(
        token=decrypt(doc["access_token_enc"]) if doc.get("access_token_enc") else None,
        refresh_token=decrypt(doc["refresh_token_enc"]) if doc.get("refresh_token_enc") else None,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPES,
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(GoogleRequest())
        doc["access_token_enc"] = encrypt(creds.token)
        if creds.refresh_token:
            doc["refresh_token_enc"] = encrypt(creds.refresh_token)
        doc["expiry"] = creds.expiry
    return build("drive", "v3", credentials=creds)

@app.post("/oauth/store-token")
def store_token(payload: OAuthTokenIn):
    DB[payload.user_id] = {
        "user_id": payload.user_id,
        "access_token_enc": encrypt(payload.access_token),
        "refresh_token_enc": encrypt(payload.refresh_token) if payload.refresh_token else None,
        "expiry": datetime.now(timezone.utc) + timedelta(seconds=payload.expires_in or 3600),
        "folder_id": SHARED_FOLDER_ID,
        "updated_at": datetime.now(timezone.utc),
    }
    return {"ok": True}

@app.post("/drive/upload-csv")
def upload_csv(req: UploadRequest):
    service = drive_client(req.user_id)
    file_metadata = {"name": req.filename, "parents": [SHARED_FOLDER_ID]}
    media = MediaFileUpload(req.csv_path, mimetype="text/csv", resumable=True)
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id,name,parents",
            supportsAllDrives=True,
        ).execute()
        return file
    except HttpError as e:
        raise HTTPException(500, detail=str(e))

@app.post("/drive/sync-now")
def sync_now(user_id: str):
    # Example: export latest time-entry CSV and upload it
    csv_path = "/tmp/time_entries.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "project", "hours"])
        writer.writerow(["2026-06-11", "Client A", 1.5])
    return upload_csv(UploadRequest(user_id=user_id, csv_path=csv_path, filename="time_entries.csv"))
```

### Scheduled daily/weekly exports
Use APScheduler for recurring jobs [APScheduler docs]:
```python
from apscheduler.triggers.cron import CronTrigger

def run_export_all_users():
    for user_id in DB.keys():
        try:
            sync_now(user_id)
        except Exception as e:
            print(f"sync failed for {user_id}: {e}")

scheduler.add_job(run_export_all_users, CronTrigger(day_of_week="mon", hour=2, minute=0))
scheduler.add_job(run_export_all_users, CronTrigger(hour=2, minute=0))  # daily example
```

### Real-time sync
Drive supports webhook notifications via `changes.watch` / `files.watch`; for shared drives, use `supportsAllDrives=true`, and for incremental polling use `changes.getStartPageToken` + `changes.list` [Drive push notifications, changes API].

```python
@app.post("/drive/watch")
def watch_changes(user_id: str):
    service = drive_client(user_id)
    channel = {
        "id": f"chan-{user_id}",
        "type": "web_hook",
        "address": os.environ["DRIVE_WEBHOOK_URL"],
    }
    return service.changes().watch(
        pageToken="START_PAGE_TOKEN_FROM_DB",
        body=channel,
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
```

> For Shared Drive sync, replay the **shared drive change log**, not just the user log [Drive changes docs].

---

## 4) Expo React Native + React Native Web OAuth example

### `app.config.ts`
```ts
export default {
  expo: {
    scheme: "myapp",
    web: { bundler: "metro" },
  },
};
```

### `auth.ts`
```ts
import * as WebBrowser from "expo-web-browser";
import * as AuthSession from "expo-auth-session";
WebBrowser.maybeCompleteAuthSession();

const discovery = {
  authorizationEndpoint: "https://accounts.google.com/o/oauth2/v2/auth",
  tokenEndpoint: "https://oauth2.googleapis.com/token",
};

export async function connectGoogle() {
  const redirectUri = AuthSession.makeRedirectUri({ scheme: "myapp" });
  const authUrl = `${discovery.authorizationEndpoint}?` + new URLSearchParams({
    client_id: process.env.EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID!,
    redirect_uri: redirectUri,
    response_type: "code",
    scope: "https://www.googleapis.com/auth/drive.file",
    access_type: "offline",
    prompt: "consent",
    include_granted_scopes: "true",
  }).toString();

  const result = await AuthSession.startAsync({ authUrl, returnUrl: redirectUri });
  if (result.type !== "success") throw new Error("OAuth failed");
  return result.params.code;
}
```

### Exchange code on backend
```ts
import axios from "axios";

export async function completeGoogleConnect(userId: string) {
  const code = await connectGoogle();
  await axios.post(`${process.env.EXPO_PUBLIC_API_BASE}/oauth/exchange`, {
    user_id: userId,
    code,
    redirect_uri: AuthSession.makeRedirectUri({ scheme: "myapp" }),
  });
}
```

> On web, this works through the browser; on mobile, use a Development Build, not Expo Go [Expo AuthSession].

---

## 5) Testing procedures

### Backend tests
1. **OAuth token refresh**: mock expired credentials and confirm refresh occurs.
2. **Shared drive upload**: verify `parents=[folderId]` and `supportsAllDrives=True`.
3. **Scheduled job**: run APScheduler job manually and assert upload call.
4. **Webhook handler**: send fake Drive `X-Goog-*` headers and verify sync queue entry.

### Example pytest skeleton
```python
def test_upload_csv(monkeypatch):
    called = {}
    class FakeFiles:
        def create(self, **kwargs): called.update(kwargs); return self
        def execute(self): return {"id": "file123"}
    class FakeSvc:
        def files(self): return FakeFiles()
    monkeypatch.setattr("main.drive_client", lambda user_id: FakeSvc())
    res = upload_csv(UploadRequest(user_id="u1", csv_path="/tmp/a.csv", filename="a.csv"))
    assert res["id"] == "file123"
    assert called["supportsAllDrives"] is True
```

### OAuth flow testing
- Verify redirect URI matches console config exactly [Google OAuth web-server].
- Test native + web separately.
- Confirm refresh token is returned only with offline access and consent when needed [Google OAuth].

### Manual Drive checks
- Uploaded file appears in the **specific shared folder**.
- File owner/permissions reflect the shared drive’s model.
- Daily/weekly job runs on schedule.
- Real-time webhook receives `sync` then `change/update` notifications.

---

## 6) Common pitfalls

1. **Forgetting `supportsAllDrives=true`** → shared-drive uploads/listing fail [Drive shared drives].
2. **Wrong parent ID** → must use the folder’s actual ID in `parents`.
3. **No offline access** → no refresh token, so automation breaks [Google OAuth].
4. **Storing tokens in the app** → keep refresh tokens on the backend, encrypted [Expo + Google OAuth].
5. **Using Expo Go for OAuth** → use a Development Build instead [Expo AuthSession].
6. **Assuming user log sync is enough** → for shared drives, use the shared drive change log [Drive changes docs].
7. **No retry/backoff** → retry 403/429/5xx with exponential backoff [Drive limits/errors].
8. **Not handling expired watch channels** → webhook subscriptions must be renewed periodically.

---

## 7) Minimal production checklist
- [ ] Enable Drive API
- [ ] Configure OAuth consent + test users
- [ ] Create web + native OAuth clients
- [ ] Implement Expo AuthSession login
- [ ] Exchange code on FastAPI backend
- [ ] Encrypt and store refresh tokens in MongoDB
- [ ] Upload CSVs with `files.create(... supportsAllDrives=True, parents=[folderId])`
- [ ] Schedule exports with APScheduler
- [ ] Add Drive change notifications / polling
- [ ] Add exponential backoff + logging + token revoke flow

If you want, I can turn this into a **single copy-paste repo skeleton** with FastAPI + Expo + MongoDB files laid out.

---
Sources:
1. https://developers.google.com/workspace/drive/api/guides/manage-uploads
2. https://developers.google.com/drive/api/guides/enable-shareddrives
3. https://developers.google.com/workspace/drive/api/guides/api-specific-auth
4. https://developers.google.com/identity/protocols/oauth2/web-server
5. https://docs.expo.dev/guides/authentication
6. https://docs.expo.dev/develop/authentication/
7. https://www.mongodb.com/docs/languages/python/pymongo-driver/current/integrations/fastapi-integration/
8. https://developers.google.com/workspace/drive/api/guides/push
9. https://developers.google.com/workspace/drive/api/reference/rest/v3/changes/list
10. https://developers.google.com/workspace/drive/api/guides/manage-changes
11. https://developers.google.com/workspace/drive/api/guides/limits
12. https://developers.google.com/workspace/drive/api/guides/handle-errors
13. https://apscheduler.readthedocs.io/en/master/integrations.html
14. https://apscheduler.readthedocs.io/en/master/userguide.html
15. https://fastapi.tiangolo.com/tutorial/background-tasks/

`````

---
## Sample 3: Custom JWT auth — mobile (Expo React Native)

| | |
|---|---|
| Run status / stop reason | `completed` / `schema_satisfied` |
| **Latency** | **71.8 s** (incl. 13 polls at 5 s) |
| **Total cost (from Exa's `costDollars`)** | **$0.1** |
| Cost breakdown | agentCompute $0.04 · search $0.06 |
| Usage | agentComputeUnits 0.4 · searches 12 |
| Playbook length | 10,088 chars |
| Citations (real doc URLs from `output.grounding`) | 7 |

### Input — what our agent asked the tool (verbatim, same as the Perplexity/Gemini traces)

```
INTEGRATION: Custom JWT-based email/password authentication for an Expo React Native (SDK 54) mobile app with FastAPI + MongoDB backend. Need: register, login, password hashing (bcrypt), JWT token issuance/validation, secure token persistence on mobile (expo-secure-store).

CONSTRAINTS: 
- Expo SDK 54 React Native mobile app
- FastAPI backend with /api prefix on all routes
- MongoDB for user storage
- Token storage via expo-secure-store
```

### Exact API request sent to Exa

```json
{
  "url": "https://api.exa.ai/agent/runs",
  "method": "POST",
  "headers": {
    "x-api-key": "exa-REDACTED-MOCK-KEY",
    "Exa-Beta": "agent-2026-05-07",
    "Content-Type": "application/json"
  },
  "body": {
    "query": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them.\n\nCreate a detailed integration playbook for INTEGRATION: Custom JWT-based email/password authentication for an Expo React Native (SDK 54) mobile app with FastAPI + MongoDB backend. Need: register, login, password hashing (bcrypt), JWT token issuance/validation, secure token persistence on mobile (expo-secure-store).\n\nCONSTRAINTS: \n- Expo SDK 54 React Native mobile app\n- FastAPI backend with /api prefix on all routes\n- MongoDB for user storage\n- Token storage via expo-secure-store in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise.",
    "effort": "medium"
  },
  "polling": "GET https://api.exa.ai/agent/runs/{id} every 5s until status not in (queued, running)"
}
```

### Exact output returned to our agent (verbatim, 10,481 chars)

The playbook exactly as Exa Agent wrote it (`output.text`), with the grounding citation URLs appended as a `Sources:` list by our tool layer. Wrapped as `{"content": "<below>", "cost": 1.5}` (internal billing unit, unrelated to the Exa dollar cost).

`````markdown
# Integration Playbook: Custom JWT Email/Password Auth
**Stack:** Expo SDK 54 React Native + React Native Web, FastAPI (`/api` prefix), MongoDB, JWT, bcrypt, `expo-secure-store`.

> Note: Expo SecureStore is native-only (iOS/Android/tvOS); for web, use a fallback like `localStorage` or switch to httpOnly cookies. Expo’s auth guide shows a secure-store/localStorage split for web/native [Expo SecureStore][Expo Auth Guide].

---

## 1) Install

### Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn[standard] motor passlib[bcrypt] pyjwt python-dotenv email-validator
```

### Expo app (SDK 54)
```bash
npx create-expo-app@latest mobile
cd mobile
npx expo install expo-secure-store
npm i axios
```
Expo SDK 54 includes React Native Web support; no separate `react-native-web` install is needed [Expo SDK reference].

### Expo config for SecureStore
`app.json`:
```json
{
  "expo": {
    "plugins": [
      ["expo-secure-store", {
        "configureAndroidBackup": true,
        "faceIDPermission": "Allow $(PRODUCT_NAME) to access your Face ID biometric data."
      }]
    ]
  }
}
```
Use `EXPO_PUBLIC_` only for non-secret client vars like the API base URL [Expo Env Vars].

---

## 2) Secrets / environment setup

### Backend `.env`
```env
SECRET_KEY=generate-with-openssl
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MONGODB_URI=mongodb+srv://USER:PASS@cluster0.xxxxx.mongodb.net
MONGODB_DB=myapp
```
Generate the JWT secret locally:
```bash
openssl rand -hex 32
```
**Do not** expose `SECRET_KEY` to Expo. Only the API URL should be public on the client.

### Expo `.env`
```env
EXPO_PUBLIC_API_URL=http://localhost:8000
```
For device testing, replace `localhost` with your LAN IP or deployed backend URL [Expo Env Vars].

MongoDB URI comes from MongoDB Atlas “Connect” or your local MongoDB connection string.

---

## 3) FastAPI backend (`/api` prefix on all routes)

### `main.py`
```python
import os
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import jwt
from jwt import InvalidTokenError

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "myapp")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB]
users = db.users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

app = FastAPI()
auth = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    email: EmailStr


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload["exp"] = expire
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise exc
    except InvalidTokenError:
        raise exc

    user = await users.find_one({"email": email})
    if not user:
        raise exc
    return user


@app.on_event("startup")
async def startup():
    await users.create_index("email", unique=True)  # unique email constraint [MongoDB]


@auth.post("/register", response_model=Token)
async def register(data: RegisterIn):
    email = data.email.lower()
    if await users.find_one({"email": email}):
        raise HTTPException(400, "Email already registered")

    await users.insert_one({
        "email": email,
        "password_hash": hash_password(data.password),
        "created_at": datetime.now(timezone.utc),
    })
    return Token(access_token=create_access_token({"sub": email}))


@auth.post("/login", response_model=Token)
async def login(data: LoginIn):
    user = await users.find_one({"email": data.email.lower()})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(401, "Incorrect email or password")
    return Token(access_token=create_access_token({"sub": user["email"]}))


@app.get("/api/me", response_model=UserOut)
async def me(user=Depends(get_current_user)):
    return {"email": user["email"]}

app.include_router(auth, prefix="/api")
```
FastAPI’s JWT flow and bearer token validation pattern is the same one used in the official tutorial [FastAPI JWT]. FastAPI also documents `/api`-style router prefixes via `include_router(..., prefix=...)` [FastAPI APIRouter].

> bcrypt note: FastAPI’s latest tutorial recommends Argon2 for new apps, but bcrypt is still acceptable and supported via PassLib [FastAPI][pyca/bcrypt].

---

## 4) Expo React Native + React Native Web client

### `lib/tokenStorage.ts`
```ts
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const KEY = 'auth_token';

export async function saveToken(token: string) {
  if (Platform.OS === 'web') localStorage.setItem(KEY, token);
  else await SecureStore.setItemAsync(KEY, token);
}

export async function loadToken() {
  if (Platform.OS === 'web') return typeof localStorage === 'undefined' ? null : localStorage.getItem(KEY);
  return SecureStore.getItemAsync(KEY);
}

export async function clearToken() {
  if (Platform.OS === 'web') localStorage.removeItem(KEY);
  else await SecureStore.deleteItemAsync(KEY);
}
```

### `lib/api.ts`
```ts
import axios from 'axios';
import { loadToken } from './tokenStorage';

export const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL,
});

api.interceptors.request.use(async (config) => {
  const token = await loadToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

### `lib/auth.ts`
```ts
import { api } from './api';
import { saveToken, clearToken } from './tokenStorage';

export async function register(email: string, password: string) {
  const { data } = await api.post('/api/auth/register', { email, password });
  await saveToken(data.access_token);
}

export async function login(email: string, password: string) {
  const { data } = await api.post('/api/auth/login', { email, password });
  await saveToken(data.access_token);
}

export async function logout() {
  await clearToken();
}

export async function fetchMe() {
  const { data } = await api.get('/api/me');
  return data;
}
```

### Example screen (`app/index.tsx` or similar)
```tsx
import React, { useState } from 'react';
import { View, TextInput, Button, Text } from 'react-native';
import { login, register, fetchMe } from '../lib/auth';

export default function Screen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  return (
    <View style={{ padding: 24, gap: 12 }}>
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} autoCapitalize="none" />
      <TextInput placeholder="Password" secureTextEntry value={password} onChangeText={setPassword} />
      <Button title="Register" onPress={async () => setMsg(JSON.stringify(await register(email, password)))} />
      <Button title="Login" onPress={async () => { await login(email, password); setMsg('logged in'); }} />
      <Button title="Me" onPress={async () => setMsg(JSON.stringify(await fetchMe()))} />
      <Text>{msg}</Text>
    </View>
  );
}
```
For web, Expo’s auth guide uses `localStorage` as the fallback; SecureStore is native-only [Expo Auth Guide][Expo SecureStore].

---

## 5) Testing

### Backend
```bash
uvicorn main:app --reload
```
Try:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"a@b.com","password":"secret123"}'
```
Then test protected route:
```bash
curl http://localhost:8000/api/me \
  -H "Authorization: Bearer YOUR_JWT"
```
Expected: valid JWT returns user; invalid/expired JWT returns `401` with `WWW-Authenticate: Bearer` [FastAPI JWT].

### Expo mobile/web
```bash
npx expo start
# press i / a / w, or use Expo Go/dev build
```
- Register/login once.
- Restart app: token should persist.
- Web: refresh page; token should still load from `localStorage`.
- Mobile: verify token persists via SecureStore.

### Database
- Confirm `users` has a unique index on `email`.
- Attempt duplicate registration; expect `400`.

---

## 6) Common pitfalls
1. **Using SecureStore on web**: it won’t work; use a web fallback or cookies [Expo SecureStore][Expo Auth Guide].
2. **Storing JWT secret in Expo**: never put `SECRET_KEY` in `EXPO_PUBLIC_*`.
3. **Missing `/api` prefix**: make client calls to `/api/auth/...` and `/api/me`.
4. **Not hashing passwords**: store only `password_hash`, never plaintext [FastAPI JWT].
5. **No unique email index**: duplicate accounts will slip in; enforce `create_index("email", unique=True)` [MongoDB].
6. **Using `localhost` on a device**: use your machine IP or deployed backend URL.
7. **Long-lived tokens**: keep JWT expiry short and re-login on expiry.

If you want, I can turn this into a copy-paste project structure (`backend/` + `mobile/`) with full file tree.

---
Sources:
1. https://docs.expo.dev/versions/v54.0.0/sdk/securestore/
2. https://docs.expo.dev/router/advanced/authentication/
3. https://docs.expo.dev/guides/environment-variables/
4. https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
5. https://fastapi.tiangolo.com/reference/apirouter/
6. https://www.mongodb.com/docs/manual/core/index-unique/
7. https://github.com/pyca/bcrypt

`````

---
## Sample 4: JWT + mocked OTP + roles — mobile (Expo React Native)

| | |
|---|---|
| Run status / stop reason | `completed` / `schema_satisfied` |
| **Latency** | **113.4 s** (incl. 21 polls at 5 s) |
| **Total cost (from Exa's `costDollars`)** | **$0.1** |
| Cost breakdown | agentCompute $0.07 · search $0.03 |
| Usage | agentComputeUnits 0.7 · searches 6 |
| Playbook length | 13,240 chars |
| Citations (real doc URLs from `output.grounding`) | 8 |

### Input — what our agent asked the tool (verbatim, same as the Perplexity/Gemini traces)

```
INTEGRATION: JWT-based authentication for Expo React Native app with FastAPI backend. Need:
1. Email + password registration & login (working JWT auth)
2. Phone OTP mocked login (accept any 6-digit OTP for now, just generate JWT)
3. Role-based auth (customer vs admin role)
4. Token storage via expo-secure-store on client

CONSTRAINTS: 
- Backend FastAPI with MongoDB (Motor)
- Frontend Expo Router with React Native
- Use bcrypt for password hashing
- JWT tokens for session
```

### Exact API request sent to Exa

```json
{
  "url": "https://api.exa.ai/agent/runs",
  "method": "POST",
  "headers": {
    "x-api-key": "exa-REDACTED-MOCK-KEY",
    "Exa-Beta": "agent-2026-05-07",
    "Content-Type": "application/json"
  },
  "body": {
    "query": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them.\n\nCreate a detailed integration playbook for INTEGRATION: JWT-based authentication for Expo React Native app with FastAPI backend. Need:\n1. Email + password registration & login (working JWT auth)\n2. Phone OTP mocked login (accept any 6-digit OTP for now, just generate JWT)\n3. Role-based auth (customer vs admin role)\n4. Token storage via expo-secure-store on client\n\nCONSTRAINTS: \n- Backend FastAPI with MongoDB (Motor)\n- Frontend Expo Router with React Native\n- Use bcrypt for password hashing\n- JWT tokens for session in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise.",
    "effort": "medium"
  },
  "polling": "GET https://api.exa.ai/agent/runs/{id} every 5s until status not in (queued, running)"
}
```

### Exact output returned to our agent (verbatim, 13,670 chars)

The playbook exactly as Exa Agent wrote it (`output.text`), with the grounding citation URLs appended as a `Sources:` list by our tool layer. Wrapped as `{"content": "<below>", "cost": 1.5}` (internal billing unit, unrelated to the Exa dollar cost).

`````markdown
Below is a practical JWT auth playbook for **FastAPI + MongoDB (Motor) + Expo Router (React Native / Web)**. FastAPI’s recommended pattern is bearer-token auth with JWT verification, Expo Router recommends a `SessionProvider` + `Stack.Protected`, SecureStore is native-only with a web fallback, and MongoDB now notes Motor is deprecated in favor of PyMongo Async (but Motor still works for this build) [FastAPI JWT][Expo Router Auth][SecureStore][Motor].

## 1) Install

### Backend
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install fastapi uvicorn[standard] motor pyjwt bcrypt email-validator
```

### Frontend (Expo Router)
```bash
npx create-expo-app@latest myapp -t expo-router
cd myapp
npx expo install expo-secure-store
# if not already present:
# npx expo install expo-router react-native-web react-dom
```

### Where to get secrets/keys
- **MongoDB URI**: MongoDB Atlas → **Database** → **Connect** → **Drivers**.
- **JWT secret**: generate locally, do **not** use Expo public env vars:
```bash
openssl rand -hex 32
```
- **No external API key is needed** for the mocked OTP flow.

## 2) Backend setup

### `.env`
```env
MONGO_URI=mongodb+srv://...
DB_NAME=app
JWT_SECRET=your_long_random_secret
ACCESS_TOKEN_MINUTES=60
CORS_ORIGINS=http://localhost:8081,http://localhost:19006
```

### `app/main.py`
```python
import os, uuid, bcrypt, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field

SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "60"))
client = AsyncIOMotorClient(os.environ["MONGO_URI"])
db = client[os.getenv("DB_NAME", "app")]
users = db.users

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:8081").split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class OtpIn(BaseModel):
    phone: str
    otp: str = Field(pattern=r"^\d{6}$")

class UserOut(BaseModel):
    uid: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

@app.on_event("startup")
async def startup():
    await users.create_index("uid", unique=True)
    await users.create_index("email", unique=True, sparse=True)
    await users.create_index("phone", unique=True, sparse=True)

def hash_pw(p: str) -> str:
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def verify_pw(p: str, hashed: str) -> bool:
    return bcrypt.checkpw(p.encode(), hashed.encode())

def make_token(user: dict) -> str:
    payload = {
        "sub": user["uid"],
        "role": user["role"],
        "email": user.get("email"),
        "phone": user.get("phone"),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await users.find_one({"uid": payload["sub"]})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_roles(*roles):
    async def dep(user: Annotated[dict, Depends(current_user)]):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return dep

@app.post("/auth/register", response_model=TokenOut, status_code=201)
async def register(data: RegisterIn):
    if await users.find_one({"email": data.email}):
        raise HTTPException(status_code=409, detail="Email already in use")
    user = {
        "uid": uuid.uuid4().hex,
        "email": data.email,
        "password_hash": hash_pw(data.password),
        "role": "customer",
        "created_at": datetime.now(timezone.utc),
    }
    await users.insert_one(user)
    return {"access_token": make_token(user), "user": {k: user.get(k) for k in ["uid", "email", "phone", "role"]}}

@app.post("/auth/login", response_model=TokenOut)
async def login(data: LoginIn):
    user = await users.find_one({"email": data.email})
    if not user or not verify_pw(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"access_token": make_token(user), "user": {k: user.get(k) for k in ["uid", "email", "phone", "role"]}}

@app.post("/auth/phone-otp", response_model=TokenOut)
async def phone_otp(data: OtpIn):
    # mocked OTP: accept any 6-digit code
    user = await users.find_one({"phone": data.phone})
    if not user:
        user = {
            "uid": uuid.uuid4().hex,
            "phone": data.phone,
            "role": "customer",
            "phone_verified": True,
            "created_at": datetime.now(timezone.utc),
        }
        await users.insert_one(user)
    return {"access_token": make_token(user), "user": {k: user.get(k) for k in ["uid", "email", "phone", "role"]}}

@app.get("/me")
async def me(user: Annotated[dict, Depends(current_user)]):
    return {"uid": user["uid"], "email": user.get("email"), "phone": user.get("phone"), "role": user["role"]}

@app.get("/admin/panel")
async def admin_panel(user: Annotated[dict, Depends(require_roles("admin"))]):
    return {"ok": True, "admin": user.get("email") or user.get("phone")}
```

### Admin role setup
Create admins manually in MongoDB (don’t trust client-sent role):
```js
db.users.updateOne({ email: "admin@example.com" }, { $set: { role: "admin" } })
```

## 3) Frontend setup (Expo Router + SecureStore)

### `.env`
```env
EXPO_PUBLIC_API_URL=http://localhost:8000
```
> Expo only inlines `EXPO_PUBLIC_` vars into client code, so never put secrets there [Expo Env].

### `lib/storage.ts`
```ts
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const KEY = 'auth_token';

export async function setToken(value: string | null) {
  if (Platform.OS === 'web') {
    if (value) localStorage.setItem(KEY, value);
    else localStorage.removeItem(KEY);
    return;
  }
  if (value) await SecureStore.setItemAsync(KEY, value);
  else await SecureStore.deleteItemAsync(KEY);
}

export async function getToken() {
  if (Platform.OS === 'web') return localStorage.getItem(KEY);
  return SecureStore.getItemAsync(KEY);
}
```

### `context/session.tsx`
```tsx
import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { getToken, setToken } from '../lib/storage';

const API = process.env.EXPO_PUBLIC_API_URL!;

type Session = { token: string; role: 'customer' | 'admin' } | null;

type Ctx = {
  session: Session;
  loading: boolean;
  register: (email: string, password: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  otpLogin: (phone: string, otp: string) => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<Ctx | null>(null);

async function api(path: string, body?: any, token?: string) {
  const res = await fetch(`${API}${path}`, {
    method: body ? 'POST' : 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail ?? 'Request failed');
  return json;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const token = await getToken();
      if (token) {
        const me = await api('/me', undefined, token);
        setSession({ token, role: me.role });
      }
      setLoading(false);
    })();
  }, []);

  async function save(auth: { access_token: string; user: { role: 'customer' | 'admin' } }) {
    await setToken(auth.access_token);
    setSession({ token: auth.access_token, role: auth.user.role });
  }

  const value = useMemo<Ctx>(() => ({
    session,
    loading,
    register: async (email, password) => save(await api('/auth/register', { email, password })),
    login: async (email, password) => save(await api('/auth/login', { email, password })),
    otpLogin: async (phone, otp) => save(await api('/auth/phone-otp', { phone, otp })),
    signOut: async () => { await setToken(null); setSession(null); },
  }), [session, loading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
};
```

### `app/_layout.tsx`
```tsx
import { Stack } from 'expo-router';
import { AuthProvider, useAuth } from '../context/session';

function RootNav() {
  const { session, loading } = useAuth();
  if (loading) return null;
  return (
    <Stack>
      <Stack.Protected guard={!session}>
        <Stack.Screen name="(auth)" />
      </Stack.Protected>
      <Stack.Protected guard={!!session}>
        <Stack.Screen name="(app)" />
      </Stack.Protected>
    </Stack>
  );
}

export default function Layout() {
  return (
    <AuthProvider>
      <RootNav />
    </AuthProvider>
  );
}
```

### `app/(auth)/sign-in.tsx`
```tsx
import { useState } from 'react';
import { View, TextInput, Button } from 'react-native';
import { useAuth } from '../../context/session';
import { useRouter } from 'expo-router';

export default function SignIn() {
  const { login, register, otpLogin } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('123456');

  return (
    <View style={{ padding: 16, gap: 12 }}>
      <TextInput placeholder="email" value={email} onChangeText={setEmail} />
      <TextInput placeholder="password" secureTextEntry value={password} onChangeText={setPassword} />
      <Button title="Register" onPress={async () => { await register(email, password); router.replace('/'); }} />
      <Button title="Login" onPress={async () => { await login(email, password); router.replace('/'); }} />
      <TextInput placeholder="phone" value={phone} onChangeText={setPhone} />
      <TextInput placeholder="6-digit otp" value={otp} onChangeText={setOtp} />
      <Button title="Mock OTP Login" onPress={async () => { await otpLogin(phone, otp); router.replace('/'); }} />
    </View>
  );
}
```

## 4) Testing

### Backend
```bash
uvicorn app.main:app --reload
```
Then verify:
```bash
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"Pass123!"}'
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"Pass123!"}'
curl -X POST http://localhost:8000/auth/phone-otp -H "Content-Type: application/json" -d '{"phone":"+15550001111","otp":"123456"}'
curl http://localhost:8000/me -H "Authorization: Bearer YOUR_TOKEN"
curl http://localhost:8000/admin/panel -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### Frontend
```bash
npx expo start
npx expo start --web
```
Check:
- registration/login works
- OTP accepts any 6 digits
- token survives app restart (SecureStore on native, localStorage on web)
- admin route is blocked for `customer`

## 5) Common pitfalls
- **Sending JSON to OAuth2 password endpoints**: FastAPI’s password flow expects form data if you use `OAuth2PasswordRequestForm`; this playbook uses custom JSON endpoints to keep Expo simple [FastAPI JWT].
- **CORS misconfig**: don’t use `*` with credentials; allow explicit origins for Expo web/native hosts [FastAPI CORS].
- **Putting JWT secret in `EXPO_PUBLIC_` env vars**: Expo inlines those into client code, so keep secrets only on the backend [Expo Env].
- **SecureStore on web**: SecureStore is native-first; use localStorage fallback for web [SecureStore][Expo Router Auth].
- **bcrypt 72-byte limit**: very long passwords need a pre-hash strategy or a max-length policy [bcrypt].
- **Motor deprecation**: it works, but MongoDB recommends PyMongo Async for new work; plan a future migration [Motor].
- **Role changes not reflected**: if you change a user’s role in MongoDB, reissue the JWT.

That’s the full working integration: email/password signup/login, mocked phone OTP login, role-based access, and secure token persistence for Expo RN + web.

---
Sources:
1. https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
2. https://fastapi.tiangolo.com/tutorial/cors/
3. https://www.mongodb.com/docs/drivers/motor/
4. https://pypi.org/project/bcrypt/
5. https://docs.expo.dev/router/advanced/authentication/
6. https://docs.expo.dev/versions/latest/sdk/securestore/
7. https://docs.expo.dev/guides/environment-variables/
8. https://docs.expo.dev/versions/latest/sdk/router/

`````

---
## Sample 5: PayPal checkout — web (FastAPI + React) store

| | |
|---|---|
| Run status / stop reason | `completed` / `schema_satisfied` |
| **Latency** | **50.7 s** (incl. 9 polls at 5 s) |
| **Total cost (from Exa's `costDollars`)** | **$0.1** |
| Cost breakdown | agentCompute $0.055 · search $0.045 |
| Usage | agentComputeUnits 0.55 · searches 9 |
| Playbook length | 9,125 chars |
| Citations (real doc URLs from `output.grounding`) | 16 |

### Input — what our agent asked the tool (verbatim, same as the Perplexity/Gemini traces)

```
INTEGRATION: PayPal payment processing for e-commerce checkout
CONSTRAINTS: Need to integrate PayPal checkout button and payment processing for a dropshipping store
```

### Exact API request sent to Exa

```json
{
  "url": "https://api.exa.ai/agent/runs",
  "method": "POST",
  "headers": {
    "x-api-key": "exa-REDACTED-MOCK-KEY",
    "Exa-Beta": "agent-2026-05-07",
    "Content-Type": "application/json"
  },
  "body": {
    "query": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: reactjs frontend with shadcn, fastapi backend, mongodb database\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them.\n\nCreate a detailed integration playbook for INTEGRATION: PayPal payment processing for e-commerce checkout\nCONSTRAINTS: Need to integrate PayPal checkout button and payment processing for a dropshipping store in reactjs frontend with shadcn, fastapi backend, mongodb database application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise.",
    "effort": "medium"
  },
  "polling": "GET https://api.exa.ai/agent/runs/{id} every 5s until status not in (queued, running)"
}
```

### Exact output returned to our agent (verbatim, 10,086 chars)

The playbook exactly as Exa Agent wrote it (`output.text`), with the grounding citation URLs appended as a `Sources:` list by our tool layer. Wrapped as `{"content": "<below>", "cost": 1.5}` (internal billing unit, unrelated to the Exa dollar cost).

`````markdown
# PayPal Checkout Integration Playbook

PayPal Checkout should be wired so the **frontend only gets the PayPal Client ID**, while the **FastAPI backend creates/captures orders with the PayPal Client Secret** using OAuth 2.0 access tokens [PayPal Dev]. Use the PayPal JavaScript SDK/button flow for the buyer UI and the Orders v2 API on the server for create/capture [PayPal Orders API].

## 1) Install

### Frontend (React + shadcn)
```bash
npm install @paypal/react-paypal-js
npx shadcn@latest add button card
```

### Backend (FastAPI + MongoDB)
```bash
pip install fastapi uvicorn httpx motor pydantic-settings python-dotenv pytest anyio
```

### MongoDB
- Use MongoDB Atlas or a local **replica set** if you plan to use transactions; MongoDB transactions require a replica set or sharded cluster [MongoDB Transactions].
- Create an `orders` collection and a unique index on `paypalOrderId` to prevent duplicate captures [MongoDB Unique Index].

```js
db.orders.createIndex({ paypalOrderId: 1 }, { unique: true })
```

## 2) API keys + security

### Where to get PayPal keys
1. Log in to the **PayPal Developer Dashboard**.
2. Open **Apps & Credentials**.
3. Create/select your app and copy the **Client ID** and **Client Secret** [PayPal Dev].
4. Use **Sandbox** credentials while testing.

### Security rules
- **Frontend:** only use `PAYPAL_CLIENT_ID`.
- **Backend:** store `PAYPAL_CLIENT_SECRET` in `.env` / secret manager; never commit it [FastAPI Settings].
- Do **not** create/capture orders from the browser directly; call PayPal REST APIs from FastAPI [PayPal Orders API].
- Reuse OAuth access tokens until expiry; refresh on 401/expiry [PayPal Auth].
- Add webhook verification in production for payment status reconciliation [PayPal Webhooks].

## 3) Backend (FastAPI + MongoDB)

### `.env`
```env
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com
MONGODB_URI=mongodb+srv://...
MONGO_DB=shop
CORS_ORIGINS=http://localhost:5173
```

### `app/main.py`
```python
from datetime import datetime, timezone, timedelta
from typing import Optional
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    paypal_client_id: str
    paypal_client_secret: SecretStr
    paypal_base_url: str = "https://api-m.sandbox.paypal.com"
    mongodb_uri: str
    mongo_db: str = "shop"
    cors_origins: str = "http://localhost:5173"

settings = Settings()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo = AsyncIOMotorClient(settings.mongodb_uri)
db = mongo[settings.mongo_db]

_token: dict = {"access_token": None, "expires_at": datetime.min.replace(tzinfo=timezone.utc)}

class CreateOrderIn(BaseModel):
    amount: float
    currency: str = "USD"

class CaptureOrderIn(BaseModel):
    orderID: str

async def paypal_access_token() -> str:
    now = datetime.now(timezone.utc)
    if _token["access_token"] and now < _token["expires_at"]:
        return _token["access_token"]
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"{settings.paypal_base_url}/v1/oauth2/token",
            auth=(settings.paypal_client_id, settings.paypal_client_secret.get_secret_value()),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"},
        )
    r.raise_for_status()
    data = r.json()
    _token["access_token"] = data["access_token"]
    _token["expires_at"] = now + timedelta(seconds=int(data.get("expires_in", 900)) - 60)
    return _token["access_token"]

@app.post("/api/paypal/create-order")
async def create_order(payload: CreateOrderIn):
    token = await paypal_access_token()
    body = {
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": payload.currency, "value": f"{payload.amount:.2f}"}}],
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"{settings.paypal_base_url}/v2/checkout/orders",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=body,
        )
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.text)
    order = r.json()
    await db.orders.update_one(
        {"paypalOrderId": order["id"]},
        {"$set": {"paypalOrderId": order["id"], "status": "CREATED", "amount": payload.amount, "currency": payload.currency, "updatedAt": datetime.now(timezone.utc)}},
        upsert=True,
    )
    return {"id": order["id"]}

@app.post("/api/paypal/capture-order")
async def capture_order(payload: CaptureOrderIn):
    token = await paypal_access_token()
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"{settings.paypal_base_url}/v2/checkout/orders/{payload.orderID}/capture",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )
    if r.status_code >= 400:
        raise HTTPException(r.status_code, r.text)
    capture = r.json()
    await db.orders.update_one(
        {"paypalOrderId": payload.orderID},
        {"$set": {"status": "CAPTURED", "capture": capture, "updatedAt": datetime.now(timezone.utc)}},
        upsert=True,
    )
    return capture
```

## 4) Frontend (React + shadcn)

### `src/components/PaypalCheckout.tsx`
```tsx
import { PayPalButtons, PayPalScriptProvider } from "@paypal/react-paypal-js";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function PaypalCheckout({ amount }: { amount: number }) {
  const clientId = import.meta.env.VITE_PAYPAL_CLIENT_ID;
  const apiBase = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

  return (
    <Card className="max-w-md">
      <CardHeader><CardTitle>Checkout with PayPal</CardTitle></CardHeader>
      <CardContent>
        <PayPalScriptProvider options={{ clientId, currency: "USD", intent: "capture" }}>
          <PayPalButtons
            style={{ layout: "vertical", label: "paypal" }}
            createOrder={async () => {
              const res = await fetch(`${apiBase}/api/paypal/create-order`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ amount, currency: "USD" }),
              });
              const data = await res.json();
              return data.id;
            }}
            onApprove={async (data) => {
              await fetch(`${apiBase}/api/paypal/capture-order`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ orderID: data.orderID }),
              });
              alert("Payment successful");
            }}
            onError={(err) => console.error(err)}
          />
        </PayPalScriptProvider>
      </CardContent>
    </Card>
  );
}
```

### Use it on your checkout page
```tsx
import { PaypalCheckout } from "@/components/PaypalCheckout";
export default function CheckoutPage() {
  return <PaypalCheckout amount={49.99} />;
}
```

## 5) Testing

### Backend tests
Use FastAPI’s test tools; for async endpoints, `pytest.mark.anyio` + `httpx.AsyncClient` is the recommended pattern [FastAPI Testing].

```python
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_create_order():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/paypal/create-order", json={"amount": 10.0})
        assert res.status_code in (200, 201)
```

### Manual PayPal sandbox test
1. Use a **sandbox buyer** account to click the button.
2. Approve payment.
3. Confirm the payment appears in the **sandbox business account** recent activity [PayPal Dev].
4. Simulate webhooks in the PayPal dashboard to test fulfillment logic [PayPal Webhooks].

## 6) Common pitfalls
- **Putting the secret in React** → never do this; keep secret only in FastAPI [FastAPI Settings].
- **Calling capture on the client** → always capture on the server [PayPal Orders API].
- **Mixing sandbox and live credentials** → client ID, secret, and base URL must match environment [PayPal Auth].
- **Duplicate orders** → enforce a unique index on `paypalOrderId` [MongoDB Unique Index].
- **Using MongoDB standalone with transactions** → transactions need replica set/sharded cluster [MongoDB Transactions].
- **Expired PayPal tokens** → cache until expiry, then fetch a new one [PayPal Auth].

If you want, I can turn this into a ready-to-paste repo structure (`frontend/`, `backend/`, `.env.example`, and tests).

---
Sources:
1. https://developer.paypal.com/docs/multiparty/checkout/standard/integrate/
2. https://developer.paypal.com/reference/get-an-access-token/
3. https://developer.paypal.com/api/rest/authentication/
4. https://developer.paypal.com/api/orders/v2
5. https://developer.paypal.com/docs/api/webhooks/v1/
6. https://developer.paypal.com/docs/checkout/standard/customize/single-page-app/
7. https://fastapi.tiangolo.com/advanced/settings/
8. https://fastapi.tiangolo.com/tutorial/testing/
9. https://fastapi.tiangolo.com/advanced/async-tests/
10. https://www.mongodb.com/docs/manual/core/transactions/
11. https://www.mongodb.com/docs/manual/core/index-unique/create/
12. https://www.mongodb.com/docs/manual/core/index-unique/
13. https://www.mongodb.com/docs/manual/data-modeling/enforce-consistency/transactions/
14. https://ui.shadcn.com/docs/installation/manual
15. https://ui.shadcn.com/docs/components/base/button
16. https://ui.shadcn.com/docs/new

`````

---
## Notes

- The API key in all request dumps is mocked (`exa-REDACTED-MOCK-KEY`); everything else is byte-exact.
- Exa costs are the actual billed amounts returned in `costDollars`; Perplexity costs are from its `usage.cost`; Gemini costs are computed from exact token counts x published rates (it returns no dollar figure).
