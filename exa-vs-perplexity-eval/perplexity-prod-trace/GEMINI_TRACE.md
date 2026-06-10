# How we call Gemini for the same playbook tool — exact trace

**Purpose:** Companion to the Perplexity trace. We have implemented a Gemini-backed variant of the same integration-playbook tool. This doc shows exactly how it calls Gemini, with the **same 5 real production inputs** replayed — measured latency, cost, and complete outputs — so the two providers can be compared like-for-like.

**Method:** Same 5 verbatim production tool inputs as the Perplexity trace, replayed through the byte-identical request construction of our Gemini implementation. The prompt templates are IDENTICAL to the Perplexity path (same system + user templates, same tech_stack injection) — only the provider call differs.

---

## 1. The exact API call

Our service calls Gemini's `generateContent` with the built-in `google_search` grounding tool (it can route via Vertex AI or the direct Gemini API — identical model and request semantics; these samples were measured via the direct API):

```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key=GEMINI-REDACTED-MOCK-KEY
Content-Type: application/json
```

```json
{
  "systemInstruction": { "parts": [ { "text": "<SAME SYSTEM PROMPT as the Perplexity trace>" } ] },
  "contents": [ { "role": "user", "parts": [ { "text": "<SAME USER PROMPT as the Perplexity trace>" } ] } ],
  "tools": [ { "googleSearch": {} } ],
  "generationConfig": { "responseMimeType": "text/plain", "maxOutputTokens": 8192 }
}
```

### Settings — complete list

| Setting | Value | Notes |
|---|---|---|
| Model | `gemini-3.1-pro-preview` | hardcoded |
| Grounding | `google_search` built-in tool | Gemini runs the searches internally |
| `maxOutputTokens` | 8192 | |
| `responseMimeType` | `text/plain` | |
| `temperature` / `topP` / `topK` | **not sent** | Gemini defaults apply |
| Retries | provider-level fallback only (Vertex → direct API) | no call-level retry |

### Prompts

Identical templates to the Perplexity trace (section 3 there) — same `Integration_Playbook_Expert` system prompt with `{stack}`, same user prompt with `{query}` embedded whole.

### Cost basis

Gemini returns exact token counts (`usageMetadata`) but no dollar figure. Costs below = exact tokens x published list rates (**$2/1M input, $12/1M output**) + **$0.014/call** google_search grounding fee ($14/1k grounded prompts).

### What we do with the response

1. Concatenate all text parts of the first candidate (the playbook markdown).
2. Extract unique citation URLs from `groundingMetadata.groundingChunks[].web.uri`. In practice Gemini often surfaces few or zero URLs here even though grounding ran (visible from the per-call search activity) — the playbook content itself is still search-grounded.
3. If any URLs were surfaced, append them as the same `Sources:` list format; wrap as `{"content": ..., "cost": 1.5}` (internal billing unit).

## 2. Samples — summary (same 5 inputs as the Perplexity trace)

| # | Sample | Latency | Total cost | Playbook | Citation URLs |
|---|---|---|---|---|---|
| 1 | Stripe checkout — mobile (Expo React Native) school-fee app | 35.9 s | $0.04698 | 10,061 ch | 0 |
| 2 | Google Drive CSV upload — FastAPI backend | 32.0 s | $0.04653 | 9,685 ch | 0 |
| 3 | Custom JWT auth — mobile (Expo React Native) | 33.0 s | $0.05147 | 10,700 ch | 0 |
| 4 | JWT + mocked OTP + roles — mobile (Expo React Native) | 36.1 s | $0.0554 | 11,856 ch | 0 |
| 5 | PayPal checkout — web (FastAPI + React) store | 27.4 s | $0.04279 | 8,642 ch | 0 |

**Averages:** latency **32.9 s**, cost **$0.0486/call**, playbook **10,188 chars**.

## 3. Side-by-side vs Perplexity (identical inputs)

| # | Latency (Gemini / Perplexity) | Cost (Gemini / Perplexity) | Playbook (Gemini / Perplexity) |
|---|---|---|---|
| 1 | 35.9 s / 258.3 s | $0.04698 / $0.83704 | 10,061 / 67,943 ch |
| 2 | 32.0 s / 321.2 s | $0.04653 / $0.94294 | 9,685 / 90,197 ch |
| 3 | 33.0 s / 261.7 s | $0.05147 / $0.91603 | 10,700 / 67,328 ch |
| 4 | 36.1 s / 317.9 s | $0.0554 / $1.25735 | 11,856 / 77,531 ch |
| 5 | 27.4 s / 229.6 s | $0.04279 / $1.04711 | 8,642 / 63,374 ch |

---

## Sample 1: Stripe checkout — mobile (Expo React Native) school-fee app

| | |
|---|---|
| HTTP status | 200 |
| **Latency** | **35.9 s** |
| **Total cost (computed)** | **$0.04698** |
| Cost breakdown | input $0.00047 · output $0.03251 · grounding fee $0.014 |
| Tokens (exact, from `usageMetadata`) | prompt 235 · output 2,709 · total 4,225 |
| Playbook length | 10,061 chars |
| Citation URLs surfaced in grounding metadata | 0 |

### Input — what our agent asked the tool (verbatim, same as the Perplexity trace)

```
INTEGRATION: Stripe payment integration for Expo React Native mobile app + FastAPI backend. Use case: students/parents pay school registration fee for pondok pesantren (Islamic boarding school). Need test mode payment with checkout session. CONSTRAINTS: Mobile app uses Expo SDK 54, no login (registration ID based), Stripe test keys available in pod environment.
```

### Exact API request sent to Gemini

```json
{
  "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key=GEMINI-REDACTED-MOCK-KEY",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "systemInstruction": {
      "parts": [
        {
          "text": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
        }
      ]
    },
    "contents": [
      {
        "role": "user",
        "parts": [
          {
            "text": "Create a detailed integration playbook for INTEGRATION: Stripe payment integration for Expo React Native mobile app + FastAPI backend. Use case: students/parents pay school registration fee for pondok pesantren (Islamic boarding school). Need test mode payment with checkout session. CONSTRAINTS: Mobile app uses Expo SDK 54, no login (registration ID based), Stripe test keys available in pod environment. in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
          }
        ]
      }
    ],
    "tools": [
      {
        "googleSearch": {}
      }
    ],
    "generationConfig": {
      "responseMimeType": "text/plain",
      "maxOutputTokens": 8192
    }
  }
}
```

### Exact output returned to our agent (verbatim, 10,061 chars)

No citation URLs were surfaced in grounding metadata for this call, so no `Sources:` list is appended — the playbook below is the complete tool output. Wrapped as `{"content": "<below>", "cost": 1.5}` (internal billing unit).

