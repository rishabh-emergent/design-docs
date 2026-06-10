#!/usr/bin/env python3
"""
Replay REAL prod integration_playbook_expert_v2 tool inputs against the
Perplexity API using the EXACT request construction from production
(llm-proxy-service/pkg/tools/perplexity/client.go).

Faithfulness notes:
- System prompt: verbatim copy of systemPromptTemplate with %s = strings.Join(techStack, ", ")
- User prompt:   verbatim copy of the Execute() fmt.Sprintf (query embedded whole)
- Body:          {"model": "sonar-deep-research", "messages": [...]} — NOTHING else
                 (prod sets no temperature, no max_tokens, no top_p)
- Headers:       Authorization: Bearer <key>, Content-Type: application/json
- tech_stack:    exact values from emergent/agents/service/templates/config.yaml
                 (expo_mongo_base_image → ['expo react native', 'mongodb database', 'react native web'])
- Inputs:        exact `action` text of real prod tool calls (trajectories_full_view),
                 each verified to have triggered the Perplexity fallback in prod.
"""
import concurrent.futures as cf
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent / "samples"
OUT.mkdir(exist_ok=True)


def _gcloud_secret(name, project):
    return subprocess.run(
        ["gcloud", "secrets", "versions", "access", "latest", "--secret", name, "--project", project],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


PPLX_KEY = os.environ.get("PERPLEXITY_API_KEY") or _gcloud_secret("PERPLEXITY_API_KEY", "emergent-default")

# VERBATIM from llm-proxy-service/pkg/tools/perplexity/client.go
SYSTEM_PROMPT_TEMPLATE = """You are Integration_Playbook_Expert, responsible for creating detailed integration guides.
Research and provide a complete integration playbook for the requested technology that includes:

1. Installation instructions
2. API key setup & security best practices
3. Complete code examples for this tech stack: {stack}
4. Testing procedures
5. Common pitfalls and how to avoid them

Format your response in a structured, step-by-step guide that a developer can follow.
Include all necessary code samples.
If the integration involves API keys, include instructions on where to get them."""

USER_PROMPT_TEMPLATE = "Create a detailed integration playbook for {query} in {stack} application. Include all necessary installation steps, code samples, and testing procedures. Keep it short and precise."

API_URL = "https://api.perplexity.ai/chat/completions"
MODEL = "sonar-deep-research"

# Exact per-template tech_stack (emergent/agents/service/templates/config.yaml)
EXPO_STACK = ["expo react native", "mongodb database", "react native web"]

# Real prod tool inputs (verbatim `action` from analytics.trajectories_full_view;
# all four jobs ran on expo_mongo_base_image and hit the Perplexity fallback in prod).
SAMPLES = [
    {
        "id": "sample-1-stripe-expo",
        "prod_job_id": "5573afd7-c9dc-46f1-bdd4-1e5e573f3c83",
        "prod_called_at": "2026-06-10T08:58:53.706 UTC",
        "tech_stack": EXPO_STACK,
        "query": "INTEGRATION: Stripe payment integration for Expo React Native mobile app + FastAPI backend. Use case: students/parents pay school registration fee for pondok pesantren (Islamic boarding school). Need test mode payment with checkout session. CONSTRAINTS: Mobile app uses Expo SDK 54, no login (registration ID based), Stripe test keys available in pod environment.",
    },
    {
        "id": "sample-2-google-drive",
        "prod_job_id": "7abb5ac8-1f08-45fc-b1f2-a50ce10e6e44",
        "prod_called_at": "2026-06-10T08:56:29.590 UTC",
        "tech_stack": EXPO_STACK,
        "query": "INTEGRATION: Google Drive API integration for Python FastAPI backend\nREQUIREMENTS:\n- Upload CSV files to a specific shared Google Drive folder\n- Auto-sync functionality for daily/weekly exports\n- Real-time sync of time entry data\n- User will provide OAuth tokens/credentials\n- Need to handle authentication and file upload to shared folder ID\nCONSTRAINTS:\n- Must work with FastAPI backend\n- Need to support automated scheduled uploads\n- Handle OAuth2 authentication flow",
    },
    {
        "id": "sample-3-jwt-auth-expo",
        "prod_job_id": "dc6c8b51-79c3-4468-8f94-dcbacb9af514",
        "prod_called_at": "2026-06-10T08:55:47.765 UTC",
        "tech_stack": EXPO_STACK,
        "query": "INTEGRATION: Custom JWT-based email/password authentication for an Expo React Native (SDK 54) mobile app with FastAPI + MongoDB backend. Need: register, login, password hashing (bcrypt), JWT token issuance/validation, secure token persistence on mobile (expo-secure-store).\n\nCONSTRAINTS: \n- Expo SDK 54 React Native mobile app\n- FastAPI backend with /api prefix on all routes\n- MongoDB for user storage\n- Token storage via expo-secure-store",
    },
    {
        "id": "sample-4-jwt-otp-roles-expo",
        "prod_job_id": "da83523f-7735-4b4f-a92a-8569b343a1ec",
        "prod_called_at": "2026-06-10T08:55:13.078 UTC",
        "tech_stack": EXPO_STACK,
        "query": "INTEGRATION: JWT-based authentication for Expo React Native app with FastAPI backend. Need:\n1. Email + password registration & login (working JWT auth)\n2. Phone OTP mocked login (accept any 6-digit OTP for now, just generate JWT)\n3. Role-based auth (customer vs admin role)\n4. Token storage via expo-secure-store on client\n\nCONSTRAINTS: \n- Backend FastAPI with MongoDB (Motor)\n- Frontend Expo Router with React Native\n- Use bcrypt for password hashing\n- JWT tokens for session",
    },
]


def run_sample(s):
    stack = ", ".join(s["tech_stack"])
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(stack=stack)
    user_prompt = USER_PROMPT_TEMPLATE.format(query=s["query"], stack=stack)
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    print(f"[{s['id']}] firing...", flush=True)
    t0 = time.time()
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {PPLX_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=1500) as resp:
            status = resp.status
            response_body = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        latency = time.time() - t0
        print(f"[{s['id']}] FAILED after {latency:.1f}s: {e}", flush=True)
        record = {"sample": s, "error": str(e), "latency_s": latency}
        (OUT / f"{s['id']}.json").write_text(json.dumps(record, indent=2))
        return record

    latency = time.time() - t0
    record = {
        "sample_id": s["id"],
        "prod_job_id": s["prod_job_id"],
        "prod_called_at": s["prod_called_at"],
        "replayed_at_epoch": int(t0),
        "request": {
            "url": API_URL,
            "method": "POST",
            "headers": {
                "Authorization": "Bearer pplx-REDACTED-MOCK-KEY",
                "Content-Type": "application/json",
            },
            "body": body,
        },
        "http_status": status,
        "latency_s": round(latency, 1),
        "response": response_body,
    }
    (OUT / f"{s['id']}.json").write_text(json.dumps(record, indent=2))
    usage = response_body.get("usage", {})
    cost = usage.get("cost", {}).get("total_cost")
    content_len = len(response_body.get("choices", [{}])[0].get("message", {}).get("content", ""))
    n_cit = len(response_body.get("citations", []))
    print(f"[{s['id']}] OK {latency:.1f}s  cost=${cost}  content={content_len} ch  citations={n_cit}", flush=True)
    return record


def main():
    print(f"Replaying {len(SAMPLES)} real prod queries against {API_URL} (model={MODEL})...")
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(run_sample, SAMPLES))
    print(f"\nDone in {time.time()-t0:.0f}s. Files in {OUT}/")
    total_cost = 0.0
    for r in results:
        if "response" in r:
            total_cost += r["response"].get("usage", {}).get("cost", {}).get("total_cost", 0)
    print(f"Total replay cost: ${total_cost:.3f}")


if __name__ == "__main__":
    main()
