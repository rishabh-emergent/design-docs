# How we call Perplexity today — exact production trace

**Purpose:** Reference for the Exa team showing exactly how our integration-playbook tool calls Perplexity in production — request construction, settings, prompts — with 5 fully-inlined real samples (measured latency + cost + the complete output our agent receives).

**Method:** We took 5 real production tool inputs (from jobs in the last few hours that hit the Perplexity research path) and replayed them through the byte-identical request construction our production service uses. Every number is measured, not estimated. The prompt templates below are verbatim copies of our production code; the inputs are verbatim agent tool calls from production.

---

## 1. Where the Perplexity call sits

```
Coding agent (Claude Opus 4.7)
    |  calls tool: integration_playbook_expert_v2
    |  input: free-text "INTEGRATION: ... CONSTRAINTS: ..." block
    v
Our tool server
    |  1) internal knowledge-base check: an LLM classifier matches the query
    |     against our DB of pre-verified playbooks
    |
    |- match found  -> return cached verified playbook (NO Perplexity call)
    |
    \- no match     -> the check also returns the job's tech_stack[]
           |
           v
       POST https://api.perplexity.ai/chat/completions   <- THE CALL DOCUMENTED HERE
```

- Volume on this research path: **~16.3k calls measured over a 7-day production window ≈ ~70k calls/month**.

## 2. The exact API call

```
POST https://api.perplexity.ai/chat/completions
Authorization: Bearer pplx-REDACTED-MOCK-KEY
Content-Type: application/json
```

```json
{
  "model": "sonar-deep-research",
  "messages": [
    { "role": "system", "content": "<SYSTEM PROMPT - see section 3>" },
    { "role": "user",   "content": "<USER PROMPT - see section 3>" }
  ]
}
```

### Settings — complete list

| Setting | Value | Notes |
|---|---|---|
| Model | `sonar-deep-research` | hardcoded |
| `temperature` | **not sent** | Perplexity default applies |
| `max_tokens` | **not sent** | Perplexity default applies |
| `top_p` / `top_k` | **not sent** | |
| `stream` | **not sent** (non-streaming) | |
| `search_domain_filter` / `search_recency_filter` | **not sent** | |
| `web_search_options` | **not sent** | |
| HTTP timeout | 25 minutes | |
| Retries | **none** — single attempt | |

The body contains **only** `model` and `messages` — everything else is Perplexity's default behavior.

## 3. Prompt construction

Two inputs vary per call:

- `{query}` — the agent's tool input, embedded **whole and unmodified** (the entire `INTEGRATION: ... CONSTRAINTS: ...` block, newlines included)
- `{stack}` — comma-joined `tech_stack` of the job's project template

### System prompt (verbatim template)

```
You are Integration_Playbook_Expert, responsible for creating detailed integration guides.
Research and provide a complete integration playbook for the requested technology that includes:

1. Installation instructions
2. API key setup & security best practices
3. Complete code examples for this tech stack: {stack}
4. Testing procedures
5. Common pitfalls and how to avoid them

Format your response in a structured, step-by-step guide that a developer can follow.
Include all necessary code samples.
If the integration involves API keys, include instructions on where to get them.
```

### User prompt (verbatim template)

```
Create a detailed integration playbook for {query} in {stack} application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise.
```

Because `{query}` is a multi-line block, the assembled user prompt inlines the full agent message mid-sentence (see each sample's exact request below).

### `tech_stack` values per project template (exact)

| Project template | `tech_stack` |
|---|---|
| Web (main) | `["reactjs frontend with shadcn", "fastapi backend", "mongodb database"]` |
| Mobile | `["expo react native", "mongodb database", "react native web"]` |
| Next.js | `["nextjs fullstack", "mongodb database", "shadcn ui"]` |
| Web (legacy) | `["reactjs frontend", "fastapi backend", "mongodb database"]` |
| Fallback | `["Python", "FastAPI"]` |

## 4. What we do with the response

1. Take `choices[0].message.content` as-is (markdown with inline numeric citation markers like `[4]`, `[13]` that index into the `citations` array).
2. Append the citations as a plain `Sources:` list (exact format visible at the end of every sample output below).
3. Wrap into the tool result: `{"content": "<playbook + sources>", "cost": 1.5}` (internal billing unit, unrelated to the Perplexity dollar cost).

The coding agent reads the playbook prose + inline code blocks and writes the integration.

## 5. Samples — summary

| # | Sample | Latency | Total cost | Playbook | Citations | Searches |
|---|---|---|---|---|---|---|
| 1 | Stripe checkout — mobile (Expo React Native) school-fee app | 258.3 s | $0.83704 | 67,943 ch | 42 | 50 |
| 2 | Google Drive CSV upload — FastAPI backend | 321.2 s | $0.94294 | 90,197 ch | 48 | 50 |
| 3 | Custom JWT auth — mobile (Expo React Native) | 261.7 s | $0.91603 | 67,328 ch | 41 | 50 |
| 4 | JWT + mocked OTP + roles — mobile (Expo React Native) | 317.9 s | $1.25735 | 77,531 ch | 50 | 59 |
| 5 | PayPal checkout — web (FastAPI + React) store | 229.6 s | $1.04711 | 63,374 ch | 50 | 60 |

**Averages:** latency **277.7 s**, cost **$1.000/call**, playbook **73,274 chars**, **46 citations**.

From a separate 29-integration run with the same construction: avg 212.5 s, avg $0.957/call, avg 68,546 chars, 29/29 success. At ~70k research calls/month, the current Perplexity path costs **~$67k/month**.

---

## Sample 1: Stripe checkout — mobile (Expo React Native) school-fee app

| | |
|---|---|
| HTTP status | 200 |
| **Latency** | **258.3 s** |
| **Total cost (from Perplexity's `usage.cost`)** | **$0.83704** |
| Cost breakdown | input $0.00046 · output $0.10798 · citation $0.04094 · reasoning $0.43766 · search $0.25 |
| Tokens | prompt 230 · completion 13,498 · citation 20,470 · reasoning 145,885 |
| Search queries run by Perplexity internally | 50 |
| Playbook length | 67,943 chars |
| Citations | 42 |

### Input — what our agent asked the tool (verbatim)

```
INTEGRATION: Stripe payment integration for Expo React Native mobile app + FastAPI backend. Use case: students/parents pay school registration fee for pondok pesantren (Islamic boarding school). Need test mode payment with checkout session. CONSTRAINTS: Mobile app uses Expo SDK 54, no login (registration ID based), Stripe test keys available in pod environment.
```

### Exact API request sent to Perplexity

```json
{
  "url": "https://api.perplexity.ai/chat/completions",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer pplx-REDACTED-MOCK-KEY",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "sonar-deep-research",
    "messages": [
      {
        "role": "system",
        "content": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
      },
      {
        "role": "user",
        "content": "Create a detailed integration playbook for INTEGRATION: Stripe payment integration for Expo React Native mobile app + FastAPI backend. Use case: students/parents pay school registration fee for pondok pesantren (Islamic boarding school). Need test mode payment with checkout session. CONSTRAINTS: Mobile app uses Expo SDK 54, no login (registration ID based), Stripe test keys available in pod environment. in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
      }
    ]
  }
}
```

### Exact output returned to our agent (verbatim, 70,378 chars)

This is the complete tool result the coding agent receives — the playbook exactly as Perplexity wrote it, with the citation URLs appended as a `Sources:` list by our tool layer. (It is then wrapped as `{"content": "<below>", "cost": 1.5}` — the `1.5` is an internal billing unit, unrelated to the Perplexity dollar cost.)

`````markdown
# Stripe Checkout Integration Playbook for an Expo React Native + FastAPI + MongoDB Registration App

This report presents a complete integration playbook for adding Stripe-powered registration fee payments to an Expo SDK 54 React Native mobile app with React Native Web support and a FastAPI backend backed by MongoDB. The target use case is parents or students paying a registration fee for a *pondok pesantren* (Islamic boarding school), with no user login and the registration identifier serving as the primary key for payment. The architecture relies on Stripe Checkout Sessions in test mode, exposed by FastAPI as API endpoints and consumed by both mobile and web clients using a shared React Native codebase. The playbook covers installation and configuration of all components, secure management of Stripe test API keys, end-to-end code samples for backend and frontend, MongoDB persistence of registration and payment state, webhook handling for reliable payment confirmation, testing procedures using Stripe’s test cards and CLI, and a discussion of common pitfalls and their mitigation. The goal is that a single development team can follow this narrative to build and operate a robust, secure, and maintainable payment flow suitable for educational institutions with minimal changes when going from test mode to live mode later.

## 1. Conceptual Architecture and Use Case Modeling

### 1.1. Use case and constraints

The central use case is collection of a one-time registration fee from students or parents for a *pondok pesantren* program. There is no user account or login system; instead, each registrant is identified by a unique registration ID that is generated and stored by the school’s information system. When a parent wants to pay, they open the mobile app (or a web version of the same app), enter the registration ID and a small amount of identifying information, and then complete payment through Stripe Checkout in test mode. The system must record that the registration fee was paid for that registration ID in MongoDB so that administrative systems can verify payment.

Because the app is built with Expo SDK 54, the React Native runtime corresponds to React Native 0.81 and Expo’s autolinking handles native modules such as Stripe’s React Native SDK automatically.[4][6] The integration must work for native platforms (iOS, Android) and for web using React Native Web, but the core payment flow will be based on Stripe Checkout Session rather than PaymentSheet, to match the requirement that payment be driven by Checkout Sessions.[11][13][5][13] The Stripe environment must remain in test mode initially, and all keys used are Stripe test keys, which will later be replaced by live keys with minimal code changes.[19][39]

The absence of a login system means that standard “customer account” flows are not strictly necessary. Instead, metadata on Stripe objects such as Checkout Session and PaymentIntent will carry the registration ID and any other minimal identifying data needed to reconcile payments with internal records.[27] MongoDB will store registration records, payments, and their association, which is typical for document databases and easily implemented with insert and update operations via PyMongo.[29][37]

### 1.2. High-level component architecture

At a high level, the architecture comprises four cooperating subsystems. First, the Expo React Native application provides the user interface for both mobile and web users, with a registration ID entry screen, optional student and guardian details, and a “Pay registration fee” action. Second, a FastAPI backend exposes REST endpoints for creating Stripe Checkout Sessions, receiving Stripe webhook notifications, and optionally querying payment status. Third, Stripe’s infrastructure provides payments, Checkout Session hosting, and outbound webhooks, configured through the Stripe Dashboard and secured using API keys and webhook signing secrets.[1][2][11][38] Fourth, MongoDB provides persistent storage of registration and payment status, accessed from the FastAPI backend using PyMongo with a connection URI.[29][37]

The typical flow proceeds as follows. A parent enters the registration ID and triggers payment. The app sends a POST request to the FastAPI endpoint that creates a Checkout Session, including the registration ID and amount. FastAPI validates the registration data, checks the registration record from MongoDB, constructs a Checkout Session via the Stripe SDK with test keys, and returns the session URL.[3][11][13][3] The mobile app opens this URL in the device browser using deep linking, while the web app simply navigates the current browser window. Once payment succeeds, Stripe redirects the user to a success URL that encodes the session ID and uses either a custom URL scheme for native apps or an HTTPS route for web.[5][6] A webhook endpoint receives a `checkout.session.completed` event, validates the signature, and updates MongoDB to mark the registration fee as paid.[3][27][38] The app can poll a status endpoint or decode the success URL to show confirmation.

This architecture intentionally uses external Checkout pages instead of collecting card data directly in the native UI. Expo and Stripe both recommend prebuilt payment UIs such as PaymentSheet for mobile apps, but Stripe Checkout remains a supported and low-code solution especially when combined with web support.[2][5][7][7] Additionally, recent changes in Apple’s rules allow native apps to link to external payment pages for digital services in allowed circumstances, which broadens the viability of Stripe Checkout from within iOS apps when used correctly.[9] By basing the design on Checkout Sessions, the same backend endpoints and metadata strategy can be reused when a school later adds a full web enrollment portal.

### 1.3. Stripe Checkout versus PaymentSheet for this scenario

Stripe offers multiple integration surfaces for React Native apps, including PaymentSheet for in-app card collection, Apple Pay and Google Pay-specific flows, and the more web-centric Checkout Sessions used through browser redirects.[5][7][7][5] For this school registration use case, there are several reasons to prefer Checkout Sessions despite the availability of a native PaymentSheet.

First, the requirement is explicitly to use Checkout Sessions in test mode. Checkout Sessions provide a simple one-time payment integration where all PCI-sensitive fields are rendered and processed on Stripe’s domain rather than inside your app. This reduces compliance burden and simplifies security considerations because the mobile app never sees full card numbers.[2][28] Second, because the application also has a React Native Web front-end, Stripe Checkout provides a single, consistent payment page that behaves identically in mobile and web contexts, which can be useful for staff support or when parents prefer to pay on desktop devices.[2][9] Third, Checkout Sessions support metadata and customizable success/cancel URLs, allowing the backend to attach registration IDs and other identifiers to ensure accurate mapping to MongoDB records.[27][13]

That said, for future expansion, the team could consider PaymentSheet integration in parallel or as an alternative path, particularly if they wish to avoid leaving the app for a browser-based flow. Stripe’s React Native SDK and Expo’s integration guide provide sample code to initialize Stripe via a `StripeProvider` or `initStripe`, create PaymentIntents on the server, and present a mobile PaymentSheet for card details and confirmation.[5][6][7][5][6] Integrating PaymentSheet would require a different backend design based on PaymentIntents rather than Checkout Sessions and is therefore outside the scope of this playbook, but the same FastAPI and MongoDB infrastructure could be extended to support it.

### 1.4. Registration ID centric design

The absence of user login means that the registration ID acts as the primary key across the system. Conceptually, each registration record in MongoDB might store attributes such as `registration_id`, student name, school year, fee amount, and payment status. The FastAPI service must validate that the supplied registration ID exists and is eligible for payment before creating a Checkout Session. This prevents parents from paying for invalid IDs and ensures that payment metadata always maps to a real student record.

Stripe’s metadata feature is particularly useful in this context. Metadata is a set of key-value pairs that can be added to objects such as Checkout Sessions, Customers, and PaymentIntents for internal reference.[27] For example, when creating the Checkout Session, the backend can set `metadata` on the session to include `registration_id` and `student_name`. When the webhook receives a `checkout.session.completed` event, it can read these metadata values and update the corresponding document in MongoDB. Because metadata is not visible to end users and is only returned to server-side requests made with secret keys, it is ideal for this integration.[27]

In addition to metadata, Stripe’s `client_reference_id` field on Checkout Sessions allows an application-specific identifier such as the registration ID to be attached to the session. This string is preserved on the Checkout Session object and can serve as a second pointer into your own database.[11][12][12][13] By combining `client_reference_id` and `metadata` in a consistent way, the team can ensure that even if the MongoDB schema evolves, existing paid records remain traceable and can be reconciled against Stripe data exported from the dashboard.

## 2. Backend Setup: FastAPI, Stripe, and MongoDB

### 2.1. Environment preparation and dependencies

The backend service will be implemented using FastAPI, a modern Python framework that supports asynchronous request handling and integrates cleanly with Pydantic for validation and configuration management.[30][41] The service will also use the official Stripe Python SDK to manage Checkout Sessions and webhooks, and PyMongo for MongoDB connectivity.[3][29][37] Configuration such as Stripe API keys and MongoDB connection URIs should be kept in environment variables and loaded by a Pydantic Settings class, which is a recommended pattern for managing settings in FastAPI applications.[30] Stripe also explicitly recommends using environment variables or secret vaults to store API keys rather than embedding them in source code.[19][39]

Assuming a Python virtual environment, the core dependencies required are `fastapi`, `uvicorn`, `stripe`, `pymongo`, and `pydantic-settings`. FastAPI’s own documentation shows how to use `pydantic-settings` by defining a Settings class with attributes mapped to environment variables and specifying an `.env` file for local development if desired.[30] The Stripe integration tutorial for FastAPI demonstrates similar patterns for reading Stripe keys and setting them globally on the Stripe SDK.[3][3] PyMongo requires specifying a connection URI such as `mongodb://localhost:27017` or a cloud connection string, then creating a `MongoClient` and accessing one or more database objects.[37]

A minimal `pyproject.toml` or `requirements.txt` would list these packages, but in this playbook we focus on the actual code. The following code block shows a representative `settings.py` module that uses Pydantic Settings to manage configuration, followed by a `database.py` module that initializes MongoDB.

```python
# settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    stripe_secret_key: str
    stripe_webhook_secret: str
    stripe_publishable_key: str
    mongo_uri: str
    mongo_db_name: str = "pondok_registration"
    app_domain: str = "http://localhost:8000"
    frontend_base_url: str = "exp+pondokapp://"
    registration_fee_cents: int = 500000  # example: 5,000 IDR represented in smallest unit if supported

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
```

This configuration class follows FastAPI’s recommended approach for loading environment variables, including reading from a `.env` file during development.[30] The `stripe_secret_key` and `stripe_publishable_key` correspond to the test keys beginning with `sk_test_` and `pk_test_`, which can be obtained from the Stripe Developers Dashboard under the API keys section.[19] The `stripe_webhook_secret` is a separate secret used to verify webhook signatures, retrieved from the Stripe Dashboard’s webhooks section or the Stripe CLI when using `stripe listen`.[3][38] The MongoDB URI and database name reflect local or cloud Mongo deployments, as described in the MongoDB PyMongo connection documentation.[37]

The database module creates a MongoDB client and exposes a `registrations` collection.

```python
# database.py
from pymongo import MongoClient
from .settings import settings

client = MongoClient(settings.mongo_uri)
db = client[settings.mongo_db_name]

registrations_collection = db["registrations"]
payments_collection = db["payments"]
```

This structure allows the rest of the backend code to import `registrations_collection` and `payments_collection` to perform insert and update operations. The PyMongo documentation shows how `insert_one`, `insert_many`, and update methods are used to manipulate documents, which we will apply later to record payment status.[29]

### 2.2. FastAPI application structure and Stripe initialization

Once configuration and database modules exist, we can set up the FastAPI app itself. The FastAPI Stripe integration tutorial uses a pattern where the Stripe SDK is configured immediately after the Settings object is created, setting `stripe.api_key` to the secret key from the environment.[3][3] Because the Stripe library is synchronous, we can call it from `def` or `async def`-path operations; FastAPI will execute synchronous code in a threadpool to avoid blocking, and the asynchronous parts can use `await` when interacting with asynchronous libraries.[41]

The following code excerpt illustrates a `main.py` that initializes FastAPI, Stripe, and exposes a health endpoint.

```python
# main.py
from fastapi import FastAPI
import stripe

from .settings import settings
from .database import registrations_collection, payments_collection

app = FastAPI(title="Pondok Registration Payments API")

# Configure Stripe with secret key
stripe.api_key = settings.stripe_secret_key
```

At this stage we have not yet defined any routes, but Stripe’s global configuration is ready. FastAPI’s ability to mix `def` and `async def` endpoints is useful. For operations that call Stripe’s synchronous API, we can keep them as `def` methods; for operations that await asynchronous libraries such as async database drivers, we can define them as `async def`.[41] In this implementation we will use PyMongo, which is synchronous, so `def` endpoints are acceptable.

We can also define Pydantic models representing the request to create a Checkout Session and a simplified response. For example, a client might send a JSON payload with `registration_id`, `student_name`, and `email`. The backend would then create a Checkout Session and return the URL.

```python
from pydantic import BaseModel, EmailStr

class CreateCheckoutRequest(BaseModel):
    registration_id: str
    student_name: str
    parent_name: str | None = None
    parent_email: EmailStr | None = None

class CheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str
```

These models provide type validation and ensure that basic data such as email addresses have plausible formats. They also provide OpenAPI schema information for automatic documentation. The request model intentionally does not include price or currency; those are set server-side to avoid trusting client-supplied amounts, which is a key security best practice recommended by Stripe.[3][3][19]

### 2.3. Creating Stripe Checkout Sessions from FastAPI

The core backend functionality is a route that creates a Stripe Checkout Session given a registration request. Stripe’s API reference for Checkout Sessions shows that a session can be created by POSTing to `/v1/checkout/sessions` with data such as `success_url`, `cancel_url`, `line_items`, and `mode`.[11][13][12][13] Using the Python Stripe SDK, the equivalent is calling `stripe.checkout.Session.create` with named parameters. The FastAPI Stripe integration tutorial demonstrates a similar pattern for one-time payments, building the session and returning the `url` field to the client.[3][3]

For a pondok registration fee, assume that each registration ID has a fixed fee stored in MongoDB. For simplicity we can store the fee amount in the Settings object as `registration_fee_cents`, but in a production system it might be read from the registration document. The success and cancel URLs should be chosen to support both native deep links and web callbacks. For web, we might use `https://school.example.com/payment/success`; for native, we might use a custom scheme such as `pondokapp://payment-success`. Expo’s documentation for linking and Stripe integration suggests using `Linking.createURL` in combination with `Constants.appOwnership` to choose the right scheme when initializing Stripe or constructing URLs.[6][6] For Checkout Sessions, which run in the browser, we can simply direct Stripe’s `success_url` to a backend endpoint that then redirects into the app using a deep link; however, to keep this playbook focused, we will have the web success page and a mobile deep link variant both handled by the frontend.

The following FastAPI route creates a Checkout Session:

```python
from fastapi import HTTPException
from fastapi import APIRouter

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create-checkout-session", response_model=CheckoutSessionResponse)
def create_checkout_session(payload: CreateCheckoutRequest):
    # Verify registration exists (simplified example)
    registration = registrations_collection.find_one(
        {"registration_id": payload.registration_id}
    )
    if not registration:
        raise HTTPException(status_code=404, detail="Registration ID not found")

    # Determine amount and currency; here we use a fixed fee from settings
    amount = settings.registration_fee_cents
    currency = "usd"  # or "idr" depending on your Stripe account configuration

    # Construct success and cancel URLs
    success_url = f"{settings.app_domain}/payments/success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{settings.app_domain}/payments/cancel?registration_id={payload.registration_id}"

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "unit_amount": amount,
                        "product_data": {
                            "name": "Pondok Registration Fee",
                            "description": f"Registration for {payload.student_name}",
                        },
                    },
                    "quantity": 1,
                }
            ],
            client_reference_id=payload.registration_id,
            metadata={
                "registration_id": payload.registration_id,
                "student_name": payload.student_name,
                "parent_name": payload.parent_name or "",
                "parent_email": payload.parent_email or "",
            },
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Optionally, create a pending payment record in MongoDB
    payments_collection.insert_one(
        {
            "registration_id": payload.registration_id,
            "session_id": session.id,
            "status": "created",
            "amount": amount,
            "currency": currency,
        }
    )

    return CheckoutSessionResponse(
        checkout_url=session.url,
        session_id=session.id,
    )
```

Here we follow several Stripe and FastAPI best practices. We validate the registration ID against MongoDB before creating the session, so parents cannot pay for nonexistent IDs. We compute the `amount` and `currency` on the server, avoiding client manipulation of prices, as recommended by Stripe’s security guidelines.[19] We include the registration ID both in `client_reference_id` and the session metadata, which makes reconciliation easier and aligns with Stripe’s metadata usage guide.[27] We insert a pending payment record in MongoDB when the session is created; when the webhook later confirms completion, we update that record’s status to “paid”.

The success URL uses the special placeholder `{CHECKOUT_SESSION_ID}`, which Stripe substitutes with the actual session ID when redirecting after payment.[11][13] The app domain `settings.app_domain` should point to your FastAPI host for backend routes; in development this may be `http://localhost:8000`. In production it will be your server’s domain name, and you must ensure it is accessible from Stripe’s Checkout pages.

### 2.4. Webhook handling for payment confirmation

Reliable payment confirmation should not depend solely on the client being redirected back to the app. For example, a parent might close the browser before the redirect occurs. Stripe recommends using webhooks to receive asynchronous event notifications when payment events occur, such as `checkout.session.completed` or `invoice.payment_failed`.[3][38] The FastAPI Stripe tutorial shows how to implement a webhook endpoint that reads the request body, verifies the signature using Stripe’s `construct_event` helper, and then handles event types appropriately.[3]

A webhook endpoint for this system needs to perform several tasks. It must validate that incoming requests are from Stripe using the webhook signing secret. It must extract the Checkout Session from the `checkout.session.completed` event, pull out the registration ID from metadata or `client_reference_id`, and then update MongoDB to mark that registration as paid, including storing the PaymentIntent or charge ID for audit purposes. The endpoint must be idempotent because Stripe may retry webhook deliveries; therefore, updating payment status should handle duplicates gracefully.[38]

The following code example implements a webhook in FastAPI.

```python
from fastapi import Request, Header
from fastapi.responses import JSONResponse

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=settings.stripe_webhook_secret,
        )
    except ValueError:
        # Invalid payload
        return JSONResponse(status_code=400, content={"error": "Invalid payload"})
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return JSONResponse(status_code=400, content={"error": "Invalid signature"})

    event_type = event["type"]
    data_object = event["data"]["object"]

    if event_type == "checkout.session.completed":
        session = data_object
        registration_id = session.get("client_reference_id") or session.get("metadata", {}).get("registration_id")
        payment_intent_id = session.get("payment_intent")

        if registration_id:
            # Update payment record
            payments_collection.update_one(
                {"session_id": session["id"]},
                {
                    "$set": {
                        "status": "paid",
                        "payment_intent_id": payment_intent_id,
                    }
                },
                upsert=True,
            )

            # Update registration document
            registrations_collection.update_one(
                {"registration_id": registration_id},
                {
                    "$set": {
                        "payment_status": "paid",
                        "paid_at": session.get("created"),
                        "payment_intent_id": payment_intent_id,
                    }
                },
            )

    # Handle other event types of interest as needed

    return JSONResponse(status_code=200, content={"received": True})
```

This route reads the raw request body, obtains the `stripe-signature` header, and uses `stripe.Webhook.construct_event` with the configured webhook secret, exactly as shown in Stripe’s examples and FastAPI tutorials, to ensure authenticity of the webhook call.[3][38] The event type is then inspected; for `checkout.session.completed` we read the registration ID and the PaymentIntent ID, and update MongoDB accordingly. The `update_one` with `upsert=True` ensures that if the pending payment record was not created earlier, it will still be inserted; this is useful in case the `create-checkout-session` call fails to write to MongoDB but payment nevertheless completes.

To make webhooks work in local development, the Stripe CLI can be used to forward events to `http://localhost:8000/payments/webhook`. The CLI commands `stripe login` followed by `stripe listen --forward-to localhost:8000/payments/webhook` will set up a tunnel and output a webhook secret that can be placed in `.env` as `stripe_webhook_secret`.[17][3] Stripe’s documentation emphasizes that webhook signing secrets are distinct from API secret keys and that test and live modes use separate endpoint configurations and secrets.[19][38]

### 2.5. Success and cancel callback endpoints

For completeness, the backend may also provide success and cancel endpoints referenced in the Checkout Session creation. While the security and persistence of payment status should rely on webhooks, these callback endpoints can be used to show user-friendly pages in web flows or to pass minimal status data to the client before it queries a separate status endpoint. The FastAPI Stripe integration article illustrates a success endpoint that retrieves the Checkout Session from Stripe and then checks `payment_status` to confirm the payment, which we can adopt here.[3]

A simple success endpoint might look like this:

```python
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from fastapi import Query

templates = Jinja2Templates(directory="templates")

@router.get("/success")
async def payment_success(session_id: str = Query(...)):
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status == "paid":
        registration_id = session.get("client_reference_id")
        # Optionally, we could also re-confirm DB status here
        return {"status": "paid", "registration_id": registration_id}
    return {"status": "unpaid"}
```

In a real deployment this endpoint might render an HTML template using `Jinja2Templates` for web browsers, or it could redirect to a specific frontend route. For native applications, you might not need this route at all if the Checkout `success_url` points directly to a deep link for the mobile app; in that case, the mobile app would read the session ID from the URL and query a status endpoint like `/payments/status?session_id=...` to display confirmation. In any case, this callback endpoint is a convenient place to ensure that the success URL cannot be forged because it re-fetches the session details from Stripe using the secret API key.[3][31]

A cancel endpoint can be simpler, perhaps returning a message that payment was not completed and encouraging the user to try again. It need not modify the database, but it can be used to clean up pending records if desired.

```python
@router.get("/cancel")
async def payment_cancel(registration_id: str = Query(...)):
    # Optional: mark last payment attempt as cancelled in DB
    return {"status": "cancelled", "registration_id": registration_id}
```

By separating the responsibilities of webhook-driven persistence and callback-driven user feedback, this backend design remains robust while providing a good user experience.

## 3. Frontend Setup: Expo SDK 54, React Native, and Web

### 3.1. Expo project initialization and core dependencies

On the frontend side, the goal is to build a universal app that runs on iOS, Android, and the web using Expo SDK 54 and React Native Web. Expo SDK 54 ships with React Native 0.81 and offers features such as improved autolinking of native modules, which simplifies integration with Stripe’s React Native SDK.[4][6] To begin, a new Expo app can be created using `npx create-expo-app pondok-payments`, after which dependencies for Stripe and any HTTP client libraries can be added.

Because the payment flow uses Stripe Checkout rather than PaymentSheet, the React Native Stripe SDK is not strictly required to collect card details. However, installing `@stripe/stripe-react-native` remains useful if you plan to extend the app to use PaymentSheet in the future or integrate Apple Pay and Google Pay directly.[5][6][7][15][6] Expo’s Stripe module is supported by autolinking and includes a config plugin to configure merchant identifiers and Google Pay settings through `app.json`.[6][6] Installing the Stripe React Native SDK using `npx expo install @stripe/stripe-react-native` ensures that you get the correct version compatible with Expo SDK 54.[4][6]

In addition to Stripe, the frontend needs `expo-linking` to manage deep links, `expo-constants` for configuration, and possibly an HTTP client such as `axios`, although the built-in `fetch` API is often sufficient. To support web, React Native Web is already configured by Expo; you only need to ensure that navigation and linking behave correctly across platforms. For larger apps, Expo Router or React Navigation can be used to structure screens, but the integration with Stripe Checkout is essentially independent of routing.

Because the user requested that Stripe test keys be available in the “pod environment”, we assume that the backend environment holds secret keys and the frontend only needs the publishable key for cases where the Stripe React Native SDK is used. For a pure Checkout flow, the frontend does not need any Stripe keys at all, because it simply redirects to the Checkout URL returned by the backend; this is preferable from a security standpoint.[2][19] Nevertheless, we will show how to configure a minimal `StripeProvider` in case you wish to later add PaymentSheet.

### 3.2. Configuring app.json for deep linking and Stripe

Deep linking is central to returning parents from the Stripe Checkout page back into the mobile app after payment. Expo’s documentation recommends defining a `scheme` in `app.json` under the `expo` key and potentially using the Stripe config plugin to configure Apple Pay and Google Pay support.[6][22][6] For this app, we might choose `pondokapp` as the URL scheme, yielding deep links like `pondokapp://payment-success`.

A sample `app.json` configuration could look like this:

```json
{
  "expo": {
    "name": "Pondok Registration",
    "slug": "pondok-registration",
    "scheme": "pondokapp",
    "version": "1.0.0",
    "sdkVersion": "54.0.0",
    "platforms": ["ios", "android", "web"],
    "plugins": [
      [
        "@stripe/stripe-react-native",
        {
          "merchantIdentifier": "merchant.com.yourschool.pondok",
          "enableGooglePay": true
        }
      ]
    ]
  }
}
```

The `scheme` property instructs Expo and the underlying native platforms to recognize URLs like `pondokapp://` as belonging to this app, enabling deep linking from web pages such as Stripe Checkout’s success redirect.[6][22][6] The Stripe config plugin is optional for a Checkout-only flow but necessary if you plan to offer Apple Pay and Google Pay via PaymentSheet or other native flows. It requires a valid Apple merchant identifier, which can be configured via Expo EAS Build and the Apple Developer Program.[6][6][18]

Expo’s Stripe docs note that when relying on browser redirects (for example, for 3D Secure authentication), you may need to pass a `urlScheme` into `initStripe`, using logic from `expo-linking` and `expo-constants` to ensure consistent behavior in Expo Go versus standalone builds.[6][6] Although this is more relevant for PaymentSheet, the same deep linking approach applies to Stripe Checkout’s success and cancel URLs when they are configured to use custom schemes.

### 3.3. Registration screen and API integration

The core UI in the app will be a registration payment screen that collects the registration ID and minimal student or parent details. This screen then calls the backend’s `/payments/create-checkout-session` endpoint, receives the Checkout URL, and opens it in a browser. On the web, this is as simple as setting `window.location.href` to the URL; on native platforms, we use Expo Linking’s `openURL` function.

Here is a simplified `RegistrationPaymentScreen.tsx` implemented in TypeScript to emphasize types, though JavaScript could be used as well:

```tsx
// app/RegistrationPaymentScreen.tsx
import React, { useState } from "react";
import { View, Text, TextInput, Button, Platform, Alert } from "react-native";
import * as Linking from "expo-linking";

const API_BASE_URL = "http://localhost:8000"; // In production, use your server URL

export default function RegistrationPaymentScreen() {
  const [registrationId, setRegistrationId] = useState("");
  const [studentName, setStudentName] = useState("");
  const [parentName, setParentName] = useState("");
  const [parentEmail, setParentEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const onPayPress = async () => {
    if (!registrationId || !studentName) {
      Alert.alert("Error", "Please enter registration ID and student name.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/payments/create-checkout-session`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          registration_id: registrationId,
          student_name: studentName,
          parent_name: parentName,
          parent_email: parentEmail || undefined
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to create checkout session");
      }

      const data = await response.json();
      const checkoutUrl = data.checkout_url;

      if (Platform.OS === "web") {
        window.location.href = checkoutUrl;
      } else {
        await Linking.openURL(checkoutUrl);
      }
    } catch (error: any) {
      Alert.alert("Payment error", error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ flex: 1, padding: 16, justifyContent: "center" }}>
      <Text style={{ fontSize: 24, marginBottom: 16 }}>Pondok Registration Fee</Text>
      <TextInput
        style={{ borderWidth: 1, padding: 8, marginBottom: 12 }}
        placeholder="Registration ID"
        value={registrationId}
        onChangeText={setRegistrationId}
      />
      <TextInput
        style={{ borderWidth: 1, padding: 8, marginBottom: 12 }}
        placeholder="Student name"
        value={studentName}
        onChangeText={setStudentName}
      />
      <TextInput
        style={{ borderWidth: 1, padding: 8, marginBottom: 12 }}
        placeholder="Parent name (optional)"
        value={parentName}
        onChangeText={setParentName}
      />
      <TextInput
        style={{ borderWidth: 1, padding: 8, marginBottom: 12 }}
        placeholder="Parent email (optional)"
        value={parentEmail}
        onChangeText={setParentEmail}
        keyboardType="email-address"
      />
      <Button title={loading ? "Creating..." : "Pay registration fee"} onPress={onPayPress} disabled={loading} />
    </View>
  );
}
```

This screen uses basic React Native components that render appropriately on mobile and web via React Native Web. It uses the same backend URL regardless of platform, though in development you may need to replace `localhost` with your machine’s IP for devices on the same network. The design adheres to Stripe’s guideline that payment amounts and product details should be computed server-side, as the client only sends registration identifiers and non-sensitive metadata.[3][3][19]

For success handling, the app will need another screen that can parse the deep link or web URL and display a confirmation. On web, the success URL might be `https://your-frontend-domain/payment/success?session_id=...`, where a route reads the query parameter, calls the backend `/payments/success` or `/payments/status`, and shows the result. In native apps where the success URL uses the `pondokapp://` scheme, Expo Linking can be configured to handle incoming URLs via a root component or navigation container.

### 3.4. Handling deep links on native platforms

To handle deep links triggered by Stripe’s redirect to a custom scheme, the app must register a URL listener using Expo Linking. A simple approach is to create a top-level component that listens for initial URLs and subscription events and navigates accordingly. If using React Navigation or Expo Router, this can be integrated into the navigation container. For this playbook, a simple example uses `useEffect` and `Linking.addEventListener`.

```tsx
// app/Root.tsx
import React, { useEffect } from "react";
import * as Linking from "expo-linking";
import { View, Text } from "react-native";

export default function Root() {
  useEffect(() => {
    const handleUrl = (event: Linking.EventType) => {
      const url = event.url;
      const parsed = Linking.parse(url);
      if (parsed.path === "payment-success" && parsed.queryParams?.session_id) {
        // Navigate to a success screen or show confirmation
        console.log("Payment success for session", parsed.queryParams.session_id);
      }
    };

    Linking.getInitialURL().then((url) => {
      if (url) {
        handleUrl({ url } as any);
      }
    });

    const subscription = Linking.addEventListener("url", handleUrl);
    return () => subscription.remove();
  }, []);

  return (
    <View style={{ flex: 1 }}>
      {/* Render your registration screen or navigation stack here */}
      <Text>Root component</Text>
    </View>
  );
}
```

Expo’s Stripe documentation suggests using `Linking.createURL` along with `Constants.appOwnership` to generate correct URLs inside the app, especially when using Expo Go versus production builds.[6][6] For Checkout, we mostly need to ensure that the `success_url` configured in the backend uses a supported scheme. For native devices, that means `pondokapp://payment-success?session_id={CHECKOUT_SESSION_ID}`. To support both web and native, you can configure two different success URLs using branching logic on the backend based on a parameter from the client, or standardize on a backend HTML page that then uses JavaScript to redirect into the app via deep link if it detects a mobile device.

### 3.5. Optional StripeProvider configuration for future PaymentSheet

Although Checkout integration does not require the React Native Stripe SDK, you may wish to prepare the app to use PaymentSheet as an alternative in the future. Stripe’s React Native SDK expects you to wrap your payment screens with a `StripeProvider` or call `initStripe`, passing at least the publishable key.[5][7][7][5][6][15] Expo’s integration guide shows how to add the Stripe config plugin to `app.json` and then use `StripeProvider` at the top level.[6][6].

A minimal setup looks like this:

```tsx
// app/_layout.tsx or App.tsx
import React from "react";
import { StripeProvider } from "@stripe/stripe-react-native";

const STRIPE_PUBLISHABLE_KEY = "pk_test_XXXXXXXXXXXXXXXXXXXXXXXX";

export default function App() {
  return (
    <StripeProvider publishableKey={STRIPE_PUBLISHABLE_KEY}>
      {/* Your navigation or root component */}
    </StripeProvider>
  );
}
```