`````markdown
Here is the complete integration playbook for setting up a Stripe Checkout Session payment flow for a Pondok Pesantren registration fee, using Expo React Native (SDK 54), React Native Web, FastAPI, and MongoDB.

This approach uses **Stripe Hosted Checkout Sessions** via Expo WebBrowser, which is the most reliable method for a no-login, Registration ID-based flow across both mobile and web.

---

### 1. Installation Instructions

**Backend (FastAPI + MongoDB + Stripe):**
```bash
pip install fastapi uvicorn stripe motor python-dotenv pydantic
```

**Frontend (Expo React Native SDK 54 + Web):**
```bash
npx expo install expo-web-browser expo-linking
npx expo install react-native-web react-dom @expo/metro-runtime
```

---

### 2. API Key Setup & Security Best Practices

1. **Get your Stripe Keys**: Go to the [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys). Toggle "Test mode" on.
2. **Environment Variables**: Never hardcode keys. Create a `.env` file in your FastAPI backend.
3. **Webhook Secret**: Crucial for security. You must verify that the webhook actually came from Stripe.

**Backend `.env` file:**
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
MONGODB_URI=mongodb://localhost:27017
FRONTEND_URL=exp://127.0.0.1:8081 # Use your production domain/scheme when deployed
```

---

### 3. Complete Code Examples

#### Backend: FastAPI + MongoDB (`main.py`)
This handles creating the session and listening to the webhook to update the database.

```python
import os
import stripe
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

app = FastAPI()

# MongoDB Setup
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.pesantren_db
registrations = db.registrations

class CheckoutRequest(BaseModel):
    registration_id: str

@app.post("/create-checkout-session")
async def create_checkout_session(req: CheckoutRequest):
    # Verify registration ID exists in MongoDB
    student = await registrations.find_one({"registration_id": req.registration_id})
    if not student:
        raise HTTPException(status_code=404, detail="Registration ID not found")
        
    if student.get("payment_status") == "paid":
        raise HTTPException(status_code=400, detail="Fee already paid")

    try:
        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'idr', # Indonesian Rupiah
                    'product_data': {
                        'name': 'Pondok Pesantren Registration Fee',
                        'description': f'Registration ID: {req.registration_id}',
                    },
                    'unit_amount': 50000000, # Rp 500,000 (amount in smallest currency unit)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{os.getenv('FRONTEND_URL')}/--/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/--/payment-cancel",
            client_reference_id=req.registration_id # Link session to the student
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        registration_id = session.get('client_reference_id')
        
        # Update MongoDB payment status safely
        if registration_id:
            await registrations.update_one(
                {"registration_id": registration_id},
                {"$set": {"payment_status": "paid", "stripe_session_id": session.get("id")}}
            )

    return {"status": "success"}
```

#### Frontend: Expo React Native + Web (`App.js`)
This screen asks for the Registration ID, calls the backend, and opens the Stripe URL.

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert, Platform } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import * as Linking from 'expo-linking';

export default function App() {
  const [registrationId, setRegistrationId] = useState('');
  const [loading, setLoading] = useState(false);

  // Handle deep linking return from Stripe WebBrowser
  useEffect(() => {
    const handleUrl = (event) => {
      const { path, queryParams } = Linking.parse(event.url);
      if (path === 'payment-success') {
        Alert.alert("Success", "Registration fee paid successfully!");
        WebBrowser.dismissBrowser(); // Close the in-app browser on mobile
      } else if (path === 'payment-cancel') {
        Alert.alert("Cancelled", "Payment was cancelled.");
        WebBrowser.dismissBrowser();
      }
    };

    const subscription = Linking.addEventListener('url', handleUrl);
    
    // Check initial URL (useful for React Native Web)
    Linking.getInitialURL().then((url) => {
      if (url) handleUrl({ url });
    });

    return () => subscription.remove();
  }, []);

  const handlePayment = async () => {
    if (!registrationId) return Alert.alert("Error", "Enter Registration ID");
    setLoading(true);

    try {
      // Replace with your FastAPI backend IP/URL
      const response = await fetch('http://192.168.1.xxx:8000/create-checkout-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ registration_id: registrationId }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to create session');
      }

      // Open the Stripe Checkout Session
      if (Platform.OS === 'web') {
        window.location.href = data.checkout_url; // Redirect directly on web
      } else {
        await WebBrowser.openBrowserAsync(data.checkout_url); // In-app browser on mobile
      }
    } catch (error) {
      Alert.alert("Error", error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Pondok Pesantren Registration</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter Registration ID (e.g., PP-2026-001)"
        value={registrationId}
        onChangeText={setRegistrationId}
      />
      <Button 
        title={loading ? "Processing..." : "Pay Registration Fee"} 
        onPress={handlePayment} 
        disabled={loading} 
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20, backgroundColor: '#fff' },
  title: { fontSize: 20, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 10, marginBottom: 20, borderRadius: 5 }
});
```

---

### 4. Testing Procedures

1. **Database Prep**: Manually insert a test student into MongoDB.
   ```json
   { "registration_id": "TEST-123", "payment_status": "unpaid" }
   ```
2. **Local Webhook Testing**:
   * Install the Stripe CLI: `stripe login`
   * Forward webhooks to your FastAPI local instance:
     `stripe listen --forward-to localhost:8000/webhook`
   * Copy the webhook signing secret output by the CLI and paste it into your `.env` as `STRIPE_WEBHOOK_SECRET`.
3. **App Testing (Mobile)**:
   * Run the Expo app (`npx expo start`).
   * Enter "TEST-123", tap Pay.
   * Enter Stripe's test card details (`4242 4242 4242 4242`, any future date, any CVC).
   * Upon completion, verify that the deep link successfully closes the browser and shows the "Success" alert.
4. **App Testing (Web)**:
   * Run `npx expo start --web`.
   * Complete payment, verify the page automatically redirects back to your React Native Web instance at `http://localhost:8081/payment-success`.
5. **Backend Verification**: Check MongoDB to ensure `payment_status` changed from `unpaid` to `paid`.

---

### 5. Common Pitfalls & How to Avoid Them