In test-mode-only deployments, the publishable key should be the test key obtained from the Stripe dashboard. Because this key is not secret, it can be bundled into the app or provided via an environment mechanism such as `app.config.js`, though for better flexibility you may still want to inject it at build time. Stripe’s documentation emphasizes that secret keys such as `sk_test_...` must never be exposed in frontend code, whereas publishable keys beginning with `pk_test_` are safe to embed but should still be rotated periodically.[19][6]

## 4. Security and API Key Management

### 4.1. Stripe API keys: test versus live modes

Stripe uses different sets of API keys for sandbox (test) and live environments. Standard secret keys begin with `sk_test_` for test mode and `sk_live_` for live mode, whereas publishable keys begin with `pk_test_` and `pk_live_`.[19] When building and testing an integration, you must use test mode keys, which allow you to simulate payments using Stripe’s test card numbers without affecting real funds.[16][19][16] When your integration is ready to accept real payments, you switch to live mode keys in your backend configuration and ensure that your Stripe Dashboard is set to live mode for the relevant products and webhooks.[19][39]

Stripe’s API key documentation explains that keys can be created, revealed, and rotated in the Developers Dashboard under the API keys tab.[19] When creating a new secret key, Stripe shows it only once; you must copy and store it in a secure location such as environment variables or a secrets vault. You should never hardcode it in source code or configuration files that might be committed to version control.[19][39] For the pondok registration system, the `stripe_secret_key` used by FastAPI should be set from the environment using Pydantic Settings, as shown earlier. The `stripe_webhook_secret` is separate and obtained from the Webhooks section of the dashboard or via the Stripe CLI when using `stripe listen`.[19][38]

To switch from test mode to live mode later, you typically need to change the environment variables `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, and `STRIPE_WEBHOOK_SECRET` to their live equivalents, update webhook endpoints in Stripe to point to the production URL, and ensure that any product or price IDs referenced by code exist in live mode.[39] Because this integration uses inline `price_data` rather than pre-configured price IDs, you have fewer dependencies on static Stripe objects; however, if you later move to using Products and Prices, you must create those objects in both test and live modes with consistent IDs.[3][28][39]

### 4.2. Backend key storage and rotation

The backend must treat Stripe secret keys like any other sensitive secret. Stripe recommends storing keys in a vault or, if that is not feasible, as environment variables injected at runtime.[19] Pydantic Settings already reads from environment variables and optionally `.env` files; for production, `.env` files should be carefully secured, and in many deployments, environment variables provided by the platform (e.g., Docker secrets, Kubernetes secrets, or managed configuration) are preferred.

Keys should be rotated periodically, and especially before going live, to minimize the risk that keys used during development were stored insecurely.[19][39] Stripe’s Dashboard allows setting expiration dates on keys when rotating them; your backend can be updated to accept both old and new keys during a migration window, though for most small integrations a single rotation is sufficient.[19] After changing the `stripe_secret_key` environment variable, you must restart the FastAPI server so that the new key is loaded and set as `stripe.api_key`.

Webhook signing secrets are also sensitive and should be stored similarly. Because each webhook endpoint has its own signing secret and test and live modes have separate endpoints, you must maintain separate `stripe_webhook_secret` values for test and live environments.[3][38] The backend code remains unchanged; only the environment variables change.

### 4.3. Frontend key usage and exposure

For a pure Checkout integration, the frontend does not need any secret or publishable keys. The app simply calls the backend endpoint to get a Checkout URL and navigates there. This design has a significant security advantage: even if the frontend code is decompiled or inspected, there are no keys for attackers to steal and misuse. All Stripe communication uses server-side secret keys that are protected by the backend’s own security measures.[2][19]

If you decide to integrate the React Native Stripe SDK for PaymentSheet or other flows, the frontend will need the publishable key but never the secret key. Stripe’s key documentation makes clear that publishable keys can be embedded in client applications because they restrict what operations can be performed and do not expose sensitive account-level privileges.[19] Nonetheless, you should still avoid shipping test publishable keys into production builds, as they might cause confusion or break functionality. Managing the publishable key via environment configuration or compile-time injection ensures that mobile builds destined for production use the correct live `pk_live_` key.[19][6]

### 4.4. Minimizing sensitive data and aligning with PCI requirements

An important advantage of Stripe Checkout is that the app never handles full card numbers, expiration dates, or CVC codes. Stripe’s own Checkout page handles all sensitive entry and transmits data directly to Stripe’s servers. For the pondok registration app, the mobile and web clients only send registration IDs and non-sensitive metadata such as names and emails to the backend, and the backend only receives card-related information via Stripe objects such as PaymentIntent and Charge IDs.[2][10][28] This architecture dramatically reduces the PCI DSS scope of your system because you are not directly processing or storing card data.

Stripe’s metadata feature must not be used to store sensitive information such as card numbers or bank accounts, and Stripe’s documentation explicitly warns against this.[27] Instead, metadata should contain registration IDs, internal order identifiers, or non-sensitive business context. If you require more elaborate data structures than metadata’s limits allow, you should store that data in MongoDB and use a simple key or ID in Stripe metadata that points back to your own records.[27]

The backend must also avoid logging sensitive data. Logs should contain Stripe object IDs, registration IDs, and limited details sufficient for debugging but not full cardholder information, which Stripe never sends to you in the first place when using Checkout. Stripe’s go-live checklist emphasizes reviewing logging and error handling to ensure that configurations do not inadvertently log sensitive data.[39]

### 4.5. HTTPS, CORS, and other security aspects

Although this playbook’s code samples use `http://localhost:8000` for development, production deployments must use HTTPS for all connections between client and backend, and between Stripe and backend for webhook calls.[3][19] Stripe requires HTTPS for many of its features, and browsers increasingly block mixed content. Configuring TLS on the FastAPI host and ensuring that the app’s base URL uses `https://` is therefore essential.

If the frontend app domain differs from the backend domain, Cross-Origin Resource Sharing (CORS) must be configured appropriately. FastAPI provides middleware to set CORS policies, and you should restrict allowed origins to your own domains. Because the app might be deployed on web at `https://school.example.com` and the API at `https://api.school.example.com`, you should list the app domain in the CORS allowed origins.

On the backend, you should validate inputs such as `registration_id` and `email` to avoid injection or unexpected behavior. Pydantic models already enforce types for basic fields like `EmailStr`, but you can also add regex-based constraints or internal lookup rules to ensure that only legitimate registration IDs are accepted. Stripe’s error documentation lists various error codes that can occur when payments fail, and your backend and frontend should treat them as user-visible issues (like card declines) or internal errors depending on their type.[36] By designing error pathways clearly, you can avoid exposing internal stack traces or configuration details to parents who attempt to pay.

## 5. Testing Strategy and Procedures

### 5.1. Stripe test cards and scenarios

Stripe provides a range of test card numbers that can be used to simulate successful payments, declines, and authentication-required flows in test mode.[16][16] For basic testing of Checkout Sessions, the most commonly used card is `4242 4242 4242 4242`, which simulates successful Visa payments in many countries.[16][3][16] To test a decline, you can use, for example, `4000 0000 0000 0002`, which simulates a card being declined.[3][16] To test 3D Secure authentication flows, a card such as `4000 0025 0000 3155` can trigger additional authentication steps.[3][16][16]

When testing the pondok registration app, you should create a few sample registration records in MongoDB with distinct registration IDs and then use Stripe Checkout to pay for them using these test cards. Each payment attempt should be made with a different scenario card to ensure that the system correctly handles success, decline, and authentication-required situations, though for Checkout, much of the latter is handled entirely by Stripe’s page. The key is to ensure that the webhook and database updates occur as expected.

When entering card details in Stripe’s Checkout page, use any future expiration date (for example, 12/34) and three-digit CVC, as described in many Stripe integration tutorials.[3][3][16] The billing name and address can be arbitrary because they do not affect test transactions, though they can be useful for verifying that metadata or receipts appear as expected in the Stripe dashboard.[2]

### 5.2. Local testing of webhooks with Stripe CLI

Testing webhooks locally is crucial before deploying to production. The Stripe CLI provides a convenient way to forward webhook events from Stripe to your local FastAPI server running on `localhost`. The process is as follows. First, install the Stripe CLI for your platform and log in using `stripe login`, which opens a browser window and asks for authorization.[17][3] Once authenticated, you can run `stripe listen --forward-to localhost:8000/payments/webhook` to cause Stripe to send events to that endpoint whenever they occur, and the CLI will display a webhook signing secret that you paste into your `.env` file as `STRIPE_WEBHOOK_SECRET`.[17][3][38]

With the FastAPI server running and the CLI forwarding events, you can trigger events manually using `stripe trigger checkout.session.completed` and other commands. The FastAPI Stripe webhook example demonstrates using `stripe trigger` to simulate subscription cancellations and payment failures as well.[3][17] When events arrive, your FastAPI logs should show them being handled; you can also query MongoDB to confirm that payment documents and registration status fields are updated.

By combining manual triggers with real Checkout flows, you can verify both the event-handling logic and the end-to-end integration. Stripe’s documentation stresses that webhook endpoints should be able to handle retries, out-of-order events, and occasional delays.[38][39] You can simulate such conditions by stopping and restarting your server while events are being delivered, ensuring that your code is idempotent and robust.

### 5.3. End-to-end test flows on mobile and web

Beyond backend-focused testing, you must validate the full flow from the user’s perspective on both mobile and web. On the web, open the app in a browser (served via `npx expo start --web` or a production build) and navigate to the registration payment screen. Enter a valid registration ID and student name, then click the pay button. The browser should navigate to a Stripe Checkout page showing the product name “Pondok Registration Fee” and the correct amount. Enter the `4242` test card and complete payment. Upon completion, Stripe should redirect to the configured success URL, which in a web context should be an app route that shows payment confirmation. At the same time, Stripe sends a webhook event that updates MongoDB.

On mobile, run the app via Expo Go or a development build and navigate to the same registration screen. After entering registration data and pressing pay, the app should call the backend and then open the Checkout URL in the device browser via `Linking.openURL`. The user completes card details in Safari or Chrome, and upon success, Stripe redirects to either a web success page or a deep link back into the app, depending on your configuration. You must verify that the app can correctly handle this return path: either by reading query parameters from a deep link or by having the success page show a message.

Because the integration is based on Checkout Sessions rather than PaymentSheet, some of the mobile-specific intricacies described in Stripe’s React Native documentation, such as `returnURL` and `handleURLCallback` for PaymentIntents, are less relevant.[5][42] Nonetheless, deep linking remains crucial if you want the user to return to the app automatically after payment. In early iterations, it may be acceptable to show a simple “Payment successful, you can close this tab and return to the app” message on the success page, relying on webhooks for actual status updates.

### 5.4. Error handling and edge-case testing

Stripe’s error code documentation lists many potential errors that might occur during payment processing, including `card_error` for declines, `invalid_request_error` for malformed parameters, and `api_error` for unexpected server-side issues.[36] Although Checkout abstracts many of these away from the client, your backend may still encounter errors when creating sessions or handling webhooks. It is important to test how your system behaves when such errors occur.

For instance, intentionally misconfigure the secret key in your `.env` file to simulate an authentication failure when calling `stripe.checkout.Session.create`. The FastAPI endpoint should catch the resulting exception and return an HTTP 400 or 500 with a generic error message, while logging the underlying error detail. Similarly, simulate duplicate webhook deliveries by re-sending the same event payload to your webhook endpoint; your `update_one` operations should be idempotent such that they do not produce incorrect states.

Stripe’s go-live checklist encourages developers to test their error handling thoroughly, including cases that “should never happen”, and to ensure that user-facing messages do not expose internal details.[39] For the pondok registration app, this means showing parents messages like “Payment could not be processed, please try another card or contact the school” while logging the specific Stripe error type and code internally for support staff.

### 5.5. Load and concurrency considerations

Although a school’s registration system may not face extremely high transaction volumes, it is still prudent to consider concurrency and resource usage. FastAPI’s asynchronous model handles many simultaneous connections efficiently, but synchronous operations like Stripe’s SDK and PyMongo will be run in a thread pool. If you anticipate large volumes, consider using asynchronous MongoDB clients and strategies to avoid blocking operations. Nonetheless, for typical school enrollment scenarios, the described architecture should be sufficient.

Stripe cautions that long-running webhook handlers may cause timeouts; if your webhook endpoint performs heavy operations, you may need to queue work for asynchronous processing.[38] Here, the operations are relatively lightweight: constructing MongoDB updates and returning quickly. Logging and metrics can be offloaded to asynchronous tasks if necessary. Load testing tools can be used to send many concurrent requests to the `create-checkout-session` endpoint to verify that your server and database can handle peak registration periods.

## 6. Common Pitfalls and Mitigation Strategies

### 6.1. Mismanaging API keys and environments

One of the most frequent pitfalls is mixing test and live environments or inadvertently exposing secret keys in client code or repositories. Stripe’s documentation emphasizes that secret keys must never be placed in frontend code, mobile apps, or public repositories, and that test and live keys are entirely separate; objects created in test mode, such as Products, cannot be used in live mode.[19][39] For the pondok registration system, ensure that all secret keys appear only in server-side environment variables, and that the Expo app does not contain any reference to `sk_` keys.

Another common issue arises when toggling between test and live modes on the Stripe dashboard while forgetting to update environment variables. If you create webhooks for test mode only, live mode events will not reach your webhook endpoint unless you register live endpoints as well.[38][39] Therefore, when you later move to live mode, you must both update `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` and create a live-mode webhook endpoint in the Stripe dashboard pointing to the same or equivalent backend URL.

Key rotation can also cause surprises. After rotating a secret key in the dashboard, ensure that your backend is redeployed with the new key before the old one expires. Stripe’s tools allow you to set a grace period during which old keys remain valid, but you must plan rotation carefully.[19] Keeping keys in a central configuration module, as shown earlier, makes it easier to update them without touching business logic.

### 6.2. Incorrect success URLs and deep link handling

A second common pitfall involves misconfigured success or cancel URLs. If the `success_url` uses `localhost` when the app is running on a physical device, Stripe’s redirect will fail or navigate to an unreachable page. Similarly, using a custom scheme that is not correctly registered in `app.json` will prevent deep links from opening the app.[6][22][6] For test mode, ensure that success and cancel URLs are valid HTTP URLs for web testing and that any custom schemes correspond to the Expo app’s `scheme` configuration.

Moreover, when combining deep links with Stripe flows, some developers mistakenly filter incoming URLs incorrectly. Stripe’s React Native issues tracker documents a case where developers were checking for specific substrings (such as `safepay`) in URLs and thereby ignoring valid Stripe return URLs, preventing callbacks from being handled.[42] The recommended approach is to rely on `handleURLCallback`’s boolean return value or equivalent functions to determine whether a URL is handled by Stripe, and to avoid manual heuristics that may break under future changes.[42] For a pure Checkout flow, handling deep links is simpler, but you must still parse query parameters such as `session_id` correctly.

To minimize errors, you can centralize URL parsing using Expo Linking’s `parse` function, which returns path and query parameters in a structured way. In addition, constructing success URLs through constants or helper functions on the backend reduces the risk of typos and inconsistent schemes.

### 6.3. Relying solely on client redirects instead of webhooks

Another serious pitfall is depending entirely on the client being redirected back from Checkout to mark payments as successful. Users may close the browser or lose connectivity; redirects may fail due to ad blockers or misconfigured URLs. Stripe therefore recommends using webhooks to receive authoritative notifications of payment events and relying on those for your internal records.[3][38] The FastAPI Stripe tutorial explicitly shows how to configure webhooks and notes that they are critical for production readiness.[3][3]

In the pondok registration system, MongoDB updates marking registrations as paid should occur in the webhook handler, not solely in the `success` endpoint. The `success` endpoint can be used to show confirmation or re-fetch details, but your internal systems must not assume that absence of a redirect implies absence of payment. Instead, they should rely on Stripe’s event history and your webhook-driven updates. In cases where webhooks fail, administrators can use Stripe’s dashboard to compare records and reconcile discrepancies.

### 6.4. Using client-supplied amounts or product data

Stripe and security experts consistently warn against trusting client-side amounts or product IDs, as a malicious user could modify the request payload to pay a lower amount or a different product.[3][19] For the registration fee, the FastAPI backend must determine the fee amount and description based on registration data or configuration, not based on values sent from the app. The code sample in this playbook adheres to that principle by reading `registration_fee_cents` from configuration or from the registration record in MongoDB.

To avoid mistakes, you should design the API contract such that the client never sends amount fields. If you must allow the client to select options that affect price (such as optional services), represent them as canonical option IDs that the backend maps to amount increments. In many school registration scenarios, fees are fixed or vary only by program, which simplifies this mapping.

### 6.5. MongoDB transaction and concurrency issues

When storing payment records in MongoDB, developers sometimes attempt to use multi-document transactions for operations such as clearing and re-populating collections, which can introduce complexity and performance issues. Discussions in the MongoDB community note that transactions should be kept small and that large operations like clearing and re-populating entire collections might be better handled by alternative strategies such as using a new collection and renaming it.[20] For the pondok registration app, most operations involve single-document updates or small upserts, which do not require multi-document transactions.

However, concurrency issues may still arise if multiple sessions exist for the same registration ID. For example, a parent might tap the pay button multiple times, creating several Checkout Sessions. The webhook handler should handle this gracefully by always marking the registration as paid when it receives a `checkout.session.completed` event, but you may want to enforce that only the first completed payment is accepted and subsequent payments are refunded manually or automatically. This business logic can be implemented by checking the current payment status in MongoDB before updating and adding notes to Stripe metadata for transparency.

### 6.6. React Native and Expo version mismatches

Finally, developers integrating Stripe into React Native apps may encounter issues when the Stripe React Native SDK version is incompatible with the React Native or Expo SDK version. Expo addresses this by providing an `expo install @stripe/stripe-react-native` command that selects a compatible version for your current Expo SDK.[4][15][6] If you install the Stripe SDK via `npm install` or `yarn add` with a generic version, you may face build errors or runtime warnings. In bare React Native projects, additional steps such as editing the Podfile’s minimum iOS deployment target might be required to satisfy Stripe’s requirements, as discussed in some GitHub issues.[15][34]

Because the pondok registration app uses Expo SDK 54, which supports autolinking for React Native modules and includes Stripe integration, you should rely on `expo install` and keep Expo CLI and EAS Build updated.[4][6][33] Regularly reviewing the Expo changelog and the Stripe React Native changelog helps avoid version drift and ensures that you benefit from bug fixes and security updates.

## 7. Conclusion and Recommended Next Steps

This playbook has walked through a complete, detailed integration of Stripe Checkout Sessions into an Expo SDK 54 React Native application with a FastAPI backend and MongoDB persistence, tailored for the use case of collecting registration fees for a *pondok pesantren*. The architecture emphasizes security and simplicity by delegating card entry entirely to Stripe’s hosted Checkout, leveraging FastAPI for API endpoints and webhook handling, and using MongoDB to track registration and payment status based on registration IDs. It demonstrates how to configure Settings via Pydantic, connect to MongoDB using PyMongo, create Checkout Sessions with server-side control over amounts and metadata, and process webhooks to reliably mark payments as completed.[3][3][27][29][37][38]

On the frontend, the report describes how to initialize an Expo project on SDK 54, configure deep linking and Stripe plugins in `app.json`, build a registration payment screen that calls the backend and opens the Checkout URL appropriately on mobile and web, and optionally prepare the app for future PaymentSheet integration via `StripeProvider`.[4][6][15][6] Deep linking is handled by Expo Linking, and careful configuration of `scheme` and success URLs ensures that users can be returned to the app after payment. Throughout, Stripe’s guidance on API key management, test versus live environments, and security best practices is applied, ensuring that secret keys reside only on the backend and that test card numbers are used for sandbox validation.[16][19][16][39]

The testing section outlines how to use Stripe test cards to simulate different payment outcomes, how to use the Stripe CLI to forward webhooks to a local FastAPI server and trigger events, and how to perform end-to-end tests on both mobile and web. It also highlights the importance of robust error handling and logging to differentiate user-facing errors from background issues and to avoid exposing sensitive information.[17][3][36][39] The analysis of common pitfalls underscores the need to avoid relying solely on client redirects, to never let the client control payment amounts, to configure success URLs and deep links correctly, to maintain accurate separation between test and live environments, and to keep dependencies aligned with Expo and Stripe’s supported versions.[3][19][20][6][34][38][42]

For the development team building this pondok registration system, recommended next steps include refining the MongoDB schema for registration and payment records to match existing school data models, adding an administrative dashboard that surfaces payment status and allows staff to search by registration ID or student name, and implementing additional webhook event handling for scenarios such as refunds or disputes. As the system approaches production readiness, you should work through Stripe’s go-live checklist to verify that API versions, webhooks, logging, and error handling conform to best practices, and then switch to live mode keys and endpoints.[39] Over time, you may consider extending the integration to PaymentSheet for fully in-app payment flows, adding support for Apple Pay and Google Pay, or integrating with accounting and messaging systems to automate receipt emails and financial reporting. By following the design, code patterns, and security recommendations outlined in this playbook, you can create a robust, maintainable, and user-friendly payment solution that simplifies registration fee collection for your school community.

---
Sources:
1. https://stripe.com
2. https://stripe.com/payments/checkout
3. https://www.fast-saas.com/blog/fastapi-stripe-integration/
4. https://expo.dev/changelog/sdk-54
5. https://docs.stripe.com/payments/accept-a-payment?payment-ui=mobile&platform=react-native
6. https://docs.expo.dev/versions/latest/sdk/stripe/
7. https://docs.stripe.com/sdks/react-native
8. https://www.youtube.com/watch?v=DZlAET7Tgx4
9. https://expo.dev/blog/mobile-app-payment-processing-best-practices
10. https://stripe.com/resources/more/registration-form-with-payment-101-what-they-are-and-how-to-use-them
11. https://docs.stripe.com/api/checkout/sessions
12. https://docs.stripe.com/api/checkout/sessions/create?lang=python
13. https://docs.stripe.com/api/checkout/sessions/create
14. https://n8n.io/integrations/mongodb/and/stripe/
15. https://github.com/stripe/stripe-react-native
16. https://docs.stripe.com/testing
17. https://www.youtube.com/watch?v=WkwoBEI-bN0
18. https://www.youtube.com/watch?v=J0tyxUV_omY
19. https://docs.stripe.com/keys
20. https://www.mongodb.com/community/forums/t/using-transactions-to-clear-and-re-populate-a-collection/285429
21. https://github.com/stripe/stripe-react-native/issues/543
22. https://docs.expo.dev/versions/latest/config/app/
23. https://github.com/stripe/stripe-react-native/issues/1933
24. https://dor.georgia.gov/motor-vehicles/drives-e-services
25. https://play.google.com/store/apps/details?id=io.ionic.sppmobile&hl=en_US
26. https://apiabroad.com/project/frequently-asked-questions/
27. https://docs.stripe.com/metadata
28. https://docs.stripe.com/payments/checkout/how-checkout-works
29. https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/insert/
30. https://fastapi.tiangolo.com/advanced/settings/
31. https://docs.stripe.com/api/payment_intents/retrieve
32. https://github.com/fastapi/fastapi/issues/774
33. https://docs.expo.dev/bare/installing-expo-modules/
34. https://github.com/stripe/stripe-react-native/issues/1280
35. https://adapty.io/docs/react-native-handle-errors
36. https://docs.stripe.com/error-codes
37. https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/mongoclient/
38. https://docs.stripe.com/webhooks
39. https://docs.stripe.com/get-started/checklist/go-live
40. https://github.com/stripe/stripe-react-native/issues/1253
41. https://fastapi.tiangolo.com/async/
42. https://github.com/stripe/stripe-react-native/issues/1101

`````

---
## Sample 2: Google Drive CSV upload — FastAPI backend

| | |
|---|---|
| HTTP status | 200 |
| **Latency** | **321.2 s** |
| **Total cost (from Perplexity's `usage.cost`)** | **$0.94294** |
| Cost breakdown | input $0.00051 · output $0.14414 · citation $0.04544 · reasoning $0.50285 · search $0.25 |
| Tokens | prompt 254 · completion 18,018 · citation 22,718 · reasoning 167,616 |
| Search queries run by Perplexity internally | 50 |
| Playbook length | 90,197 chars |
| Citations | 48 |

### Input — what our agent asked the tool (verbatim)

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

### Exact API request sent to Perplexity

```json
{
  "url": "https://api.perplexity.ai/chat/completions",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer pplx-REDACTED-MOCK-KEY",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "sonar-deep-research",
    "messages": [
      {
        "role": "system",
        "content": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
      },
      {
        "role": "user",
        "content": "Create a detailed integration playbook for INTEGRATION: Google Drive API integration for Python FastAPI backend\nREQUIREMENTS:\n- Upload CSV files to a specific shared Google Drive folder\n- Auto-sync functionality for daily/weekly exports\n- Real-time sync of time entry data\n- User will provide OAuth tokens/credentials\n- Need to handle authentication and file upload to shared folder ID\nCONSTRAINTS:\n- Must work with FastAPI backend\n- Need to support automated scheduled uploads\n- Handle OAuth2 authentication flow in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
      }
    ]
  }
}
```

### Exact output returned to our agent (verbatim, 93,261 chars)

This is the complete tool result the coding agent receives — the playbook exactly as Perplexity wrote it, with the citation URLs appended as a `Sources:` list by our tool layer. (It is then wrapped as `{"content": "<below>", "cost": 1.5}` — the `1.5` is an internal billing unit, unrelated to the Perplexity dollar cost.)

`````markdown
# Integration Playbook: Google Drive CSV Export with a FastAPI Backend and Expo React Native / React Native Web Clients

This report describes an end‑to‑end integration architecture and implementation for connecting a Python FastAPI backend to the Google Drive API in order to upload CSV exports into a specific shared Drive folder, support automated daily or weekly batch exports, and provide near real‑time synchronization of time entry data originating from Expo React Native and React Native Web clients. The design assumes that user‑side applications obtain OAuth2 credentials from Google and then hand off the relevant tokens or delegated credentials to the backend, which in turn uses the official Google API Python client to upload CSV files into a known shared folder based on its folder ID.[1][2][2] The backend persists time entry data in MongoDB, implements robust configuration management via environment variables, and uses a scheduling framework integrated with FastAPI for periodic exports.[8][20][21][5] On the frontend, Expo React Native uses the recommended Google authentication libraries and platform configuration to obtain tokens,[11][7][32] while React Native Web builds on the same app codebase and interacts with the FastAPI backend via cross‑origin HTTP requests secured by proper CORS configuration.[18][28] The report covers detailed installation instructions, Google Cloud configuration, full code samples for FastAPI, MongoDB integration, and Expo React Native clients, along with testing procedures, common pitfalls, and security best practices including safe storage of refresh tokens and appropriate Drive API scopes.[19][13][40]

## Conceptual Architecture and Requirements Mapping

### End‑to‑end architecture overview

The scenario in focus involves three principal components: an API backend written in Python using FastAPI, a data store implemented with MongoDB to hold time entry data, and client applications implemented with Expo React Native that can target native platforms (Android and iOS) as well as the web via React Native Web.[8][18] The backend is responsible for receiving time entry events from authenticated users, persisting them in MongoDB, aggregating or transforming these records into CSV exports, and then uploading these CSV files into a designated shared folder in Google Drive using the Google Drive REST API and the official Python client libraries.[1][2][2] The shared folder is identified by its unique folder ID, and proper permissions must be configured so that the Google identity used by the backend (either a service account or an end‑user OAuth identity) has write access to that folder.[13][4]

On the client side, Expo React Native applications must implement OAuth2 flows against Google to obtain access and refresh tokens, generally using the recommended Google sign‑in library for Expo or a PKCE‑based OAuth2 client such as `react-native-app-auth`.[11][7][32] These tokens can be stored securely on the device using AsyncStorage or other secure storage mechanisms, and they can be sent to the FastAPI backend either for verification and server‑side persistence, or simply as bearer tokens that allow the backend to perform Drive operations on behalf of the user depending on the architecture chosen.[27][46] For React Native Web, Expo’s web workflow allows the same React components to run in the browser, but requires special handling for cross‑origin HTTP requests to the FastAPI backend, making proper CORS configuration critical to avoid browser preflight failures.[18][28]

The backend must support both one‑off and automated uploads of CSV files to Google Drive. One‑off uploads include user‑initiated uploads of a CSV file via an HTTP endpoint that accepts file uploads as multipart form data using FastAPI’s `UploadFile` abstraction, which maps naturally to the way browsers and clients send files in form data.[16] Automated uploads include scheduled daily or weekly exports, which can be implemented inside the same FastAPI process using a background scheduler such as APScheduler that can trigger Python callables at regular intervals as long as the process is running.[5][5] Finally, a real‑time or near real‑time sync requirement implies that when time entries are created or updated through the FastAPI API, either the system updates a canonical CSV file in Drive immediately, or it accumulates changes that are pushed to Drive in short intervals via a high‑frequency scheduled task.

### Mapping requirements to design decisions

The need to upload CSV files to a specific shared folder means that the Drive integration must support passing a `parents` parameter with the target folder ID when calling `files().create()` in the Drive API, along with a MIME type of `text/csv` and `uploadType=media` or `uploadType=multipart` depending on whether metadata is sent together with the file data.[2][2][4] Because the folder is shared, permissions must be configured in Drive so that the authenticated user or service account has at least writer permissions on that folder; this typically involves sharing the folder with the email address of the service account or ensuring the signed‑in user is an organizer or writer on that shared drive.[13]

Auto‑sync functionality for daily or weekly exports suits scheduled jobs. FastAPI on its own does not provide a built‑in scheduler, but it can be combined with APScheduler’s `BackgroundScheduler`, which allows setting up cron‑like or interval triggers to run tasks at specified times, such as midnight every day or once per week, while the FastAPI process is running.[5][5][31] For more complex workloads, one could integrate a full task queue like Celery, using its `celery beat` scheduler to trigger periodic tasks that upload CSV files; however, for the purposes of this integration playbook, APScheduler is sufficient and keeps the deployment model simpler.[12][14][31]

Real‑time sync of time entry data suggests that the system should not wait for daily batch exports to update Drive. FastAPI can handle this by triggering background work either with FastAPI’s own background tasks or by publishing update events into a queue consumed by a worker process that updates Drive files; alternatively, small CSV fragments can be pushed directly to Drive whenever a time entry is created or updated. From the perspective of code complexity and clarity, this report focuses on a model where each time entry write triggers a synchronous write to MongoDB and an asynchronous update to Drive through a scheduled job or lightweight background task in the FastAPI process.

The constraint that “user will provide OAuth tokens/credentials” and that the system must “handle authentication and file upload to shared folder ID” leads to a separation of responsibilities: the client applications conduct the Google OAuth2 authorization flow and obtain tokens through platform‑appropriate libraries, while the backend validates, stores, and uses these tokens to build Google API clients using the `google-auth` and `google-api-python-client` libraries.[1][19][22] This respects Google’s guidance that OAuth tokens, especially refresh tokens, should be stored securely and reused to obtain new access tokens as needed, with refresh tokens placed in long‑term storage and never exposed in plaintext in logs or insecure storage.[19]

In terms of persistence, MongoDB is a natural fit for storing time entry documents and user OAuth token information, especially when combined with an asynchronous driver like Motor or the new PyMongo async API, which integrate well with FastAPI’s asynchronous request handling.[8][24] Since Motor is in deprecation in favor of PyMongo’s async API and will only receive limited support in coming years, it is prudent to design a data access layer that isolates MongoDB calls so that the system can later switch drivers without changing business logic.[24] Environment variables and Pydantic’s settings management, along with optional `.env` file support, allow the application to store sensitive configuration like MongoDB connection strings and Google OAuth credentials outside the codebase, which is a recommended best practice for both security and operational flexibility.[17][20][21]

The remainder of this report elaborates these design choices, provides explicit setup instructions and code samples, and examines testing strategies and common pitfalls in detail.

## Environment and Dependency Setup for FastAPI, MongoDB, and Google Drive

### FastAPI project initialization and dependency installation

To build the backend, one starts by creating a new Python project with a virtual environment, installing FastAPI along with Uvicorn as the ASGI server, and then adding Google and MongoDB dependencies. FastAPI includes Uvicorn when installed with the `standard` extras, and Uvicorn can be used as the production server by invoking `fastapi run` or by directly running Uvicorn with a `module:app` reference.[33] For example, the server can be started with a command similar to `uvicorn main:app --host 0.0.0.0 --port 8000`, where `main` is the Python module that defines `app = FastAPI()`.[33] This pattern is consistent whether the application is in local development or deployed in a container or cloud environment.

The Google Drive API integration relies on the official Python client libraries, specifically `google-api-python-client` for API calls, and `google-auth` and `google-auth-oauthlib` for OAuth2 credentials and token flows.[1][22] Google’s Python quickstart for Drive shows that these libraries can be installed using `python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`, after which the application can build a Drive API service object using user credentials or a service account.[1][22] For service account flows in other Google APIs, similar client libraries plus `oauth2client` can be used, although `google-auth` is preferred for modern code and many newer samples use it exclusively.[26]

For MongoDB, the TestDriven.io tutorial on FastAPI and MongoDB illustrates using Motor, an asynchronous MongoDB driver, with connection code like `client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)` where `MONGO_DETAILS` is a MongoDB connection string, and then obtaining a database and collection via `database = client.students` and `student_collection = database.get_collection("students_collection")`.[8] This pattern generalizes easily to a `time_entries` collection and a `users` or `tokens` collection. It is important to note that Motor is now officially deprecated in favor of the asynchronous API in the PyMongo driver as of 2025, and while it will continue to receive bug fixes until 2026 and critical bug fixes until 2027, new development should keep this deprecation timeline in mind.[24] Nonetheless, Motor remains compatible with FastAPI’s asynchronous code patterns, so it is still suitable for current projects, provided a migration path is planned.[24]

The environment variables for configuration can be managed via Pydantic’s settings utilities. FastAPI’s advanced settings tutorial demonstrates how to create a subclass of `BaseSettings` that defines typed configuration attributes (such as MongoDB URI or Google client IDs), and how to load these from environment variables or a `.env` file.[20] In Pydantic v2, settings management uses `pydantic-settings` and the `SettingsConfigDict` to declare the `.env` file path so that environment variables are automatically loaded into the application configuration.[20][21] For example, a `Settings` class can specify `model_config = SettingsConfigDict(env_file=".env")`, and the application can import a singleton instance using a dependency to avoid reloading environment variables for each request.[20]

The following Python code shows a foundational `config.py` module that integrates Pydantic settings with environment variables and `.env` support, exposing configuration for MongoDB, Google OAuth credentials, and Drive folder ID:

```python
# app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Time Entry Sync API"
    mongo_uri: str
    mongo_db_name: str = "time_entries_db"
    google_client_id: str
    google_client_secret: str
    google_project_id: str
    google_drive_folder_id: str
    google_oauth_redirect_uri: str
    google_oauth_scopes: str = "https://www.googleapis.com/auth/drive.file"
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

This design mirrors the recommended pattern in FastAPI’s documentation where a single `get_settings` dependency returns a cached `Settings` object per process, improving performance and allowing overrides during testing.[20] The `.env` file itself stores connection strings and secrets, which can be securely loaded into the environment in production or development; this practice echoes MongoDB’s own guidance on using environment variables to store connection URIs instead of embedding them directly in scripts.[17]

With configuration in place, one can define the FastAPI application, integrate the database, and later add routers for Drive uploads and time entry endpoints. A minimal `main.py` skeleton would import `FastAPI`, configure routes, and start Uvicorn using the `uvicorn main:app` pattern, as in various FastAPI examples and templates.[33][39][34]

### MongoDB setup and connection management

Setting up MongoDB for development can follow the pattern in the TestDriven.io FastAPI and MongoDB guide. That guide suggests installing MongoDB on the local machine, starting the `mongod` daemon process, and verifying the installation by connecting via the `mongo` shell.[8] For local development, the connection string might be `mongodb://localhost:27017`, which instructs the driver to connect to a MongoDB server listening on the default port of 27017 on the local host.[24] Once the server is running and accessible, an asynchronous driver such as Motor can connect using:

```python
# app/db.py
import motor.motor_asyncio
from .config import get_settings

settings = get_settings()
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.mongo_db_name]
time_entries_collection = database.get_collection("time_entries")
tokens_collection = database.get_collection("user_tokens")
```

This pattern is analogous to the `students` database example in TestDriven.io’s tutorial, which uses `MONGO_DETAILS` and obtains a `students_collection`.[8] In a production environment, rather than connecting to a local `mongod`, the application would often use MongoDB Atlas, a managed cloud service. The same tutorial describes creating an Atlas cluster, setting up a user, whitelisting IP addresses (locally for development and more tightly for production), and then obtaining a connection string like `mongodb+srv://user:password@cluster0.0reol.mongodb.net/students?retryWrites=true&w=majority` to be used as `MONGO_DETAILS`.[8] That connection string can be stored in `MONGO_URI` or `mongo_uri` in the `.env` file, and when deploying to platforms like Heroku, the `MONGO_DETAILS` environment variable can be set via configuration commands such as `heroku config:set MONGO_DETAILS="your_mongo_connection_url"`.[8]

MongoDB performance considerations, particularly around indexing, become important when the volume of time entries grows large. MongoDB’s indexing best practices recommend using compound indexes that align with query patterns, following an ESR (Equality, Sort, Range) rule where equality fields are indexed first, followed by sort keys, and then range fields, to optimize query performance.[42] For example, if time entries are frequently queried by user ID, then by date range, an index on `(user_id, date)` may accelerate queries used in daily or weekly export generation. The same best practices suggest using covered queries where possible, partial indexes when only certain subsets of documents are relevant, and multi‑key indexes for arrays, which may be useful if time entries store arrays like tags or project codes.[42]

Regardless of the driver chosen, the application should centralize collection access in utility functions to encapsulate persistence operations. For instance, one might define asynchronous functions for inserting, updating, and querying time entries and token documents, similar to the `retrieve_students` and `add_student` functions shown in the TestDriven.io tutorial.[8] Such a data access layer allows tests to mock database interactions more easily and supports driver migration if Motor is replaced with PyMongo’s async API in the future.[24]

### Google Drive client library installation and Python quickstart pattern

The Google Drive Python quickstart outlines the basic sequence for a Python application that interacts with Google Drive. It requires Python 3.10.7 or greater, pip, a Google Cloud project, and a Google account with Drive enabled.[1] The quickstart instructs developers to enable the Drive API in the Cloud console, configure the OAuth consent screen, and create OAuth 2.0 client credentials (initially for a desktop app in the quickstart) before downloading the credentials JSON file as `credentials.json`.[1] The Python client libraries are then installed with the command:

```bash
python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

and a sample `quickstart.py` uses `google.oauth2.credentials.Credentials` and `google_auth_oauthlib.flow.InstalledAppFlow` to authenticate and list files.[1] Although the quickstart focuses on a desktop client, the underlying pattern—creating `Credentials` objects with access and refresh tokens and building a Drive service via `build('drive', 'v3', credentials=creds)`—is applicable to server‑side code as well; the difference is that in the backend we typically obtain credentials from user tokens or a service account instead of launching a browser for user consent.[1]

To integrate with a FastAPI backend that receives tokens from client applications, we can bypass the interactive authorization steps from the quickstart and instead construct `Credentials` objects directly using the token data persisted in MongoDB. However, the quickstart’s use of Drive scopes is still a useful reference: it defines a `SCOPES` constant such as `["https://www.googleapis.com/auth/drive.metadata.readonly"]` to specify the required access.[1] In our case, because we need to create and upload CSV files, the scope `https://www.googleapis.com/auth/drive.file` or `https://www.googleapis.com/auth/drive` may be more appropriate, as it allows file creation in Drive or more general file access respectively.[6][19]

The Google OAuth2 documentation emphasizes that refresh tokens are long‑lived credentials that should be saved in secure storage and reused to obtain new short‑lived access tokens; refresh tokens should not be frequently re‑issued, and applications should avoid discarding them unnecessarily because re‑authorization flows can burden users.[19] This implies that when the backend receives tokens from client applications, it should store access and refresh tokens in a dedicated collection, encrypted if possible, and use Google’s `google-auth` library to handle token refresh automatically when building a Drive API client.[19]

The `google-auth-oauthlib` library integrates oauthlib with `google-auth` and can be installed with `pip install google-auth-oauthlib`; it is used in some Google samples to create flows and manage OAuth2 for Google APIs.[22] In our backend, we primarily need `google.oauth2.credentials.Credentials` for user tokens or `google.oauth2.service_account.Credentials` for service accounts, while `googleapiclient.discovery.build` from `google-api-python-client` constructs the Drive service object.[1][26]

### Expo React Native and React Native Web environment configuration

On the client side, Expo provides a unified workflow for building React Native applications that can target both native platforms and the web. Expo’s web documentation explains that web support can be enabled by adding React DOM, React Native Web, and the Expo Metro runtime as dependencies via a command like `npx expo install react-dom react-native-web @expo/metro-runtime`.[18] If the project does not yet use the `expo` package, it can be added via `npm install expo`, and the entry file should use `registerRootComponent` from Expo instead of `AppRegistry.registerComponent`, as shown in the documented transition from `AppRegistry.registerComponent(appName, () => App)` to `registerRootComponent(App)`.[18] Once these dependencies are installed and the entry file updated, the developer can start a development server with `npx expo start --web`, which will compile the React Native code and serve it to the browser.[18] For production, Expo supports exporting a static website via `npx expo export --platform web`, which can then be hosted like any other static site.[18]

Authentication flows in React Native applications often rely on React Navigation to manage screens and transitions between authentication screens and main app content. React Navigation’s documentation details a typical auth flow where the app loads authentication state from persistent storage (e.g., encrypted storage or AsyncStorage), decides whether the user is signed in, and either shows authentication screens or the main app stack accordingly.[46] The code uses context to store auth state and provides methods like `signIn` and `signOut`, and sets conditional screens in a single Stack navigator so that transitions from login to main app screens are smooth.[46]

For persistent storage of tokens on the device, React Native Async Storage provides an asynchronous, unencrypted key‑value store and is widely used for caching simple data like tokens, user preferences, or small configuration values.[27] Its GitHub documentation describes it as an asynchronous, persistent storage system for React Native, and outlines how tests can be run on Android or iOS by bundling the app and executing end‑to‑end tests.[27] In this architecture, Async Storage can be used to hold short‑lived access tokens and ID tokens, while more sensitive refresh tokens may be synced with the backend and removed from the client when possible, depending on the trust model.

Google authentication in Expo projects can use the `@react-native-google-signin/google-signin` library, which Expo’s documentation describes as a way to integrate Google authentication, including native sign‑in buttons and support for obtaining authorization to use Google APIs.[11] This library requires native code and thus cannot be used directly in the Expo Go client; instead, it requires a custom EAS build.[11] The documentation emphasizes that developers must configure their Google project for Android and iOS, which includes uploading the app to the Google Play Store for production, providing SHA‑1 certificate fingerprints from the Play Console, and configuring Firebase or Google Cloud Console accordingly.[11] For Android, the SHA‑1 fingerprint can be captured from the Play Console’s App Integrity section, either from upload key certificates or app signing key certificates.[11] For iOS, the developer must configure the iOS bundle identifier and associated settings in Firebase or Google Cloud; these details are typically captured in `GoogleService-Info.plist` for iOS and `google-services.json` for Android, which can either be checked into the repository or treated as secret files and injected into EAS builds.[11]

Alternative libraries such as `react-native-app-auth` provide a generic OAuth2 / OpenID Connect client for React Native that uses the Authorization Code with PKCE flow and can support providers like Google, Apple, and Facebook.[7][32] These libraries require platform‑specific configuration such as redirect URIs and app schemes in iOS `AppDelegate` and Android manifest files, as described in documentation that shows setting `appAuthRedirectScheme` in `android/app/build.gradle` and registering custom URL schemes for iOS.[7][32] In a configuration file like `config.json`, the library expects fields such as `issuer`, `clientId`, `redirectUrl`, and `scopes`, which are provided in the example for a SecureAuth authorization server but map similarly to Google OAuth configurations.[32]

The combination of Expo, React Navigation, Async Storage, and an OAuth library like `@react-native-google-signin/google-signin` or `react-native-app-auth` forms the backbone of the client‑side environment necessary for obtaining OAuth tokens to later hand off to the FastAPI backend.

## Google Cloud and Google Drive Configuration for Secure Uploads

### Enabling the Drive API and configuring OAuth consent

Before any Python code can call the Google Drive API, the corresponding API must be enabled on a Google Cloud project, and the OAuth consent screen must be configured so that users can authorize their data access. The Drive API quickstart for Python instructs developers to enable the API in the Google Cloud console by navigating to the project and toggling the Drive API, then configuring the OAuth consent screen with information such as the app name, user support email, and contact email.[1] The consent configuration includes choosing an internal or external audience type and accepting the Google API Services User Data Policy.[1] For internal applications within a Google Workspace organization, the audience can be set to Internal; for applications intended for general users, the audience type should be External, and additional steps like verification may be required depending on scopes and user count.[1]

The consent screen also allows specifying the scopes used by the application, though for a basic quickstart this step may be skipped initially.[1] In a production integration, it is crucial to add the minimal set of scopes required for the application to function, such as `https://www.googleapis.com/auth/drive.file` to allow file creation and access to files created by the app, or `https://www.googleapis.com/auth/drive` for more extensive access including reading and writing files across the user’s Drive.[19][6] Using narrower scopes aligns with the principle of least privilege and can reduce the consent burden on users.

In addition to consent, the application needs client credentials. For desktop quickstarts, the instructions involve creating OAuth 2.0 client IDs for a Desktop app, downloading the credential JSON, and renaming it to `credentials.json` in the working directory.[1] For mobile and web applications, different client types must be created, including Android, iOS, and Web application types, each with specific redirect URIs and platform‑specific configuration—these details are especially important for Expo and React Native projects that integrate Google Sign‑In.[11] For example, a Google client ID for Android will be associated with the app’s SHA‑1 fingerprint, whereas a web client ID will use HTTP or HTTPS redirect URLs that correspond to the backend or front‑end domain.

The OAuth 2.0 documentation describes the general flow for obtaining access and refresh tokens, and emphasizes that a refresh token allows the application to obtain new access tokens and must be saved in secure long‑term storage.[19] For mobile and JavaScript clients, Google encourages using the Authorization Code flow with PKCE instead of implicit flows, and server‑side components should store refresh tokens in databases like MongoDB with appropriate protection. If the backend uses a service account instead, the OAuth consent screen may be less prominent for end users, but the service account still needs proper configuration and trust relationships.

### Service accounts versus end‑user OAuth tokens

There are two main approaches to authenticating the backend to Drive: using end‑user OAuth tokens received from client apps, or using a separate service account that the backend controls. The case of a service account is illustrated in Google’s zero‑touch enrollment Python quickstart, which walks through creating a service account with a specific role, generating a JSON key file, and using `ServiceAccountCredentials.from_json_keyfile_name` to create credentials for API calls.[26] The steps include enabling the API, creating a service account, assigning it the “Service Account User” role, generating a JSON key, and moving the key file into the working directory as `service_account_key.json`.[26] The sample `quickstart.py` uses this file and a scope list to create an authorized API client and then call the zero‑touch enrollment API.[26]

Translating this pattern to Google Drive involves creating a service account with the appropriate Drive scopes and then sharing the target Drive folder with the service account’s email address so that it has permission to write into it.[13] Once shared, the backend can create Drive clients with the service account credentials without involving end‑users directly; this can simplify architecture for system‑wide exports where files are not tied to individual user drives.

However, the requirements described in this scenario state that “user will provide OAuth tokens/credentials” and “need to handle authentication and file upload to shared folder ID.” This implies that the application model is at least partially user‑delegated: users authenticate with Google via the mobile or web client, retrieve tokens, and then provide them to the backend, which uses them to upload into a folder that is shared among team members. In this user‑delegated model, a service account may still be used, but the tokens provided by users could instead be used for other Google APIs, while Drive uploads occur through the shared service account identity.

The integration playbook therefore must describe both possibilities and clarify where tokens and credentials are used. If end‑user tokens are used for Drive, then the target shared folder must be accessible by each user who uploads files; that is, the folder’s permissions must grant write access to those users in the domain or group.[13] If a service account is used for Drive, then the folder must be shared with the service account, and the backend uses the service account credentials exclusively for Drive uploads, while user tokens might be used only for authentication to the backend or other user‑specific operations.

### Permissions and sharing in the target Drive folder

Google Drive’s guide on sharing files, folders, and drives explains that every file, folder, and shared drive has associated `permissions` resources that specify the scope type (`user`, `group`, `domain`, or `anyone`) and a role (`owner`, `organizer`, `fileOrganizer`, `writer`, `commenter`, `reader`).[13] For example, a permission with `type=user` and `role=reader` grants read‑only access to a specific user, whereas `type=domain` with `role=commenter` grants everyone in a domain the ability to comment on a file.[13] For shared drives, there are additional nuances: to share a file in a shared drive, the user must have `role=writer`, `role=fileOrganizer`, or `role=organizer`, and the `writersCanShare` setting is treated as if it is always `true` in shared drives.[13]

To programmatically create a permission, one uses the `create` method on the `permissions` resource with a `fileId` path parameter and a request body specifying `type`, `role`, and optionally `emailAddress` or `domain` depending on the type.[13] The HTTP endpoint for creating a permission is `POST https://www.googleapis.com/drive/v3/files/FILE_ID/permissions`, and listing permissions uses the `list` method on the `permissions` resource.[13] However, in many integration scenarios, it is sufficient to configure sharing for the target folder manually in the Google Drive web UI, sharing the folder with the relevant users or service accounts. When using a service account, the usual approach is to share the folder with the service account’s email address, ensuring that the service account can create files in that folder.

The Latenode community discussion about transferring CSV files to Google Drive using Python notes that for uploading into a folder, one can obtain the folder ID from the Drive URL after `/folders/`, and then use `files().create()` with the `parents` parameter set to a list containing that folder ID.[4] It also emphasizes explicitly specifying the MIME type, such as `text/csv`, to avoid unexpected behavior or formatting issues.[4] This direct use of the folder ID and MIME type specification aligns with the official Drive upload guide’s description of setting headers like `Content-Type` and, in API clients, metadata fields like `mimeType`.[2][2]

### Drive upload types and upload configuration

The Google Drive upload guide describes three types of uploads that can be performed: simple uploads, multipart uploads, and resumable uploads.[2][2] A simple upload involves creating a `POST` request to the method’s `/upload` URI with `uploadType=media` and sending the file data as the request body, with headers including `Content-Type` set to the file’s MIME type and `Content-Length` set to the byte count (unless using chunked transfer encoding).[2][2] In such simple uploads, basic metadata is created and some attributes are inferred from the file, such as MIME type or modification time.[2][2] The guide suggests using simple uploads for small files where metadata is not critical.[2][2]

Multipart uploads use `uploadType=multipart` and allow sending metadata and file data together in a single request, with the request body structured as `multipart/related` content and boundaries separating parts.[2] Resumable uploads, with `uploadType=resumable`, are designed for large files and allow uploads to be paused and resumed via a session URI returned by an initiation request that responds with `200 OK` and a `Location` header specifying the session URI.[2] For CSV exports, which are typically small to moderate in size, simple or multipart uploads are usually sufficient.

In Python, the `google-api-python-client` library abstracts much of this complexity. The developer can use `MediaIoBaseUpload` or `MediaFileUpload` to wrap the file data and then call `drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()` with appropriate parameters. The `file_metadata` dictionary includes `name` and `parents`, with `parents` set to a list containing the target folder ID, as recommended in practice and described in the Latenode discussion.[4] The `mimeType` can be set to `"text/csv"` in either the metadata or the media wrapper. For this integration playbook, the FastAPI backend will implement this upload logic in a function that takes a file‑like object or bytes and uploads it to the designated folder.

Drive APIs enforce quotas and rate limits, and the Drive labels usage limits page describes an exponential backoff algorithm as the recommended strategy for handling time‑based errors and rate limit responses.[44] Exponential backoff involves retrying failed requests with increasingly longer wait times, e.g., waiting `1 + random` seconds, then `2 + random`, then `4 + random`, and so on, up to a maximum backoff time, before stabilizing the wait time and eventually giving up after a maximum number of retries.[44] The `google-api-core` library offers a retry decorator that can be used to add exponential backoff behavior to RPC calls, enabling automatic retries for transient errors like network interruptions or `429 Too Many Requests` responses.[38] Combining this with careful use of Drive quotas—600 read requests and 300 write requests per second per user per project as described for Drive Labels—helps ensure robust operation.[44]

Having now established the Google Cloud configuration, we can turn to the concrete implementation of the FastAPI backend, starting with configuration and database wiring and progressing to authentication and Drive upload endpoints.

## FastAPI Backend Implementation: Configuration, Time Entries, and Drive Uploads

### FastAPI application structure and settings dependency

A typical FastAPI backend for this integration can be structured around a main application module, configuration module, database module, and routers for time entries and Drive uploads. The main module imports FastAPI, includes routers, configures CORS middleware, and sets up application startup and shutdown handlers. CORS is necessary because the React Native Web client will run in a browser on an origin different from the backend, and modern browsers enforce CORS restrictions that require the backend to explicitly permit cross‑origin requests.[28] FastAPI provides a `CORSMiddleware` that can be configured with a list of allowed origins, whether credentials are allowed, allowed methods, and allowed headers.[28] For example, one can import `CORSMiddleware` from `fastapi.middleware.cors`, create a list of allowed origins like `"http://localhost:19006"` or `"http://localhost:3000"`, and then add the middleware to the app with:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name)

origins = [
    "http://localhost:19006",
    "http://localhost:3000",
    "https://your-production-web-origin.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

The CORS documentation explains that using `"*"` as the allowed origins is possible but will disallow certain types of communication, particularly those involving credentials like cookies or authorization headers; for full support with credentials, the allowed origins should be specified explicitly.[28] With CORS in place, the backend can serve both mobile and web clients correctly.

The `config.py` module shown earlier defines a `Settings` class that loads environment variables from `.env`, as described in FastAPI’s settings management documentation.[20] Using the `get_settings` dependency in endpoints allows the backend to access configuration such as MongoDB URI and Google Drive folder ID without scattering environment variable access across the codebase. A typical pattern is to create a dependency function:

```python
from fastapi import Depends

def get_config(settings: Settings = Depends(get_settings)) -> Settings:
    return settings
```

Then, path operation functions can include `settings: Settings = Depends(get_config)` to access configuration where needed. Because `get_settings` is decorated with `lru_cache`, it reads the `.env` file once at startup, and subsequent calls are served from memory, reducing overhead.[20]

### Time entry models and MongoDB schema

Time entry data can be modeled with Pydantic to ensure validation and serialization. For example, a `TimeEntry` model might contain fields like `user_id`, `project_id`, `start_time`, `end_time`, `duration_minutes`, and `description`. FastAPI uses Pydantic models to parse and validate request bodies, and it can automatically generate OpenAPI documentation based on these models.[48] The use of `Field` allows additional metadata and validation to be specified, such as requiring a positive number for the duration, or providing titles and descriptions for documentation.[48]

Here is an example of a Pydantic model for time entries:

```python
# app/models.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TimeEntryCreate(BaseModel):
    user_id: str = Field(..., description="User identifier")
    project_id: str = Field(..., description="Project identifier")
    start_time: datetime = Field(..., description="Start time in ISO8601")
    end_time: datetime = Field(..., description="End time in ISO8601")
    description: Optional[str] = Field(default=None, max_length=500)


class TimeEntryDB(TimeEntryCreate):
    id: str = Field(..., description="Database identifier")
    duration_minutes: int = Field(..., gt=0, description="Computed duration in minutes")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
```

The `Field` function is used similarly to `Query`, `Path`, and `Body` for declaring additional metadata and validation, and FastAPI will include this information in the generated JSON Schema.[48] The database layer can then convert between Pydantic models and MongoDB documents, storing `TimeEntryDB` objects in the `time_entries` collection.

Inserting time entries into MongoDB with Motor is done via asynchronous operations. For instance:

```python
# app/db_time_entries.py
from datetime import datetime
from bson import ObjectId
from .db import time_entries_collection
from .models import TimeEntryCreate, TimeEntryDB


async def create_time_entry(data: TimeEntryCreate) -> TimeEntryDB:
    start = data.start_time
    end = data.end_time
    duration_minutes = int((end - start).total_seconds() // 60)
    now = datetime.utcnow()
    doc = {
        "user_id": data.user_id,
        "project_id": data.project_id,
        "start_time": start,
        "end_time": end,
        "description": data.description,
        "duration_minutes": duration_minutes,
        "created_at": now,
        "updated_at": now,
    }
    result = await time_entries_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return TimeEntryDB(**doc)
```

Although the Python `datetime` module documentation notes that `datetime.utcnow()` returns a naive datetime and recommends using `datetime.now(timezone.utc)` for timezone‑aware timestamps, using `utcnow` is still common for UTC timestamps in many codebases, with the caveat that the naive datetime represents UTC time.[47] If timezone awareness is essential, the code can be updated to use `datetime.now(timezone.utc)` and a timezone‑aware field type instead.

Similar functions can be created to query entries by user and date range, which will be used when generating CSV exports. Indexing on fields like `user_id` and `start_time` improves query performance for these operations, and the MongoDB indexing best practices can be applied to design appropriate compound indexes.[42]

### Accepting file uploads with FastAPI and preparing CSV content

FastAPI’s `UploadFile` abstraction is used to receive files from clients. The documentation explains that file uploads are sent as form data, and using `UploadFile` allows the server to access the file via a spooled temporary file rather than loading it entirely into memory, which is more efficient for large files.[16] The `UploadFile` object has attributes like `filename`, `content_type`, and `file`, where `file` is a file‑like object.[16] Path operation functions can declare parameters of type `UploadFile` with `File()` to indicate that the data should be interpreted as file uploads in form data.[16]

A basic FastAPI endpoint to accept CSV file uploads from a client and then forward them to Drive might look like this:

```python
# app/routes/drive_upload.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from .config import Settings, get_settings
from .db_tokens import get_user_tokens
import io

router = APIRouter(prefix="/drive", tags=["Drive"])


def build_drive_service_from_tokens(access_token: str, refresh_token: str, settings: Settings) -> object:
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        scopes=[settings.google_oauth_scopes],
    )
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
    service = build("drive", "v3", credentials=creds)
    return service


@router.post("/upload-csv")
async def upload_csv_to_drive(
    user_id: str,
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
):
    if file.content_type not in ("text/csv", "application/vnd.ms-excel"):
        raise HTTPException(status_code=400, detail="Invalid file type, expected CSV")
    tokens = await get_user_tokens(user_id)
    if tokens is None:
        raise HTTPException(status_code=401, detail="No Google tokens for user")
    drive_service = build_drive_service_from_tokens(tokens.access_token, tokens.refresh_token, settings)
    file_bytes = await file.read()
    media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype="text/csv", resumable=False)
    file_metadata = {
        "name": file.filename,
        "parents": [settings.google_drive_folder_id],
        "mimeType": "text/csv",
    }
    uploaded = drive_service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
    return {"file_id": uploaded["id"], "webViewLink": uploaded.get("webViewLink")}
```

This code demonstrates several important aspects. First, it enforces that the uploaded file has a content type consistent with CSV, either `text/csv` or (for some browsers) `application/vnd.ms-excel`. Second, it retrieves the stored tokens for the given `user_id` from MongoDB, raising an HTTP 401 error if none are found; FastAPI’s `HTTPException` is the recommended way to return error responses with status codes and details, rather than returning error objects directly.[43] Third, it constructs a `Credentials` object using the access and refresh tokens and client credentials, refreshes the access token if it is invalid and a refresh token is present, and then builds a Drive service using `build("drive", "v3", credentials=creds)` as shown in the Drive quickstart.[1] Finally, it wraps the file bytes in a `MediaIoBaseUpload` object, sets the metadata including the `parents` field with the shared folder ID, and executes `files().create()` to upload the CSV.[2][2][4]

The use of `parents` with the folder ID corresponds directly with the recommendation from practitioners who note that the folder ID can be taken from the Drive URL and passed as a parent when creating files.[4][15] Setting the `mimeType` to `text/csv` ensures that Google Drive identifies the file correctly; the Latenode discussion explicitly mentions that specifying the MIME type explicitly avoids CSV formatting headaches.[4] Though the underlying HTTP semantics may include headers like `Content-Type` and `Content-Length`, the Python client handles these details internally when given a `MediaIoBaseUpload` object.[2][2]

If the backend uses a service account for Drive uploads rather than user tokens, the `build_drive_service_from_tokens` function would instead use `google.oauth2.service_account.Credentials.from_service_account_file` and the `service_account_key.json` file as in the zero‑touch example, but with Drive scopes and no need for access/refresh tokens.[26]

### Token storage and backend authentication

To use user‑delegated OAuth tokens in the backend, the system must store them securely and associate them with user identities in the application. The token documents in MongoDB might contain fields like `user_id`, `access_token`, `refresh_token`, `expiry`, and `scopes`. The `db_tokens` module would define asynchronous functions such as `get_user_tokens(user_id: str)` and `save_user_tokens(user_id: str, tokens: dict)`.

For example:

```python
# app/db_tokens.py
from datetime import datetime
from .db import tokens_collection


class UserTokens:
    def __init__(self, user_id: str, access_token: str, refresh_token: str, expiry: datetime):
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expiry = expiry


async def get_user_tokens(user_id: str) -> UserTokens | None:
    doc = await tokens_collection.find_one({"user_id": user_id})
    if not doc:
        return None
    return UserTokens(
        user_id=doc["user_id"],
        access_token=doc["access_token"],
        refresh_token=doc["refresh_token"],
        expiry=doc["expiry"],
    )


async def save_user_tokens(user_id: str, tokens: dict) -> None:
    doc = {
        "user_id": user_id,
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"),
        "expiry": tokens.get("expiry"),
        "scopes": tokens.get("scope"),
        "updated_at": datetime.utcnow(),
    }
    await tokens_collection.update_one({"user_id": user_id}, {"$set": doc}, upsert=True)
```

The backend can expose an endpoint like `/auth/google/tokens` that the client calls after it completes the OAuth2 flow and obtains an access token and refresh token from Google via the mobile library. The endpoint would accept a request body containing the tokens and the user’s application identifier (or use a previously authenticated session) and persist the tokens via `save_user_tokens`. Optionally, the backend can verify the ID token (if provided) using Google’s token verification APIs, similar to the Node.js code shown in the React Native OAuth2 guide, which uses `google-auth-library`’s `OAuth2Client` and `verifyIdToken` to authenticate tokens and obtain user info.[7] In Python, equivalent verification can be done with `google.oauth2.id_token.verify_oauth2_token`.

An example endpoint skeleton:

```python
# app/routes/auth_google.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from .config import get_settings
from .db_tokens import save_user_tokens

router = APIRouter(prefix="/auth/google", tags=["Auth"])


class GoogleTokenPayload(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str | None = None
    id_token: str | None = None


@router.post("/tokens")
async def receive_google_tokens(payload: GoogleTokenPayload):
    settings = get_settings()
    if payload.id_token:
        try:
            idinfo = id_token.verify_oauth2_token(
                payload.id_token,
                requests.Request(),
                settings.google_client_id,
            )
            if idinfo["sub"] != payload.user_id:
                raise HTTPException(status_code=400, detail="User mismatch in token")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID token")
    await save_user_tokens(payload.user_id, payload.model_dump())
    return {"status": "ok"}
```

This approach parallels the backend validation example in the React Native OAuth2 guide, which shows verifying a Google ID token using `google-auth-library` in Node.js.[7] Storing tokens this way ensures that the backend can later construct Drive API clients with appropriate credentials for file uploads, and also allows the backend to update or revoke tokens as needed.

For authentication to the backend itself, one can implement a JWT‑based scheme, using FastAPI’s security utilities for OAuth2 with password and bearer tokens, as described in the FastAPI security tutorial.[6][37] That tutorial explains how to define `OAuth2PasswordBearer` and `OAuth2PasswordRequestForm` dependencies, handle login endpoints that return JWTs, and secure endpoints by requiring bearer tokens.[6][37] In this integration, the backend’s authentication mechanism is orthogonal to Google tokens; the backend may treat Google tokens as a secondary auth method or just as credentials for Drive, while JWTs or session tokens handle authentication of API calls. For brevity, this report focuses on Google tokens for Drive operations and assumes an existing or simple backend auth mechanism.

### Generating CSV exports from MongoDB data

Daily or weekly exports require the backend to query time entries for a time window and convert them into CSV format. Python’s `csv` module or pandas can be used for this purpose. While pandas’ documentation on reading CSV files with `pd.read_csv('data.csv')` demonstrates CSV handling from file to dataframe and back,[35] it is often simpler to use the standard `csv` module when generating CSVs from Python data structures for streaming to Drive. To maintain clear separation of concerns, a function can be defined that accepts a list of time entry records and returns bytes of CSV content.

A simple implementation could be:

```python
# app/csv_export.py
import csv
import io
from typing import List, Dict


def time_entries_to_csv(rows: List[Dict]) -> bytes:
    if not rows:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["user_id", "project_id", "start_time", "end_time", "duration_minutes", "description"])
        return output.getvalue().encode("utf-8")

    output = io.StringIO()
    fieldnames = ["user_id", "project_id", "start_time", "end_time", "duration_minutes", "description"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                "user_id": row["user_id"],
                "project_id": row["project_id"],
                "start_time": row["start_time"].isoformat(),
                "end_time": row["end_time"].isoformat(),
                "duration_minutes": row["duration_minutes"],
                "description": row.get("description") or "",
            }
        )
    return output.getvalue().encode("utf-8")
```

If the data set is large and memory usage is a concern, generating CSVs in a streaming fashion may be necessary. FastAPI supports streaming responses via `StreamingResponse`, as described in the custom response documentation, which allows the application to stream file content as it is generated, though static exports to Drive can often be generated in memory for small to medium data sets.[29] For this integration, the total volume of data per export is assumed to fit comfortably in memory.

Once a CSV byte stream is available, it can be wrapped in a `MediaIoBaseUpload` object and sent to Drive as shown earlier. Alternatively, the CSV could be written to a temporary file, and `MediaFileUpload` could be used with the file path. Before writing to a local file, Python’s file handling best practices recommend checking whether a file exists using `pathlib.Path.is_file()` or handling `FileNotFoundError` in a `try/except` block, but in this scenario, local file existence checks are not essential because the CSV files are ephemeral.[41]

### Scheduled exports with APScheduler integrated into FastAPI

To implement daily or weekly exports, one approach is to integrate the Advanced Python Scheduler (APScheduler) with the FastAPI application. APScheduler’s `BackgroundScheduler` runs tasks in the background in the same process, and tasks can be scheduled using interval or cron triggers that specify when and how often they should run.[5][5][31] Sentry’s answer on scheduling tasks with FastAPI shows a minimal FastAPI application where a `BackgroundScheduler` is created, a `CronTrigger` is configured for midnight every day, and the scheduler is started in the application’s lifespan context.[5][5] The example demonstrates using an `asynccontextmanager` to set up and tear down the scheduler, ensuring it shuts down properly when the application stops.[5]

An adaptation for daily CSV export might look like this:

```python
# app/scheduler.py
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from .db_time_entries import get_entries_for_period
from .csv_export import time_entries_to_csv
from .config import get_settings
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
import io
import logging

logger = logging.getLogger(__name__)


def perform_daily_export():
    settings = get_settings()
    # For illustration, assume a service account is used for exports
    creds = ServiceAccountCredentials.from_service_account_file(
        "service_account_key.json",
        scopes=[settings.google_oauth_scopes],
    )
    service = build("drive", "v3", credentials=creds)
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=1)
    rows = get_entries_for_period_sync(start_date, end_date)  # wrapper around async function
    csv_bytes = time_entries_to_csv(rows)
    media = MediaIoBaseUpload(io.BytesIO(csv_bytes), mimetype="text/csv", resumable=False)
    file_metadata = {
        "name": f"time_entries_{start_date.isoformat()}_{end_date.isoformat()}.csv",
        "parents": [settings.google_drive_folder_id],
        "mimeType": "text/csv",
    }
    uploaded = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    logger.info("Uploaded daily export file %s", uploaded["id"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=0, minute=0)  # midnight UTC every day
    scheduler.add_job(perform_daily_export, trigger)
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
```

The Sentry guide explains that `BackgroundScheduler` can handle multiple tasks with different triggers, and `CronTrigger` uses cron‑like syntax to schedule jobs, such as running at midnight every day or at specific times like every second Tuesday at 12:13 pm.[5][5] It also notes that `IntervalTrigger` can be used to run tasks at fixed intervals, for example every 24 hours starting from a given date.[5] The Martin Heinz blog further elaborates on scheduling recurring jobs with Python and compares various libraries and their capabilities; APScheduler emerges as a flexible choice for cron‑like and interval scheduling.[31]

In the above code, `perform_daily_export` uses a service account for demonstration; if end‑user tokens are used for exports, the function would need to aggregate time entries per user and build user‑specific Drive clients using stored tokens. Additionally, the function should implement retry logic with exponential backoff for Drive upload calls, either manually or by using `google-api-core`’s `Retry` functionality.[38][44] For instance, an upload call can be wrapped in a decorator that retries on transient HTTP errors, capping the maximum backoff and retry attempts as recommended by Google’s guidance on exponential backoff.[44]

Using logging inside scheduled jobs is crucial for observability. Python logging best practices suggest creating module‑level loggers using `logging.getLogger(__name__)`, setting appropriate logging levels, and possibly using `logging.config.dictConfig` for structured configuration.[40] The Coralogix article notes that log levels like `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL` should be used consistently to indicate event severity, and that global logging settings can be adjusted using `logging.disable` to suppress low‑level logs when necessary.[40] In distributed systems, adding correlation IDs to logs can help trace related events across components, and FastAPI’s discussion on correlation ID middleware suggests using middleware or exception handlers to attach unique request IDs to responses and logs.[45]

With scheduled jobs in place, the backend can now produce daily or weekly CSV exports automatically. The next step is to implement real‑time or near real‑time sync for time entry changes.

### Real‑time sync strategies and background processing

Real‑time synchronization of time entry data to Google Drive can be interpreted in several ways. In this context, a straightforward approach is to trigger Drive updates whenever time entries are created or updated in MongoDB, rather than waiting for daily exports. For instance, when a `POST /time-entries` endpoint is called, the backend can insert the time entry into MongoDB and immediately, or via a background task, generate a small CSV or update an existing CSV file in Drive.

FastAPI supports background tasks that run after the response is sent, using the `BackgroundTasks` class. While not as robust as a full task queue like Celery, background tasks can handle lighter workloads and are simple to set up.[14] The Celery and FastAPI guide notes that Celery is better suited for heavy background computations or tasks that must survive process restarts, while FastAPI’s `BackgroundTasks` runs only as long as the process is alive.[14] Since this integration already uses APScheduler for scheduled tasks, adding background tasks for near real‑time operations is consistent with this pattern.

An example endpoint for creating a time entry and triggering a background Drive update:

```python
# app/routes/time_entries.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from .models import TimeEntryCreate, TimeEntryDB
from .db_time_entries import create_time_entry
from .drive_realtime import upload_single_entry_csv

router = APIRouter(prefix="/time-entries", tags=["Time Entries"])


@router.post("/", response_model=TimeEntryDB)
async def create_time_entry_endpoint(
    entry: TimeEntryCreate,
    background_tasks: BackgroundTasks,
):
    saved = await create_time_entry(entry)
    background_tasks.add_task(upload_single_entry_csv, saved)
    return saved
```

The `upload_single_entry_csv` function might build a very small CSV containing just the new entry, or it could append the entry to a daily file in Drive; implementing appends with Drive requires careful handling of file download and re‑upload or using Google Sheets instead of plain CSV. For the sake of this playbook, generating small per‑entry CSV files in a designated folder is a simple approach.

The Celery integration guide describes how to offload long‑running tasks to Celery workers and schedule tasks using `celery beat`, which is useful when tasks might exceed the lifespan of a request or require horizontal scalability across multiple workers.[12][14] However, for moderate workloads and simpler deployments, APScheduler and FastAPI’s background tasks are often sufficient. If the system grows and requires more scalability, the design can be refactored to use Celery for both periodic exports and real‑time updates.

With the backend implemented, the remaining pieces involve client‑side integration in Expo React Native and React Native Web, ensuring that OAuth2 flows and HTTP calls are correctly configured.

## Expo React Native and React Native Web Integration

### Implementing Google OAuth2 in Expo React Native

Expo’s guide on using Google authentication demonstrates how to integrate the `@react-native-google-signin/google-signin` library into an Expo project using a config plugin.[11] This library provides a high‑level interface for Google sign‑in on React Native, including native sign‑in buttons and methods to obtain user identity and tokens, and it supports authenticating the user as well as obtaining authorization to use Google APIs.[11] Because the library requires custom native code, it cannot run inside Expo Go; it must be used in a custom EAS build.[11]

The setup involves installing the library according to its documentation, configuring the app’s Google project for Android and iOS, and providing platform‑specific parameters like SHA‑1 fingerprints for Android and bundle identifiers for iOS in Firebase or Google Cloud Console.[11] For Android, the SHA‑1 certificate fingerprints can be obtained from the Google Play Console under Release → Setup → App Integrity → Upload key certificate or App signing key certificate, depending on whether the fingerprint is for an uploaded APK or a production app.[11] For iOS, the developer must configure Firebase or Google Cloud accordingly and manage `GoogleService-Info.plist` files.[11]

The `GoogleSignin` API typically requires configuration at app startup, specifying the web client ID and other parameters. For example:

```typescript
// src/services/googleAuth.ts
import { GoogleSignin } from '@react-native-google-signin/google-signin';

export function configureGoogleSignIn() {
  GoogleSignin.configure({
    webClientId: 'YOUR_WEB_CLIENT_ID.apps.googleusercontent.com',
    offlineAccess: true,
    scopes: ['openid', 'profile', 'email', 'https://www.googleapis.com/auth/drive.file'],
  });
}
```

The `offlineAccess: true` option instructs the library to request refresh tokens, which are necessary for long‑term access to Drive APIs.[19] After the user taps a sign‑in button, `GoogleSignin.signIn()` can be executed to prompt the user for credentials and obtain an object containing `idToken`, `accessToken`, and user profile information. These tokens can be stored in Async Storage for subsequent sessions.[27]

Alternatively, `react-native-app-auth` can be used as an OAuth2 client, as described in the OneUptime blog on implementing OAuth2 in React Native and the SecureAuth AppAuth tutorial.[7][32] This library uses an `authorize` function that accepts a configuration object including `issuer`, `clientId`, `redirectUrl`, and `scopes`, and returns tokens upon successful authentication. The SecureAuth tutorial demonstrates a `config.json` file with fields like `issuer`, `clientId`, `redirectUrl`, and `scopes`, and shows calling `authorize(config)` inside a React component.[32] For Google, the configuration would point to `https://accounts.google.com` as the issuer, the Google client ID, and a redirect URL such as `com.yourapp.auth:/oauth2redirect/google`, with scopes including `openid`, `profile`, `email`, and `https://www.googleapis.com/auth/drive.file` if Drive access is needed.[7]

The AppAuth example further illustrates that on Android, `appAuthRedirectScheme` must be specified in `android/app/build.gradle` as the URL scheme for the redirect, and on iOS, `AppDelegate` must implement methods to handle the redirect and pass URLs back to the AppAuth authorization flow.[32][7] These platform‑specific changes ensure that the OAuth2 flow can redirect from the system browser back into the application.

Once tokens are obtained, they can be stored in Async Storage using keys like `@auth_tokens` and `@auth_user`, similar to the storage patterns shown in the AppAuth service example where Async Storage is used to persist both tokens and user information.[7][27] The application can then use React Navigation’s auth flow patterns to conditionally show login screens or main app screens depending on whether valid tokens exist in storage, as described in React Navigation’s authentication documentation.[46]

### React Native Web build and backend connectivity

Expo’s web workflow allows the same React Native codebase to be compiled to the web, with support for static exports suitable for deployment to web hosting. The documentation on developing websites with Expo outlines how to install `react-dom`, `react-native-web`, and `@expo/metro-runtime`, adjust the entry file to use `registerRootComponent`, and start the dev server with `npx expo start --web`.[18] This process transforms the React Native components into a web app that can run in the browser, though some native modules that rely on device hardware or platform‑specific APIs may not function on the web unless replaced with web equivalents.

When calling the FastAPI backend from the web app, CORS must be configured to allow requests from the web origin. FastAPI’s CORS tutorial explains that cross‑origin requests from a frontend running on one origin (e.g., `http://localhost:8080`) to a backend on another origin (e.g., `http://localhost:8000`) require the backend to handle `OPTIONS` preflight requests and respond with appropriate CORS headers, including `Access-Control-Allow-Origin` set to the frontend origin.[28] The `CORSMiddleware` configuration described earlier handles these details by specifying allowed origins, methods, headers, and whether credentials are allowed.[28]

In the web environment, Google authentication needs to be implemented in a way compatible with browsers. The `@react-native-google-signin/google-signin` library does not support web, so a separate approach may be necessary, such as using Google’s JavaScript Identity Services on the web or performing a web‑based OAuth2 flow through the backend. One pattern is to direct web users to a backend endpoint like `/auth/google/login`, which initiates an OAuth2 authorization request to Google with appropriate redirect URIs, and then handle the callback at `/auth/google/callback`, where the backend exchanges the code for tokens and either stores them in the backend or passes session information to the frontend via cookies or query parameters. While this pattern is common, the specifics are not detailed in the provided search results, so this report refrains from prescribing the exact web OAuth implementation and focuses instead on the mobile OAuth flows and the backend’s consumption of tokens.

From the perspective of HTTP calls to the backend, both the mobile app and the web app can use standard HTTP clients like `fetch` or Axios to call endpoints like `/time-entries` and `/drive/upload-csv`. When uploading CSV files from the web app, the app can create a `FormData` object, append a `file` field with a `Blob` or `File`, and send it to the backend; FastAPI will receive it as an `UploadFile`, as described in the file upload documentation.[16] Handling errors returned by the backend, such as HTTP 400 for invalid file type or HTTP 401 for missing tokens, can be implemented in the client to show appropriate user messages.

React Navigation’s auth flow documentation suggests that the app should load stored auth state from persistent storage at startup, then present either auth or main screens based on the presence of valid tokens.[46] In this integration, the React app can also check with the backend whether it has stored Google tokens for the user, and if not, trigger a Google sign‑in flow. Upon successful sign‑in, the app can call `/auth/google/tokens` to store tokens in the backend, and then proceed to use features like manual Drive uploads or real‑time time entry sync.

### Persisting auth state and handling token refresh on the client

While the backend is responsible for using refresh tokens for Drive operations, the client must also manage tokens for its own interaction with the backend, which may involve JWTs or other tokens. React Navigation’s documentation notes that the app should track a loading state while restoring tokens from storage, then set an `isSignedIn` flag accordingly.[46] It also emphasizes that when using conditions like `isSignedIn` to determine which screens are available, the navigation state should be configured in a way that avoids back navigation into auth screens once the user is signed in, such as by using a single Stack navigator and placing the conditional logic inside, rather than swapping navigators entirely.[46]

The React Native Async Storage library’s documentation states that it is an asynchronous, unencrypted persistent key‑value storage system for React Native.[27] Though not encrypted, it is sufficient for storing non‑critical tokens when additional layers of security, like OS keychains, are not required. When testing on Android and iOS, the library suggests running bundling and end‑to‑end tests with commands like `yarn bundle:android`, `yarn build:e2e:android`, and `yarn test:e2e:android`, though these commands are for the library itself rather than the app using it.[27] For this integration, developers can design their own tests for verifying that tokens are stored and retrieved correctly, and that the app responds to token expiration by either refreshing tokens through the backend or re‑prompting for sign‑in.

By coordinating these client‑side and backend implementations, the system can provide a smooth experience where users sign in with Google, the backend obtains tokens to interact with Drive, time entries are synchronized in near real‑time, and periodic CSV exports are uploaded to a shared Drive folder automatically.

## Security, Configuration Management, and Operational Considerations

### Managing secrets and environment variables

Security for OAuth credentials, MongoDB connection strings, and JWT secrets revolves around keeping these values out of source code and version control, instead loading them from environment variables or secrets management systems. MongoDB’s guidance on using environment variables for connection strings illustrates creating a `.env` file with a variable like `MONGODB_URI="<connection-string>"`, loading it into the script’s environment using `loadEnvFile`, and then accessing it via `process.env.MONGODB_URI` in MongoDB shell scripts.[17] Similarly, in a Python application, environment variables like `MONGO_URI`, `GOOGLE_CLIENT_ID`, and `GOOGLE_CLIENT_SECRET` can be defined in a `.env` file and loaded into the application via Pydantic settings, as demonstrated earlier.[20][21]

FastAPI’s settings and environment variables tutorial discusses using `BaseSettings` to map environment variables to typed attributes, and using `.env` files with Pydantic’s `SettingsConfigDict` to automatically load environment variables from a particular file.[20] It recommends using a dependency to retrieve a `Settings` object so that tests can override the settings easily, and also suggests using `@lru_cache` to avoid reloading settings on every request.[20] For production deployments, environment variables can be set by the container orchestrator, cloud platform, or process manager, and the `.env` file can be used locally for development.

Pydantic’s settings management documentation further expands on advanced loading mechanisms, including secrets files and custom sources.[21] For example, secrets can be stored in a directory where each file contains the value of a secret, and `BaseSettings` can be configured to load from these files, providing an extra layer of security when combined with OS‑level access controls.[21] In high‑security environments, one might use a dedicated secrets manager such as HashiCorp Vault or cloud provider secrets services, but this goes beyond the scope of the current integration.

The combined use of environment variables and Pydantic settings ensures that secrets remain outside the codebase, can be rotated without code changes, and can be configured differently per environment (development, staging, production) while the application code remains identical.

### OAuth scopes, token storage, and least privilege

The OAuth2 documentation emphasizes that applications must request the minimal scopes necessary for their functionality, and that refresh tokens should be stored in secure long‑term storage and reused for as long as they remain valid.[19] For Google Drive operations limited to uploading and accessing files created by the app, the `https://www.googleapis.com/auth/drive.file` scope is generally sufficient, as it allows the app to view and manage Google Drive files and folders that it has opened or created.[19] If the application needs to access arbitrary files, a broader scope such as `https://www.googleapis.com/auth/drive` might be required, but this increases risk and scope of access.

Refresh tokens, because they enable long‑term access without the user’s presence, must be protected from exfiltration. Storing refresh tokens in MongoDB requires precautions such as encrypting them at rest, limiting database access to only necessary services, and ensuring TLS is used between the application and database. Additionally, communication between client and backend must be over HTTPS so that tokens are not exposed in transit. Logs must never include full token values to avoid information leakage; logging best practices recommend carefully choosing what to log and avoiding sensitive data, as well as disabling unnecessary logging of process and thread IDs to reduce overhead.[40]

On the client side, storing refresh tokens in Async Storage is less secure because it is unencrypted, although OS‑level protections still apply.[27] If the application uses the backend as the primary holder of refresh tokens, the client can store only short‑lived access tokens or ID tokens, minimizing the value of any compromised device. The architecture must strike a balance between usability and security.

### Quota management and resilience to API failures

Google Drive APIs impose per‑user and per‑project quotas for read and write operations, for example 600 read requests per second and 300 write requests per second for certain resources as described in the Drive labels limits documentation.[44] When requests exceed quotas, the API may return time‑based errors such as HTTP 429, and the documentation recommends using truncated exponential backoff to retry failed requests without overwhelming the API.[44] An exponential backoff algorithm doubles the wait time after each failure, starting from a base wait (e.g., one second), adding a small random jitter, until a maximum backoff time is reached; it then continues retrying with the maximum backoff time for a limited number of attempts.[44]

The `google-api-core` library includes a `Retry` class that can be used as a decorator or passed to methods to apply exponential backoff to RPC calls; by default, it retries transient API errors with exponential backoff.[38] Using this library can reduce boilerplate and ensure consistent behavior across API calls. For example, uploading a CSV file can be wrapped with a custom `upload_with_retry` function that uses `Retry` to handle transient errors.

Operationally, the system should monitor Drive API usage, log errors, and trigger alerts when repeated failures occur. If uploads fail after all retries, the backend can mark the export as failed in MongoDB and schedule a manual retry or notify administrators.

### Error handling and logging in FastAPI

FastAPI provides default exception handlers for common error types like `HTTPException` and request validation errors, returning JSON responses that include error details.[43] When services need custom error handling, FastAPI allows adding custom exception handlers using the `@app.exception_handler` decorator, which can intercept exceptions and return tailored responses.[43] For example, a custom handler for token errors can return a standardized error structure for all auth failures.

In addition to exceptions, logging is a key part of observability. The Coralogix article on Python logging best practices recommends creating module‑level loggers, using predefined logging levels, and configuring logging via `logging.config.dictConfig` for structured configuration.[40] It suggests avoiding excessive logging that captures thread and process IDs unless necessary, as these can increase overhead.[40] For correlation IDs, FastAPI’s GitHub discussion on correlation ID middleware shows that adding headers or context for each request can help trace logs across asynchronous boundaries, though implementing robust correlation ID handling may require writing middleware that wraps `call_next` in `try/except` or `try/finally` blocks.[45]

By combining proper exception handling with structured logging, the backend can surface issues like failed Drive uploads, token expiration, or MongoDB errors quickly, aiding in debugging and reliability.

## Testing Strategy and Common Pitfalls

### Unit and integration testing of FastAPI endpoints

Testing FastAPI endpoints typically involves using `TestClient` from `fastapi.testclient`, which allows writing synchronous tests against asynchronous FastAPI endpoints.[20] For endpoints that accept file uploads, such as `/drive/upload-csv`, tests can simulate multipart form data by creating a file‑like object and passing it to `client.post` with a `files` parameter. An issue raised in a FastAPI GitHub discussion on testing `UploadFile` parameters notes that reading an `UploadFile` is an asynchronous operation, and that using `httpx.AsyncClient` may be necessary when testing asynchronous file operations, as opposed to the synchronous `TestClient`.[25] In either case, test code must ensure that the file is properly sent and that the backend handles the file type and size correctly.

For endpoints that rely on external services like Google Drive or MongoDB, it is best to mock these dependencies during unit tests. For example, the `build_drive_service_from_tokens` function can be patched to return a mock object whose `files().create().execute()` method returns a predetermined response, allowing the test to validate how the endpoint handles success and failure scenarios without making real network calls. MongoDB access functions can be similarly patched to return static data sets.

In integration tests, one can run the FastAPI app with a test configuration (e.g., using a test MongoDB database and a test Drive folder) and perform real HTTP calls to verify end‑to‑end behavior. For Drive integration tests, using a separate test folder in Drive ensures that test uploads do not clutter production folders, and that test credentials are isolated.

### Testing scheduled tasks and real‑time synchronization

Testing scheduled tasks involves verifying that scheduled functions behave correctly when invoked, and that scheduling triggers are configured properly. While APScheduler tasks are typically triggered in the background, tests can call functions like `perform_daily_export` directly to verify that they query the correct date range, generate CSV content, and call the Drive client as expected. The Sentry and APScheduler documentation hint that triggers can be configured programmatically, and integration tests might temporarily use an `IntervalTrigger` with a short interval (e.g., every few seconds) for testing, though care must be taken not to overrun Drive quotas.[5][5]

For real‑time synchronization, tests should ensure that creating or updating time entries initiates the correct background tasks. In the example `create_time_entry_endpoint`, tests can override the `upload_single_entry_csv` function or the `BackgroundTasks` mechanism to track when real‑time updates are scheduled, ensuring that each time entry triggers exactly one Drive update.

### Common pitfalls and mitigation strategies

Several common pitfalls can arise in this integration.

One pitfall involves misconfigured OAuth credentials or redirect URIs. For Expo apps, using `@react-native-google-signin/google-signin` requires that the web client ID and Android/iOS configurations match those registered in Google Cloud or Firebase, including SHA‑1 fingerprints and bundle IDs.[11] Mismatches result in sign‑in failures. Ensuring that `google-services.json` and `GoogleService-Info.plist` files are correctly placed and included in EAS builds is essential.[11] For AppAuth‑based flows, misconfigured redirect schemes or missing manifest entries can also break the flow.[7][32]

Another pitfall is forgetting to share the target Drive folder with the service account or ensuring appropriate permissions for end‑user accounts. If the authenticated user or service account lacks write permissions, `files().create()` calls will fail with authorization errors. The sharing documentation clarifies that for shared drives, only certain roles such as `writer`, `fileOrganizer`, or `organizer` grant permission to share or write files, and that `writersCanShare` is always considered `true` for shared drives.[13] Manual verification of folder sharing with the service account email or test user accounts is an important step.

File upload issues can also occur. If MIME types are not correctly specified, Google Drive may misinterpret CSV files or cause formatting issues. The Latenode community discussion underscores the importance of explicitly specifying `text/csv` as the MIME type when uploading CSVs, and notes that using `files().create()` with the `parents` parameter set to the folder ID ensures correct placement.[4] The Drive upload documentation reiterates that `Content-Type` must be set to the MIME type of the object being uploaded in simple uploads.[2][2]

Scheduling tasks with APScheduler can lead to hidden failures if the scheduler is not properly integrated with the FastAPI application lifecycle. The Sentry example shows that the scheduler should be started in the lifespan context and shut down on application exit, otherwise tasks may not trigger or may leave resources hanging.[5][5] Ensuring that the scheduler is started exactly once per process and that time zones are correctly handled (e.g., by setting `app.conf.timezone` in Celery or using timezone‑aware triggers in APScheduler) helps avoid confusion where tasks run at unexpected times.[12][31]

CORS misconfigurations are a frequent source of issues when integrating React Native Web clients with FastAPI. If `allow_origins` is not set to include the front‑end origin, or if `allow_credentials` is misconfigured, browsers will block requests or preflight checks will fail. The CORS documentation explains that using `"*"` as allowed origins prevents the use of credentials like cookies or authorization headers, so explicit origin lists are preferred when credentials are involved.[28]

Finally, neglecting proper error handling and logging can make diagnosing problems difficult. The FastAPI error handling documentation encourages using `HTTPException` and custom exception handlers, while Python logging best practices recommend structured logging and appropriate log levels.[43][40] Implementing correlation IDs as suggested in FastAPI discussions can further improve traceability for requests that span multiple services.[45]

By anticipating these pitfalls and applying the mitigations discussed, the integration can be made robust and maintainable.

## Conclusion

This integration playbook has detailed a comprehensive architecture and implementation strategy for connecting a Python FastAPI backend to the Google Drive API to upload CSV exports into a shared Drive folder, orchestrated by Expo React Native and React Native Web client applications and backed by MongoDB for time entry data storage. It has shown how Google Cloud configuration begins with enabling the Drive API, configuring the OAuth consent screen, and creating appropriate OAuth credentials for mobile and web applications as well as potentially for service accounts.[1][11][26] It has explained the nuances of Drive folder permissions and the use of the `parents` parameter in `files().create()` to ensure that CSV files are correctly placed in the target shared folder with a MIME type of `text/csv`.[2][2][4][13]

On the backend, the playbook has illustrated how FastAPI, combined with Uvicorn, can serve as a robust API layer that accepts time entry data and file uploads, uses Pydantic models to validate and serialize data, and persists time entries and Google tokens in MongoDB using an asynchronous driver like Motor or the PyMongo async API.[8][20][24][48] It has outlined how OAuth tokens obtained by Expo React Native clients can be transmitted to the backend and stored securely, and how the backend can construct `Credentials` objects and Drive service clients with `google-api-python-client` and `google-auth-oauthlib` to upload files on behalf of users.[1][19][22] Daily or weekly exports are scheduled via APScheduler’s `BackgroundScheduler`, integrated into FastAPI’s lifespan context, and real‑time synchronization is achieved by triggering background tasks when time entries are created or updated.[5][5][31][14]

On the client side, the report has described how Expo React Native uses libraries such as `@react-native-google-signin/google-signin` or `react-native-app-auth` to implement OAuth2 flows with Google, and how React Navigation and Async Storage maintain auth state and drive the user experience between authentication screens and main application content.[11][7][32][46][27] For React Native Web, the report has discussed enabling web support via Expo’s web workflow, managing CORS with FastAPI’s CORSMiddleware, and adapting authentication flows to the browser environment.[18][28]

Security considerations have emphasized the need to store secrets and connection strings in environment variables leveraged via Pydantic settings, to select OAuth scopes according to least privilege, to store refresh tokens securely, and to guard against common pitfalls like misconfigured CORS, incorrect Drive folder permissions, and misaligned OAuth redirect URIs.[17][20][21][19][13][28][40] The report has also highlighted the importance of logging, error handling, and correlation IDs for observability and maintainability.[40][43][45]

Although this playbook has been extensive, the integration remains adaptable. Systems requiring higher throughput or resilience could adopt Celery with `celery beat` for scheduling, or implement dedicated microservices for Drive uploads.[12][14] As MongoDB drivers evolve, projects may migrate from Motor to PyMongo’s async API while preserving the data access layer described.[24] Further enhancements might include implementing Drive push notifications to detect changes in shared folders, integrating with Google Sheets for append‑friendly data stores, or extending the OAuth flows to support additional providers alongside Google.

By following the patterns, code examples, and best practices described here, developers can implement a robust, secure, and scalable integration between FastAPI, Google Drive, MongoDB, and Expo React Native clients that satisfies the requirements of scheduled and real‑time CSV export workflows into shared Google Drive folders.

---
Sources:
1. https://developers.google.com/workspace/drive/api/quickstart/python
2. https://developers.google.com/workspace/drive/api/guides/manage-uploads
3. https://blog.futuresmart.ai/integrating-google-authentication-with-fastapi-a-step-by-step-guide
4. https://community.latenode.com/t/how-to-transfer-csv-files-from-local-computer-to-google-drive-using-python/34226
5. https://sentry.io/answers/schedule-tasks-with-fastapi/
6. https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
7. https://oneuptime.com/blog/post/2026-01-15-react-native-oauth2/view
8. https://testdriven.io/blog/fastapi-mongo/
9. https://dev.to/derlin/fastapi-celery--33mh
10. https://github.com/seandavi/fastapi-google-oauth-example
11. https://docs.expo.dev/guides/google-authentication/
12. https://docs.celeryq.dev/en/main/userguide/periodic-tasks.html
13. https://developers.google.com/workspace/drive/api/guides/manage-sharing
14. https://testdriven.io/courses/fastapi-celery/intro/
15. https://groups.google.com/g/google-api-python-client/c/2wcNgnmgWdo
16. https://fastapi.tiangolo.com/tutorial/request-files/
17. https://www.mongodb.com/docs/mongodb-shell/write-scripts/env-variables/
18. https://docs.expo.dev/workflow/web/
19. https://developers.google.com/identity/protocols/oauth2
20. https://fastapi.tiangolo.com/advanced/settings/
21. https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/
22. https://pypi.org/project/google-auth-oauthlib/
23. https://fastapi.tiangolo.com/reference/dependencies/
24. https://www.mongodb.com/docs/drivers/motor/
25. https://github.com/fastapi/fastapi/issues/1536
26. https://developers.google.com/zero-touch/guides/customer/quickstart/python-service-account
27. https://github.com/react-native-async-storage/async-storage
28. https://fastapi.tiangolo.com/tutorial/cors/
29. https://fastapi.tiangolo.com/advanced/custom-response/
30. https://ai.google.dev/gemini-api/docs/batch-api
31. https://martinheinz.dev/blog/39
32. https://docs.secureauth.com/iam/react-native-application-with-appauth
33. https://fastapi.tiangolo.com/deployment/manually/
34. https://github.com/rochacbruno/fastapi-project-template/blob/main/requirements.txt
35. https://www.w3schools.com/python/pandas/pandas_csv.asp
36. https://groups.google.com/g/firebase-talk/c/-T1zoG-7X0s
37. https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
38. https://googleapis.dev/python/google-api-core/latest/retry.html
39. https://gist.github.com/Jarmos-san/0b655a3f75b698833188922b714562e5
40. https://coralogix.com/blog/python-logging-best-practices-tips/
41. https://mimo.org/tutorials/python/how-to-check-if-a-file-exists-in-python
42. https://www.mongodb.com/company/blog/performance-best-practices-indexing
43. https://fastapi.tiangolo.com/tutorial/handling-errors/
44. https://developers.google.com/workspace/drive/labels/limits
45. https://github.com/fastapi/fastapi/discussions/8190
46. https://reactnavigation.org/docs/auth-flow/
47. https://docs.python.org/3/library/datetime.html
48. https://fastapi.tiangolo.com/tutorial/body-fields/

`````

---
## Sample 3: Custom JWT auth — mobile (Expo React Native)

| | |
|---|---|
| HTTP status | 200 |
| **Latency** | **261.7 s** |
| **Total cost (from Perplexity's `usage.cost`)** | **$0.91603** |
| Cost breakdown | input $0.00051 · output $0.10977 · citation $0.0575 · reasoning $0.49826 · search $0.25 |
| Tokens | prompt 254 · completion 13,721 · citation 28,749 · reasoning 166,085 |
| Search queries run by Perplexity internally | 50 |
| Playbook length | 67,328 chars |
| Citations | 41 |

### Input — what our agent asked the tool (verbatim)

```
INTEGRATION: Custom JWT-based email/password authentication for an Expo React Native (SDK 54) mobile app with FastAPI + MongoDB backend. Need: register, login, password hashing (bcrypt), JWT token issuance/validation, secure token persistence on mobile (expo-secure-store).

CONSTRAINTS: 
- Expo SDK 54 React Native mobile app
- FastAPI backend with /api prefix on all routes
- MongoDB for user storage
- Token storage via expo-secure-store
```

### Exact API request sent to Perplexity

```json
{
  "url": "https://api.perplexity.ai/chat/completions",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer pplx-REDACTED-MOCK-KEY",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "sonar-deep-research",
    "messages": [
      {
        "role": "system",
        "content": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
      },
      {
        "role": "user",
        "content": "Create a detailed integration playbook for INTEGRATION: Custom JWT-based email/password authentication for an Expo React Native (SDK 54) mobile app with FastAPI + MongoDB backend. Need: register, login, password hashing (bcrypt), JWT token issuance/validation, secure token persistence on mobile (expo-secure-store).\n\nCONSTRAINTS: \n- Expo SDK 54 React Native mobile app\n- FastAPI backend with /api prefix on all routes\n- MongoDB for user storage\n- Token storage via expo-secure-store in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
      }
    ]
  }
}
```

### Exact output returned to our agent (verbatim, 69,965 chars)

This is the complete tool result the coding agent receives — the playbook exactly as Perplexity wrote it, with the citation URLs appended as a `Sources:` list by our tool layer. (It is then wrapped as `{"content": "<below>", "cost": 1.5}` — the `1.5` is an internal billing unit, unrelated to the Perplexity dollar cost.)

`````markdown
# End-to-End Integration Playbook for JWT-Based Email/Password Authentication with Expo React Native (SDK 54), FastAPI, and MongoDB