| Pitfall | How to Avoid |
| :--- | :--- |
| **Trusting the Frontend for Payment Status** | *Never* update MongoDB directly from the frontend's success URL. The user can simply visit the success URL without paying. Always rely on the backend `stripe-webhook` event (`checkout.session.completed`) to update the database. |
| **Mobile Deep Links Failing** | For Expo Go, deep links use the `exp://` scheme. In a standalone production app, you must configure `scheme` in `app.json` (e.g., `scheme: "pesantrenapp"`) and update your FastAPI `FRONTEND_URL` environment variable accordingly (e.g., `pesantrenapp://`). |
| **WebBrowser Not Closing on iOS/Android** | Ensure your `cancel_url` and `success_url` are properly formatted to match the app scheme. `Linking.addEventListener` must be mounted *before* the browser opens to catch the deep-link return and fire `WebBrowser.dismissBrowser()`. |
| **Incorrect Currency Units** | Stripe expects amounts in the *smallest currency unit*. For IDR (Indonesian Rupiah), this is the actual amount. `50000000` is 50,000,000 Rupiah *if* the currency uses decimals, but IDR doesn't. Wait—IDR in Stripe is actually a zero-decimal currency. So `unit_amount: 500000` = Rp 500,000. Double-check your specific Stripe currency logic! |
`````

---
## Sample 2: Google Drive CSV upload — FastAPI backend

| | |
|---|---|
| HTTP status | 200 |
| **Latency** | **32.0 s** |
| **Total cost (computed)** | **$0.04653** |
| Cost breakdown | input $0.00052 · output $0.032 · grounding fee $0.014 |
| Tokens (exact, from `usageMetadata`) | prompt 261 · output 2,667 · total 4,136 |
| Playbook length | 9,685 chars |
| Citation URLs surfaced in grounding metadata | 0 |

### Input — what our agent asked the tool (verbatim, same as the Perplexity trace)

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

### Exact API request sent to Gemini

```json
{
  "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key=GEMINI-REDACTED-MOCK-KEY",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "systemInstruction": {
      "parts": [
        {
          "text": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
        }
      ]
    },
    "contents": [
      {
        "role": "user",
        "parts": [
          {
            "text": "Create a detailed integration playbook for INTEGRATION: Google Drive API integration for Python FastAPI backend\nREQUIREMENTS:\n- Upload CSV files to a specific shared Google Drive folder\n- Auto-sync functionality for daily/weekly exports\n- Real-time sync of time entry data\n- User will provide OAuth tokens/credentials\n- Need to handle authentication and file upload to shared folder ID\nCONSTRAINTS:\n- Must work with FastAPI backend\n- Need to support automated scheduled uploads\n- Handle OAuth2 authentication flow in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
          }
        ]
      }
    ],
    "tools": [
      {
        "googleSearch": {}
      }
    ],
    "generationConfig": {
      "responseMimeType": "text/plain",
      "maxOutputTokens": 8192
    }
  }
}
```

### Exact output returned to our agent (verbatim, 9,685 chars)

No citation URLs were surfaced in grounding metadata for this call, so no `Sources:` list is appended — the playbook below is the complete tool output. Wrapped as `{"content": "<below>", "cost": 1.5}` (internal billing unit).

`````markdown
Here is a comprehensive, precise integration playbook for Google Drive API using a Python FastAPI backend, Expo React Native (App & Web) frontend, and MongoDB.

---

# 📖 Integration Playbook: Google Drive API (FastAPI + Expo + MongoDB)

## 1. API Key Setup & Security Best Practices
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and navigate to **APIs & Services > Library**. Enable the **Google Drive API**.
3. Go to **OAuth consent screen** and configure it (choose "External" or "Internal"). Add scope: `https://www.googleapis.com/auth/drive.file`.
4. Go to **Credentials > Create Credentials > OAuth client ID**.
   - Create a **Web Application** client for the FastAPI backend and Expo Web.
   - Create an **iOS/Android** client if using native Expo builds.
   - Add authorized redirect URIs (e.g., `https://auth.expo.io/@your-username/your-app-slug` for Expo Go, and your backend URI).
5. Download the `credentials.json` file.

**Security Best Practices:**
- Never hardcode the `client_secret` or tokens in frontend code.
- Always request offline access (`access_type='offline'`) to get a **Refresh Token** for automated backend syncs.
- Only request the `drive.file` scope (least privilege) which allows access only to files created by the app.

---

## 2. Installation Instructions

**Backend (Python/FastAPI):**
```bash
pip install fastapi uvicorn motor google-api-python-client google-auth-httplib2 google-auth-oauthlib pandas apscheduler
```

**Frontend (Expo React Native / Web):**
```bash
npx expo install expo-auth-session expo-crypto @react-native-async-storage/async-storage
```

---

## 3. Complete Code Examples

### A. Database (MongoDB via Motor Async) & Backend (FastAPI)

Create a file `main.py` for your FastAPI backend. This includes OAuth token storage, the real-time CSV upload to a shared folder, and the automated daily scheduler.

```python
import io
import pandas as pd
from fastapi import FastAPI, BackgroundTasks, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel

app = FastAPI()

# MongoDB Setup
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client.drive_integration
tokens_collection = db.user_tokens

SHARED_FOLDER_ID = "YOUR_SHARED_FOLDER_ID"

class TokenPayload(BaseModel):
    user_id: str
    token: str
    refresh_token: str
    token_uri: str
    client_id: str
    client_secret: str

@app.post("/api/save-tokens")
async def save_tokens(payload: TokenPayload):
    """Store OAuth tokens in MongoDB from the frontend"""
    await tokens_collection.update_one(
        {"user_id": payload.user_id},
        {"$set": payload.dict()},
        upsert=True
    )
    return {"status": "Tokens saved successfully"}

async def get_drive_service(user_id: str):
    user_data = await tokens_collection.find_one({"user_id": user_id})
    if not user_data:
        raise HTTPException(status_code=404, detail="User tokens not found")
    
    creds = Credentials(
        token=user_data['token'],
        refresh_token=user_data['refresh_token'],
        token_uri=user_data['token_uri'],
        client_id=user_data['client_id'],
        client_secret=user_data['client_secret']
    )
    return build('drive', 'v3', credentials=creds)

@app.post("/api/sync-time-entries/{user_id}")
async def sync_time_entries(user_id: str, background_tasks: BackgroundTasks):
    """Real-time sync of time entry data triggered by frontend"""
    background_tasks.add_task(upload_csv_to_drive, user_id)
    return {"status": "Sync initiated"}

def upload_csv_to_drive(user_id: str):
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    service = loop.run_until_complete(get_drive_service(user_id))
    
    # 1. Generate CSV Data
    df = pd.DataFrame([{"date": "2026-06-10", "hours": 8, "project": "Playbook"}])
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    # 2. Upload to Google Drive (Supports Shared Drives)
    file_metadata = {
        'name': 'time_entries_export.csv',
        'parents': [SHARED_FOLDER_ID]
    }
    media = MediaIoBaseUpload(io.BytesIO(csv_buffer.getvalue().encode('utf-8')),
                              mimetype='text/csv',
                              resumable=True)
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True # CRITICAL for Shared Folders
    ).execute()
    print(f"File uploaded with ID: {file.get('id')}")

# Auto-Sync Scheduler (Daily)
scheduler = BackgroundScheduler()
@scheduler.scheduled_job('cron', hour=23, minute=59)
def scheduled_daily_export():
    import asyncio
    # In production, loop through all users who need auto-sync
    print("Running scheduled daily CSV export...")

scheduler.start()
```