This report presents a complete, implementation-ready integration playbook for building a custom email/password authentication system using JSON Web Tokens (JWT) across an Expo React Native mobile and web application (SDK 54), backed by a FastAPI REST API and MongoDB user store. The focus is on secure registration and login flows, password hashing using bcrypt, JWT issuance and validation on the backend, and secure token persistence on clients using `expo-secure-store` on native platforms and appropriate alternatives on the web. The report describes stepwise environment setup, code-level details for each layer, security and secret-management practices, testing strategies, and common pitfalls, drawing on documented best practices from FastAPI, MongoDB, Expo, and industry guidance on JWT security and token storage.[1][3][2][11][13][11][19][23][24][25][29][31][3][39] The result is a coherent, reusable blueprint that can be adopted or adapted for production-grade projects.

## 1. Architectural Overview and Requirements

The target architecture consists of three main components: an Expo React Native client application (supporting both mobile and web), a FastAPI backend API with all routes under the `/api` prefix, and a MongoDB database used for persistent user storage and associated authentication data. The client provides screens for user registration and login, manages authentication state, and persists tokens securely on the device. The backend exposes JSON endpoints for user registration, login, token refresh (if used), and retrieval of the currently authenticated user, while handling password hashing, JWT issuance, and token verification. MongoDB stores user documents with unique email addresses and securely hashed passwords, and may also store refresh tokens or token families if refresh-token rotation is implemented.[11][11][23]

Expo SDK 54 is used on the front end, which bundles React Native 0.81 and provides a unified developer experience across iOS, Android, and the web.[1][29] The project is initialized via `create-expo-app` with an SDK 54 template, ensuring compatibility of dependencies and tooling with the latest Expo features.[29] On mobile platforms, token storage leverages `expo-secure-store`, which provides encrypted key-value storage backed by the device keychain/keystore and is recommended for small, sensitive values like access and refresh tokens.[3][3][19][3] On the web, where `expo-secure-store` is not available, a different strategy is required, such as secure HttpOnly cookies or carefully-scoped in-memory or local storage for less sensitive scenarios, consistent with guidance that native apps use platform-secure storage and web apps favor HttpOnly cookies over localStorage for sensitive tokens.[13][19]

On the backend, FastAPI provides an asynchronous, high-performance web framework with first-class support for Pydantic models, automatic generation of OpenAPI documentation, and straightforward integration with MongoDB via the PyMongo driver and its asynchronous variants.[11][11][30] FastAPI’s security utilities and middleware support, together with libraries such as `python-jose` and bcrypt, facilitate secure implementation of JWT-based authentication flows, including generating signed tokens, decoding and validating them on incoming requests, and integrating authentication dependencies into path operations.[2][16][37]

At the database layer, MongoDB is hosted either locally or on a managed platform such as Atlas, with connection strings stored in environment variables for security.[9][11][28] The MongoDB collection that stores users includes a unique index on the email field, preventing duplicate registration and simplifying uniqueness checks during signup.[23] For integration with FastAPI, a global asynchronous MongoDB client is instantiated based on the `MONGODB_URL` environment variable, and references to the target database and collection (for example, `auth_db` and `users`) are created and attached to the application context.[11][11]

Security requirements for this architecture include strong password hashing with salt and configurable work factors (bcrypt rounds), secure management of the JWT signing key, short-lived access tokens with optional refresh-token support, strict use of HTTPS in production, minimal and non-sensitive JWT claims, and robust CORS configuration that allows the intended front-end origins while preserving the ability to send Authorization headers.[2][13][20][26][31] The following sections translate these requirements into concrete installation steps, configuration patterns, source code, and testing practices.

## 2. Backend Environment, Database, and Project Setup

### 2.1. FastAPI Project Initialization and Dependencies

The backend project is organized as a standard Python package with clearly separated modules for configuration, database access, models, authentication logic, and API routing. Using FastAPI’s asynchronous features, the API can efficiently handle concurrent requests and integrate with MongoDB via an asynchronous driver.[11][11]

To begin, a Python virtual environment is created and activated. Within this environment, dependencies like FastAPI, Uvicorn for ASGI serving, PyMongo’s asynchronous client, bcrypt or passlib for password hashing, and `python-jose` for JWT encoding and decoding are installed. This follows the general pattern of setting up FastAPI applications detailed in the FastAPI and MongoDB integration tutorials, which emphasize virtual environments and dependency isolation.[11][11] Environment variables are used to store sensitive values such as the MongoDB connection string and JWT secret, following the pattern of setting `MONGODB_URL` with an export command or `.env` file.[2][11]

A minimal `pyproject.toml` or `requirements.txt` may specify core dependencies such as:

```bash
pip install fastapi uvicorn[standard] "pymongo[srv]" motor bcrypt python-jose[cryptography] python-dotenv
```

Here, `motor` provides an asynchronous MongoDB client implementation, while `python-jose` offers JWT support, and `python-dotenv` facilitates loading environment variables from a `.env` file during development. Using `uvicorn[standard]` is recommended for robust production-ready ASGI serving.[11][11] On startup, the FastAPI application will load configuration from environment variables, establish a MongoDB connection, and include routers under the `/api` prefix using `APIRouter`, as described in the FastAPI router documentation.[7][11]

### 2.2. MongoDB Cluster and Connection Configuration

MongoDB can be deployed on a local instance or as a cloud cluster, for example via MongoDB Atlas. When using Atlas, a free M0 cluster can be provisioned through the Atlas UI or CLI, and a database user and IP access list entry are configured, as outlined in the Atlas free-tier documentation.[28] The resulting connection string, which includes the username, password, cluster URL, and database name, is then stored in an environment variable such as `MONGODB_URL`, consistent with MongoDB’s guidance for PyMongo integration with FastAPI.[11]

An example connection string exported in a shell or declared in a `.env` file might look like:

```bash
export MONGODB_URL="mongodb+srv://<username>:<password>@<cluster-url>/auth_db?retryWrites=true&w=majority"
```

The FastAPI-MongoDB integration tutorial demonstrates how to retrieve this environment variable and construct an asynchronous MongoDB client using `AsyncMongoClient`, then obtain a database reference and a collection reference for storing user documents.[11][11] A typical initialization in `db.py` would be:

```python
# db.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

MONGODB_URL = os.environ.get("MONGODB_URL")

client: AsyncIOMotorClient | None = None
db = None
users_collection = None

async def connect_to_mongo():
    global client, db, users_collection
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database("auth_db")
    users_collection = db.get_collection("users")

async def close_mongo_connection():
    global client
    if client:
        client.close()
```

During application startup and shutdown, FastAPI event handlers call these functions to manage the database connection lifecycle, similar to the pattern shown in MongoDB’s FastAPI integration tutorial.[11][11]

To prevent duplicate registrations, a unique index on the `email` field should be created. The MongoDB indexing documentation shows how to do this with `createIndex` in the Mongo shell, and the same can be achieved in code using `create_index` with `unique=True`.[23] An initialization function might include:

```python
async def ensure_indexes():
    await users_collection.create_index("email", unique=True)
```

This ensures that each email appears at most once, and attempts to insert duplicate documents will result in a duplicate key error.[23]

### 2.3. FastAPI Application Skeleton with /api Prefix and CORS

The core FastAPI application is defined in `main.py`. It imports the database connection utilities, defines startup and shutdown events, and configures CORS middleware to allow the Expo dev server origins and the production frontend origins. FastAPI’s CORS tutorial explains that when Authorization headers are used (for example, for Bearer tokens), the list of allowed origins must be explicit; using `"*"` for origins prevents the use of credentials such as Authorization headers.[20]

A typical `main.py` skeleton looks like:

```python
# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from db import connect_to_mongo, close_mongo_connection, ensure_indexes

app = FastAPI(title="Auth API")

origins = [
    "http://localhost:8081",  # Expo web dev
    "http://localhost:19006", # Another possible Expo dev URL
    "http://localhost",       # Generic local
    # Add production web origin, e.g., "https://app.example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await connect_to_mongo()
    await ensure_indexes()

@app.on_event("shutdown")
async def on_shutdown():
    await close_mongo_connection()

app.include_router(auth_router, prefix="/api")
```

The `auth_router` is an `APIRouter` instance that groups authentication-related routes, and is included under the `/api` prefix, ensuring that endpoints such as registration and login are exposed as `/api/auth/register` and `/api/auth/login` respectively.[7] CORS settings are tuned to include allowed origins that correspond to the Expo dev server addresses and any deployed web frontends, in line with FastAPI’s CORS recommendations for backends accessed by JavaScript SPAs.[20]

### 2.4. User Models and Data Structures

FastAPI leverages Pydantic models for request bodies and response schemas, a pattern emphasized in its tutorial on request bodies, allowing type-checked and validated inputs and outputs.[30][30] For user authentication, it is important to use distinct models for user input, database storage, and API responses, as illustrated in FastAPI’s “Extra Models” documentation. The input model includes plaintext password, the database model stores a hashed password, and the output model omits any password information.[16]

In `auth/models.py`, one can define:

```python
# auth/models.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserInDB(UserBase):
    id: str
    hashed_password: str

class UserPublic(UserBase):
    id: str
```

The `UserCreate` model captures registration input, including password, and applies minimal length validations. The `UserInDB` represents the persisted document, containing a stringified `id` and `hashed_password`. The `UserPublic` model is used as a response schema and intentionally omits the password field, consistent with FastAPI’s guidance that plaintext passwords must never be stored or returned, and that only secure hashes should be persisted.[16]

Because MongoDB uses `ObjectId` for `_id` fields by default, it is common to convert these to strings when returning data to clients or to use custom Pydantic types that handle `ObjectId` conversion automatically, as described in MongoDB’s FastAPI integration tutorial.[11][11] In this playbook, string IDs are used in response models for simplicity, and conversion is handled when reading from or writing to MongoDB.

## 3. Authentication Backend: Password Hashing, JWT Issuance, and Protected Routes

### 3.1. Password Hashing with bcrypt

Storing passwords in plaintext is never acceptable. Instead, passwords should be hashed using a slow, salted algorithm like bcrypt, Argon2, or scrypt, with configurable work factors that can be increased as hardware improves.[16][26][35] Bcrypt is a widely used choice, and is illustrated in several FastAPI tutorials that show how to hash passwords and verify them at login time.[4][4]

In Python, bcrypt can be used directly or via a higher-level library such as `passlib`. For clarity and explicit control, this playbook uses the `bcrypt` package directly, wrapping hash and verification in helper functions. Security guidelines suggest choosing bcrypt rounds that yield a per-hash latency of roughly 100–250 ms for standard web applications, and adjusting based on server performance and expected authentication load.[35]

A module `auth/security.py` can contain:

```python
# auth/security.py
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Any, Dict
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = "CHANGE_ME_IN_ENV"  # overridden from env in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

class TokenData(BaseModel):
    sub: Optional[str] = None

def get_password_hash(password: str) -> str:
    # bcrypt.gensalt() generates a salt; default rounds typically 12.
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False
```

In production, the number of rounds can be adjusted after benchmarking as recommended by bcrypt tuning guides, balancing security and authentication latency.[35] The `get_password_hash` function is called when a new user registers or resets their password; `verify_password` is called at login, comparing the provided password with the stored hash. This follows the general registration and login pattern described in bcrypt-based FastAPI tutorials, where passwords are hashed on registration and verified on login before issuing a token.[4][4]

### 3.2. JWT Token Creation and Validation

JWTs are signed tokens that encode claims such as subject (`sub`), expiration (`exp`), and optional metadata. FastAPI’s OAuth2 with JWT tutorial shows how to use `python-jose` to encode and decode tokens using a secret key and algorithm, and how to integrate token verification into dependency-injected functions that retrieve the current user.[2][2][2] Industry best practices emphasize several key aspects: the signing key must be kept secret, tokens should carry minimal and non-sensitive data, tokens must have expiration times, and all interactions must occur over HTTPS.[13][31]

In `auth/security.py`, token creation functions can be defined:

```python
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

This function takes a dictionary of claims and an optional expiration delta. At minimum, the payload should include a `sub` claim whose value uniquely identifies the user, often using the user ID or a namespaced identifier like `"user:<id>"`. FastAPI’s example stresses that the subject claim should uniquely identify the principal across the application.[2]

To decode and validate tokens, a helper function uses `jwt.decode`:

```python
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str | None = payload.get("sub")
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing subject",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenData(sub=sub)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

The `OAuth2PasswordBearer` dependency instructs FastAPI to expect a Bearer token in the Authorization header for protected endpoints, using the provided `tokenUrl` as the form-based login endpoint in OpenAPI docs.[2] Each protected route can then depend on a `get_current_user` function that extracts the token from the header, decodes it, and loads the corresponding user document from MongoDB.

### 3.3. Registration and Login Endpoints with /api Prefix

The core authentication endpoints are registration and login, exposed under `/api/auth/register` and `/api/auth/login` respectively. FastAPI’s OAuth2 tutorial uses `/token` as the login route, but the underlying flow is the same: a client sends credentials, the backend verifies them, and returns a signed JWT to be used in subsequent requests.[2][18]

In `auth/routes.py`, an `APIRouter` is defined:

```python
# auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from db import users_collection
from .models import UserCreate, UserPublic, UserInDB
from .security import get_password_hash, verify_password, create_access_token, decode_token, oauth2_scheme
from typing import Any

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate) -> Any:
    existing = await users_collection.find_one({"email": user_in.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = get_password_hash(user_in.password)
    doc = {
        "email": user_in.email,
        "full_name": user_in.full_name,
        "hashed_password": hashed_password,
    }
    result = await users_collection.insert_one(doc)
    user_out = UserPublic(id=str(result.inserted_id), email=user_in.email, full_name=user_in.full_name)
    return user_out

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    user_id = str(user["_id"])
    access_token = create_access_token(data={"sub": f"user:{user_id}"})
    return TokenResponse(access_token=access_token)
```

The registration endpoint validates that the email is not already in use (backed by a unique index at the database level)[23], hashes the password, and inserts the new document. It returns a public representation of the user, without password fields.[16] The login endpoint expects form data using the `OAuth2PasswordRequestForm` model, in line with FastAPI’s OAuth2 implementation, and returns an access token when credentials are valid.[2]

While OAuth2PasswordRequestForm uses `username` as the form field name, for email/password authentication the `username` field is repurposed to carry the user’s email address. On the client side, Axios requests can send form-encoded data or JSON with appropriate headers; fastapi supports both with minor adjustments.[2][30]

For JSON-based login rather than form-encoded, a custom model like `LoginRequest(email, password)` could be used instead of OAuth2PasswordRequestForm, with the understanding that OpenAPI might not fully reflect OAuth2 flows.

### 3.4. Current User Dependency and Protected Routes

To protect routes and associate them with authenticated users, a dependency function `get_current_user` is defined. It extracts the Bearer token via `oauth2_scheme`, decodes it, and loads the corresponding user document from MongoDB. FastAPI’s JWT tutorial demonstrates precisely this pattern, where `get_current_user` is reused across multiple path operations to enforce authentication.[2]

An example in `auth/dependencies.py`:

```python
# auth/dependencies.py
from fastapi import Depends, HTTPException, status
from .security import oauth2_scheme, decode_token
from db import users_collection
from .models import UserInDB

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    token_data = await decode_token(token)
    if not token_data.sub or not token_data.sub.startswith("user:"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = token_data.sub.split(":", 1)[1]
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserInDB(
        id=str(user["_id"]),
        email=user["email"],
        full_name=user.get("full_name"),
        hashed_password=user["hashed_password"],
    )
```

A protected endpoint can then be defined as:

```python
@router.get("/me", response_model=UserPublic)
async def read_current_user(current_user: UserInDB = Depends(get_current_user)):
    return UserPublic(id=current_user.id, email=current_user.email, full_name=current_user.full_name)
```

The use of `WWW-Authenticate` headers with “Bearer” aligns with HTTP authentication semantics and helps clients understand that Bearer tokens are required.[2][40] Each request to `/api/auth/me` must include an Authorization header like `Authorization: Bearer <token>`, and the FastAPI security utilities will ensure the token is extracted and passed to the dependency.[2]

### 3.5. Optional Refresh Tokens and Token Lifetime Strategy