### B. Frontend (Expo React Native & Web)

Create a component `DriveSync.tsx` in your Expo app to handle Google OAuth and trigger the backend.

```javascript
import React, { useEffect } from 'react';
import { View, Button, Text } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import * as Google from 'expo-auth-session/providers/google';

WebBrowser.maybeCompleteAuthSession();

export default function DriveSync() {
  const [request, response, promptAsync] = Google.useAuthRequest({
    webClientId: 'YOUR_WEB_CLIENT_ID.apps.googleusercontent.com',
    iosClientId: 'YOUR_IOS_CLIENT_ID.apps.googleusercontent.com',
    androidClientId: 'YOUR_ANDROID_CLIENT_ID.apps.googleusercontent.com',
    scopes: ['https://www.googleapis.com/auth/drive.file'],
    // Request offline access to get refresh token
    extraParams: { access_type: 'offline', prompt: 'consent' },
  });

  useEffect(() => {
    if (response?.type === 'success') {
      const { authentication } = response;
      sendTokensToBackend(authentication);
    }
  }, [response]);

  const sendTokensToBackend = async (auth) => {
    await fetch('http://YOUR_BACKEND_IP:8000/api/save-tokens', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: 'user_123',
        token: auth.accessToken,
        refresh_token: auth.refreshToken, // Only returned on first consent
        token_uri: 'https://oauth2.googleapis.com/token',
        client_id: 'YOUR_WEB_CLIENT_ID.apps.googleusercontent.com',
        client_secret: 'YOUR_CLIENT_SECRET' // Security note: Ideally, exchange Auth Code on Backend instead of sending secret from frontend.
      })
    });
  };

  const triggerRealTimeSync = async () => {
    await fetch('http://YOUR_BACKEND_IP:8000/api/sync-time-entries/user_123', {
      method: 'POST'
    });
    alert('Sync Triggered!');
  };

  return (
    <View style={{ padding: 20 }}>
      <Button 
        disabled={!request}
        title="1. Connect Google Drive" 
        onPress={() => promptAsync()} 
      />
      <View style={{ marginVertical: 10 }} />
      <Button 
        title="2. Trigger Real-Time Sync" 
        onPress={triggerRealTimeSync} 
      />
    </View>
  );
}
```

*Note: For production, to keep `client_secret` strictly on the backend, use `responseType: "code"` in Expo, send the Authorization Code to FastAPI, and have FastAPI exchange it for tokens using `google-auth-oauthlib`.*

---

## 4. Testing Procedures

1. **OAuth Flow Verification**: 
   - Click "Connect Google Drive" on Web, iOS, and Android. 
   - Verify the consent screen asks for Google Drive file permissions.
   - Check MongoDB (`db.user_tokens.find()`) to ensure the `refresh_token` and `token` are saved.
2. **Real-time Sync Test**:
   - Trigger the sync button. 
   - Check your FastAPI logs for `File uploaded with ID: ...`.
   - Open the target Shared Google Drive folder and verify `time_entries_export.csv` appears with correct data.
3. **Automated Scheduler Test**:
   - Temporarily alter the `BackgroundScheduler` cron to run every minute (`scheduler.add_job(..., 'interval', minutes=1)`).
   - Verify the CSV is successfully uploaded to the shared drive without any user interaction.
4. **Token Expiry Test**:
   - Manually revoke the app's access in Google Account Settings.
   - Trigger a sync to ensure the backend gracefully handles the `401 Unauthorized` exception.

---

## 5. Common Pitfalls & How to Avoid Them

| Pitfall | Solution |
| :--- | :--- |
| **Missing Refresh Tokens** | Google only sends a `refresh_token` on the *first* authorization. If missing, pass `prompt: 'consent'` and `access_type: 'offline'` in your OAuth request. |
| **Shared Drive Upload Fails** | Standard Drive API requests fail for Shared Drives. You **must** include `supportsAllDrives=True` in your `files().create()` execution payload. |
| **Broad Scopes leading to App Rejection** | Avoid `https://www.googleapis.com/auth/drive` (full access). Use `drive.file`. Google's OAuth verification process will reject your app if you use the full access scope without a rigorous security audit. |
| **Files Uploaded as Binary instead of Sheets** | If you want the CSV to be automatically converted to a Google Sheet, add `mimeType: 'application/vnd.google-apps.spreadsheet'` to `file_metadata`. |
| **Cron Jobs Blocking FastAPI** | Use `BackgroundScheduler` (from `apscheduler.schedulers.background`) or an async scheduler to ensure your scheduled daily exports do not block the ASGI event loop of your FastAPI backend. |
`````

---
## Sample 3: Custom JWT auth — mobile (Expo React Native)

| | |
|---|---|
| HTTP status | 200 |
| **Latency** | **33.0 s** |
| **Total cost (computed)** | **$0.05147** |
| Cost breakdown | input $0.00053 · output $0.03694 · grounding fee $0.014 |
| Tokens (exact, from `usageMetadata`) | prompt 267 · output 3,078 · total 4,343 |
| Playbook length | 10,700 chars |
| Citation URLs surfaced in grounding metadata | 0 |

### Input — what our agent asked the tool (verbatim, same as the Perplexity trace)

```
INTEGRATION: Custom JWT-based email/password authentication for an Expo React Native (SDK 54) mobile app with FastAPI + MongoDB backend. Need: register, login, password hashing (bcrypt), JWT token issuance/validation, secure token persistence on mobile (expo-secure-store).