Although not strictly required for basic authentication, refresh tokens improve user experience by allowing short-lived access tokens while avoiding frequent re-logins.[13][21] In mobile scenarios, a common pattern is to issue an access token with a relatively short lifetime (for example, 10–15 minutes) and a refresh token with a longer lifetime (for example, days), storing both securely and implementing refresh-token rotation to mitigate replay attacks.[10][13][21]

The React Native JWT refresh token guide outlines a flow in which the client stores both access and refresh tokens, automatically refreshes tokens before expiry, and uses a backend that tracks refresh token “families” and invalidates them on signs of replay.[10] Auth0’s refresh token documentation further recommends configuring idle and absolute expiration for refresh tokens to prevent token stockpiles and to bound the window of misuse.[21][31] In the context of this playbook, adding refresh tokens would involve:

1. Extending the login endpoint to issue both `access_token` and `refresh_token`, with the latter stored in MongoDB or a dedicated collection, and optionally grouped into families for rotation.
2. Creating an `/api/auth/refresh` endpoint that validates the refresh token, checks that it has not been revoked or reused, issues a new access token and possibly a new refresh token, and updates the stored refresh-token record.
3. Implementing client-side logic that detects approaching expiry of the access token and calls the refresh endpoint proactively, as described in React Native refresh token guides and token best-practice documents.[10][13][21]

For brevity, the remainder of this playbook focuses on access tokens; however, the architecture described here can be extended with refresh tokens following the same patterns and best practices.

## 4. Client Integration: Expo React Native SDK 54, Secure Token Storage, and Routing

### 4.1. Creating the Expo Project and Running on Mobile and Web

The frontend is built using Expo SDK 54, which bundles React Native 0.81 and supports running the same project on iOS, Android, and web via React Native Web.[1][29] The Expo tutorial suggests using `create-expo-app` to initialize a new project, choosing the SDK 54 template when prompted.[29]

The initialization process is:

```bash
npx create-expo-app@latest auth-app
# Select SDK 54 when prompted
cd auth-app
npm run reset-project  # Optional: start from minimal template
```

The `reset-project` script, described in the Expo tutorial, strips boilerplate and leaves a simple starting point with an `app` directory containing a minimal `index.tsx` and layout file.[29] To run the project on mobile and web, `npx expo start` is used, and the developer scans the displayed QR code with Expo Go on a device or presses `w` in the terminal to run the app in a web browser.[29]

React Native Web integration is handled automatically by Expo; components like `View` and `Text` render appropriately on the web when using the Expo-managed workflow.[29] This unified environment is crucial for testing authentication flows on all platforms.

### 4.2. Installing and Configuring expo-secure-store

Secure local storage on mobile devices is implemented via `expo-secure-store`, which provides an encrypted key-value store backed by platform-specific hardware security modules such as the iOS Keychain and Android Keystore.[3][3][19][3] Expo’s SecureStore documentation notes that each Expo project has its own isolated storage, that it is suitable for small secrets like tokens and keys, and that it is included in Expo Go, making it easy to test on physical devices.[3][3][3]

To install the library in an Expo SDK 54 project, the Expo docs recommend using:

```bash
npx expo install expo-secure-store
```

This command ensures the correct version for the current SDK is installed.[3][3] For projects using Continuous Native Generation (CNG) or config plugins, additional configuration options are available, such as controlling Android backup behavior and requesting Face ID permissions on iOS, as shown in the SecureStore docs.[3][3] For example, `app.json` can be configured:

```json
{
  "expo": {
    "plugins": [
      [
        "expo-secure-store",
        {
          "configureAndroidBackup": true,
          "faceIDPermission": "Allow $(PRODUCT_NAME) to access your Face ID biometric data."
        }
      ]
    ],
    "ios": {
      "config": {
        "usesNonExemptEncryption": false
      }
    }
  }
}
```

The `usesNonExemptEncryption` setting informs Apple’s export compliance about the nature of encryption used in the app.[3] Because `expo-secure-store` is intended for storing small secrets, it is appropriate for access tokens and refresh tokens, but not for large datasets.[19][3]

On the web, `expo-secure-store` is not available in the same manner, and Expo’s data storage documentation advises considering alternatives like AsyncStorage, the browser’s localStorage, or cookies, depending on encryption requirements and threat models.[19] Contemporary best-practice resources recommend that for web applications, sensitive tokens be stored in secure, HttpOnly cookies rather than localStorage, to mitigate XSS risks.[13][31] Therefore, the client architecture differs slightly between native and web: native uses SecureStore, while web uses either cookies (where the backend is configured for cookie-based auth) or a short-lived in-memory token plus refresh tokens that are not accessible to scripts.

### 4.3. Token Storage Strategy on Native and Web

The core requirement is that tokens be stored in a way that balances usability and security. For native mobile apps, Duende Software’s JWT best-practices guide emphasizes using platform-secure storage APIs such as Keychain on iOS and Keystore on Android to hold tokens that grant system access or represent long-lived privileges like refresh tokens.[13] Expo-secure-store provides a cross-platform abstraction over these APIs, making it an appropriate choice for storing JWT access tokens and refresh tokens on mobile.[3][3][19][3]

The Expo Store Data documentation describes `expo-secure-store` as an encrypted store for tokens and keys, and differentiates it from AsyncStorage, which is unencrypted and suited for non-sensitive preferences or app state.[19] Therefore, the client app should:

1. Store the access token and refresh token in `SecureStore` on iOS and Android.
2. Avoid storing tokens in AsyncStorage or other unencrypted storage mechanisms for sensitive use cases.
3. On web, either:
   - Rely on secure, HttpOnly cookies set by the backend, with the React Native Web client making requests that include cookies automatically, or
   - Store only short-lived access tokens in memory and handle refresh tokens more cautiously, recognizing the limitations of web storage.

Auth0 and Duende both caution against storing JWTs in localStorage or sessionStorage for high-security scenarios due to susceptibility to XSS, and instead recommend HttpOnly cookies or secure storage where possible.[13][31] However, when using React Native Web as a SPA, fully HttpOnly cookie-based flows may require additional backend configuration, and some projects choose to accept the risk of localStorage while implementing strong XSS protections.

In this playbook, for clarity, the code will define a `TokenStorage` abstraction that uses SecureStore when available (native) and falls back to a simple in-memory storage for web, with a clear note that production web deployments should consider HttpOnly cookies or hardened localStorage strategies for better security.

### 4.4. Axios API Client and Token Interceptors

The client communicates with the FastAPI backend via HTTP requests. Axios is a popular choice for HTTP in React applications, and tutorials on attaching JWTs to Axios requests illustrate using interceptors to inject Authorization headers automatically.[8][15] One approach is to create an Axios instance with a base URL and interceptors that:

1. Retrieve the current access token from storage.
2. Attach it as `Authorization: Bearer <token>` on outbound requests.
3. Optionally, intercept 401 responses and automatically attempt token refresh.

The Axios plus React Native error-handling article shows how to centralize interceptors, add metadata, and handle retry logic in a consistent way.[15] For the present playbook, the focus is on attaching tokens and basic failure handling.

In `src/api/client.ts`:

```typescript
// src/api/client.ts
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const API_BASE_URL = 'http://localhost:8000/api'; // adjust for production

let inMemoryToken: string | null = null;

async function getAccessToken(): Promise<string | null> {
  if (Platform.OS === 'web') {
    return inMemoryToken;
  }
  try {
    const token = await SecureStore.getItemAsync('accessToken');
    return token;
  } catch {
    return null;
  }
}

export async function setAccessToken(token: string | null): Promise<void> {
  if (Platform.OS === 'web') {
    inMemoryToken = token;
    return;
  }
  if (token) {
    await SecureStore.setItemAsync('accessToken', token);
  } else {
    await SecureStore.deleteItemAsync('accessToken');
  }
}

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
});

apiClient.interceptors.request.use(
  async (config: AxiosRequestConfig) => {
    const token = await getAccessToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;
```

This pattern mirrors the Axios interceptor example that sets Authorization headers globally, except here tokens are retrieved asynchronously from secure storage and attached as Bearer tokens to every request.[8][15] The use of an Axios instance avoids sending tokens to unrelated APIs and aligns with the recommended practice of scoped Axios instances described in JWT-with-Axios tutorials.[8]

A more advanced implementation could catch 401 responses, use a stored refresh token to request a new access token, and retry the failed request, following the refresh patterns described in React Native and Angular refresh tutorials and Auth0’s refresh token rotation guidance.[10][21][32][34] For brevity, this example focuses on sending tokens on initial requests.

### 4.5. Auth Service Functions and Context

To encapsulate authentication operations and state, a service layer and a React context are used. The OneUptime React Native JWT guide demonstrates an `AuthService` class with methods for login, logout, token refresh, and initialization, which is then consumed by higher-level hooks or context providers.[10] Similarly, Expo’s Router authentication docs show how to wrap the app in a `SessionProvider` that exposes authentication state and actions like `signIn` and `signOut`.[25][39]

An `AuthService` in `src/services/authService.ts` might look like:

```typescript
// src/services/authService.ts
import apiClient, { setAccessToken } from '../api/client';

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export async function login(email: string, password: string): Promise<void> {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await apiClient.post<LoginResponse>('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  const { access_token } = response.data;
  await setAccessToken(access_token);
}

export async function register(
  email: string,
  password: string,
  fullName?: string
): Promise<void> {
  const body = { email, password, full_name: fullName };
  await apiClient.post('/auth/register', body);
}

export async function logout(): Promise<void> {
  await setAccessToken(null);
}
```

To expose authentication state to the rest of the app, a context can be created in `src/context/AuthContext.tsx`:

```tsx
// src/context/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';
import { login as apiLogin, logout as apiLogout, register as apiRegister } from '../services/authService';

interface AuthContextValue {
  isAuthenticated: boolean;
  initializing: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  signUp: (email: string, password: string, fullName?: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [initializing, setInitializing] = useState(true);

  useEffect(() => {
    const loadToken = async () => {
      try {
        let token: string | null = null;
        if (Platform.OS === 'web') {
          // in-memory token is not persisted across reloads
          token = null;
        } else {
          token = await SecureStore.getItemAsync('accessToken');
        }
        setIsAuthenticated(!!token);
      } finally {
        setInitializing(false);
      }
    };
    loadToken();
  }, []);

  const signIn = async (email: string, password: string) => {
    await apiLogin(email, password);
    setIsAuthenticated(true);
  };

  const signOut = async () => {
    await apiLogout();
    setIsAuthenticated(false);
  };

  const signUp = async (email: string, password: string, fullName?: string) => {
    await apiRegister(email, password, fullName);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, initializing, signIn, signOut, signUp }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return ctx;
}
```

Expo’s authentication guides demonstrate a similar pattern of wrapping the app in a provider and exposing `session` or `isAuthenticated` flags, which can then be used in route guards or conditional rendering.[22][25][39] The `initializing` flag allows a splash screen or loading indicator to be displayed while token state is being restored.

### 4.6. Route Protection with Expo Router or React Navigation

Expo’s modern routing solution, Expo Router, integrates naturally with React context-based authentication. Its authentication documentation explains how to create a `SessionProvider`, a splash-screen controller, and route groups that only render when a user is authenticated; otherwise, navigation redirects to a sign-in screen.[25][39]

If using Expo Router, the root layout might look like:

```tsx
// app/_layout.tsx
import { Slot } from 'expo-router';
import { AuthProvider } from '../src/context/AuthContext';

export default function RootLayout() {
  return (
    <AuthProvider>
      <Slot />
    </AuthProvider>
  );
}
```

Within an authenticated route group `(app)`, a layout file can check `isAuthenticated`:

```tsx
// app/(app)/_layout.tsx
import { Redirect, Stack } from 'expo-router';
import { Text } from 'react-native';
import { useAuth } from '../../src/context/AuthContext';

export default function AppLayout() {
  const { isAuthenticated, initializing } = useAuth();

  if (initializing) {
    return <Text>Loading...</Text>;
  }

  if (!isAuthenticated) {
    return <Redirect href="/sign-in" />;
  }

  return <Stack />;
}
```

The Expo Router authentication guide shows a nearly identical pattern, in which unauthenticated users are redirected to a `/sign-in` route, while authenticated users can access routes under the `(app)` group.[25][39] This enables client-side protection of routes without requiring server-side session checks, as long as the access token is valid and present.

The `/sign-in` screen can call `signIn` from `useAuth` on form submission, while a `/register` screen can call `signUp`. Once `signIn` sets `isAuthenticated` to true, the protected routes become accessible. Subsequent API calls made from those screens will include the Authorization header thanks to the Axios interceptor configured earlier.

### 4.7. Minimal Login and Registration Screens

A simple login screen using React Native components, and basic client-side validation as described in login-validation tutorials, can improve user experience and enforce password policies before hitting the backend.[36][41] For example:

```tsx
// app/sign-in.tsx
import React, { useState } from 'react';
import { View, TextInput, Button, Text } from 'react-native';
import { useAuth } from '../src/context/AuthContext';

export default function SignInScreen() {
  const { signIn } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async () => {
    setError(null);
    try {
      await signIn(email, password);
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? 'Login failed');
    }
  };

  return (
    <View style={{ padding: 16 }}>
      <Text>Email</Text>
      <TextInput
        autoCapitalize="none"
        autoCorrect={false}
        keyboardType="email-address"
        onChangeText={setEmail}
        value={email}
        style={{ borderWidth: 1, marginBottom: 8 }}
      />
      <Text>Password</Text>
      <TextInput
        secureTextEntry
        onChangeText={setPassword}
        value={password}
        style={{ borderWidth: 1, marginBottom: 16 }}
      />
      {error && <Text style={{ color: 'red' }}>{error}</Text>}
      <Button title="Sign In" onPress={onSubmit} />
    </View>
  );
}
```

Client-side email validation can use a regular expression as shown in React Native validation examples, preventing obviously invalid input from being sent to the server.[41] More advanced UI enhancements, including animated transitions between login and signup screens, can be achieved using libraries like React Native Reanimated and React Navigation, as demonstrated in login UI tutorials, but they are not essential for functional integration.[36]

## 5. Security and Secret Management Best Practices

### 5.1. Managing JWT Secret Keys and MongoDB Credentials

The JWT signing key (`SECRET_KEY`) and MongoDB connection string (`MONGODB_URL`) are both highly sensitive secrets. Auth0’s token best-practices documentation stresses that signing keys must be kept secret and only revealed to services that must sign or verify tokens.[31] Similarly, MongoDB advises storing connection strings in environment variables rather than code, and FastAPI’s security and configuration examples demonstrate loading these values via environment variables and configuration classes.[2][11][18]

In Python, `python-dotenv` can load environment variables from a `.env` file during development. For example:

```python
# config.py
from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    mongodb_url: SecretStr
    jwt_secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

The `.env` file, which is excluded from version control, might contain:

```text
MONGODB_URL="mongodb+srv://user:pass@cluster-url/auth_db?retryWrites=true&w=majority"
JWT_SECRET_KEY="RANDOM_LONG_SECRET_GENERATED_SECURELY"
```

FastAPI’s JWT tutorial specifically recommends generating a random, secure secret key using a command like `openssl rand -hex 32`, and copying it into the application configuration rather than using any sample value.[2] The `Settings` model can then be imported where needed, and `settings.jwt_secret_key.get_secret_value()` used as the secret key.

On mobile, it is crucial to understand that the JWT signing key must never be embedded in the client application; the client only receives tokens signed by the backend and never signs or verifies them independently beyond local checks. If the signing key were embedded in the client, an attacker could extract it and forge tokens.

### 5.2. CORS and HTTPS Enforcement

CORS configuration plays a crucial role in allowing the SPA or React Native Web client to access the backend from a different origin. FastAPI’s CORS tutorial clarifies that when Authorization headers are involved, allowed origins cannot be `"*"`; instead, specific origins must be listed.[20] The CORS middleware in `main.py` therefore specifies the set of known origins, including local Expo dev URLs and the deployed production frontend URL, and sets `allow_credentials=True` to allow Authorization headers.[20]

In production, all communication between client and server must occur over HTTPS. Token best-practice guides emphasize that tokens must not be sent over non-HTTPS connections, as the requests could be intercepted and tokens compromised.[13][31] Thus, the FastAPI backend should be served behind a TLS-terminating proxy or a platform that handles TLS (such as a cloud load balancer), and the client’s `API_BASE_URL` should begin with `https://`.

### 5.3. Token Lifetime, Rotation, and Revocation Strategy

Token lifetimes should be calibrated to limit damage from token compromise while maintaining usability. Duende Software recommends keeping JWTs short-lived, often in the range of 5–15 minutes, with refresh tokens granting the ability to obtain new tokens without login.[13] Auth0 similarly advises that tokens must have explicit expiration (`exp`), and that systems should have strategies for both expiring and revoking tokens, including refresh token expiration and rotation.[21][31]

For an initial implementation, an access token lifetime of 15 minutes represents a reasonable balance, as used in FastAPI JWT tutorials.[2] If the app includes highly sensitive operations or elevated privileges, shorter lifetimes may be appropriate, especially when combined with refresh tokens and device identification. When refresh tokens are introduced, it is important to implement either rotation (where each use invalidates the previous refresh token and issues a new one) or idle and absolute expiration limits, so that unused tokens are eventually invalidated, and token reuse can be detected as a potential replay attack.[10][21]

Revocation is more challenging in stateless JWT systems. If immediate revocation is required (for example, after password changes or account compromise), approaches include maintaining a blacklist of revoked token IDs or using reference tokens stored server-side rather than self-contained JWTs.[13] For many mobile applications, revocation at the refresh-token level may suffice: access tokens expire quickly, and revoking refresh tokens prevents new tokens from being issued.

### 5.4. Password Policies and Validation

Security guidance from large providers like Microsoft encourages organizations to adopt password policies that emphasize length and diversity, ban commonly used passwords, and avoid forced periodic rotation which users may circumvent with predictable patterns.[26] Specifically, recommendations include minimum lengths of at least 14 characters, avoiding easy-to-guess passwords like `password` or `123456`, and encouraging users not to reuse organizational passwords on external sites.[26]

Client-side validation in React Native can enforce basic rules such as minimum length, presence of uppercase and lowercase letters, digits, and absence of whitespace, as demonstrated in password-validation tutorials.[41] For example, a validation function can check for length, allowed characters, and complexity before enabling the login or signup button, reducing unnecessary API calls.[41] However, password validation must also occur on the backend, which can enforce constraints via Pydantic validators or explicit checks before hashing. Rejecting passwords that fail complexity requirements and returning clear error messages gives users immediate feedback.

In addition, multi-factor authentication (MFA) and other identity-protection features can be layered on top of password-based authentication for higher-risk scenarios, as advised by password-policy best-practice documents.[26] This playbook focuses on the foundational email/password and JWT layer, but the backend architecture can be extended to support OTPs, WebAuthn, or other second factors.

### 5.5. Where to Store JWTs and How Much Data to Encode

Decisions about where to store JWTs differ between native and web contexts. For native apps, Duende recommends using platform-secure storage APIs like Keychain or Keystore for tokens that allow system access, including refresh tokens.[13] Expo-secure-store provides the appropriate abstraction for this functionality, and is used in this playbook for native platforms.[3][3][19][3]

For web applications, recommended practice is to use Secure, HttpOnly cookies to store tokens, instead of localStorage or sessionStorage, which are accessible to JavaScript and therefore vulnerable to XSS.[13] Secure cookies can be configured with flags that restrict them to HTTPS, specific domains, and limited durations, and can integrate with CSRF protection mechanisms. However, when using React Native Web as a SPA with a purely API-based backend, cookies may require more careful CORS and credential configuration. If localStorage or in-memory tokens are used, they must be accompanied by strong XSS mitigations and minimal token lifetimes.[13][31]

JWT payloads should contain only the minimal information required. Auth0’s token best-practices and Duende’s JWT guidance both caution against including sensitive personal data in the payload, since tokens are easily decoded even though they are signed.[13][31] Typical claims include a user ID, issued-at (`iat`), expiration (`exp`), and perhaps roles or scopes. Including large or sensitive objects can affect performance and increase risk if tokens are leaked. For this playbook, the `sub` claim encodes a namespaced user ID, and no additional user metadata is embedded in the token.

## 6. Testing Strategy for Backend and Client

### 6.1. Backend Testing with FastAPI’s TestClient and pytest

FastAPI’s testing tutorial demonstrates how to test FastAPI applications using `TestClient`, which is based on the HTTPX library, and `pytest` for executing test cases.[24] Testing authentication flows involves simulating requests to registration and login endpoints, verifying response codes and bodies, and confirming that protected routes reject unauthenticated requests while allowing authenticated requests with valid tokens.

A `tests/test_auth.py` might look like:

```python
# tests/test_auth.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_and_login_user():
    email = "test@example.com"
    password = "StrongPass123!"

    # Register
    response = client.post("/api/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert "id" in data

    # Login
    response = client.post(
        "/api/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Access protected route
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    me_data = response.json()
    assert me_data["email"] == email
```

FastAPI’s testing guide notes that test functions are normal `def` functions, the `TestClient` handles the asynchronous nature of FastAPI routes internally, and that HTTPX-style methods are used to send requests.[24] Additional tests can cover invalid credentials, duplicate registration attempts, and expired or malformed tokens.

Running `pytest` in the project root executes these tests and reports results. The testing tutorial emphasizes that `pytest` automatically discovers files with `test_` prefix and functions starting with `test_`, and that simple `assert` statements suffice for verification.[24]

### 6.2. Manual Testing via OpenAPI /docs and MongoDB Atlas

FastAPI automatically generates an interactive OpenAPI documentation interface at `/docs` (Swagger UI), allowing developers to manually execute requests, inspect responses, and experiment with query parameters and request bodies.[11][30] When the server is running (for instance via `uvicorn main:app --reload`), visiting `http://127.0.0.1:8000/docs` in a browser reveals the available endpoints, including `/api/auth/register`, `/api/auth/login`, and `/api/auth/me` with their schemas, documented request bodies, and response models.[11][30]

Developers can use this interface to register new users, log in, and then authorize requests by clicking the "Authorize" button in Swagger UI, pasting the `Bearer <token>`, and testing the `/api/auth/me` endpoint. This manual testing complements automated tests by providing visual feedback and ensuring that the OpenAPI schema matches expectations.[11]

At the database level, MongoDB Atlas’s web UI allows inspection of the `auth_db` database and `users` collection, verifying that inserted documents include email, full_name, and hashed_password fields, and that passwords are never stored in plaintext.[9][11][11] When using a local MongoDB instance, the `mongosh` shell can be used for similar inspection, and to verify that the unique index on `email` exists.

### 6.3. Client-Side Testing with Expo Go and Web

On the client side, Expo’s development tooling enables live reloading and interactive testing on both mobile and web platforms. The `npx expo start` command starts a bundler that serves the project to Expo Go on physical devices and via the browser for React Native Web.[29] Developers can perform the following manual testing sequence:

First, ensure that the `API_BASE_URL` in the Axios client matches the backend server URL, including `/api` prefix. In development, this might be `http://localhost:8000/api` or an IP address accessible to the device.

Second, on web, open the app in the browser via the Expo dev server and attempt to register and log in using test credentials. Successful login should result in calls to the `/api/auth/login` endpoint and the receipt of a JWT that is stored (in the development example, in memory for web).

Third, on mobile, test the same flows via Expo Go. When login succeeds, inspect logs to ensure that the Authorization header is present on subsequent API calls, and that protected endpoints return user data.

Client-side error handling can be enhanced using global Axios error interceptors, as described in error-handling and retry logic guides for React Native, adding consistent user-facing error messages and optional retries for network failures and server errors.[8][15] Testing should verify that network errors, HTTP 400 responses (bad credentials), and 401 responses (invalid or expired tokens) result in predictable behavior such as error messages, prompts to re-authenticate, or silent token refresh attempts.

### 6.4. Observability, Logging, and Monitoring

Beyond functional testing, monitoring authentication activity and API performance is important in production. FastAPI’s middleware model enables logging of incoming requests and outgoing responses, as well as integration with metrics systems like Prometheus.[37][27] For example, a logging middleware can print method, path, and response status for each request, while a Prometheus integration can expose metrics such as request rate and error rate at a `/metrics` endpoint.[27][37]

A monitoring tutorial for FastAPI shows how to create a middleware that measures request durations, logs requests and responses, and exposes metrics for scraping by Prometheus.[27] Applying similar patterns to the authentication API allows teams to detect anomalies such as spikes in failed login attempts, unusual access patterns, and performance degradation. Combined with logs from the client application (for example, using a centralized logging service or crash report tool), these metrics support proactive maintenance and incident response.

## 7. Common Pitfalls and How to Avoid Them

### 7.1. CORS Misconfiguration and /api Prefix Mismatch

One of the most frequent integration problems between an SPA or mobile client and a backend is CORS misconfiguration. FastAPI’s CORS documentation explains that when a frontend running in the browser calls a backend on a different origin, the browser sends an OPTIONS preflight request; the backend must respond with appropriate CORS headers for the request to proceed.[20] If `allow_origins` is too restrictive or does not include the exact domain and port used by the Expo dev server, requests may fail with CORS errors in the browser console.

Additionally, using `"*"` for `allow_origins` while `allow_credentials` is true and Authorization headers are used may cause browsers to reject the responses, since wildcard origins are incompatible with credentialed requests.[20] The solution is to specify the exact allowed origins, such as `http://localhost:19006` for Expo web and the production domain for the deployed SPA, and to set `allow_credentials=True`.

Another subtle pitfall is forgetting the `/api` prefix on client URLs. If the Axios base URL or endpoint paths do not include `/api`, requests will not reach the intended routes. Ensuring that the Axios client’s base URL ends in `/api` and that FastAPI’s routers are included with the same prefix avoids such mismatches.

### 7.2. Expo SDK 54 Networking and Hermes Issues

Expo SDK versions occasionally introduce platform-specific quirks. For SDK 54, a GitHub issue documents a networking bug on Android related to the Hermes JavaScript engine that results in Axios POST requests failing with "Network Error". The issue suggests workarounds such as polyfills or disabling Hermes for the time being.[17] When encountering unexplained network errors on Android while requests succeed on iOS and web, investigating SDK-specific issues and testing with Hermes disabled can help isolate the problem.

The Expo SDK 54 changelog and upgrade guides also recommend using `expo-doctor` and `npx expo install --fix` to align dependency versions and check for compatibility issues.[1][12] Developers should ensure that the Expo version used by the client matches the SDK template and that all packages, including `expo-secure-store`, are installed with `expo install` for correct native bindings.[3][29][3]

### 7.3. MongoDB Indexing and ObjectId Handling

Failing to create a unique index on the `email` field can result in multiple user documents with the same email address, complicating login logic and causing ambiguous results. MongoDB’s documentation on unique indexes explains how to create such an index and emphasizes that unique constraints ensure no two documents share the same value for indexed fields.[23] In code, calling `create_index("email", unique=True)` during startup ensures that duplicates are prevented.[23]

ObjectId handling is another source of confusion. By default, MongoDB uses `ObjectId` values for the `_id` field, which are not JSON-serializable. The MongoDB FastAPI integration tutorial recommends converting `ObjectId` values to strings when returning them to clients or using custom Pydantic fields like `PyObjectId` that handle conversion automatically.[11][11] Failing to convert `_id` leads to serialization errors when returning user documents in JSON responses.

### 7.4. JWT Signature and Algorithm Errors

JWT-related errors commonly arise when the secret key changes, the algorithm mismatch occurs, or tokens expire. If `ALGORITHM` is set inconsistently between encoding and decoding (for example, encoding with HS256 and decoding with a different algorithm), `python-jose` will raise JWT errors.[2] Similarly, if the secret key is rotated without invalidating existing tokens, previously issued tokens will fail signature verification, resulting in 401 unauthorized responses.

Best-practice resources emphasize always specifying a strong signing algorithm, such as HS256 for symmetric keys or RS256/ES256 for asymmetric keys, and never allowing an algorithm of `"none"`.[13][31] When using symmetric keys, ensure that the same secret key and algorithm are used consistently across all services that issue and verify tokens. If the secret key is changed intentionally, plan for revoking or expiring existing tokens and updating clients gracefully.

Token expiration errors occur when the `exp` claim is in the past. On the server side, JWT libraries will raise an exception indicating that the token has expired. In such cases, clients must be prepared to handle 401 responses and either prompt the user to log in again or use a refresh token to obtain a new access token. Clock skew between client and server can also cause tokens to appear expired prematurely, so relying on server-side `exp` validations and ignoring client clocks in token logic is recommended.

### 7.5. Insecure Token Storage on Web and Native

On web, storing access tokens in localStorage or sessionStorage is an easy but risky choice: any XSS vulnerability in the application allows an attacker to read stored tokens and use them to impersonate users. Duende and Auth0 both discourage using such storage for sensitive tokens, recommending HttpOnly cookies as a more secure alternative.[13][31] If localStorage must be used, implement defense-in-depth measures like strict Content Security Policy, input sanitization, and minimal token lifetimes.

On native platforms, storing tokens in AsyncStorage or unencrypted files undermines platform security features. Expo’s data storage documentation distinguishes between AsyncStorage, which is unencrypted, and SecureStore, which is encrypted and backed by device keychain/keystore, making it suitable for tokens and keys.[19] Thus, tokens should be stored in `expo-secure-store` on iOS and Android, and never in plain AsyncStorage for sensitive use cases.[19][3]

Furthermore, developers must be cautious not to log tokens in debug logs or analytics events, which can leak them to log aggregators or crash-reporting tools. Server-side logs and client logs should redact Authorization headers and token values where possible.

### 7.6. Password Handling Pitfalls

Common mistakes in password handling include storing plaintext passwords, using weak or unsalted hashes, and relying solely on client-side validation. FastAPI’s extra-models documentation explicitly warns developers to never store plaintext passwords and always store secure hashes, an admonition echoed across security best-practice resources.[16][26] Using bcrypt with appropriate rounds and a unique salt per password protects against offline cracking and rainbow-table attacks, although it does not defend against credential stuffing when passwords are reused across services.[35]

On the client, neglecting to disable login buttons during validation can result in repeated API calls with invalid or empty input, wasting server resources and complicating error handling. React Native validation tutorials show how to disable login buttons until email and password meet minimal syntactic criteria, improving user experience.[41] However, client-side validation should never be treated as a security boundary; the backend must re-validate all inputs and enforce password policies.

## 8. Conclusion and Recommended Next Steps

This playbook has presented a detailed, end-to-end integration strategy for implementing custom JWT-based email/password authentication using an Expo React Native (SDK 54) client, a FastAPI backend with all routes under `/api`, and MongoDB for user data storage. On the backend, FastAPI integrates with MongoDB via an asynchronous client, enforces unique email addresses through MongoDB indexes, and uses bcrypt to hash passwords securely, ensuring that plaintext passwords are never stored or returned.[11][16][11][23] JWTs are issued using `python-jose` with HS256, controlled through environment-managed secret keys, and validated for each protected request using FastAPI’s security dependencies, aligning with OAuth2 and JWT best practices for token lifetimes, minimal claims, and HTTPS-only transmission.[2][13][31]

On the client side, Expo SDK 54 and React Native Web provide a unified codebase that runs on iOS, Android, and web. Expo-secure-store, backed by platform keychains and keystores, is used to store tokens securely on native platforms, while web-specific storage approaches are carefully considered in light of JWT token-storage guidance, favoring secure cookies or cautious use of in-memory storage.[3][3][13][19][3] Axios instances with request interceptors automatically attach Authorization headers to outbound API requests, and a React context, inspired by Expo Router’s authentication patterns, maintains global authentication state and protects routes on the client.[8][22][25][39]

Testing strategies combine FastAPI’s `TestClient` and pytest for backend unit and integration tests, the automatically generated `/docs` interface for manual verification and inspection of API schemas, and Expo’s development tools for interactive testing on both mobile and web clients.[11][24][29][30] Observability can be enhanced by logging middlewares and Prometheus metrics integration, providing visibility into authentication traffic and performance.[27][37]

Security best practices underscore the importance of secret management via environment variables and configuration models, explicit CORS and HTTPS configuration, thoughtful token lifetime and refresh strategies, and careful token and password handling on both server and client. Guidance from Duende, Auth0, MongoDB, Microsoft, and others inform these recommendations, ensuring that the architecture is robust against common vulnerabilities such as token theft, weak passwords, and insecure storage.[13][21][23][26][31]

For next steps in a production setting, teams may consider augmenting this foundation with refresh-token rotation and device-bound token families to reduce replay risks, MFA or WebAuthn to harden authentication, rate limiting and IP throttling on login endpoints to mitigate brute-force attacks, and structured logging and alerting to detect anomalies in authentication patterns.[10][13][14][27][35] They may also evaluate moving to asymmetric JWT signing (for example, RS256) if multiple services or external identity providers are involved, and introducing reference tokens or session-backed authentication for scenarios requiring easier token revocation.[13][31]

By following the patterns, code examples, and guidelines outlined in this report, developers can construct a scalable, secure, and maintainable authentication layer for Expo-based mobile and web applications backed by FastAPI and MongoDB, while preserving the flexibility to evolve toward more sophisticated identity solutions as their applications grow.

---
Sources:
1. https://expo.dev/changelog/sdk-54
2. https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
3. https://docs.expo.dev/versions/latest/sdk/securestore/
4. https://www.youtube.com/watch?v=4fKavID0hoI
5. https://curity.io/resources/learn/oauth-for-mobile-apps-best-practices/
6. https://www.youtube.com/watch?v=ac4p2jelZdk&vl=en
7. https://fastapi.tiangolo.com/reference/apirouter/
8. https://www.youtube.com/watch?v=-u04JD5Eo-c
9. https://www.mongodb.com/resources/languages/python
10. https://oneuptime.com/blog/post/2026-01-15-react-native-jwt-refresh-tokens/view
11. https://www.mongodb.com/docs/languages/python/pymongo-driver/current/integrations/fastapi-integration/
12. https://docs.expo.dev/workflow/upgrading-expo-sdk-walkthrough/
13. https://duendesoftware.com/learn/best-practices-using-jwts-with-web-and-mobile-apps
14. https://supertokens.com/blog/implementing-a-forgot-password-flow
15. https://oneuptime.com/blog/post/2026-01-15-react-native-api-errors-retry/view
16. https://fastapi.tiangolo.com/tutorial/extra-models/
17. https://github.com/expo/expo/issues/40061
18. https://www.youtube.com/watch?v=Go4wYJJhR3k
19. https://docs.expo.dev/develop/user-interface/store-data/
20. https://fastapi.tiangolo.com/tutorial/cors/
21. https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/
22. https://docs.expo.dev/develop/authentication/
23. https://www.mongodb.com/docs/manual/core/index-unique/
24. https://fastapi.tiangolo.com/tutorial/testing/
25. https://docs.expo.dev/router/advanced/authentication/
26. https://learn.microsoft.com/en-us/microsoft-365/admin/misc/password-policy-recommendations?view=o365-worldwide
27. https://www.youtube.com/watch?v=3ZOFHFxnvxE
28. https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/
29. https://docs.expo.dev/tutorial/create-your-first-app/
30. https://fastapi.tiangolo.com/tutorial/body/
31. https://auth0.com/docs/secure/tokens/token-best-practices
32. https://www.herodevs.com/blog-posts/reauth-in-angular-made-easy
33. https://www.billtalkstoomuch.com/2016/08/23/the-app-great-ways-to-debug-azure-mobile-apps-part-1/
34. https://www.youtube.com/watch?v=hbvnsse4xGI
35. https://dev.to/mochafreddo/finding-the-optimal-bcrypt-rounds-for-your-machine-2kpf
36. https://www.youtube.com/watch?v=M8u_w6_o584
37. https://fastapi.tiangolo.com/tutorial/middleware/
38. https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/insert/
39. https://docs.expo.dev/router/advanced/authentication-rewrites/
40. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
41. https://www.youtube.com/watch?v=vfHekEsxgRk

`````

---
## Sample 4: JWT + mocked OTP + roles — mobile (Expo React Native)

| | |
|---|---|
| HTTP status | 200 |
| **Latency** | **317.9 s** |
| **Total cost (from Perplexity's `usage.cost`)** | **$1.25735** |
| Cost breakdown | input $0.00053 · output $0.13248 · citation $0.06797 · reasoning $0.76137 · search $0.295 |
| Tokens | prompt 267 · completion 16,560 · citation 33,983 · reasoning 253,791 |
| Search queries run by Perplexity internally | 59 |
| Playbook length | 77,531 chars |
| Citations | 50 |

### Input — what our agent asked the tool (verbatim)

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

### Exact API request sent to Perplexity

```json
{
  "url": "https://api.perplexity.ai/chat/completions",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer pplx-REDACTED-MOCK-KEY",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "sonar-deep-research",
    "messages": [
      {
        "role": "system",
        "content": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: expo react native, mongodb database, react native web\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
      },
      {
        "role": "user",
        "content": "Create a detailed integration playbook for INTEGRATION: JWT-based authentication for Expo React Native app with FastAPI backend. Need:\n1. Email + password registration & login (working JWT auth)\n2. Phone OTP mocked login (accept any 6-digit OTP for now, just generate JWT)\n3. Role-based auth (customer vs admin role)\n4. Token storage via expo-secure-store on client\n\nCONSTRAINTS: \n- Backend FastAPI with MongoDB (Motor)\n- Frontend Expo Router with React Native\n- Use bcrypt for password hashing\n- JWT tokens for session in expo react native, mongodb database, react native web application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
      }
    ]
  }
}
```

### Exact output returned to our agent (verbatim, 80,574 chars)

This is the complete tool result the coding agent receives — the playbook exactly as Perplexity wrote it, with the citation URLs appended as a `Sources:` list by our tool layer. (It is then wrapped as `{"content": "<below>", "cost": 1.5}` — the `1.5` is an internal billing unit, unrelated to the Perplexity dollar cost.)

`````markdown
# End-to-end Integration Playbook: JWT Authentication between an Expo React Native App and a FastAPI + MongoDB Backend

This document presents a complete, end-to-end integration playbook for implementing JWT‑based authentication between an Expo React Native application (using Expo Router and React Native Web) and a FastAPI backend backed by MongoDB via Motor. It covers email/password registration and login with bcrypt hashing, a mocked phone OTP login flow that accepts any six-digit code for now, role-based access control distinguishing customer and admin users, and secure token storage on the client using `expo-secure-store`. The report explains the architecture and security model, walks through precise installation and configuration steps, provides extensive backend and frontend code samples, details testing strategies, and analyzes common pitfalls and their mitigations. The goal is for a developer to be able to follow this document from an empty folder to a working, secure authentication stack with clear upgrade paths for production‑grade hardening.

## Overall Architecture and Security Model

### High-level architecture

The system consists of three main parts: a FastAPI backend, a MongoDB database accessed through Motor, and an Expo application that runs on iOS, Android, and Web via React Native Web and Expo Router. FastAPI is chosen because it combines high performance with automatic data validation, schema generation, and first‑class support for OAuth2 and JWT patterns, making it well suited for building secure APIs backed by typed Pydantic schemas.[31][9] MongoDB is accessed via Motor, the asynchronous driver that integrates naturally with FastAPI’s async model, enabling non‑blocking I/O when handling user and session data.[19][8]

Authentication is based on JSON Web Tokens (JWTs). A JWT is a compact, URL‑safe token composed of a header, payload, and signature, and is digitally signed with a shared secret using an HMAC algorithm such as HS256.[25] The server issues short‑lived JWT access tokens when the user successfully authenticates via email/password or mocked phone OTP, embedding claims such as the user identifier and their role(s) in the payload alongside an expiration (`exp`) timestamp.[25][29] On each subsequent request to a protected backend endpoint, the client presents this token in the `Authorization: Bearer <token>` header; the backend validates the signature, checks expiration, and uses the role information to decide whether to authorize the request.[25][49]

To safeguard user credentials, the backend never stores plaintext passwords but instead persists bcrypt hashes generated and verified using Passlib’s `CryptContext`. Passlib provides a high‑level abstraction for creating and verifying password hashes with modern algorithms such as bcrypt and PBKDF2, handling salting and parameter selection so that application code does not deal with low‑level cryptography directly.[33][50] This aligns with FastAPI’s documentation, which encourages secure password hashing and provides examples using Passlib.[9][32]

On the client side, the Expo app uses a React Context–based session provider, analogous to the Expo Router authentication example, to hold the current user session and expose sign‑in, sign‑out, and registration actions across the component tree.[4][4][21][45] Routes in Expo Router are grouped into authenticated and unauthenticated stacks, with navigation guards implemented using `Stack.Protected` so that only authenticated users can access application screens, and only admins can see admin‑only screens.[4][4][48] JWT access tokens are stored on-device using `expo-secure-store`, which wraps the native iOS Keychain and Android Keystore to provide encrypted key–value storage, significantly more secure than `AsyncStorage` for sensitive secrets such as authentication tokens.[2][2][2][2][34]

The mocked phone OTP flow is designed for development convenience: any six‑digit numeric code is accepted as valid, and the backend simply verifies that the format is correct. In a production setting this logic must be replaced with a real OTP generator and SMS provider such as Twilio, along with robust expiry and rate limiting, but this playbook keeps the flow simple intentionally while still validating input shape and passing through the full authentication pipeline.[46][24][37]

Finally, security is reinforced by short JWT lifetimes, explicit CORS configuration in FastAPI to support the Expo dev and web origins while allowing Bearer credentials, and clear separation of secrets via environment variables on the backend. JWT expiration times are set in minutes rather than days or months to reduce the window of token misuse if stolen, consistent with JWT security best practices.[15][29] The Expo app uses public environment variables only for non‑sensitive configuration such as the API base URL and never for secrets, as values prefixed with `EXPO_PUBLIC_` are inlined into the JavaScript bundle and therefore publicly visible.[42]

## Backend Foundation: FastAPI, Motor, JWT, and Bcrypt

### Backend environment setup and dependency installation

The backend is implemented in Python using FastAPI and Motor with an asynchronous event loop. To begin, you create and activate a dedicated virtual environment and install the required packages. FastAPI’s documentation shows how to set up a minimal app and notes that for OAuth2 flows it is convenient to install the standard extras.[18][9] The Motor documentation describes installing the MongoDB async driver with `pip install motor`.[8][19] Although Motor is now deprecated in favor of PyMongo’s async API and will eventually reach end of life, it is still fully functional for current projects; migrating to PyMongo’s async interface later is straightforward when needed.[8]

You can structure the backend project as a Python package named `backend`, but even a flat layout can work. The following terminal sequence illustrates a typical setup (adapt the Python version as needed):

```bash
mkdir fastapi-jwt-backend
cd fastapi-jwt-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install "fastapi[standard]" uvicorn motor "passlib[bcrypt]" pyjwt pydantic-settings python-dotenv
```

FastAPI with the `"standard"` extra installs Uvicorn, `python-multipart`, and other recommended components, and PyJWT provides JWT encoding/decoding utilities similar to those used in FastAPI’s JWT security tutorial and in dedicated blog posts.[9][1] Passlib’s bcrypt support comes from installing `passlib[bcrypt]`, which automatically configures bcrypt as an available hashing scheme.[33][50]

### Configuration management and environment variables

All sensitive configuration such as the JWT signing secret and MongoDB URI should be sourced from environment variables rather than hard‑coded in code. For this, you can use `pydantic-settings`, which provides a `BaseSettings` class that loads configuration from environment variables and optional `.env` files in a type‑safe way.[32] A central `config.py` keeps configuration cohesive.

Create `backend/config.py`:

```python
# backend/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MONGODB_URI: str = Field(..., description="MongoDB connection string")
    MONGODB_DB_NAME: str = Field("jwt_auth_demo", description="Database name")

    JWT_SECRET_KEY: SecretStr = Field(..., description="HS256 signing secret")
    JWT_ALGORITHM: str = Field("HS256", description="JWT signing algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(15, description="Access token lifetime in minutes")

    # For completeness, you can define a refresh lifetime for future use
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application metadata
    PROJECT_NAME: str = "FastAPI JWT Auth Demo"

settings = Settings()
```

In the project root, define a `.env` file for local development:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=jwt_auth_demo
JWT_SECRET_KEY=your_super_secret_signing_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

The `JWT_SECRET_KEY` is loaded as a `SecretStr` and should be long and random; it must never be exposed to clients. JWTs will be signed with HS256 using this secret, consistent with the JWT specification and typical HMAC usage.[25] Each token includes an `exp` claim representing the Unix timestamp at which the token expires; the playbook uses 15‑minute access tokens, aligning with recommendations to keep access tokens short‑lived and rely on refresh tokens for longer sessions if required.[15][29][41]

### MongoDB connection with Motor

Motor’s `AsyncIOMotorClient` provides an asynchronous interface to MongoDB. You typically create a single client on application startup and share it across requests; the Motor documentation emphasizes that obtaining database and collection objects from the client is cheap and does not perform I/O until an actual operation (like `find_one`) is awaited.[19] To integrate this cleanly with FastAPI, you can use startup and shutdown event handlers.

Create `backend/db.py`:

```python
# backend/db.py
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import FastAPI

from .config import settings

class MongoClientManager:
    client: Optional[AsyncIOMotorClient] = None

mongo_manager = MongoClientManager()

async def connect_to_mongo(app: FastAPI) -> None:
    mongo_manager.client = AsyncIOMotorClient(settings.MONGODB_URI)
    app.mongodb_client = mongo_manager.client
    app.mongodb_db = mongo_manager.client[settings.MONGODB_DB_NAME]

async def close_mongo_connection(app: FastAPI) -> None:
    client = getattr(app, "mongodb_client", None)
    if client:
        client.close()
```

In your main application file, you register these functions with FastAPI’s lifecycle:

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import connect_to_mongo, close_mongo_connection
from .routers import auth, users

app = FastAPI(title=settings.PROJECT_NAME)

# Configure CORS so that your Expo dev server and web origin can call the API with credentials.
origins = [
    "http://localhost:8081",  # Common Expo web dev port
    "http://localhost:19006",  # Alternate Expo web port
    "http://127.0.0.1:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo(app)

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection(app)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
```

FastAPI’s CORS tutorial explains that to accept Authorization headers and cookies from a different origin, you must not use the wildcard `"*"` for origins; instead, you explicitly list allowed origins as above, and set `allow_credentials=True`.[26][26] This configuration allows the Expo web bundle served at `localhost` to call the FastAPI backend with Bearer tokens in the Authorization header, while still preventing arbitrary third‑party origins from making credentialed requests.[26][26]

### Data models and Pydantic schemas

MongoDB stores documents as BSON, but Motor returns results as Python dictionaries. To enforce validation and define the API contract, you use Pydantic models for request and response bodies, as recommended by the FastAPI schema tutorial.[13] In Pydantic v2, models inherit from `BaseModel` and can use rich types such as `EmailStr` for email validation.[13] Even though email validation performance and implementation details are evolving, using `EmailStr` is still a convenient way to ensure the `email` field has a valid format.

Create `backend/schemas.py`:

```python
# backend/schemas.py
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = Field(default=None, description="E.164 phone number as string")
    role: str = Field(default="customer", description="Role, e.g. 'customer' or 'admin'")

class UserCreate(UserBase):
    password: str = Field(min_length=8, description="Plaintext password for registration")

class UserLoginEmail(BaseModel):
    email: EmailStr
    password: str

class PhoneOtpLogin(BaseModel):
    phone: str = Field(description="E.164 phone number as string")
    otp: str = Field(description="6-digit OTP code as string")

class UserInDB(BaseModel):
    id: str
    email: EmailStr
    phone: Optional[str]
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: int
    type: str
```

Here `UserCreate` extends `UserBase` to include a `password` field for registration, but the hashed password is never exposed in public responses.[13] The `UserInDB` model represents the sanitized user document returned to clients; it could include additional fields such as `updated_at` or `is_active` in more complex applications. `TokenPayload` maps to the JWT payload claims and is used to type-check decoded tokens.

On the MongoDB side, you will store documents in a `users` collection with fields like `_id`, `email`, `phone`, `role`, `hashed_password`, and `created_at`. It is important to enforce uniqueness on the `email` field with a unique index, since Mongoose’s `unique` flag is not itself a validator but rather a helper that creates MongoDB unique indexes under the hood.[14][28] In Motor or plain MongoDB, you explicitly call `create_index` with `unique=True`.[40][28]

You can define a helper that ensures indexes are created at startup:

```python
# backend/models.py
from typing import Any
import pymongo
from motor.motor_asyncio import AsyncIOMotorDatabase

USER_COLLECTION_NAME = "users"

async def init_indexes(db: AsyncIOMotorDatabase) -> None:
    await db[USER_COLLECTION_NAME].create_index(
        [("email", pymongo.ASCENDING)],
        unique=True,
        name="uniq_email",
    )
```

Then call `init_indexes` in the startup event after connecting to MongoDB. This guarantees that duplicate email registrations result in a MongoDB duplicate key error rather than silently creating multiple users with the same email.[28][14][40]

### Password hashing with bcrypt via Passlib

Storing passwords as plaintext is never acceptable; instead, passwords must be hashed using a slow, salted algorithm such as bcrypt, PBKDF2, or Argon2.[9][33][50] Passlib provides a `CryptContext` manager that wraps one or more algorithms and offers high‑level `hash` and `verify` methods to create and check password hashes securely.[33][50] FastAPI’s own security tutorial uses Passlib and encourages this approach to password handling.[9]

Create `backend/security.py`:

```python
# backend/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Dict

import jwt  # PyJWT
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from .config import settings
from .schemas import TokenPayload

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-email")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

`CryptContext.hash` automatically generates a random salt and chooses parameter values, while `verify` compares a plaintext password to a previously stored hash and returns a boolean result.[33][50] Under the hood, this uses the bcrypt algorithm as configured, which is widely recommended for password storage due to its CPU cost and built‑in salt.[33][50]

The `OAuth2PasswordBearer` dependency configured with `tokenUrl="/auth/login-email"` tells FastAPI that tokens will be obtained by posting credentials to the `/auth/login-email` endpoint, following the OAuth2 “password” flow with Bearer tokens.[18][9] FastAPI uses this to generate interactive documentation that can obtain and reuse tokens, and to extract the token from the `Authorization` header on protected routes automatically.[18][49]

### JWT creation and verification

JWT tokens are encoded and decoded with PyJWT, using an HMAC secret stored in `settings.JWT_SECRET_KEY`. A JWT is composed of a base64‑encoded header specifying the algorithm (for example, HS256), a payload containing claims such as `sub` (subject), `role`, `exp` (expiration timestamp), and an HMAC signature over the header and payload using the secret.[25] The `exp` claim uses Unix time, i.e., seconds since January 1, 1970 UTC.[29] During creation, you choose an expiration time such as 15 minutes for access tokens; this is considered a good balance between security and usability.[15][29][41]

Add to `backend/security.py`:

```python
def create_access_token(
    subject: str,
    role: str,
    expires_delta: Optional[timedelta] = None,
    token_type: str = "access",
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    payload: Dict[str, Any] = {
        "sub": subject,
        "role": role,
        "exp": int(expire.timestamp()),
        "type": token_type,
    }
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )
    return token

def decode_token(token: str) -> TokenPayload:
    try:
        decoded = jwt.decode(
            token,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM],
        )
        return TokenPayload(**decoded)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
```

If the `exp` claim represents a time in the past, decoding should fail and the backend should return a `401 Unauthorized` response, prompting the client to re‑authenticate or to use a refresh token if implemented.[29][41] While this playbook focuses on access tokens, the same `create_access_token` function can be used with a different `token_type` and longer `expires_delta` to issue refresh tokens later.[41]

### Current user dependency and role-based authorization

To avoid repeating token parsing logic across endpoints, you define a dependency `get_current_user` that extracts the Bearer token using `oauth2_scheme`, decodes it, and loads the corresponding user document from MongoDB. FastAPI’s security tutorials demonstrate this pattern: the dependency receives the token as a `str`, verifies and decodes it, and either returns the user object or raises an HTTP error.[18][9][9] Once you have access to the current user, you can implement role‑based access control (RBAC) using additional dependencies that examine the `role` attribute and reject forbidden requests.[5][12][36]

Create `backend/deps.py`:

```python
# backend/deps.py
from typing import Annotated

from fastapi import Depends, HTTPException, status, Request
from motor.motor_asyncio import AsyncIOMotorDatabase

from .security import oauth2_scheme, decode_token
from .schemas import UserInDB
from .db import mongo_manager
from .models import USER_COLLECTION_NAME

async def get_db(request: Request) -> AsyncIOMotorDatabase:
    db = getattr(request.app, "mongodb_db", None)
    if db is None:
        raise RuntimeError("Database not initialized")
    return db

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> UserInDB:
    payload = decode_token(token)
    if payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    user_doc = await db[USER_COLLECTION_NAME].find_one({"_id": payload.sub})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return UserInDB(
        id=str(user_doc["_id"]),
        email=user_doc["email"],
        phone=user_doc.get("phone"),
        role=user_doc.get("role", "customer"),
        created_at=user_doc["created_at"],
    )

class RoleChecker:
    def __init__(self, allowed_roles: list[str]) -> None:
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        current_user: Annotated[UserInDB, Depends(get_current_user)],
    ) -> UserInDB:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to perform this action",
            )
        return current_user
```

The `RoleChecker` class implements role‑based access control using dependency injection: endpoints can include `Depends(RoleChecker(["admin"]))` to require that the current user has the admin role, a pattern similar to RBAC tutorials that use custom dependencies to check user roles in FastAPI.[5][12][36] If the user’s role is not in the allowed list, a `403 Forbidden` error is raised with a descriptive message.[38][36]

Note that the `sub` claim in the JWT stores the user’s identifier, which is used to retrieve the user from the database. This ensures that authorization checks are always based on server‑trusted data rather than client‑supplied values.[25][36]

### Auth and user routers: registration, email login, phone OTP login, and protected routes

With the security and database infrastructure in place, you can define the authentication endpoints in an `auth` router and user‑related endpoints in a `users` router, leveraging FastAPI’s `APIRouter` for modular organization.[47]

Create `backend/routers/auth.py`:

```python
# backend/routers/auth.py
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from ..deps import get_db
from ..schemas import UserCreate, UserLoginEmail, PhoneOtpLogin, Token
from ..security import hash_password, verify_password, create_access_token
from ..models import USER_COLLECTION_NAME

router = APIRouter()

@router.post("/register", response_model=Token)
async def register_user(
    payload: UserCreate,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> Token:
    users = db[USER_COLLECTION_NAME]
    hashed = hash_password(payload.password)
    user_doc = {
        "email": payload.email,
        "phone": payload.phone,
        "role": payload.role or "customer",
        "hashed_password": hashed,
        "created_at": datetime.now(timezone.utc),
    }
    try:
        result = await users.insert_one(user_doc)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user_id = str(result.inserted_id)
    access_token = create_access_token(subject=user_id, role=user_doc["role"])
    return Token(access_token=access_token)

@router.post("/login-email", response_model=Token)
async def login_with_email(
    payload: UserLoginEmail,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> Token:
    users = db[USER_COLLECTION_NAME]
    user_doc = await users.find_one({"email": payload.email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not verify_password(payload.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    user_id = str(user_doc["_id"])
    role = user_doc.get("role", "customer")
    access_token = create_access_token(subject=user_id, role=role)
    return Token(access_token=access_token)

@router.post("/login-phone-otp", response_model=Token)
async def login_with_phone_otp(
    payload: PhoneOtpLogin,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> Token:
    if not (len(payload.otp) == 6 and payload.otp.isdigit()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP format; must be six digits",
        )

    users = db[USER_COLLECTION_NAME]
    user_doc = await users.find_one({"phone": payload.phone})
    if not user_doc:
        # For development, automatically create a user for this phone number.
        user_doc = {
            "email": f"{payload.phone}@pseudo.local",
            "phone": payload.phone,
            "role": "customer",
            "hashed_password": hash_password("phone-otp-placeholder"),
            "created_at": datetime.now(timezone.utc),
        }
        result = await users.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id

    user_id = str(user_doc["_id"])
    role = user_doc.get("role", "customer")
    access_token = create_access_token(subject=user_id, role=role)
    return Token(access_token=access_token)
```

The `/auth/register` endpoint hashes the user’s password with bcrypt before saving it, in line with Passlib’s password hashing tutorial and FastAPI guidance on secure credential storage.[33][9] Duplicate emails are prevented by catching `DuplicateKeyError` from the unique index on `email` and returning a `400 Bad Request` error to the client.[28][14][40] The registration endpoint immediately issues a JWT access token upon success, simplifying the client flow.

`/auth/login-email` mirrors common username/password login flows: it retrieves the user by email, verifies the provided password against the stored bcrypt hash using `verify_password`, and returns a new JWT if everything matches.[33][9][32]

`/auth/login-phone-otp` represents the mocked OTP flow. It validates that the OTP is a six‑digit numeric string but does not verify it against any stored or SMS‑sent code. This is clearly insecure if deployed as‑is to production, but for development it allows you to exercise the same JWT generation and session management code paths without setting up an SMS provider. For real OTP systems, tutorials demonstrate generating random numeric codes, sending them via a provider like Twilio, storing them in a database with expiration, and verifying the user‑entered code against the stored value before granting access.[46][24][37] The endpoint also auto‑creates a user document for new phone numbers, using a pseudo email derived from the phone number and assigning the default `customer` role.

Next, define the user router in `backend/routers/users.py`:

```python
# backend/routers/users.py
from typing import Annotated

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..deps import get_current_user, get_db, RoleChecker
from ..schemas import UserInDB

router = APIRouter()

@router.get("/me", response_model=UserInDB)
async def read_current_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
) -> UserInDB:
    return current_user

admin_required = RoleChecker(["admin"])

@router.get("/admin-summary", dependencies=[Depends(admin_required)])
async def admin_summary(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> dict:
    user_count = await db["users"].count_documents({})
    return {"user_count": user_count, "message": "Admin-only summary"}
```

The `/users/me` endpoint is a typical “current user” route returning the authenticated user’s profile, similar to FastAPI’s `/users/me` examples in the JWT tutorial.[9][9][32] It demonstrates how the `get_current_user` dependency injects user information into the handler once the token is validated. The `/users/admin-summary` endpoint shows how to restrict access based on roles: the `admin_required` dependency is attached to the route via `dependencies`, so any request with a non‑admin role results in a 403 error.[12][36][5]

### Summary of backend flows

The key authentication flows implemented are summarized in the following table:

| Flow                     | Endpoint                | Credentials sent            | Backend checks                                             | Response                                              |
|--------------------------|-------------------------|-----------------------------|-----------------------------------------------------------|------------------------------------------------------|
| Registration             | `POST /auth/register`   | Email, password, phone, role | Valid email; email uniqueness; bcrypt hash saved         | 201 with JWT access token (role from payload)        |
| Email/password login     | `POST /auth/login-email`| Email, password             | User exists; bcrypt verify                               | 200 with JWT access token                            |
| Mocked phone OTP login   | `POST /auth/login-phone-otp` | Phone, 6‑digit OTP       | OTP format; auto‑create user if phone unknown            | 200 with JWT access token                            |
| Get current user         | `GET /users/me`         | Bearer token only           | JWT signature; `exp` not expired; user exists            | 200 with user profile (id, email, phone, role)       |
| Admin-only summary       | `GET /users/admin-summary` | Bearer token only        | Same as above; plus `role == 'admin'`                   | 200 for admins; 403 for non‑admins                   |

This foundation provides the server‑side mechanisms needed to support JWT‑based sessions in the Expo app, role‑aware route protection, and both email/password and OTP login flows.

## Frontend Foundation: Expo Router, Secure Token Storage, and Auth Context

### Creating the Expo project and installing dependencies

The client is an Expo project using Expo Router so that routes are defined by filesystem layout and navigation is handled declaratively.[48][45] The same codebase is intended to run on iOS, Android, and Web via React Native Web. The authentication state and token management are abstracted into a React Context, following patterns endorsed in Expo Router’s authentication guide and React Native tutorials on creating an auth or user context.[4][4][21][45]

From your preferred workspace, create the Expo project using the Router template:

```bash
npx create-expo-app jwt-auth-client -e with-router
cd jwt-auth-client

npx expo install expo-secure-store
npm install axios
```

`expo-secure-store` provides encrypted key–value storage using the device’s Keychain on iOS and Keystore on Android, making it appropriate for sensitive tokens and keys.[2][2][2][2][34] Axios is used for HTTP requests so that you can easily configure interceptors to attach Bearer tokens and handle automatic token refresh later; an alternative would be to use the Fetch API, which requires manually calling `response.json()` and lacks built‑in interceptors.[30][27][16] For authentication, either works; this playbook uses Axios for clarity of token injection, drawing on patterns from React Native JWT tutorials that use Axios interceptors for token management.[11]

### Environment variables and API base URL

Expo’s environment variable support automatically inlines variables starting with `EXPO_PUBLIC_` into your JavaScript bundle, making them accessible at build time via `process.env.EXPO_PUBLIC_*`.[42] This is convenient for non‑secret configuration such as your API base URL but must not be used for secrets such as JWT signing keys, since those would become part of the shipped bundle.[42]

In the Expo project root, add a `.env` file:

```env
EXPO_PUBLIC_API_URL=http://127.0.0.1:8000
```

When the Expo CLI runs, it loads `.env` and replaces any references to `process.env.EXPO_PUBLIC_API_URL` in your code with the literal value.[42] This allows you to switch between development, staging, and production backends by changing the environment variable without editing source code.

For convenience, define a small module `src/config/api.ts`:

```ts
// src/config/api.ts
export const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
```

The client will construct URLs such as `${API_BASE_URL}/auth/login-email` to reach the backend. Unlike secrets, this base URL is safe to expose because it is intended to be public; the backend still enforces authorization via JWT and RBAC.[42][26]

### Token storage abstraction with expo-secure-store

On native platforms, `expo-secure-store` encrypts stored values with platform key management systems, making it far superior to `AsyncStorage` for secrets.[2][2][2][2][34] AsyncStorage is not encrypted and is vulnerable to device compromise and debugging tools; several guides explicitly warn against storing tokens or API keys in AsyncStorage.[11][34] However, `expo-secure-store` is not fully supported on the web, where the underlying secure storage mechanisms differ. A pragmatic approach is to implement a storage abstraction that uses SecureStore on native, and an in‑memory object—optionally wrapped around `localStorage`—on web, with clear caveats that web security is weaker.

Create `src/lib/tokenStorage.ts`:

```ts
// src/lib/tokenStorage.ts
import * as SecureStore from "expo-secure-store";
import { Platform } from "react-native";

const ACCESS_TOKEN_KEY = "access_token";

let inMemoryToken: string | null = null;

async function saveToken(token: string): Promise<void> {
  if (Platform.OS === "web") {
    inMemoryToken = token;
    return;
  }
  await SecureStore.setItemAsync(ACCESS_TOKEN_KEY, token);
}

async function getToken(): Promise<string | null> {
  if (Platform.OS === "web") {
    return inMemoryToken;
  }
  return SecureStore.getItemAsync(ACCESS_TOKEN_KEY);
}

async function deleteToken(): Promise<void> {
  if (Platform.OS === "web") {
    inMemoryToken = null;
    return;
  }
  await SecureStore.deleteItemAsync(ACCESS_TOKEN_KEY);
}

export const tokenStorage = {
  saveToken,
  getToken,
  deleteToken,
};
```

The Expo SecureStore documentation explains how to install and configure the library and notes that each Expo project has an isolated storage namespace, and that data is encrypted using the system keystore mechanisms.[2][2][2][2][34] The above abstraction ensures that on native devices, tokens are stored encrypted; on web, tokens are ephemeral and lost on reload, but this trade‑off prevents storing tokens in ordinary localStorage, which is vulnerable to XSS and should not hold long‑lived tokens.[20][34]

### Auth context and session provider

To share authentication state across the app, you define an `AuthContext` that tracks whether the user is authenticated, the current user profile, the access token, and loading states. This mirrors the pattern shown in Expo Router’s authentication guide, which uses a context provider to expose a `session` object and `signIn`/`signOut` functions to all routes.[4][4][4][45] Similarly, React Native tutorials show how to create a `UserProvider` or `AuthProvider` that wraps the router and uses a `useAuth` hook for accessibility.[21]

Create `src/context/AuthContext.tsx`:

```tsx
// src/context/AuthContext.tsx
import React, { createContext, useContext, useEffect, useState, ReactNode } from "react";
import axios, { AxiosInstance } from "axios";
import { tokenStorage } from "../lib/tokenStorage";
import { API_BASE_URL } from "../config/api";

type User = {
  id: string;
  email: string;
  phone?: string | null;
  role: "customer" | "admin";
};

type AuthContextValue = {
  user: User | null;
  accessToken: string | null;
  isLoading: boolean;
  signInWithEmail: (email: string, password: string) => Promise<void>;
  registerWithEmail: (email: string, password: string, phone?: string | null) => Promise<void>;
  signInWithPhoneOtp: (phone: string, otp: string) => Promise<void>;
  signOut: () => Promise<void>;
  authAxios: AxiosInstance;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const authAxios = axios.create({
    baseURL: API_BASE_URL,
  });

  authAxios.interceptors.request.use((config) => {
    if (accessToken) {
      config.headers = config.headers ?? {};
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  });

  useEffect(() => {
    const bootstrap = async () => {
      try {
        const token = await tokenStorage.getToken();
        if (token) {
          setAccessToken(token);
          const meResponse = await axios.get<User>(`${API_BASE_URL}/users/me`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          setUser(meResponse.data);
        }
      } catch (err) {
        setUser(null);
        setAccessToken(null);
        await tokenStorage.deleteToken();
      } finally {
        setIsLoading(false);
      }
    };
    bootstrap();
  }, []);

  const handleAuthSuccess = async (token: string) => {
    setAccessToken(token);
    await tokenStorage.saveToken(token);
    const meResponse = await axios.get<User>(`${API_BASE_URL}/users/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setUser(meResponse.data);
  };

  const signInWithEmail = async (email: string, password: string) => {
    const response = await axios.post<{ access_token: string }>(
      `${API_BASE_URL}/auth/login-email`,
      { email, password },
    );
    await handleAuthSuccess(response.data.access_token);
  };

  const registerWithEmail = async (email: string, password: string, phone?: string | null) => {
    const response = await axios.post<{ access_token: string }>(
      `${API_BASE_URL}/auth/register`,
      { email, password, phone, role: "customer" },
    );
    await handleAuthSuccess(response.data.access_token);
  };

  const signInWithPhoneOtp = async (phone: string, otp: string) => {
    const response = await axios.post<{ access_token: string }>(
      `${API_BASE_URL}/auth/login-phone-otp`,
      { phone, otp },
    );
    await handleAuthSuccess(response.data.access_token);
  };

  const signOut = async () => {
    setUser(null);
    setAccessToken(null);
    await tokenStorage.deleteToken();
  };

  const value: AuthContextValue = {
    user,
    accessToken,
    isLoading,
    signInWithEmail,
    registerWithEmail,
    signInWithPhoneOtp,
    signOut,
    authAxios,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
};
```

This provider performs several key tasks. On initial mount, it calls `tokenStorage.getToken` to retrieve any previously stored JWT and, if found, calls `GET /users/me` to verify it and hydrate the user state.[2][34][45] If the token is invalid or expired, the call fails and the provider clears local state. For each successful authentication action—register, email login, or phone OTP login—the provider saves the access token in SecureStore, sets it in memory, and calls `/users/me` to fetch the user profile. Axios interceptors on `authAxios` ensure that every request made through this instance includes the `Authorization: Bearer <token>` header when a token is available, following patterns documented in JWT authentication examples with Axios interceptors.[11][30]

The `AuthContext` interface exposes strongly‑typed methods for `signInWithEmail`, `registerWithEmail`, and `signInWithPhoneOtp`, along with `signOut` and `authAxios`. This mirrors and extends the kind of session API the Expo Router authentication guide refers to when it discusses a `SessionProvider` and `signIn()`/`signOut()` functions that can be used from screens.[4][4][4][45]

### Integrating authentication with Expo Router

Expo Router organizes routes into directories such as `app/(auth)` for public screens and `app/(app)` for authenticated screens.[48] The authentication guide suggests using a context provider, a splash screen controller to defer hiding the splash screen until authentication state is loaded, and `Stack.Protected` guards that show different stacks depending on whether a session exists.[4][4][4][35]

First, create a small splash controller `src/splash.tsx`:

```tsx
// src/splash.tsx
import { SplashScreen } from "expo-router";
import React from "react";
import { useAuth } from "./context/AuthContext";

SplashScreen.preventAutoHideAsync();

export function SplashScreenController() {
  const { isLoading } = useAuth();

  if (!isLoading) {
    SplashScreen.hideAsync();
  }
  return null;
}
```

The Expo SplashScreen module provides `preventAutoHideAsync` and `hideAsync` to control when the splash screen disappears, which is useful when the initial authentication state must be loaded asynchronously.[35][4] In this setup, the splash is kept visible until `isLoading` becomes false, which happens after the `AuthProvider` either recovers a session or determines that no session exists.

Then, update `app/_layout.tsx` to wrap the stack in the `AuthProvider` and apply route guards:

```tsx
// app/_layout.tsx
import { Stack } from "expo-router";
import React from "react";
import { AuthProvider, useAuth } from "../src/context/AuthContext";
import { SplashScreenController } from "../src/splash";

function RootNavigator() {
  const { user } = useAuth();

  return (
    <Stack>
      <Stack.Screen name="(auth)" options={{ headerShown: false }} />
      <Stack.Screen name="(app)" options={{ headerShown: false }} />
      <Stack.Screen name="+not-found" />
      <Stack.Screen name="+error" />
      <Stack.Screen
        name="index"
        options={{
          redirect: user ? "/(app)/home" : "/(auth)/login",
        }}
      />
    </Stack>
  );
}

export default function RootLayout() {
  return (
    <AuthProvider>
      <SplashScreenController />
      <RootNavigator />
    </AuthProvider>
  );
}
```

Expo Router’s authentication guide illustrates a similar approach where a `SessionProvider` wraps the root layout and a `RootNavigator` chooses between `(app)` and `sign-in` screens based on session state.[4][4][4] Instead of `Stack.Protected`, which is available in newer Expo Router versions and allows declarative guards, this example uses conditional redirects via the `redirect` option and by structuring the app so that the `(app)` group’s screens themselves consult `useAuth` to decide whether to render content or trigger a redirect. In current Expo Router versions, either pattern—`Stack.Protected` or conditional logic—is viable for protecting routes.[4][48]

You can further refine route protection by adding an `index` screen inside `(auth)` for login and ensuring that all screens inside `(app)` check that `user` is non‑null and, when necessary, that `user.role === "admin"`.

In `app/(auth)/login.tsx`:

```tsx
// app/(auth)/login.tsx
import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import { useAuth } from "../../src/context/AuthContext";
import { Link, useRouter } from "expo-router";

export default function LoginScreen() {
  const { signInWithEmail, signInWithPhoneOtp } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");

  const handleEmailLogin = async () => {
    await signInWithEmail(email, password);
    router.replace("/(app)/home");
  };

  const handlePhoneOtpLogin = async () => {
    await signInWithPhoneOtp(phone, otp);
    router.replace("/(app)/home");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Email Login</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        autoCapitalize="none"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <Button title="Login with Email" onPress={handleEmailLogin} />

      <Text style={styles.title}>Phone OTP (Mocked)</Text>
      <TextInput
        style={styles.input}
        placeholder="Phone"
        keyboardType="phone-pad"
        value={phone}
        onChangeText={setPhone}
      />
      <TextInput
        style={styles.input}
        placeholder="6-digit OTP"
        keyboardType="number-pad"
        value={otp}
        onChangeText={setOtp}
      />
      <Button title="Login with Phone OTP" onPress={handlePhoneOtpLogin} />

      <Link href="/(auth)/register">No account? Register</Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: "center", gap: 16 },
  title: { fontSize: 18, fontWeight: "bold" },
  input: { borderWidth: 1, borderColor: "#ccc", padding: 8, borderRadius: 4 },
});
```

The email login flow calls `signInWithEmail` with the provided credentials, which in turn sends a POST request to `/auth/login-email` and, upon success, stores the access token and fetches `/users/me`. The phone OTP login flow does the same with `/auth/login-phone-otp`, sending phone and OTP values to the server. The OTP input expects a six‑digit code; however, because the server accepts any format that matches six digits, there is no SMS roundtrip involved in this mock. In a real application, you would call an endpoint like `/auth/send-otp` to trigger SMS sending, and then a `/auth/verify-otp` endpoint to verify user input, consistent with patterns seen in Twilio/OTP tutorials.[46][24][37]

In `app/(auth)/register.tsx`:

```tsx
// app/(auth)/register.tsx
import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import { useAuth } from "../../src/context/AuthContext";
import { useRouter } from "expo-router";

export default function RegisterScreen() {
  const { registerWithEmail } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    await registerWithEmail(email, password, phone);
    router.replace("/(app)/home");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create Account</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        autoCapitalize="none"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Phone (optional)"
        keyboardType="phone-pad"
        value={phone}
        onChangeText={setPhone}
      />
      <TextInput
        style={styles.input}
        placeholder="Password (min 8 chars)"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <Button title="Register" onPress={handleRegister} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: "center", gap: 16 },
  title: { fontSize: 18, fontWeight: "bold" },
  input: { borderWidth: 1, borderColor: "#ccc", padding: 8, borderRadius: 4 },
});
```

Registration uses the backend’s `/auth/register` endpoint, which immediately issues an access token upon successful insertion. This pattern is common in modern SPAs and mobile apps and aligns with the idea that after creating an account, the user should be considered logged in without requiring a separate login step.[32][11]

The authenticated home screen might look like this in `app/(app)/home.tsx`:

```tsx
// app/(app)/home.tsx
import React, { useEffect, useState } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import { useAuth } from "../../src/context/AuthContext";
import { useRouter } from "expo-router";