CONSTRAINTS: 
- Expo SDK 54 React Native mobile app
- FastAPI backend with /api prefix on all routes
- MongoDB for user storage
- Token storage via expo-secure-store
```

### Exact API request sent to Gemini

```json
{
  "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key=GEMINI-REDACTED-MOCK-KEY",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "systemInstruction": {
      "parts": [
        {
          "text": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
        }
      ]
    },
    "contents": [
      {
        "role": "user",
        "parts": [
          {
            "text": "Create a detailed integration playbook for INTEGRATION: Custom JWT-based email/password authentication for an Expo React Native (SDK 54) mobile app with FastAPI + MongoDB backend. Need: register, login, password hashing (bcrypt), JWT token issuance/validation, secure token persistence on mobile (expo-secure-store).\n\nCONSTRAINTS: \n- Expo SDK 54 React Native mobile app\n- FastAPI backend with /api prefix on all routes\n- MongoDB for user storage\n- Token storage via expo-secure-store in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
          }
        ]
      }
    ],
    "tools": [
      {
        "googleSearch": {}
      }
    ],
    "generationConfig": {
      "responseMimeType": "text/plain",
      "maxOutputTokens": 8192
    }
  }
}
```

### Exact output returned to our agent (verbatim, 10,700 chars)

No citation URLs were surfaced in grounding metadata for this call, so no `Sources:` list is appended — the playbook below is the complete tool output. Wrapped as `{"content": "<below>", "cost": 1.5}` (internal billing unit).

`````markdown
Here is the complete integration playbook for setting up a custom JWT-based authentication system using Expo React Native (SDK 54), FastAPI, and MongoDB.

---

## 1. Installation Instructions

### Backend (FastAPI + MongoDB)
Initialize your Python environment and install the required dependencies.
```bash
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn motor passlib[bcrypt] pyjwt pydantic-settings python-dotenv
```

### Frontend (Expo SDK 54)
Create a new Expo project and install dependencies.
```bash
npx create-expo-app@latest frontend
cd frontend
npx expo install expo-secure-store axios
```

---

## 2. API Key Setup & Security Best Practices

1. **Environment Variables**: Never hardcode secrets. Create a `.env` file in your backend directory:
   ```env
   MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   JWT_SECRET_KEY=generate_a_random_secure_string_here_like_openssl_rand_hex_32
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_MINUTES=1440
   ```
2. **Security Best Practices**:
   * **Password Hashing:** Always use `bcrypt` with a strong work factor (handled via `passlib`).
   * **CORS:** Ensure CORS is strictly configured in production, only allowing your app/web domains.
   * **Token Storage:** Use `expo-secure-store` for iOS/Android (uses Keychain/Keystore). Use `localStorage` on Web (since `expo-secure-store` does not support Web).

---

## 3. Complete Code Examples

### Backend: FastAPI + MongoDB

**`main.py`**
```python
import os
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
security = HTTPBearer()

# CORS configuration (required for React Native Web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database & Config
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 1440))

client = AsyncIOMotorClient(MONGO_URI)
db = client.auth_db
users_collection = db.users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Utils
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await users_collection.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return {"email": user["email"], "id": str(user["_id"])}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Endpoints
@app.post("/api/register", response_model=UserResponse)
async def register(user: UserCreate):
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_dict = {"email": user.email, "hashed_password": hashed_password}
    result = await users_collection.insert_one(user_dict)
    
    return {"email": user.email, "id": str(result.inserted_id)}

@app.post("/api/login", response_model=Token)
async def login(user: UserCreate):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": db_user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
```

Run Backend: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

---

### Frontend: Expo React Native (+ Web Support)

**`utils/storage.js`**
Handle the constraint where `expo-secure-store` doesn't support web.
```javascript
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const TOKEN_KEY = 'jwt_token';

export const saveToken = async (token) => {
  if (Platform.OS === 'web') {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    await SecureStore.setItemAsync(TOKEN_KEY, token);
  }
};

export const getToken = async () => {
  if (Platform.OS === 'web') {
    return localStorage.getItem(TOKEN_KEY);
  } else {
    return await SecureStore.getItemAsync(TOKEN_KEY);
  }
};

export const deleteToken = async () => {
  if (Platform.OS === 'web') {
    localStorage.removeItem(TOKEN_KEY);
  } else {
    await SecureStore.deleteItemAsync(TOKEN_KEY);
  }
};
```

**`api/axiosConfig.js`**
```javascript
import axios from 'axios';
import { getToken } from '../utils/storage';
import { Platform } from 'react-native';

// Important: Use your local IP for mobile (e.g., 192.168.1.x), localhost for web
const BASE_URL = Platform.OS === 'web' ? 'http://localhost:8000/api' : 'http://192.168.1.100:8000/api'; 

const api = axios.create({
  baseURL: BASE_URL,
});

api.interceptors.request.use(async (config) => {
  const token = await getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

**`App.js`** (Simplified Auth Flow)
```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import api from './api/axiosConfig';
import { saveToken, getToken, deleteToken } from './utils/storage';

export default function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [user, setUser] = useState(null);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = await getToken();
    if (token) {
      try {
        const res = await api.get('/me');
        setUser(res.data);
      } catch (e) {
        deleteToken();
      }
    }
  };

  const handleRegister = async () => {
    try {
      await api.post('/register', { email, password });
      Alert.alert('Success', 'Registered! Now please login.');
    } catch (e) {
      Alert.alert('Error', e.response?.data?.detail || 'Registration failed');
    }
  };

  const handleLogin = async () => {
    try {
      const res = await api.post('/login', { email, password });
      await saveToken(res.data.access_token);
      checkAuth();
    } catch (e) {
      Alert.alert('Error', e.response?.data?.detail || 'Login failed');
    }
  };

  const handleLogout = async () => {
    await deleteToken();
    setUser(null);
  };

  if (user) {
    return (
      <View style={styles.container}>
        <Text>Welcome, {user.email}</Text>
        <Button title="Logout" onPress={handleLogout} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} style={styles.input} autoCapitalize="none" />
      <TextInput placeholder="Password" value={password} onChangeText={setPassword} style={styles.input} secureTextEntry />
      <Button title="Login" onPress={handleLogin} />
      <Button title="Register" onPress={handleRegister} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20 },
  input: { borderWidth: 1, padding: 10, marginBottom: 10, borderRadius: 5 }
});
```

---

## 4. Testing Procedures

1. **Test Backend Independently**:
   * Navigate to `http://localhost:8000/docs` (FastAPI auto-generated Swagger UI).
   * Try creating a user using the `/api/register` endpoint.
   * Log in via `/api/login` and copy the generated token.
   * Click the "Authorize" button at the top, enter the token, and test `/api/me`.
2. **Test React Native Web**:
   * Run `npx expo start -w` in the frontend. 
   * Verify token is persisted in DevTools > Application > Local Storage.
3. **Test Mobile (iOS/Android)**:
   * **Crucial:** Update `BASE_URL` in `axiosConfig.js` to your computer's local IP network address (e.g., `192.168.1.x`). Mobile emulators/devices cannot reach `localhost:8000`.
   * Run `npx expo start` and test on an emulator. Close the app completely and reopen it to ensure `expo-secure-store` correctly retrieves the token.

---

## 5. Common Pitfalls & How to Avoid Them

| Pitfall | How to Avoid |
| :--- | :--- |
| **`Network Error` on Android/iOS Emulator** | Emulators resolve `localhost` to themselves, not your development machine. Use your dev machine's local IP (e.g., `192.168.x.x`) in the Axios `BASE_URL` for mobile. |
| **`expo-secure-store` crashes on Web** | Expo Secure Store relies on native modules (Keychain/Keystore) unavailable in browsers. Always use `Platform.OS === 'web'` to fallback to `localStorage`. |
| **CORS Errors on Web App** | React Native Web makes standard browser preflight requests. Ensure your FastAPI app has `CORSMiddleware` explicitly configured to allow the web app's origin (or `"*"` for development). |
| **Async Storage Race Conditions** | `getToken` is asynchronous. Do not render protected views until the auth check resolves (add an `isLoading` state in production). |
`````

---
## Sample 4: JWT + mocked OTP + roles — mobile (Expo React Native)

| | |
|---|---|
| HTTP status | 200 |
| **Latency** | **36.1 s** |
| **Total cost (computed)** | **$0.0554** |
| Cost breakdown | input $0.00056 · output $0.04084 · grounding fee $0.014 |
| Tokens (exact, from `usageMetadata`) | prompt 280 · output 3,403 · total 4,846 |
| Playbook length | 11,856 chars |
| Citation URLs surfaced in grounding metadata | 0 |

### Input — what our agent asked the tool (verbatim, same as the Perplexity trace)

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

### Exact API request sent to Gemini

```json
{
  "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key=GEMINI-REDACTED-MOCK-KEY",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "systemInstruction": {
      "parts": [
        {
          "text": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
        }
      ]
    },
    "contents": [
      {
        "role": "user",
        "parts": [
          {
            "text": "Create a detailed integration playbook for INTEGRATION: JWT-based authentication for Expo React Native app with FastAPI backend. Need:\n1. Email + password registration & login (working JWT auth)\n2. Phone OTP mocked login (accept any 6-digit OTP for now, just generate JWT)\n3. Role-based auth (customer vs admin role)\n4. Token storage via expo-secure-store on client\n\nCONSTRAINTS: \n- Backend FastAPI with MongoDB (Motor)\n- Frontend Expo Router with React Native\n- Use bcrypt for password hashing\n- JWT tokens for session in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
          }
        ]
      }
    ],
    "tools": [
      {
        "googleSearch": {}
      }
    ],
    "generationConfig": {
      "responseMimeType": "text/plain",
      "maxOutputTokens": 8192
    }
  }
}
```

### Exact output returned to our agent (verbatim, 11,856 chars)

No citation URLs were surfaced in grounding metadata for this call, so no `Sources:` list is appended — the playbook below is the complete tool output. Wrapped as `{"content": "<below>", "cost": 1.5}` (internal billing unit).

`````markdown
Here is a complete, step-by-step integration playbook for setting up a JWT-based authentication system using FastAPI, MongoDB (Motor), and Expo React Native (with Web support).

---

# 📘 Integration Playbook: JWT Auth (FastAPI + MongoDB + Expo)

## 1. Installation Instructions

### Backend (FastAPI + MongoDB)
Initialize a Python virtual environment and install dependencies:
```bash
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn motor passlib[bcrypt] python-jose[cryptography] pydantic pydantic-settings python-dotenv
```

### Frontend (Expo React Native + Web)
Initialize your Expo Router app and install libraries:
```bash
npx create-expo-app@latest my-app
cd my-app
npx expo install expo-secure-store axios jwt-decode react-native-web react-dom @expo/metro-runtime
```

---

## 2. Security Setup & Environment Variables

### Generating Secrets
You need a secure random string for your JWT signature. Generate one in your terminal:
```bash
openssl rand -hex 32
```

### Backend `.env`
Create a `.env` file in the `backend` directory:
```env
MONGO_URI=mongodb://localhost:27017
JWT_SECRET=your_generated_hex_string_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### Security Best Practices
1. **Never commit `.env` files** to version control (add to `.gitignore`).
2. **Use HTTPS** in production to prevent Man-in-the-Middle (MITM) attacks.
3. **Short-lived tokens**: In production, use short-lived access tokens (15 mins) and implement refresh tokens. 

---

## 3. Backend Implementation (FastAPI + Motor)

Create a file named `main.py` in your backend folder. This includes DB setup, JWT/bcrypt logic, CORS (crucial for React Native Web), and the requested endpoints.

```python
import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

load_dotenv()

# --- Configurations ---
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- Database setup ---
client = AsyncIOMotorClient(MONGO_URI)
db = client.auth_db
users_collection = db.users

# --- Security Utilities ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/email")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Pydantic Models ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "customer" # "customer" or "admin"

class EmailLogin(BaseModel):
    email: EmailStr
    password: str

class OTPLogin(BaseModel):
    phone: str
    otp: str

# --- Dependencies ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def require_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user

# --- Routes ---
@app.post("/register")
async def register(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])
    await users_collection.insert_one(user_dict)
    return {"message": "User created successfully"}

@app.post("/login/email")
async def login_email(user: EmailLogin):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": db_user["email"], "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login/otp")
async def login_otp(data: OTPLogin):
    # Mocked OTP Logic: Accept any 6 digit OTP
    if len(data.otp) != 6 or not data.otp.isdigit():
        raise HTTPException(status_code=400, detail="Invalid OTP. Must be 6 digits.")
    
    # Create or fetch user based on phone
    db_user = await users_collection.find_one({"phone": data.phone})
    if not db_user:
        new_user = {"phone": data.phone, "email": f"{data.phone}@mock.com", "role": "customer"}
        await users_collection.insert_one(new_user)
        role = "customer"
        email = new_user["email"]
    else:
        role = db_user.get("role", "customer")
        email = db_user.get("email")

    token = create_access_token(data={"sub": email, "role": role})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/admin-only")
async def admin_dashboard(user: dict = Depends(require_admin)):
    return {"message": "Welcome Admin!", "user": user}
```
*Run it via: `uvicorn main:app --reload`*

---

## 4. Frontend Implementation (Expo React Native + Web)

### Universal Secure Store Wrapper
`expo-secure-store` does not work natively on the Web. You must create a wrapper to fallback to `localStorage` when running on React Native Web.

Create `utils/storage.ts`:
```typescript
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const TOKEN_KEY = 'jwt_token';

export const saveToken = async (token: string) => {
  if (Platform.OS === 'web') {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    await SecureStore.setItemAsync(TOKEN_KEY, token);
  }
};