export default function HomeScreen() {
  const { user, signOut, authAxios } = useAuth();
  const router = useRouter();
  const [adminSummary, setAdminSummary] = useState<string | null>(null);

  useEffect(() => {
    if (!user) {
      router.replace("/(auth)/login");
      return;
    }
    if (user.role === "admin") {
      authAxios
        .get<{ user_count: number; message: string }>("/users/admin-summary")
        .then((res) => {
          setAdminSummary(`Users in system: ${res.data.user_count}`);
        })
        .catch(() => {
          setAdminSummary(null);
        });
    }
  }, [user]);

  if (!user) {
    return null;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, {user.email}</Text>
      <Text>Your role: {user.role}</Text>
      {adminSummary && <Text>{adminSummary}</Text>}
      <Button
        title="Sign Out"
        onPress={async () => {
          await signOut();
          router.replace("/(auth)/login");
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: "center", gap: 16 },
  title: { fontSize: 20, fontWeight: "bold" },
});
```

This screen demonstrates how the client can enforce role‑based UI behavior by conditionally calling the admin‑only endpoint `/users/admin-summary` and showing extra information when the user is an admin. The backend still enforces authorization via the `RoleChecker` dependency; even if a non‑admin user forced a call to the admin endpoint, the backend would respond with 403 and the client would see an error.[5][12][36]

### HTTP requests and Authorization header

Axios is configured in the `AuthProvider` with a base URL and a request interceptor that injects the Bearer token when present. This pattern is consistent with JWT authentication tutorials that use Axios interceptors to attach `Authorization: Bearer <token>` headers to each request automatically.[11][30] For contexts where you prefer the Fetch API, the same effect can be achieved by explicitly passing the header for each request:

```ts
const response = await fetch(`${API_BASE_URL}/users/me`, {
  method: "GET",
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});
const user = await response.json();
```

The Fetch API documentation and examples show that headers are passed via the `headers` option and that Bearer tokens are conveyed through the `Authorization` header.[27][25][49] Axios simply wraps this pattern, automatically serializing JSON payloads and parsing JSON responses.[30][11]

## End-to-end Flows and Security Considerations

### Email/password registration and login

The email/password flow is designed to adhere to standard security best practices for password handling and token issuance. When the user completes the registration form in the Expo app and submits it, the client sends a JSON body containing the email, plaintext password, and optional phone number to `POST /auth/register`. FastAPI automatically validates the body against `UserCreate`, ensuring that the email has correct format, the password meets minimum length, and the phone, if supplied, is a string.[13] If a user with the same email already exists, MongoDB’s unique index raises a `DuplicateKeyError`, which the endpoint converts into a `400 Bad Request` response with an informative message.[28][14][40]

Internally, the backend uses `hash_password` to convert the plaintext password into a bcrypt hash, which includes a salt and cost factor such that brute‑force attacks are slowed.[33][50][9] The hash—not the password—is stored in the `hashed_password` field. When the user later attempts to log in via `POST /auth/login-email`, the backend retrieves the user by email and calls `verify_password` to compare the supplied password to the stored hash. Passlib’s `verify` method ensures that timing differences are minimized and that only matching password/hash pairs succeed.[33][50]

Upon successful login or registration, the backend calls `create_access_token` to form a JWT with claims `sub` (user ID as a string), `role` (the user’s role), `exp` (Unix timestamp `now + 15 minutes`), and `type` set to `"access"`. The JWT is signed with HS256 using the secret loaded from `JWT_SECRET_KEY` and returned to the client in the JSON field `access_token`.[25][29][9] The client stores this token in `expo-secure-store` and immediately calls `/users/me` to fetch the current user profile, which is then kept in the `AuthContext` state.[2][34][45]

JWT expiration is handled on the backend; if the `exp` timestamp has passed, PyJWT raises an `ExpiredSignatureError` and the `decode_token` function responds with a 401 error. This means that clients must handle the case where previously working tokens start failing due to expiration. While this playbook does not implement refresh tokens, you could add a `/auth/refresh-token` endpoint that accepts a long‑lived refresh token, validates it, and issues a new short‑lived access token, as described in resources on JWT expiration and refresh token patterns.[29][41][15] For development, simply re‑authenticating via email/password or OTP when a token expires is sufficient.

### Phone OTP mocked login

The phone OTP flow in this playbook is intentionally simplified: the Expo app collects a phone number and a six‑digit code, and the backend accepts any OTP that matches the pattern `[0-9]{6}` as valid. This allows front‑end and backend developers to exercise OTP‑like flows without integrating a real SMS provider or managing OTP storage and expiration. The `login_with_phone_otp` endpoint validates the OTP format and either finds an existing user document with the same phone number or creates a new one, using a placeholder password and the default role `customer`. It then issues a JWT just like in the email/password flow.

In production, such a mocked OTP system would be insecure because an attacker could simply guess any six‑digit code; even though the search space is 10^6, modern automation can exhaust it quickly, and without rate limiting or lockout, this is unacceptable.[37] Real OTP workflows use randomly generated codes, short expiration windows (typically a few minutes), attempt limits, and out‑of‑band delivery (via SMS or push notifications), with verification logic that checks the supplied OTP against a stored or computed value.[46][24][37] Additionally, OTP mechanisms are usually a second factor layered on top of password‑based authentication rather than a standalone factor.[37]

A future upgrade path would be to add endpoints `/auth/send-otp` and `/auth/verify-otp`, where the former generates and sends an OTP using an SMS provider like Twilio and stores it in Redis or MongoDB with an expiration timestamp, and the latter checks the user’s input against the stored code before issuing a JWT.[46][24] Tests could mock the HTTP call to the SMS provider while exercising your own OTP validation logic, a pattern recommended in discussions about avoiding mocks for OTP internals.[24]

### Role-based authorization on backend and client

Role‑based access control is implemented at two levels. On the backend, the JWT’s `role` claim is interpreted by `get_current_user`, which returns a `UserInDB` with a `role` attribute. The `RoleChecker` dependency, parameterized with allowed roles, inspects `current_user.role` and raises HTTP 403 if the role is not permitted.[12][36][5] This is a clear example of “coarse‑grained” RBAC where each user has a single role such as `"customer"` or `"admin"`, and each endpoint declares which roles are allowed.

On the client, the `AuthContext` exposes the current `user` object including their role, allowing UI components to conditionally render admin‑only features or routes. For instance, the home screen calls `/users/admin-summary` only if `user.role === "admin"`, and non‑admin users never even see admin data in the UI. While UI‑level checks are not a security boundary—they can be bypassed by a determined attacker—they provide better UX and reduce the likelihood of ordinary users stumbling into unauthorized screens. The real enforcement occurs on the backend via RBAC dependencies.[36][5]

This combination of token‑embedded roles, dependency‑based checks, and selective UI features is consistent with FastAPI RBAC tutorials and JWT‑based RBAC explanation videos, which show how roles can be added to the JWT payload and used in dependencies to constrain access to certain endpoints.[5][12][36]

### Token storage, CORS, and transport security

On mobile platforms, storing access tokens in `expo-secure-store` is significantly more secure than using `AsyncStorage` because SecureStore encrypts values using the device’s keystore and segregates data per app, whereas AsyncStorage is unencrypted and accessible with device debugging tools.[2][2][2][2][34][11] However, no local storage mechanism can fully protect against a compromised device or malicious OS‑level attackers; these threats are mitigated by short token lifetimes and the ability to revoke tokens server‑side if a user reports theft.[15][29][41]

On web, token storage is more delicate. Storing JWTs in `localStorage` or `sessionStorage` exposes them to XSS attacks; storing them in HttpOnly cookies protects against XSS but introduces CSRF risks and complicated CORS configurations.[20][49][26] Some security experts argue that the most secure pattern for SPAs is to hold tokens only in memory and rely on refresh tokens stored in HttpOnly cookies or on short sessions, trading off persistence for security.[20][41] This playbook takes a middle path for development: on web it stores tokens only in memory; refresh or reload loses the session, but there is no persistent token sitting in browser storage, and no HttpOnly cookies are used. For production, especially for pure web clients, stronger patterns involving HttpOnly cookies and CSRF protection should be considered.[20][49][26]

CORS must be configured correctly on the backend to allow the Expo web origin to make requests with Authorization headers and credentials. FastAPI’s CORS tutorial explains that setting `allow_origins=["*"]` blocks credentials such as cookies and Authorization headers, so you must explicitly list allowed origins and set `allow_credentials=True`.[26][26] The `main.py` configuration above does exactly this, listing `http://localhost:8081` and related URLs as allowed origins. When deploying to production, you will adjust this list to include the actual web origin (for example, `https://app.example.com`) and remove the local dev origins.

All communication between client and server should be performed over HTTPS in production. Bearer authentication schemes such as JWT tokens sent in the Authorization header must be used only over TLS to prevent token leakage via network sniffing, as emphasized in both Swagger’s bearer authentication documentation and general JWT security guidelines.[49][15][25]

## Testing Strategy for Backend and Client

### Backend automated tests with pytest, TestClient, and AsyncClient

FastAPI integrates well with pytest, and its testing tutorial shows how to mount the app in a `TestClient` and write tests using regular synchronous functions that call HTTP endpoints directly.[17][17] For asynchronous I/O beyond simple endpoints, particularly when using Motor, you may prefer to use `httpx.AsyncClient` with `pytest.mark.anyio` to run tests as async functions so that you can await async functions such as MongoDB operations.[23][19]

A basic test file `backend/tests/test_auth.py` might look like this:

```python
# backend/tests/test_auth.py
import pytest
from httpx import AsyncClient, ASGITransport

from backend.main import app
from backend.db import connect_to_mongo, close_mongo_connection
from backend.config import settings

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
  await connect_to_mongo(app)
  db = app.mongodb_db
  await db["users"].delete_many({})
  yield
  await db["users"].delete_many({})
  await close_mongo_connection(app)

@pytest.mark.anyio
async def test_register_and_login_email():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        register_resp = await ac.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "password123", "phone": None, "role": "customer"},
        )
        assert register_resp.status_code == 200
        token = register_resp.json()["access_token"]

        me_resp = await ac.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me_resp.status_code == 200
        data = me_resp.json()
        assert data["email"] == "test@example.com"
        assert data["role"] == "customer"

        login_resp = await ac.post(
            "/auth/login-email",
            json={"email": "test@example.com", "password": "password123"},
        )
        assert login_resp.status_code == 200

@pytest.mark.anyio
async def test_phone_otp_login_and_role():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        phone = "+15555550123"
        otp = "123456"
        resp = await ac.post(
            "/auth/login-phone-otp",
            json={"phone": phone, "otp": otp},
        )
        assert resp.status_code == 200
        token = resp.json()["access_token"]

        me_resp = await ac.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me_resp.status_code == 200
        data = me_resp.json()
        assert data["phone"] == phone
        assert data["role"] == "customer"
```

The FastAPI async testing guide demonstrates how to use `pytest.mark.anyio` and `AsyncClient` with `ASGITransport` to make requests against the app in an async context, allowing integration tests that include asynchronous database operations.[23] The tests above verify that registration returns a token, that `/users/me` returns the expected email and role, that subsequent login works, and that the mocked phone OTP flow correctly issues a token and creates a user with the correct phone. Additional tests can verify failure modes such as wrong password, invalid OTP format, expired token handling, and access to admin‑only endpoints with and without the appropriate role.

Note that this setup uses the same MongoDB instance for tests as for development; in a real project you would point `MONGODB_DB_NAME` to a dedicated test database, or use an in‑memory MongoDB instance in the CI environment. It is also important to initialize indexes in the test setup to ensure duplicate email behavior matches production.[28][14][40]

### Manual and exploratory testing of the Expo app

For the client, automated testing tends to focus on unit tests for hooks and context logic (with Jest and React Testing Library) and instrumentation or end‑to‑end tests with tools like Detox. However, for this integration playbook, detailed manual testing is essential to verify that navigation, token storage, and backend flows behave as intended.

A typical manual test sequence for development includes starting the backend with Uvicorn and starting the Expo dev server, then confirming the following behaviors:

In the initial state, visiting the root of the Expo app on web or launching it in Expo Go should show the login screen, with the splash screen visible until `isLoading` becomes false. Once loaded, if no token is stored, the user is redirected to `/ (auth)/login`. This matches the design in Expo’s authentication guide where the sign‑in screen is accessible when no session is present.[4][4][45]

On successful registration, after filling out email, password, and optional phone and pressing “Register”, the app should automatically navigate to the home screen, and a token should be stored in SecureStore on native. Closing and reopening the app should result in the home screen being shown immediately after the splash, as the app recovers the stored token and calls `/users/me` to rebuild the session. On web, refreshing the page may lose the session because tokens are stored only in memory; this behavior should be documented for testers.

For email login, similar behavior should occur: after logging in, the home screen shows the user’s email and role; hitting the admin endpoint should fail for non‑admin users with a 403 error on the backend and a visible message on the client if error handling is wired to display something. For admin users, after manually promoting a user’s role in the database to `"admin"`, logging in should result in admin‑only summary information showing.

The phone OTP flow should allow login with any phone number and any six‑digit OTP. New phone numbers should result in creation of new users with pseudo emails; repeated logins with the same phone should reuse the same user. Trying OTPs that are not six digits or contain non‑numeric characters should result in a backend 400 error and a visible error message if error handling is implemented.

Using developer tools, you can inspect HTTP requests to confirm that the `Authorization: Bearer <token>` header is present for protected calls and absent for public calls, and that tokens expire at the expected time, leading to 401 responses when reused after expiration.[25][29] Tampering with tokens in SecureStore (where possible) should result in 401 errors when making requests, demonstrating that the server correctly validates signatures and expiration.

### OTP testing strategy and future enhancements

Although the current OTP flow is mocked, it is useful to consider how you would test a real OTP implementation once added. Articles about testing 2FA suggest distinguishing between unit tests that mock the HTTP boundary to the SMS provider and end‑to‑end tests that occasionally send actual SMS messages to a test phone number.[24] The key insight is that you should not bypass or mock your own OTP logic—including parsing, rate limiting, and expiration—with direct calls to token generation or verification; instead, you mock the inner HTTP call to Twilio or another provider while letting your own code run as in production.[24][46]

For this playbook, you can simulate more realistic OTP behavior even before integrating a provider by introducing serverside state (for example, an in‑memory store keyed by phone number) and requiring that the OTP in `/auth/login-phone-otp` matches a previously generated code. You would then write tests that exercise the full lifecycle: request OTP, receive code in response (in a test environment), and use the code to authenticate, verifying that wrong codes, expired codes, or repeated uses fail appropriately.

## Common Pitfalls and How to Avoid Them

### Misconfigured CORS and HTTP headers

A frequent source of frustration in frontend–backend integrations is CORS misconfiguration. If the backend uses `allow_origins=["*"]` while also setting `allow_credentials=True`, browsers will block requests that include credentials such as Authorization headers, leading to mysterious failures.[26][26] The FastAPI CORS documentation explains that wildcard origins are incompatible with credentialed requests, so you must specify each allowed origin explicitly, as the backend configuration here does.[26][26] Always ensure that the origin printed in the browser’s developer tools (e.g., `http://localhost:8081`) matches an entry in the `origins` list.

Additionally, remember that Axios sends JSON bodies by default with the `Content-Type: application/json` header set automatically, but if you manually use Fetch and forget to set this header, FastAPI may not parse the body as JSON, resulting in 422 validation errors.[27][13] Using Axios or carefully setting headers with Fetch prevents these issues.

### Motor and event loop issues in tests and startup

When using Motor, it is essential to create the `AsyncIOMotorClient` in a context that has an event loop, such as a FastAPI startup event; creating it at import time in the module can lead to `RuntimeError: Task attached to a different loop` errors when running tests or when the app is reloaded.[19][23] The async testing guide notes that asynchronous objects tied to the event loop should be instantiated inside async functions, not at top‑level, when mixing test loops and application loops.[23] The `connect_to_mongo` and `close_mongo_connection` functions and their registration with `@app.on_event("startup")` and `@app.on_event("shutdown")` follow this recommendation and avoid such issues.

In tests, using `ASGITransport` and `AsyncClient` ensures that requests run in the same event loop that FastAPI uses internally, avoiding mismatch problems. Always clean up database state between tests by deleting collections or using separate databases, particularly when unique indexes are involved.[28][14][40]

### Password hashing pitfalls

Accidentally storing plaintext passwords or reusing the same salt across users is a serious vulnerability. Using Passlib’s `CryptContext` as demonstrated avoids these pitfalls because it automatically chooses per‑password random salts and appropriate work factors.[33][50][9] Another subtle mistake is comparing passwords directly with `==` in Python rather than using a constant‑time comparison; Passlib’s `verify` method prevents timing differences and should always be used to compare passwords.[33][50]

If you ever change the hashing scheme or cost parameters—for example, upgrading from bcrypt with a low cost to a higher cost—the `CryptContext` can be configured to deprecate old hashes and re‑hash passwords at login time, but that is beyond the scope of this playbook. The key takeaway is to centralize password hashing logic and avoid re‑implementing cryptographic primitives yourself.[33][50][9]

### JWT lifetime and misuse

Setting JWT expiration times too long, such as days or months, increases risk if tokens are stolen; best practices recommend lifetimes measured in minutes or at most a few hours, with refresh tokens used for long‑lived sessions.[15][29][41] The `ACCESS_TOKEN_EXPIRE_MINUTES` setting set to 15 or 30 minutes is a reasonable default for access tokens; you can then implement refresh tokens with longer lifetimes stored via more secure mechanisms (for web, HttpOnly cookies; for mobile, SecureStore or other secure enclaves).[15][29][41][20]

Another pitfall is failing to check the `type` claim in the JWT payload and accidentally accepting a refresh token where an access token is expected. This is mitigated by the `TokenPayload` model and the check `if payload.type != "access":` in `get_current_user`. Similarly, embedding too much information in the JWT, such as permissions or personal data, increases token size and leak risk; this playbook embeds only essential claims: subject ID, role, expiration, and token type.[25][15]

### Insecure token storage on the client

Storing access tokens in AsyncStorage, localStorage, or any other unencrypted storage increases the risk of theft if an attacker gains code execution in the app’s JS context or physical access to a jailbroken device.[11][20][34] The Expo SecureStore documentation and various tutorials stress that secure storage should be used for credentials, secrets, and JWTs on React Native, preferably via platform keychain/keystore wrappers.[2][2][2][2][34] This playbook uses SecureStore on native and in-memory storage on web to reduce stored attack surface. Nonetheless, on web, fully secure patterns often involve HttpOnly cookies and CSRF tokens; however, implementing those requires a different architecture and is beyond the immediate scope.[20][26][49]

Expo’s environment variable guide emphasizes that variables prefixed with `EXPO_PUBLIC_` are inlined into the bundle and should never be used for sensitive secrets. Using them only for API base URLs and other non‑secrets prevents accidentally shipping secret keys in the client code.[42]

### Unique indexes and validation

A common confusion when using MongoDB with ODMs such as Mongoose is the role of the `unique` schema option, which is not a validator but a helper to create a unique index.[14][28] In this playbook, the unique index on `email` is created explicitly at startup with `create_index` and `unique=True`, ensuring that duplicate email insertions fail at the database level.[28][14][40] This is generally more reliable than checking for existing emails in application code because it prevents race conditions where two registrations with the same email arrive concurrently.

Validation of fields such as email and password length is handled by Pydantic models on the FastAPI side. The Pydantic tutorial illustrates how schemas define the API contract and enforce validation before the endpoint handler runs, returning 422 errors for invalid data.[13][22] For example, if the password is too short or the email is malformed, the registration endpoint will never execute its body.

## Conclusion and Next Steps

This integration playbook has walked through the design and implementation of a complete JWT‑based authentication stack bridging an Expo React Native application, including React Native Web via Expo Router, and a FastAPI backend backed by MongoDB and Motor. On the backend, you created a robust foundation using FastAPI’s async capabilities, Motor’s non‑blocking MongoDB driver, Passlib’s bcrypt hashing for secure password storage, and PyJWT‑based JWT encoding and decoding. Email/password registration and login, mocked phone OTP login, and role‑based authorization were implemented using clear Pydantic schemas, security dependencies, and RBAC helpers, with secure handling of JWT expiration and claims.

On the frontend, you set up an Expo project with Expo Router, defined an `AuthContext` and `AuthProvider` that manage access tokens and user profiles, stored tokens securely on native devices using `expo-secure-store`, and integrated authentication state with routing via a splash screen controller and guarded navigation. The app provides registration, email login, and phone OTP login screens, and demonstrates both role‑based UI behavior and backend‑enforced RBAC for admin‑only endpoints. Axios interceptors ensure that the JWT is transparently attached to every authenticated request, abstracting away repetitive header handling.

The playbook further detailed testing strategies, including asynchronous integration tests for the backend using `httpx.AsyncClient` and `pytest.mark.anyio`, and manual exploratory testing of the Expo app flows. It examined common pitfalls—misconfigured CORS, event‑loop issues with Motor, password hashing mistakes, overly long JWT lifetimes, and insecure token storage—and described how the recommended patterns avoid these issues, citing best practices from FastAPI, JWT security literature, and Expo documentation.[26][26][33][50][15][29][2][2][2][2][42]

Several natural extensions suggest themselves for future work. First, adding refresh tokens with rotation and revocation support would improve user experience while maintaining security, especially for long‑lived sessions.[41][29][15] Second, replacing the mocked OTP flow with a real integration to an SMS provider such as Twilio, complete with OTP generation, storage, expiration, and rate limiting, would make the phone login path production‑ready.[46][24][37] Third, migrating from Motor to PyMongo’s async API, as recommended by MongoDB due to Motor’s deprecation, would future‑proof the database layer.[8][19] On the client, strengthening web token handling by adopting HttpOnly cookies and CSRF tokens when building a web‑only frontend could mitigate XSS and CSRF risks, albeit with increased architectural complexity.[20][26][49]

Despite these potential enhancements, the architecture and implementation described here already provide a strong, secure starting point for JWT‑based authentication in an Expo React Native app with a FastAPI + MongoDB backend. By following the detailed installation steps, code examples, testing procedures, and security guidance, a development team can implement a working authentication system that supports email/password login, mocked phone OTP login, role‑based access, and secure token handling across mobile and web clients, and adapt it to production‑grade requirements as the project evolves.

---
Sources:
1. https://testdriven.io/blog/fastapi-jwt-auth/
2. https://docs.expo.dev/versions/latest/sdk/securestore/
3. https://www.youtube.com/watch?v=4fKavID0hoI
4. https://docs.expo.dev/router/advanced/authentication/
5. https://www.permit.io/blog/fastapi-rbac-full-implementation-tutorial
6. https://www.youtube.com/watch?v=vHXZ4jJFgT0
7. https://support.iterable.com/hc/en-us/articles/43901001355412-JWT-Authentication-with-Iterable-s-React-Native-SDK
8. https://www.mongodb.com/docs/drivers/motor/
9. https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
10. https://www.youtube.com/watch?v=JitVZm8rfks
11. https://blog.logrocket.com/react-native-jwt-authentication-using-axios-interceptors/
12. https://www.youtube.com/watch?v=_k2M-LpxId8
13. https://www.youtube.com/watch?v=9GHxnttXxrA
14. https://mongoosejs.com/docs/validation.html
15. https://curity.io/resources/learn/jwt-best-practices/
16. https://www.youtube.com/watch?v=MvxVz3FfgUs
17. https://fastapi.tiangolo.com/tutorial/testing/
18. https://fastapi.tiangolo.com/tutorial/security/first-steps/
19. https://motor.readthedocs.io/en/stable/tutorial-asyncio.html
20. https://dev.to/petrussola/today-s-rabbit-hole-jwts-in-httponly-cookies-csrf-tokens-secrets-more-1jbp
21. https://www.youtube.com/watch?v=Ky43ve3b9Ss
22. https://fastapi.tiangolo.com/tutorial/schema-extra-example/
23. https://fastapi.tiangolo.com/advanced/async-tests/
24. https://dev.to/sms-activate/why-i-stopped-mocking-2fa-in-tests-and-what-i-do-instead-1epk
25. https://jwt.io/introduction
26. https://fastapi.tiangolo.com/tutorial/cors/
27. https://reqbin.com/code/javascript/ricgaie0/javascript-fetch-bearer-token
28. https://www.mongodb.com/docs/manual/core/index-unique/
29. https://mojoauth.com/blog/understanding-jwt-expiration-time-claim-exp
30. https://blog.logrocket.com/axios-vs-fetch-2025/
31. https://www.contentful.com/blog/fastapi-vs-flask/
32. https://www.youtube.com/watch?v=Go4wYJJhR3k
33. https://passlib.readthedocs.io/en/stable/narr/hash-tutorial.html
34. https://www.youtube.com/watch?v=s_tBTjQzlSg
35. https://docs.expo.dev/versions/latest/sdk/splash-screen/
36. https://www.youtube.com/watch?v=RRG5l8wJoTI
37. https://forums.grc.com/threads/is-6-digits-really-enough-for-an-otp-code.1183/
38. https://fastapi.tiangolo.com/tutorial/handling-errors/
39. https://docs.expo.dev/router/error-handling/
40. https://motor.readthedocs.io/en/stable/api-tornado/motor_collection.html
41. https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/
42. https://docs.expo.dev/guides/environment-variables/
43. https://github.com/pydantic/pydantic/issues/11062
44. https://www.youtube.com/watch?v=0A_GCXBCNUQ
45. https://docs.expo.dev/develop/authentication/
46. https://www.youtube.com/watch?v=Z1mtppCvL74
47. https://fastapi.tiangolo.com/tutorial/bigger-applications/
48. https://docs.expo.dev/router/advanced/stack/
49. https://swagger.io/docs/specification/v3_0/authentication/bearer-authentication/
50. https://passlib.readthedocs.io/en/stable/lib/passlib.context.html

`````

---
## Sample 5: PayPal checkout — web (FastAPI + React) store

| | |
|---|---|
| HTTP status | 200 |
| **Latency** | **229.6 s** |
| **Total cost (from Perplexity's `usage.cost`)** | **$1.04711** |
| Cost breakdown | input $0.00039 · output $0.10578 · citation $0.05405 · reasoning $0.58689 · search $0.3 |
| Tokens | prompt 195 · completion 13,222 · citation 27,027 · reasoning 195,629 |
| Search queries run by Perplexity internally | 60 |
| Playbook length | 63,374 chars |
| Citations | 50 |

### Input — what our agent asked the tool (verbatim)

```
INTEGRATION: PayPal payment processing for e-commerce checkout
CONSTRAINTS: Need to integrate PayPal checkout button and payment processing for a dropshipping store
```

### Exact API request sent to Perplexity

```json
{
  "url": "https://api.perplexity.ai/chat/completions",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer pplx-REDACTED-MOCK-KEY",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "sonar-deep-research",
    "messages": [
      {
        "role": "system",
        "content": "You are Integration_Playbook_Expert, responsible for creating detailed integration guides.\nResearch and provide a complete integration playbook for the requested technology that includes:\n\n1. Installation instructions\n2. API key setup & security best practices\n3. Complete code examples for this tech stack: reactjs frontend with shadcn, fastapi backend, mongodb database\n4. Testing procedures\n5. Common pitfalls and how to avoid them\n\nFormat your response in a structured, step-by-step guide that a developer can follow.\nInclude all necessary code samples.\nIf the integration involves API keys, include instructions on where to get them."
      },
      {
        "role": "user",
        "content": "Create a detailed integration playbook for INTEGRATION: PayPal payment processing for e-commerce checkout\nCONSTRAINTS: Need to integrate PayPal checkout button and payment processing for a dropshipping store in reactjs frontend with shadcn, fastapi backend, mongodb database application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."
      }
    ]
  }
}
```

### Exact output returned to our agent (verbatim, 66,508 chars)

This is the complete tool result the coding agent receives — the playbook exactly as Perplexity wrote it, with the citation URLs appended as a `Sources:` list by our tool layer. (It is then wrapped as `{"content": "<below>", "cost": 1.5}` — the `1.5` is an internal billing unit, unrelated to the Perplexity dollar cost.)

`````markdown
# Integration Playbook: PayPal Checkout for a React (shadcn) + FastAPI + MongoDB Dropshipping Store

This report presents a complete, end‑to‑end integration playbook for adding **PayPal Checkout** payment processing to a dropshipping e‑commerce application built with a React frontend (using shadcn/ui), a FastAPI backend, and a MongoDB database. The integration is built around the PayPal JavaScript SDK and the `@paypal/react-paypal-js` wrapper on the frontend, combined with direct use of PayPal’s REST Orders API from the FastAPI backend, with MongoDB used to persist orders and payment state.[1][3][7][31][7][31][45] The playbook covers environment and installation steps, PayPal app and credential configuration, secure handling of API keys, detailed backend and frontend code samples, recommended testing procedures using the PayPal sandbox, and a discussion of common pitfalls such as CORS misconfiguration, mixing sandbox and live credentials, unverified webhooks, and inconsistent order state between PayPal and MongoDB.[3][11][13][15][18][19][25][37] Although this is an implementation‑oriented guide, it also motivates design choices such as server‑side order creation, the use of MongoDB’s document model for order and fulfillment data, and asynchronous patterns in FastAPI for calling PayPal and persisting data. The result is a secure, testable, and extensible foundation for a production‑ready dropshipping checkout backed by PayPal.

## Architectural Overview and Data Flow

### End‑to‑End Flow for PayPal Checkout

The core integration pattern for PayPal Checkout in this architecture is a three‑tier flow: the React frontend renders PayPal buttons using the PayPal JavaScript SDK, the FastAPI backend creates and captures PayPal Orders via the PayPal REST API, and MongoDB persists all order and payment records.

PayPal Checkout is mediated through the **Orders v2 API**, which defines an order as a payment instruction and allows creation, approval, authorization, and capture of payment.[7][7][7] In a typical Capture‑intent flow, when a buyer clicks the PayPal button on your React checkout page, PayPal’s JavaScript SDK calls a `createOrder` function in your frontend integration. Instead of directly constructing an order in the browser, you delegate order creation to your FastAPI backend, which defines amounts, currency, and item details server‑side, calls the PayPal Orders API with those values, and returns a PayPal `orderID` to the frontend.[5][7][7][45] The PayPal popup or overlay then handles buyer authentication and approval. After the buyer approves, PayPal’s SDK calls your `onApprove` handler in the browser, which in turn calls a FastAPI endpoint that invokes the Orders API’s capture operation to move money and finalize the payment.[7][7][7][45]

At each stage, MongoDB records help you maintain a durable and auditable view of the order life cycle. When your backend creates the PayPal order, it saves a document containing the application’s internal order identifier, the PayPal `orderID`, cart contents, buyer details, and the current payment status (for example, `"CREATED"`). When the capture succeeds, the backend updates the document’s status (for example, `"COMPLETED"`), and optionally stores PayPal’s capture identifiers and response payload. This pattern is particularly important for dropshipping, where you often need to route orders to external suppliers and reconcile payouts; MongoDB’s flexible schema allows you to evolve the document model to include fulfillment tracking, supplier references, and shipment events.[10][20][26][10]

The frontend’s React code is thus responsible primarily for user experience: rendering the checkout form with shadcn/ui fields for shipping and contact details, computing the current cart, and invoking backend endpoints at `createOrder` and `onApprove` stages. React’s state and effect hooks let you represent pending, success, and error states declaratively, rather than mutating the DOM directly.[12][41] The PayPal JavaScript SDK is loaded via the `PayPalScriptProvider` component from `@paypal/react-paypal-js`, which takes query‑string options such as the `client-id`, `currency`, and `intent` that control how buttons render and how payments are processed.[1][31][31][45][45]

On the backend, FastAPI provides an asynchronous framework that can expose HTTP endpoints, validate requests using Pydantic models, and integrate with async MongoDB drivers like Motor.[40][47] A typical configuration will include a CORS middleware that allows your React origin to call backend APIs while blocking unauthorized origins.[13] The backend also manages secure storage and usage of PayPal credentials: the **client ID** and **client secret** are stored as environment variables, used to obtain OAuth 2.0 access tokens from PayPal’s `/v1/oauth2/token` endpoint, and never exposed to the browser.[3][18][25]

Finally, webhooks provide a crucial asynchronous channel from PayPal to your backend. The PayPal REST APIs can send webhook notifications for events such as `PAYMENT.CAPTURE.COMPLETED`, `CHECKOUT.ORDER.APPROVED`, or subscription events, and your FastAPI application can handle these HTTP callbacks, verify their signatures, and use them to reconcile any discrepancies between your perception of an order and PayPal’s.[11][19] For example, if your capture call times out but PayPal eventually completes the payment, a webhook can confirm the capture completion and allow your system to mark the order as paid.

### Dropshipping‑Specific Considerations

In a dropshipping store, checkout and payment are only the first part of a longer business process that includes order routing to suppliers, inventory synchronization, and shipment tracking.[20][24][50] The PayPal integration described here focuses on the payment aspect, but the way you design your MongoDB schema and your backend API should anticipate these downstream steps.

In particular, each order document in MongoDB should clearly distinguish between **payment state**, **fulfillment state**, and **supplier state**. The payment state is driven by PayPal events and API calls (for example, `"CREATED"`, `"APPROVED"`, `"COMPLETED"`, `"VOIDED"`). The fulfillment state reflects the physical fulfillment process (for example, `"PENDING_SUPPLIER"`, `"DISPATCHED"`, `"DELIVERED"`). The supplier state tracks whether the dropshipping supplier has acknowledged or shipped the order. MongoDB’s flexible document structure is well suited to modeling such nested, evolving state with embedded subdocuments for supplier line items and shipping events.[10][20][26][10]

Because PayPal’s Orders API allows sending callback URLs and shipping data, you can decide how much of your internal order state to mirror in PayPal’s `purchase_units` and related fields. For the simplest integration, you can rely primarily on your MongoDB records and treat PayPal as an external system of record only for payment confirmation. For more sophisticated integrations, you can employ additional PayPal features such as Level 2/3 data, multiparty checkouts, or order update callbacks to optimize processing costs and reduce risk.[7][7][7]

## Environment Setup and Installation

### Tooling and Global Dependencies

Before implementing the integration, you need to prepare a development environment that includes Node.js with npm for the React frontend, Python for the FastAPI backend, and a reachable MongoDB deployment either locally or in the cloud. For Node.js and npm, the recommended approach is to use a Node version manager such as `nvm` or `nvm-windows`, which allows you to install and switch between Node versions without permission issues.[49] Once the manager is installed, you can install a current LTS version of Node and verify the presence of both Node and npm using commands such as `node -v` and `npm -v`.[49]

For MongoDB, you can either run a local Community or Enterprise server or use MongoDB Atlas. If you are using a local instance on the default port, you can connect using `mongosh` or driver URIs targeting `mongodb://localhost:27017`, while an Atlas cluster requires a DNS seedlist format URI such as `mongodb+srv://clustername.hash.mongodb.net/` combined with an API version and username.[46] When using asynchronous drivers like Motor in Python, you use the same URI in your `AsyncIOMotorClient` instantiation, and MongoDB’s stable API and TLS options can be configured in the connection string.[46]

Python dependencies for the backend can be installed in a virtual environment using tools such as `venv` or `poetry`. Your backend will require `fastapi`, `uvicorn[standard]` as an ASGI server, `motor` or the async PyMongo driver for MongoDB connectivity, an HTTP client such as `httpx` or `requests` to call PayPal, and `python-dotenv` or similar to load environment variables from `.env` files in development.[35][40][47] Once installed, you can define your FastAPI application in a `main.py` and run it with `uvicorn main:app --reload`, ensuring that it listens on a port such as 8000.

### React Frontend Setup with shadcn and PayPal React SDK

The frontend can be created with any React tooling, but many teams use Create React App or a Vite‑based setup. If you use Create React App, it embeds custom environment variables prefixed with `REACT_APP_` at build time, making it convenient to expose non‑secret configuration such as the PayPal client ID.[16][16] After bootstrapping the React project, you install UI and PayPal dependencies.

For shadcn/ui, you follow its CLI‑based installation instructions to generate and configure Tailwind CSS and to pull component implementations into your project.[21][30][36] The shadcnblocks project also offers higher‑level checkout blocks built with React, Tailwind, and shadcn/ui that you can import or copy/paste into your app, simplifying the creation of stylish checkout forms.[8] Each block is a self‑contained React component that you can use as a starting point for your own checkout page.[8]

To integrate PayPal buttons in React, the recommended approach is to use the `@paypal/react-paypal-js` package, which wraps the PayPal JavaScript SDK and provides a `PayPalScriptProvider` component for script loading and a `PayPalButtons` component for rendering the buttons.[1][31][31][45] You install this package using npm or Yarn, for example:

```bash
npm install @paypal/react-paypal-js
```

Once installed, you import `PayPalScriptProvider` at your React entry point, create an `initialOptions` object containing at minimum the `client-id`, the currency, and the intent, and wrap your application with the provider. The `client-id` is the PayPal REST app’s client ID; the currency is a three‑letter code like `"USD"`; and the intent is typically `"CAPTURE"` for immediate capture flows.[1][31][31][45]

A minimal root component might look like this:

```tsx
// src/App.tsx
import React from "react";
import { PayPalScriptProvider } from "@paypal/react-paypal-js";
import { CheckoutPage } from "./CheckoutPage";

const initialOptions = {
  "client-id": process.env.REACT_APP_PAYPAL_CLIENT_ID as string,
  currency: "USD",
  intent: "CAPTURE",
};

export function App() {
  return (
    <PayPalScriptProvider options={initialOptions}>
      <CheckoutPage />
    </PayPalScriptProvider>
  );
}
```

This pattern follows the approach described in the PayPal blog example, where the root React component is responsible for loading the PayPal script once and passing configuration options via the provider.[1] The `REACT_APP_PAYPAL_CLIENT_ID` environment variable is defined in a `.env` file and injected into the build as described in the Create React App documentation.[16][16]

For shadcn, you create a checkout page that imports shadcn/ui components such as `Input` for fields like email, address, and city, and `Button` for submission controls.[21][30][43] The integration with React Hook Form and Zod described in shadcn’s form documentation is useful for client‑side validation and form state management, and you can integrate this with PayPal buttons by submitting the form data to your backend before or during PayPal order creation.[21][36]

### FastAPI Backend Setup with MongoDB and CORS

On the backend, you define a FastAPI application that connects to MongoDB and exposes endpoints for creating PayPal orders, capturing them, and handling webhooks. FastAPI’s dependency injection framework allows you to define a database dependency using `yield`, which ensures cleanup code is run in the correct order once the request is processed.[35] For asynchronous access to MongoDB, you use Motor’s `AsyncIOMotorClient` to connect to a MongoDB URI, and expose the desired database and collection objects as dependencies or global attributes.

A minimal backend setup might look like this:

```python
# app/main.py
import os
from typing import AsyncGenerator

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "dropship_store")

app = FastAPI()

client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db() -> AsyncGenerator:
    try:
        yield db
    finally:
        # In most cases, the global client is reused and not closed per request.
        pass
```

The CORS configuration is patterned after the FastAPI documentation, which explains that the backend must include the frontend’s origin (for example, `http://localhost:3000`) in `allow_origins` for cross‑origin requests to work correctly.[13] Using `"*"` for `allow_methods` and `allow_headers` in development simplifies experimentation but you may choose narrower values in production.[13]

MongoDB itself can be deployed locally or on Atlas, and Motor’s `AsyncIOMotorClient` accepts both forms of URI. When using MongoDB Atlas, you should use the recommended DNS seedlist format and configure TLS as needed.[46] MongoDB’s transaction support and ACID guarantees may become important if you later decide to coordinate complex multi‑document updates around payment events, but for many simple order flows, single‑document atomicity and careful update logic are sufficient.[26][38][42]

### MongoDB Deployment and Connection Verification

To ensure your backend can reliably write orders and payment records, you should verify the MongoDB connection independently before integrating PayPal. A simple test script that connects using the same URI as your FastAPI app and performs a ping or inserts a test document will confirm connectivity.[46][42] For example:

```python
# scripts/test_mongo.py
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

async def main():
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))
    try:
        await client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print("Error connecting to MongoDB:", e)

if __name__ == "__main__":
    asyncio.run(main())
```

This snippet follows the Motor documentation’s pattern for testing connections, including the use of MongoDB’s Stable API version. Once the connection is verified, you can safely build higher‑level logic such as order insertion, updates, and queries.

## PayPal Configuration and Credential Management

### Creating Sandbox Accounts and REST App

A secure PayPal integration begins with proper setup of sandbox accounts and REST credentials in the PayPal Developer Dashboard. PayPal’s sandbox is a test environment that mirrors real‑world transactions but uses virtual funds, which allows you to simulate both buyer and merchant behavior.[3][15][37]

When you create a PayPal Developer account, PayPal automatically provisions two default sandbox accounts: a **business** account representing the seller and a **personal** account representing the buyer.[3][37] You can view and manage these accounts under the Sandbox → Accounts section of the Developer Dashboard. Here, you can create additional business or personal accounts, customize balances, or duplicate existing accounts for diverse test scenarios.[37] For example, you might maintain separate personal sandbox accounts corresponding to different countries or card configurations.