export const getToken = async () => {
  if (Platform.OS === 'web') {
    return localStorage.getItem(TOKEN_KEY);
  } else {
    return await SecureStore.getItemAsync(TOKEN_KEY);
  }
};

export const deleteToken = async () => {
  if (Platform.OS === 'web') {
    localStorage.removeItem(TOKEN_KEY);
  } else {
    await SecureStore.deleteItemAsync(TOKEN_KEY);
  }
};
```

### Axios Interceptor Setup
Create `utils/api.ts` to automatically attach the JWT to all requests.
```typescript
import axios from 'axios';
import { getToken } from './storage';

// Use your computer's local IP for physical devices, or localhost for Web/iOS Simulator
const API_URL = 'http://localhost:8000'; 

export const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use(async (config) => {
  const token = await getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Login Screen Example
Create `app/index.tsx` (Expo Router). This includes both Email and Mocked OTP approaches.

```tsx
import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, Platform } from 'react-native';
import { api } from '../utils/api';
import { saveToken } from '../utils/storage';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');

  const handleEmailLogin = async () => {
    try {
      const res = await api.post('/login/email', { email, password });
      await saveToken(res.data.access_token);
      Alert.alert('Success', 'Logged in via Email!');
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Login failed');
    }
  };

  const handleOtpLogin = async () => {
    try {
      const res = await api.post('/login/otp', { phone, otp });
      await saveToken(res.data.access_token);
      Alert.alert('Success', 'Logged in via OTP!');
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Login failed');
    }
  };

  const testAdminRoute = async () => {
    try {
      const res = await api.get('/admin-only');
      Alert.alert('Success', res.data.message);
    } catch (err: any) {
      Alert.alert('Forbidden', err.response?.data?.detail || 'Access Denied');
    }
  };

  return (
    <View style={{ padding: 20, flex: 1, justifyContent: 'center' }}>
      <Text style={{ fontSize: 20, fontWeight: 'bold' }}>Email Login</Text>
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} style={styles.input} autoCapitalize="none" />
      <TextInput placeholder="Password" value={password} onChangeText={setPassword} style={styles.input} secureTextEntry />
      <Button title="Login with Email" onPress={handleEmailLogin} />

      <Text style={{ fontSize: 20, fontWeight: 'bold', marginTop: 30 }}>OTP Login</Text>
      <TextInput placeholder="Phone" value={phone} onChangeText={setPhone} style={styles.input} />
      <TextInput placeholder="6-digit OTP" value={otp} onChangeText={setOtp} style={styles.input} keyboardType="numeric" />
      <Button title="Login with OTP" onPress={handleOtpLogin} />

      <View style={{ marginTop: 40 }}>
        <Button title="Test Admin Route" color="red" onPress={testAdminRoute} />
      </View>
    </View>
  );
}

const styles = {
  input: { borderWidth: 1, borderColor: '#ccc', padding: 10, marginVertical: 10, borderRadius: 5 }
};
```

---

## 5. Testing Procedures

1. **Test Registration (Backend):**
   * Open Postman or execute a cURL request to POST `http://localhost:8000/register`.
   * Body: `{"email": "admin@test.com", "password": "password123", "role": "admin"}`
   * Expect: `200 OK` (User Created).

2. **Test Frontend Flow:**
   * Start frontend: `npx expo start` -> Press `w` for Web or `i` for iOS Simulator.
   * Enter the credentials created above and click "Login with Email".
   * Ensure the "Success" alert appears (token stored successfully).
   * Click "Test Admin Route". Expect "Welcome Admin!".

3. **Test OTP Flow:**
   * Enter a phone number (e.g., `1234567890`) and an OTP (e.g., `111111`).
   * Click "Login with OTP".
   * Click "Test Admin Route". Expect "Forbidden" (because OTP users default to "customer" role).

---

## 6. Common Pitfalls & How to Avoid Them

| Pitfall | Solution |
| :--- | :--- |
| **Network Error on Mobile Device** | Expo mobile apps cannot route to `localhost`. Change `API_URL` in `utils/api.ts` to your machine's local IP address (e.g., `http://192.168.1.5:8000`). |
| **`expo-secure-store` crashing on Web** | `SecureStore` doesn't support Web out-of-the-box. **Always** use the `Platform.OS === 'web'` storage wrapper provided in Step 4. |
| **CORS Errors on Web** | Web browsers enforce CORS. Ensure `CORSMiddleware` is properly added in `main.py` allowing the web origin (or `["*"]` for dev). |
| **MongoDB Async Operations Hanging** | You are using the asynchronous `motor` driver. Forgetting the `await` keyword before `users_collection.find_one()` will cause the request to hang indefinitely. |
`````

---
## Sample 5: PayPal checkout — web (FastAPI + React) store

| | |
|---|---|
| HTTP status | 200 |
| **Latency** | **27.4 s** |
| **Total cost (computed)** | **$0.04279** |
| Cost breakdown | input $0.0004 · output $0.02839 · grounding fee $0.014 |
| Tokens (exact, from `usageMetadata`) | prompt 198 · output 2,366 · total 3,583 |
| Playbook length | 8,642 chars |
| Citation URLs surfaced in grounding metadata | 0 |

### Input — what our agent asked the tool (verbatim, same as the Perplexity trace)

```
INTEGRATION: PayPal payment processing for e-commerce checkout
CONSTRAINTS: Need to integrate PayPal checkout button and payment processing for a dropshipping store
```

### Exact API request sent to Gemini

```json
{
  "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key=GEMINI-REDACTED-MOCK-KEY",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "systemInstruction": {
      "parts": [
        {
          "text": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: reactjs frontend with shadcn, fastapi backend, mongodb database\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
        }
      ]
    },
    "contents": [
      {
        "role": "user",
        "parts": [
          {
            "text": "Create a detailed integration playbook for INTEGRATION: PayPal payment processing for e-commerce checkout\nCONSTRAINTS: Need to integrate PayPal checkout button and payment processing for a dropshipping store in reactjs frontend with shadcn, fastapi backend, mongodb database application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
          }
        ]
      }
    ],
    "tools": [
      {
        "googleSearch": {}
      }
    ],
    "generationConfig": {
      "responseMimeType": "text/plain",
      "maxOutputTokens": 8192
    }
  }
}
```

### Exact output returned to our agent (verbatim, 8,642 chars)

No citation URLs were surfaced in grounding metadata for this call, so no `Sources:` list is appended — the playbook below is the complete tool output. Wrapped as `{"content": "<below>", "cost": 1.5}` (internal billing unit).

`````markdown
# PayPal E-commerce Integration Playbook

This guide details how to integrate PayPal Checkout securely for a dropshipping platform using ReactJS (shadcn/ui), FastAPI, and MongoDB. 

## 1. API Key Setup & Security Best Practices

**How to get PayPal API Keys:**
1. Log in to the [PayPal Developer Dashboard](https://developer.paypal.com/).
2. Go to **Apps & Credentials** and toggle the environment to **Sandbox** (for testing) or **Live** (for production).
3. Click **Create App**, name your app (e.g., "Dropship Checkout"), and click **Create App**.
4. Note your **Client ID** and **Secret**.

**Security Best Practices:**
*   **Never expose your `Secret`** to the frontend. It should only exist in your backend `.env` file.
*   **Always calculate/validate prices on the backend.** Never trust frontend cart totals to prevent malicious users from changing the payment amount.
*   **Verify Order Capture:** Fulfill orders only after successfully capturing the payment on the server.

---

## 2. Installation Instructions

**Backend (FastAPI):**
```bash
pip install fastapi uvicorn motor httpx python-dotenv pydantic
```

**Frontend (ReactJS):**
```bash
# Install PayPal JS SDK and shadcn dependencies
npm install @paypal/react-paypal-js lucide-react
# Assuming shadcn is initialized, add a generic card component for the UI
npx shadcn-ui@latest add card
```

---

## 3. Complete Code Examples

### Backend: FastAPI + MongoDB
Create a `.env` file for your backend:
```env
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET=your_paypal_secret
PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com
MONGO_URI=mongodb://localhost:27017
```

**`main.py`**
```python
import os
import base64
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Setup
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.dropshipping_store
orders_collection = db.orders

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL")

async def get_paypal_access_token():
    auth = base64.b64encode(f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}".encode()).decode()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            data={"grant_type": "client_credentials"},
            headers={"Authorization": f"Basic {auth}"}
        )
        response.raise_for_status()
        return response.json()["access_token"]

class CartItem(BaseModel):
    product_id: str
    quantity: int

@app.post("/api/orders")
async def create_order(cart: list[CartItem]):
    # In a real app, calculate this total by looking up product_ids in MongoDB!
    total_amount = "50.00" 

    token = await get_paypal_access_token()
    
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {"currency_code": "USD", "value": total_amount}
        }]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        if response.status_code != 201:
            raise HTTPException(status_code=400, detail="Failed to create order")
        return response.json()

@app.post("/api/orders/{order_id}/capture")
async def capture_order(order_id: str):
    token = await get_paypal_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        data = response.json()
        
        if response.status_code == 201 and data["status"] == "COMPLETED":
            # Save order to MongoDB
            await orders_collection.insert_one({
                "paypal_order_id": order_id,
                "status": "PAID",
                "payer": data["payer"],
                "purchase_units": data["purchase_units"]
            })
            return {"status": "success", "data": data}
        
        raise HTTPException(status_code=400, detail="Payment capture failed")
```

### Frontend: ReactJS + shadcn

Create a `.env` file for your React app:
```env
REACT_APP_PAYPAL_CLIENT_ID=your_paypal_client_id
```

**`Checkout.jsx`**
```jsx
import React, { useState } from "react";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function Checkout() {
  const [error, setError] = useState(null);

  const createOrder = async () => {
    const response = await fetch("http://localhost:8000/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify([{ product_id: "dropship_item_1", quantity: 1 }])
    });
    
    const orderData = await response.json();
    if (orderData.id) {
      return orderData.id;
    } else {
      setError("Failed to initialize transaction.");
      throw new Error("Order creation failed");
    }
  };

  const onApprove = async (data) => {
    const response = await fetch(`http://localhost:8000/api/orders/${data.orderID}/capture`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    
    const captureData = await response.json();
    if (captureData.status === "success") {
      alert("Payment successful! Your order is being processed.");
    } else {
      setError("Payment capture failed. Please contact support.");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-50">
      <Card className="w-[400px]">
        <CardHeader>
          <CardTitle>Secure Checkout</CardTitle>
        </CardHeader>
        <CardContent>
          {error && <p className="text-red-500 mb-4">{error}</p>}
          <PayPalScriptProvider options={{ "client-id": process.env.REACT_APP_PAYPAL_CLIENT_ID, currency: "USD" }}>
            <PayPalButtons 
              createOrder={createOrder} 
              onApprove={onApprove} 
              style={{ layout: "vertical" }} 
            />
          </PayPalScriptProvider>
        </CardContent>
      </Card>
    </div>
  );
}
```

---

## 4. Testing Procedures

1. **Setup Test Accounts:**
   * In the PayPal Developer Dashboard, navigate to **Testing Tools -> Sandbox Accounts**.
   * You will see default Business (Merchant) and Personal (Buyer) accounts. Note the email and system-generated password for the Personal account.
2. **Run the Services:**
   * Start MongoDB locally.
   * Start FastAPI: `uvicorn main:app --reload --port 8000`
   * Start React App: `npm start`
3. **Execute a Test Transaction:**
   * Open your checkout page.
   * Click the PayPal button and log in using the Sandbox **Personal** account credentials.
   * Complete the purchase.
4. **Verification:**
   * Check your terminal to ensure the backend logged a `201` status.
   * Connect to your MongoDB instance (`mongosh`) and verify the document was saved in `dropshipping_store.orders` with `status: "PAID"`.

---

## 5. Common Pitfalls and How to Avoid Them

| Pitfall | How to Avoid |
| :--- | :--- |
| **Trusting Frontend Pricing** | Never pass `amount` directly from React. Pass only `product_id` and `quantity`. Fetch the actual prices from MongoDB within the FastAPI `create_order` route to construct the PayPal payload. |
| **Silent Failures on Capture** | The user might close the window before `onApprove` completes. Use **PayPal Webhooks** (e.g., `CHECKOUT.ORDER.APPROVED`) as a fallback in FastAPI to ensure you record the payment even if the frontend disconnects. |
| **Currency Mismatches** | Ensure the currency specified in your `<PayPalScriptProvider>` (e.g., "USD") matches exactly what your FastAPI backend sends in the `purchase_units` payload. |
| **Forgetting to Switch to Live** | When deploying, change both `PAYPAL_BASE_URL` to `https://api-m.paypal.com` and use your Live Client ID and Secret in your production environment variables. |
`````

---
## Notes

- The API key in all request dumps is mocked (`GEMINI-REDACTED-MOCK-KEY`); everything else is byte-exact.
- Token counts are exact (from Gemini's `usageMetadata`); dollar figures are computed from published list rates as described in section 1.