To obtain the credentials that your application will use, you navigate to the Apps & Credentials section of the dashboard. New accounts include a default REST application, but you can also create a new app, specifying an app name and type (usually a merchant app). Once created, the app displays a **client ID** and, when expanded, a **client secret** for both sandbox and live environments.[1][3][4][25] The client ID uniquely identifies your app and can safely be used in the browser to load the JavaScript SDK and render PayPal buttons.[1][3][25] The client secret, by contrast, must be kept confidential and is used only on your server to obtain OAuth 2.0 access tokens and to authenticate server‑side API calls.[3][18][25]

For a standard JavaScript SDK integration, you may only need the client ID for the frontend to render PayPal buttons and standard credit and debit card fields. However, when your backend calls PayPal REST APIs directly, such as the Orders API for order creation and capture, it must exchange the client ID and client secret for an access token via `/v1/oauth2/token`, and you should treat both credentials as secrets.[3][5]

### OAuth 2.0 Access Tokens and API Base URLs

PayPal’s REST APIs are protected by OAuth 2.0 access tokens, which are short‑lived bearer tokens that the backend uses in the `Authorization: Bearer` header for subsequent API calls.[3] To obtain an access token, your FastAPI backend sends a POST request to `https://api-m.sandbox.paypal.com/v1/oauth2/token` in the sandbox environment, authenticating with HTTP Basic Auth using the client ID and client secret, and passing `grant_type=client_credentials` in the request body.[3] The same pattern applies in production, with the base URL switching to `https://api-m.paypal.com` and the credentials corresponding to the live app.

The documentation suggests using cURL or Postman for testing, but any HTTP client library is acceptable.[3] With Python’s `httpx`, the access token request might look like this:

```python
import os
import httpx

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PAYPAL_BASE_URL = os.getenv(
    "PAYPAL_BASE_URL",
    "https://api-m.sandbox.paypal.com",
)

async def get_paypal_access_token() -> str:
    auth = (PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=auth,
            data=data,
        )
        response.raise_for_status()
        payload = response.json()
        return payload["access_token"]
```

This function is called by your FastAPI endpoints before they invoke the Orders API. The PayPal response includes both the `access_token` and an `expires_in` duration, and in a production system you would typically cache the token until it is near expiry rather than requesting a new token on every call.[3]

### Security Best Practices for Credential Handling

Because the client secret is a powerful credential that allows your backend to act on behalf of your merchant account, PayPal’s security guidelines emphasize careful storage and handling of such secrets.[18] In practice, this means storing your `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET` as environment variables or in a secure secrets manager, not in source code. In development, `.env` files can hold these values, and tools such as `python-dotenv` can load them into the process environment. The file containing real production secrets should not be committed to version control.

On the frontend, Create React App’s documentation explains that environment variables are embedded at build time, and that custom variables must be prefixed with `REACT_APP_` to be available to JavaScript code.[16][16] To avoid accidentally exposing secrets, CRA ignores any variables not starting with this prefix (other than `NODE_ENV` and `PUBLIC_URL`).[16][16] Accordingly, you should only expose the non‑secret PayPal client ID with a name such as `REACT_APP_PAYPAL_CLIENT_ID`, and never any server secrets.[1][3][16][16]

Beyond credential storage, PayPal’s security guidance recommends using HTTPS for all API calls and webhook endpoints, validating and sanitizing all input data, implementing proper error handling without leaking sensitive information, and regularly reviewing logs for suspicious activity.[18] When using webhooks, you should verify the authenticity of each message by either computing a checksum over the payload and comparing it to the signature, or by posting the payload and headers back to PayPal’s `verify-signature` endpoint. Without this verification, your backend would have no way to distinguish genuine notifications from spoofed requests.

Finally, you should maintain strict separation between sandbox and live credentials and endpoints, ensuring that a deployment never mixes sandbox client IDs with live API base URLs or vice versa. PayPal’s documentation distinguishes `api-m.sandbox.paypal.com` from `api-m.paypal.com`, and your configuration should make this distinction explicit through environment variables or configuration profiles.[3][25]

## Backend Implementation: FastAPI + MongoDB + PayPal Orders API

### Order Data Modeling in MongoDB

A robust PayPal integration for a dropshipping store requires a carefully designed order schema in MongoDB. MongoDB’s document model encourages you to structure data around your most common queries and update patterns rather than strictly normalizing as in relational databases.[10][10] For checkout, the key elements include the cart items, buyer information, shipping address, PayPal `orderID`, payment status, and internal timestamps for auditing.

A typical order document might contain an `_id` field with a MongoDB `ObjectId`, a `paypal_order_id` string, a `status` indicating PayPal payment status, a `total` with `amount` and `currency`, an embedded `items` array with SKU, name, price, and quantity, and a `shipping` subdocument with address fields. MongoDB encourages embedding related data that is frequently accessed together, such as items and shipping, inside a single order document, which reduces the need for joins and can simplify transactional semantics.[10][26][38][42][10]

From the Python side, you define a corresponding Pydantic model for request validation and response serialization. For example:

```python
# app/models.py
from typing import List, Optional
from pydantic import BaseModel, Field

class CartItem(BaseModel):
    sku: str
    name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

class ShippingAddress(BaseModel):
    full_name: str
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country_code: str

class OrderCreateRequest(BaseModel):
    items: List[CartItem]
    shipping: ShippingAddress
    currency: str = "USD"

class OrderInDB(BaseModel):
    id: str = Field(alias="_id")
    paypal_order_id: str
    status: str
    total_amount: float
    currency: str
```

The `OrderCreateRequest` model describes the request body that the frontend sends to the backend when initiating a checkout, while `OrderInDB` represents what is stored or returned from MongoDB. FastAPI’s request body documentation underscores that such models are ideal for describing request bodies and automatically generating OpenAPI documentation.[40] MongoDB’s CRUD documentation for inserts and updates informs how you will persist and mutate these documents when PayPal events occur.[38][42]

Because MongoDB uses `ObjectId` as its default identifier type, when you query or update documents by `_id` from Python you should convert string IDs into `ObjectId` instances using the PyMongo BSON utilities.[33][38] This becomes particularly important when you later implement endpoints to fetch or update orders by ID.

### FastAPI Application Structure and Database Dependencies

To keep your application modular, you can adopt FastAPI’s recommended structure for bigger applications, separating routers into modules such as `app/routers/paypal.py` for payment endpoints and `app/routers/orders.py` for order queries.[47] The main application in `app/main.py` includes these routers and configures global dependencies like CORS and authentication. This structure allows you to share routers and dependencies across projects while keeping the core app small.[47]

An example `main.py` file integrating the PayPal router might look like this:

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import db
from .routers import paypal

app = FastAPI(title="Dropship Store API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(paypal.router, prefix="/api/paypal", tags=["paypal"])

@app.get("/")
async def root():
    return {"message": "Hello from Dropship Store API"}
```

The router module then defines the endpoints for creating and capturing orders, using the database and PayPal client helper functions as dependencies or imports. FastAPI’s router mechanism allows you to attach tags, prefixes, and additional dependencies to groups of endpoints without modifying their internal implementation.[47]

Your database module might hold the Motor client and database object, along with convenience properties for specific collections:

```python
# app/database.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "dropship_store")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]

orders_collection = db["orders"]
```

### Implementing the PayPal Client: Create and Capture Order

The key backend logic for interacting with PayPal resides in a PayPal client module that wraps API calls to create and capture orders. PayPal’s Orders API documentation describes how to send a POST to `/v2/checkout/orders` with an `intent` of `"CAPTURE"` or `"AUTHORIZE"`, a `purchase_units` array with `amount` and optional item details, and optionally a `application_context` object specifying return URLs and UX preferences.[7][7][7]

For a typical capture flow, your backend can send a payload like:

```python
# app/paypal_client.py
import os
import httpx
from typing import Dict, Any, List

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PAYPAL_BASE_URL = os.getenv(
    "PAYPAL_BASE_URL", "https://api-m.sandbox.paypal.com"
)

async def get_access_token() -> str:
    auth = (PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=auth,
            data=data,
        )
        resp.raise_for_status()
        return resp.json()["access_token"]

def build_purchase_units(
    items: List[Dict[str, Any]], currency: str
) -> List[Dict[str, Any]]:
    total = sum(
        float(item["unit_price"]) * int(item["quantity"]) for item in items
    )
    return [
        {
            "amount": {
                "currency_code": currency,
                "value": f"{total:.2f}",
            },
        }
    ]

async def create_order(
    items: List[Dict[str, Any]], currency: str
) -> Dict[str, Any]:
    access_token = await get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    purchase_units = build_purchase_units(items, currency)
    payload = {
        "intent": "CAPTURE",
        "purchase_units": purchase_units,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders",
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()

async def capture_order(order_id: str) -> Dict[str, Any]:
    access_token = await get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture",
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()
```

This implementation matches the high‑level flow described in PayPal’s Orders API documentation, where a create order call initializes the payment and a capture call moves funds after buyer approval.[7][7][7] The currency code and amount must be aligned with the assets in your store, and in production you may want to include detailed `item` and `shipping` data in `purchase_units` to improve risk handling and reduce processing costs.[7][7]

Note that both methods obtain an access token by calling `get_access_token()`, which in this simple version retrieves a fresh token each time. In a production environment, you should implement caching to avoid rate limiting or unnecessary overhead. The error handling uses `resp.raise_for_status()` so that HTTP errors propagate as exceptions that your FastAPI endpoints can convert into appropriate responses.[29]

### FastAPI Endpoints for Creating and Capturing PayPal Orders

With the PayPal client in place, you define FastAPI endpoints that orchestrate order creation and persistence. When the React `createOrder` handler calls the backend, it sends the cart items and optional shipping information as JSON; the backend validates this against `OrderCreateRequest`, calls `paypal_client.create_order()`, stores the order in MongoDB, and returns the PayPal `orderID` to the frontend.

An example router implementation might be:

```python
# app/routers/paypal.py
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from ..database import orders_collection
from ..models import OrderCreateRequest
from ..paypal_client import create_order, capture_order

router = APIRouter()

@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_paypal_order(order_req: OrderCreateRequest):
    items = [
        {
            "sku": item.sku,
            "name": item.name,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
        }
        for item in order_req.items
    ]
    paypal_resp = await create_order(items, order_req.currency)
    paypal_order_id = paypal_resp["id"]
    total = sum(
        item["unit_price"] * item["quantity"] for item in items
    )
    doc = {
        "paypal_order_id": paypal_order_id,
        "status": paypal_resp["status"],
        "items": items,
        "shipping": order_req.shipping.dict(),
        "total_amount": total,
        "currency": order_req.currency,
    }
    result = await orders_collection.insert_one(doc)
    return {
        "order_id": str(result.inserted_id),
        "paypal_order_id": paypal_order_id,
    }

@router.post("/orders/{paypal_order_id}/capture")
async def capture_paypal_order(paypal_order_id: str):
    paypal_resp = await capture_order(paypal_order_id)
    capture_status = paypal_resp["status"]
    result = await orders_collection.update_one(
        {"paypal_order_id": paypal_order_id},
        {"$set": {"status": capture_status, "paypal_capture": paypal_resp}},
    )
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return {"status": capture_status, "paypal_response": paypal_resp}
```

The use of `status_code` on the route decorator follows FastAPI’s recommendation for explicit HTTP status codes, and the HTTP 201 created status is conventional for creation endpoints.[39] The MongoDB update uses `update_one`, which updates the first document that matches the filter based on `paypal_order_id` and returns counts for matched and modified documents.[38] If no document matches, the endpoint responds with HTTP 404.

Because the amount and currency are computed entirely on the server from the items, the backend remains the source of truth for payment amounts, and the client cannot influence the charge by manipulating form fields. This pattern aligns with security best practices, in which you never trust client‑supplied totals for payment processing.[18]

### Webhook Listener Implementation for Event Reconciliation

While the synchronous create and capture calls cover successful flows initiated from your UI, robust payment integrations also rely on webhooks for asynchronous notification of events such as capture completion, disputes, or subscription changes.[11][19] PayPal’s webhooks are HTTPS POST requests sent to a listener URL you configure in the Developer Dashboard for your app, for specific event types or for all events (`*`).[11][19] To handle them, your FastAPI app defines a POST endpoint that accepts arbitrary JSON, verifies the signature, and updates MongoDB accordingly.

A simplified webhook handler might look like this:

```python
# app/routers/webhooks.py
from fastapi import APIRouter, Header, HTTPException, Request, status
from ..database import orders_collection

router = APIRouter()

@router.post("/paypal/webhook")
async def paypal_webhook(
    request: Request,
    paypal_transmission_id: str = Header(None, alias="Paypal-Transmission-Id"),
    paypal_transmission_sig: str = Header(None, alias="Paypal-Transmission-Sig"),
    paypal_cert_url: str = Header(None, alias="Paypal-Cert-Url"),
    paypal_auth_algo: str = Header(None, alias="Paypal-Auth-Algo"),
    paypal_transmission_time: str = Header(None, alias="Paypal-Transmission-Time"),
    webhook_id: str = Header(None, alias="Webhook-Id"),
):
    body = await request.body()
    # Here you would call PayPal's verify-signature endpoint to verify authenticity.[55]
    # For brevity, this example omits that call but in production you must implement it.

    event = await request.json()
    event_type = event["event_type"]
    resource = event.get("resource", {})
    if event_type == "PAYMENT.CAPTURE.COMPLETED":
        related_order_id = resource.get("supplementary_data", {}).get(
            "related_ids", {}
        ).get("order_id")
        capture_id = resource.get("id")
        if related_order_id:
            await orders_collection.update_one(
                {"paypal_order_id": related_order_id},
                {
                    "$set": {
                        "status": "COMPLETED",
                        "capture_id": capture_id,
                        "webhook_event": event,
                    }
                },
            )
    return {"status": "ok"}
```

The PayPal webhooks guide emphasizes that a listener must both receive and verify messages, and that any non‑2xx status code causes PayPal to retry delivery up to 25 times over three days.[11] In production, you implement verification by posting the `transmission_id`, `transmission_sig`, certificate URL, algorithm, and webhook ID, together with the payload, to PayPal’s `verify-signature` endpoint. Only if verification succeeds do you trust the event and act on it. The example above also shows how to extract the related order ID and capture ID from the webhook resource to update the correct MongoDB order.

By handling webhooks, your dropshipping system can recover from frontend or backend failures that occur between buyer approval and capture acknowledgement, and can also react to post‑capture events such as chargebacks or disputes.

## Frontend Implementation: React + shadcn UI + `@paypal/react-paypal-js`

### Building the Checkout Form with shadcn Components

The React frontend’s primary responsibilities are to display a user‑friendly checkout form, compute the current cart, and render the PayPal buttons. For the form, shadcn/ui provides composable components such as `Field`, `FieldLabel`, `FieldDescription`, and `Input` for text entry, which can be wired with React Hook Form for validation and better performance.[21][30][36]

A simple checkout form might collect email, name, and shipping address fields, using `useState` or React Hook Form for state management. React’s state documentation advocates describing UI states declaratively and avoiding direct DOM manipulation; for example, you define an “initial” state for an empty form, a “submitting” state when the user clicks PayPal, and a “completed” state when the capture succeeds.[12][41] The button’s disabled state and label content then derive from the current state.

An example `CheckoutForm` component using shadcn’s `Input` and `Button` could look like this:

```tsx
// src/components/CheckoutForm.tsx
import React from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface ShippingFormValues {
  fullName: string;
  line1: string;
  line2?: string;
  city: string;
  state: string;
  postalCode: string;
  countryCode: string;
  email: string;
}

interface CheckoutFormProps {
  values: ShippingFormValues;
  onChange: (values: ShippingFormValues) => void;
}

export function CheckoutForm({ values, onChange }: CheckoutFormProps) {
  const handleChange = (field: keyof ShippingFormValues) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    onChange({ ...values, [field]: e.target.value });
  };

  return (
    <div className="space-y-4">
      <Input
        placeholder="Full name"
        value={values.fullName}
        onChange={handleChange("fullName")}
      />
      <Input
        placeholder="Email"
        type="email"
        value={values.email}
        onChange={handleChange("email")}
      />
      <Input
        placeholder="Address line 1"
        value={values.line1}
        onChange={handleChange("line1")}
      />
      <Input
        placeholder="Address line 2"
        value={values.line2 ?? ""}
        onChange={handleChange("line2")}
      />
      <Input
        placeholder="City"
        value={values.city}
        onChange={handleChange("city")}
      />
      <Input
        placeholder="State"
        value={values.state}
        onChange={handleChange("state")}
      />
      <Input
        placeholder="Postal code"
        value={values.postalCode}
        onChange={handleChange("postalCode")}
      />
      <Input
        placeholder="Country code (e.g. US)"
        value={values.countryCode}
        onChange={handleChange("countryCode")}
      />
      <Button type="submit" className="hidden">
        Submit
      </Button>
    </div>
  );
}
```

In a real application, you would embed this form into a page component, connect its `onChange` handler to component state via `useState`, and potentially integrate validation logic using Zod schemas and React Hook Form, as suggested in shadcn’s form documentation.[21][36] The last hidden submit button is a placeholder illustrating that the form is logically submit‑capable even though the actual submission is triggered by PayPal button clicks.

### Integrating `PayPalScriptProvider` and `PayPalButtons`

To render the PayPal Checkout buttons, you use the `PayPalButtons` component from `@paypal/react-paypal-js`. The integration wraps the component in `PayPalScriptProvider`, which manages loading of the PayPal JavaScript SDK with appropriate query parameters. The provider’s `options` include at minimum the `client-id`, `currency`, and `intent`, mirroring the structure described in PayPal’s integration examples.[1][31][31][45]

A typical `CheckoutPage` component might combine the checkout form and PayPal buttons as follows:

```tsx
// src/CheckoutPage.tsx
import React, { useState } from "react";
import { PayPalButtons, usePayPalScriptReducer } from "@paypal/react-paypal-js";
import { CheckoutForm } from "./components/CheckoutForm";

interface CartItem {
  sku: string;
  name: string;
  quantity: number;
  unit_price: number;
}

interface ShippingFormValues {
  fullName: string;
  line1: string;
  line2?: string;
  city: string;
  state: string;
  postalCode: string;
  countryCode: string;
  email: string;
}

export function CheckoutPage() {
  const [{ isPending }] = usePayPalScriptReducer();
  const [shipping, setShipping] = useState<ShippingFormValues>({
    fullName: "",
    line1: "",
    line2: "",
    city: "",
    state: "",
    postalCode: "",
    countryCode: "US",
    email: "",
  });
  const [isPaying, setIsPaying] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const cart: CartItem[] = [
    {
      sku: "SKU123",
      name: "Example Product",
      quantity: 1,
      unit_price: 49.99,
    },
  ];

  const createOrder = async () => {
    setError(null);
    setIsPaying(true);
    try {
      const response = await fetch("http://localhost:8000/api/paypal/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          items: cart,
          shipping: {
            full_name: shipping.fullName,
            line1: shipping.line1,
            line2: shipping.line2,
            city: shipping.city,
            state: shipping.state,
            postal_code: shipping.postalCode,
            country_code: shipping.countryCode,
          },
          currency: "USD",
        }),
      });
      if (!response.ok) {
        throw new Error("Failed to create order");
      }
      const data = await response.json();
      return data.paypal_order_id as string;
    } catch (err: any) {
      setError(err.message || "Error creating order");
      setIsPaying(false);
      throw err;
    }
  };

  const onApprove = async (data: any, actions: any) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/paypal/orders/${data.orderID}/capture`,
        {
          method: "POST",
        }
      );
      if (!response.ok) {
        throw new Error("Failed to capture order");
      }
      const result = await response.json();
      setSuccessMessage("Payment completed successfully!");
    } catch (err: any) {
      setError(err.message || "Error capturing payment");
    } finally {
      setIsPaying(false);
    }
  };

  const onError = (err: any) => {
    setError("PayPal checkout error");
    setIsPaying(false);
  };

  return (
    <div className="max-w-xl mx-auto p-4 space-y-6">
      <h1 className="text-2xl font-semibold">Checkout</h1>

      <CheckoutForm values={shipping} onChange={setShipping} />

      {error && <p className="text-red-600">{error}</p>}
      {successMessage && <p className="text-green-600">{successMessage}</p>}

      {isPending && <p>Loading payment options…</p>}

      <PayPalButtons
        style={{ layout: "vertical" }}
        disabled={isPaying}
        createOrder={async () => createOrder()}
        onApprove={onApprove}
        onError={onError}
      />
    </div>
  );
}
```

This pattern corresponds to PayPal’s recommended usage of `PayPalButtons`, where `createOrder` is responsible for setting up the transaction, and `onApprove` handles the buyer’s approval and triggers capture.[1][31][31][45] Rather than using `actions.order.create()` directly in the browser, this implementation defers to the backend, which aligns with the architecture described earlier and ensures that the order amount is determined server‑side.

The loading and disabled behavior is implemented using React state, where `isPaying` and `isPending` control button interactivity and loading messages. Tutorials on React form handling emphasize this pattern: set a loading state to `true` when submission begins, disable the button to prevent duplicate submissions, and reset the state once the operation completes or fails.[12][34][41] The `style` prop can be customized further, including layout, color, and height, and the JavaScript SDK reference explains additional customization options like `disableMaxHeight` and `disableMaxWidth` if you need to adjust constraints.[45]

### Managing Loading, Error, and Success States

From a user experience perspective, a payment flow must make it obvious when work is in progress and when it has succeeded or failed. React’s `useState` and `useEffect` hooks offer the tools for this. When the user clicks the PayPal button, the `createOrder` function sets `isPaying` to `true`, which can disable the button and change its label to something like “Processing…”. If the backend call fails or PayPal’s SDK signals an error, you clear the loading state and show an error message in the UI, perhaps using a toast component or an inline alert. After a successful capture, you can display a confirmation message, navigate to a thank‑you page, or clear the cart.

React’s state management guide illustrates how to lift state up to a parent component when multiple children need to share or influence it, such as a form and a PayPal button sharing the same loading and error states.[12] For more complex screens, you might combine reducers and context to centralize state update logic and allow deeply nested components to dispatch actions that update the checkout state, but for a single page the simple useState approach is sufficient.[12][48]

In case of errors originating from the backend, you should pay attention to HTTP status codes and response bodies. If the create order endpoint responds with 4xx codes, such as 400 or 422, it indicates client errors like validation failures; 5xx codes indicate server errors, and PayPal’s own API may produce error responses for issues such as unsupported currencies or authorization problems.[29][44] Logging these errors on the backend with structured logging and correlating them with MongoDB order records will help you diagnose issues in production.[22][29]

## Testing and Validation

### Backend Testing with pytest and HTTPX

Before relying on the integration in production, you should test backend endpoints in isolation. FastAPI’s testing guidance recommends using HTTPX’s `AsyncClient` together with pytest and AnyIO to test asynchronous endpoints.[32] Instead of using the synchronous `TestClient`, asynchronous tests can await the app directly via an ASGI transport, which is particularly useful when your endpoints interact with async drivers like Motor.[32]

A simple test for the root endpoint might look like FastAPI’s example, which uses `ASGITransport` and an async pytest function:

```python
# tests/test_main.py
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello from Dropship Store API"}
```

Similar tests can be constructed for the `/api/paypal/orders` and `/api/paypal/orders/{paypal_order_id}/capture` endpoints by mocking out PayPal calls. For unit testing, you might inject a fake PayPal client that returns predetermined responses without calling the real API. The FastAPI testing documentation notes that asynchronous tests must use the `@pytest.mark.anyio` marker and that objects requiring an event loop, such as Motor clients, should be instantiated within async contexts such as startup events to avoid event loop mismatch errors.[32]

You should also test MongoDB CRUD operations to verify that order documents are inserted, updated, and retrieved as expected, paying attention to fields like `matchedCount` and `modifiedCount` returned by `update_one`.[38][42] For more realistic integration tests, you can run a local MongoDB instance, configure your FastAPI app to use it, and let the tests interact with it, cleaning up collections between runs.

### End‑to‑End Testing with PayPal Sandbox

The most important tests are end‑to‑end flows that exercise the complete stack: React frontend, FastAPI backend, MongoDB, and PayPal sandbox. To do this, you run the React app (for example, at `http://localhost:3000`) and the FastAPI backend (for example, at `http://localhost:8000`) and ensure that CORS is configured to allow the frontend to call the backend.[13] You configure the PayPal client ID to be the sandbox client ID for your test app and ensure that the backend uses the sandbox base URL `https://api-m.sandbox.paypal.com` in the `PAYPAL_BASE_URL` environment variable.[3][25]

When you load the checkout page, you should see the PayPal button rendered by the `PayPalButtons` component. Clicking it should open a PayPal sandbox login or card entry window. To test PayPal account flows, you log in with a sandbox personal account created in the Developer Dashboard. To test card flows, you use PayPal’s sandbox card numbers and card testing guidance, which describe test card numbers for different brands and recommend entering a future expiration date and arbitrary CVV to simulate successful payments.[15] The card testing documentation explains how to simulate successful captures, declines, and 3D Secure scenarios by choosing specific card numbers and trigger values.[15]

For example, to test a successful card capture, you ensure your integration is in sandbox mode, uses a sandbox client ID, and points to `api-m.sandbox.paypal.com` endpoints, then go to your checkout page, choose a test card number from PayPal’s list, enter the card details and a valid address, and submit the order.[15] After the payment, you log into your merchant sandbox account and verify that the payment appears in the activity page with the correct amount and currency.[15] This confirms that the create and capture flows are functioning correctly end‑to‑end.

PayPal’s negative testing tools also allow you to simulate API errors by setting specific values that trigger error codes. The “Test error handling” documentation shows how to trigger error conditions by embedding error code values in amount fields or other parameters.[23] For example, setting an amount of `107.55` in a `DoDirectPayment` call triggers an error code `10755` for unsupported currency.[23] While this example uses legacy APIs, the principle of using trigger values for negative tests can inspire your own strategy: you might create test orders with invalid currencies or amounts, or deliberately use mismatched sandbox credentials to ensure that your error handling surfaces meaningful messages to users and logs details for developers.[23][29][44]

### Webhook Verification and Reconciliation Testing

Once your webhook endpoint is implemented, you should test webhook handling in the sandbox. PayPal allows you to register webhook URLs per app and subscribe them to event types such as payments, orders, and subscriptions.[11][19] After you subscribe your FastAPI webhook URL for events such as `PAYMENT.CAPTURE.COMPLETED`, you perform test transactions in the sandbox and verify that your backend receives and processes the corresponding webhook messages.

The webhooks guide describes the two‑step process for handling webhooks: receipt and verification. First, your endpoint must accept POST requests and respond with a 2xx status code to confirm receipt; otherwise, PayPal retries delivery up to 25 times. Second, your endpoint must verify the message’s authenticity either by validating its signature using a CRC32 checksum or by posting the payload and header information back to PayPal’s `verify-signature` endpoint. For testing, you may temporarily log the headers and body to ensure they arrive as expected, but in production you should implement full verification.

After your handler verifies and processes the webhook, you should confirm that the corresponding MongoDB order document has been updated appropriately. For example, if a capture completes, the `status` should change to `"COMPLETED"`, the `capture_id` should be set, and the event payload may be stored for future auditing. This reconciliation ensures that your store’s internal state remains aligned with PayPal’s record even if synchronous API calls fail or time out.

## Common Pitfalls and Troubleshooting

### CORS, Environment Mismatches, and Credential Errors

One of the most frequent issues in frontend‑backend integrations is misconfigured CORS. If your React app runs at `http://localhost:3000` and your FastAPI app at `http://localhost:8000`, FastAPI’s CORS middleware must list `http://localhost:3000` in its `allow_origins` for the browser to permit calls across origins.[13] Failing to do this results in errors in the browser console indicating blocked cross‑origin requests, even though the backend endpoints are reachable via tools such as cURL or Postman.[13] You should be explicit about allowed origins, especially in production, to avoid inadvertently enabling untrusted domains.

Another common mistake is mixing sandbox and live credentials or base URLs. PayPal sandbox client IDs must be used with `api-m.sandbox.paypal.com`, while live client IDs require `api-m.paypal.com`.[3][25] If you use a sandbox client ID in the JavaScript SDK while the backend calls live endpoints, the integration will fail in non‑obvious ways. To avoid this, configure separate environment variables for sandbox and production, and ensure your deployment pipeline sets them correctly.

Credential errors can also arise from misconfigured environment variables. For example, forgetting to prefix a React environment variable with `REACT_APP_` means it will not be injected at build time, causing `process.env.REACT_APP_PAYPAL_CLIENT_ID` to be `undefined` and the `PayPalScriptProvider` to fail. The Create React App documentation emphasizes that only variables starting with `REACT_APP_` are exposed to the client, and that `.env` files must be reloaded by restarting the development server after changes.[16][16] On the backend, forgetting to set `PAYPAL_CLIENT_SECRET` will result in authorization failures when calling `v1/oauth2/token`, and PayPal’s API responses will include errors such as invalid credentials or missing client secret.[3][29]

### Data Consistency, Idempotency, and MongoDB Updates

A subtle but important aspect of payment integrations is the handling of idempotency and data consistency. Because network requests can fail, time out, or be retried, you must design your MongoDB update logic so that repeating the same capture or webhook processing does not corrupt data. MongoDB’s `update_one` semantics, which update only a single document matching the filter, can be combined with checks on current status to enforce idempotency. For instance, you might update an order’s status to `"COMPLETED"` only if the current status is not already `"COMPLETED"`, preventing double‑application of a capture event.[38][42]

MongoDB’s transaction support can further protect against partial updates when you simultaneously update multiple collections, but for a basic integration the primary concern is ensuring that each PayPal event maps to a single, consistent state transition in your order document.[26] Maintaining a log of state transitions within each document, such as an array of status changes with timestamps, can provide auditability and facilitate debugging when payments do not behave as expected.[10][26][10]

### Frontend Integration Issues with PayPal Buttons

On the frontend, integration problems often manifest as PayPal buttons not rendering, or as callbacks not firing. The `@paypal/react-paypal-js` documentation and PayPal’s JS SDK reference highlight several required conditions for successful rendering.[31][31][45] First, the `PayPalScriptProvider` must be present and must receive a valid `client-id`. Second, the component tree must not violate React hook rules; for example, you must not call `usePayPalScriptReducer` conditionally or inside loops, as React’s hook rules prohibit such usage.[12][31][31] Third, customizing button height and width must comply with constraints described in the JS SDK reference, such as not setting `style.height` and `style.disableMaxHeight` simultaneously, which would cause a rendering error.[45]

Additionally, the `createOrder` function must return a promise that resolves to a valid PayPal `orderID`. If it throws or returns an invalid value, the PayPal SDK logs errors to the console and the checkout flow breaks. Invoking asynchronous backend endpoints inside `createOrder`, as this guide recommends, is supported but requires careful handling of errors and return values. You should ensure that any thrown errors are either caught and translated into user‑visible messages or allowed to propagate to PayPal’s own error handling so that the user is not left in an ambiguous state.

### Error Handling and Logging Across the Stack

Robust error handling spans the entire stack. On the backend, you should catch exceptions from HTTP calls to PayPal and from MongoDB operations, transforming them into HTTP responses with appropriate status codes and generic messages for the client while logging detailed error information for operators.[22][29] FastAPI’s exception handling mechanisms support this pattern, and you can also implement structured logging that integrates with process managers like Gunicorn or Uvicorn. Community discussions on logging in FastAPI containers suggest configuring the gunicorn and uvicorn loggers and using log configuration files to unify logging behavior across components.[22]

On the frontend, React error boundaries can catch rendering errors and display fallback UIs, but note that error boundaries do not catch errors in event handlers or asynchronous code like promises.[27] For network errors and PayPal SDK errors, you should maintain state variables such as `error` and show user‑friendly messages. Careful distinction between validation errors, backend failures, and PayPal failures helps users understand what went wrong and what they can do, such as checking their card details or trying a different payment method.

At the PayPal layer, errors can occur for many reasons: invalid credentials, unsupported currencies, declined cards, or account limitations.[29][44] PayPal’s API responses include detailed error codes and messages, and PayPal provides separate documentation for Orders API errors, such as `NOT_ENABLED_FOR_CARD_PROCESSING` when an account is not configured for card payments.[44] Logging these error codes and correlating them with user reports allows you to address configuration issues (such as enabling Advanced card processing) or handle business constraints such as card declines gracefully.[29][44]

## Conclusion

This integration playbook has outlined a complete, technically grounded approach to adding PayPal Checkout to a dropshipping e‑commerce store built with a React frontend using shadcn/ui, a FastAPI backend, and MongoDB as the persistent store. The architecture leverages the PayPal JavaScript SDK and the `@paypal/react-paypal-js` wrapper on the client to render PayPal buttons and orchestrate buyer interactions, while ensuring that critical operations such as order creation and payment capture occur on the server using the PayPal Orders REST API.[1][3][7][31][7][31][45] This division of responsibilities aligns with security best practices by keeping sensitive logic and credentials confined to the backend.[18][25]

The environment setup section described how to prepare Node.js, Python, and MongoDB, install dependencies for the React and FastAPI projects, and configure CORS and environment variables correctly so that the stack can communicate securely and reliably.[13][16][16][46][49] The PayPal configuration section explained how to create sandbox buyer and seller accounts, obtain REST app credentials, and handle OAuth 2.0 access tokens, emphasizing the importance of keeping the client secret on the server and switching carefully between sandbox and live environments.[1][3][4][25][37]

On the backend, the guide detailed how to model orders in MongoDB with embedded items and shipping data, implement asynchronous FastAPI endpoints that create and capture PayPal orders, persist order documents, and update them as payment status changes.[10][26][38][40][42][47] It also showed how to add a webhook listener to process asynchronous PayPal events and reconcile order state, including signature verification and idempotent updates to MongoDB.[11][19]

On the frontend, the playbook showed how to build a streamlined checkout form using shadcn UI components and React state, then integrate PayPal buttons via `PayPalScriptProvider` and `PayPalButtons` such that `createOrder` and `onApprove` callbacks delegate sensitive work to the backend while providing responsive loading and error feedback to users.[1][12][21][30][31][34][31][36][41][43][45][45] The testing section outlined backend unit tests using pytest and HTTPX, and end‑to‑end flow tests using the PayPal sandbox, test card numbers, and sandbox accounts to simulate successful and failing payments, along with webhook verification tests to ensure event‑driven state changes are handled correctly.[3][11][15][19][23][29][32][37]

Finally, the discussion of common pitfalls and troubleshooting covered real‑world issues such as CORS failures, environment misconfiguration, credential errors, perils of exposing secrets on the client, data consistency challenges in MongoDB, and frontend integration anomalies that can prevent PayPal buttons from rendering or functioning as intended.[13][16][26][29][16][38][44][45] By anticipating and mitigating these problems, developers can significantly reduce integration time and production incidents.

For a dropshipping business, the integration described here provides a robust foundation for secure, scalable payment processing with PayPal, tightly integrated into a modern React and FastAPI stack and backed by MongoDB’s flexible document model for orders and fulfillment. From this baseline, you can extend functionality to include subscription billing, multi‑currency support, detailed analytics, and advanced risk controls, all while maintaining clear separation of concerns and a testable, maintainable codebase.

---
Sources:
1. https://developer.paypal.com/community/blog/how-to-add-paypal-checkout-payments-to-your-react-app/
2. https://fastapi-payments.readthedocs.io
3. https://developer.paypal.com/api/rest/
4. https://github.com/paypal-examples/docs-examples
5. https://developer.paypal.com/docs/checkout/advanced/sdk/v1/
6. https://www.fast-saas.com/blog/fastapi-stripe-integration/
7. https://developer.paypal.com/docs/api/orders/v2/
8. https://www.shadcnblocks.com/blocks/checkout
9. https://developer.paypal.com/braintree/docs/guides/paypal/server-side/python/
10. https://www.mongodb.com/community/forums/t/schmea-design-advice-for-order-management-and-shipping/218902
11. https://developer.paypal.com/docs/api/webhooks/v1/
12. https://react.dev/learn/managing-state
13. https://fastapi.tiangolo.com/tutorial/cors/
14. https://www.youtube.com/watch?v=MXwcUrI-iss
15. https://developer.paypal.com/tools/sandbox/card-testing/
16. https://create-react-app.dev/docs/adding-custom-environment-variables/
17. https://www.youtube.com/watch?v=NQSWBNY92Q8
18. https://developer.paypal.com/api/rest/reference/info-security-guidelines/
19. https://developer.paypal.com/api/rest/webhooks/event-names/
20. https://www.mongodb.com/solutions/industries/retail
21. https://ui.shadcn.com/docs/forms
22. https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/issues/19
23. https://developer.paypal.com/tools/sandbox/error-conditions/
24. https://www.inventorysource.com
25. https://developer.paypal.com/studio/checkout/standard/getstarted
26. https://www.mongodb.com/products/capabilities/transactions
27. https://legacy.reactjs.org/docs/error-boundaries.html
28. https://fastapi.tiangolo.com/tutorial/body-fields/
29. https://developer.paypal.com/api/rest/responses/
30. https://ui.shadcn.com/docs/components/radix/input
31. https://www.npmjs.com/package/@paypal/react-paypal-js
32. https://fastapi.tiangolo.com/advanced/async-tests/
33. https://pymongo.readthedocs.io/en/stable/api/bson/objectid.html
34. https://www.youtube.com/watch?v=7EFp_WxfMiI
35. https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
36. https://ui.shadcn.com/docs/forms/react-hook-form
37. https://developer.paypal.com/tools/sandbox/accounts/
38. https://www.mongodb.com/docs/manual/reference/method/db.collection.updateone/
39. https://fastapi.tiangolo.com/tutorial/response-status-code/
40. https://fastapi.tiangolo.com/tutorial/body/
41. https://dev.to/heyjoshlee/using-the-usestate-hook-and-working-with-forms-in-react-js-m6b
42. https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/insert/
43. https://ui.shadcn.com/docs/components/radix/button
44. https://developer.paypal.com/api/rest/reference/orders/v2/errors/
45. https://developer.paypal.com/sdk/js/reference/
46. https://www.mongodb.com/docs/mongodb-shell/connect/
47. https://fastapi.tiangolo.com/tutorial/bigger-applications/
48. https://itnext.io/when-you-finally-decided-to-rid-yourself-of-redux-8fff0624d2fb
49. https://docs.npmjs.com/downloading-and-installing-node-js-and-npm/
50. https://www.netsuite.com/portal/resource/articles/erp/order-fulfillment.shtml

`````

---
## Notes

- The API key in all request dumps above is mocked (`pplx-REDACTED-MOCK-KEY`); everything else is byte-exact.
- Cost figures come from the `usage.cost` object Perplexity returns in each response.
