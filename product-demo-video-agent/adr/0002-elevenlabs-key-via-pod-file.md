# ADR 0002 — ElevenLabs API key flows through pod file, not LLM context

Date: 2026-05-24
Status: Accepted

## Context

ElevenLabs is the chosen TTS provider for the product-demo-video subagent. The Emergent universal LLM key (returned by `emergent_integrations_manager`) only routes to OpenAI / Anthropic / Gemini / Sora-2 / Whisper — verified by reading `cortex/pkg/agentsdk/tools/builtin/integrations.go`. ElevenLabs is **not** covered. The user has to provide an ElevenLabs API key themselves.

Three options for getting that key from the user to the subagent:

1. **Pass in subagent input JSON**: parent calls `ask_human` for the key, then puts the raw key inside the JSON it passes to the subagent. Simple but the key flows through:
   - LLM completion logs (Anthropic-side cache + Emergent-side logs)
   - Cortex session storage (BigTable / Postgres)
   - VCR cassettes if anyone records this flow
   - Any debug prints / activity history

2. **Inject as pod env var**: cortex provisions `ELEVENLABS_API_KEY` in the pod's process env. Subagent reads `os.environ`. Rejected because cortex doesn't expose a mechanism to inject arbitrary env vars per-job — `emergent_integrations_manager` is the only path, and it only handles the universal LLM key. Building this mechanism is too large for v0.

3. **Write to pod file, pass path only**: parent calls `ask_human` for the key, then uses `mcp_create_file` to write `/app/marketing-video/.env` with `chmod 600`. Subagent's JSON contract receives only `elevenlabs_key_path: "/app/marketing-video/.env"`. The raw key appears in the parent's context once (during the create_file call), but **never appears in the subagent's context**. Subagent's bash calls read the file directly: `source /app/marketing-video/.env && curl ... -H "xi-api-key: $ELEVENLABS_API_KEY"`.

## Decision

Option 3.

The parent agent's prompt instructs: after collecting the key via `ask_human`, immediately `mcp_create_file` to `/app/marketing-video/.env` with the key, then invoke the subagent with the path. The subagent never sees the raw key value — only the path — and runs ElevenLabs calls via shell-sourced env, which doesn't return the key to LLM context (the response from `execute_bash` is just the curl output, not the env contents).

## Alternatives rejected and why

**Option 1 (raw key in JSON)**: Too much surface area for the key to leak. Anthropic logs, our session storage, our cassettes. We've already had ElevenLabs key issues in the retrospective (wrong scopes); the next problem we want to avoid is "user's ElevenLabs key showed up in someone else's debug log."

**Option 2 (pod env var)**: Right shape, wrong time. Would require: a new field on the job-submit API, a deployer-side change to project env vars into the pod, and a way for cortex to know which env vars are safe to set. Not v0.

## Consequences

- The parent agent's prompt grows by one mandatory step: "after `ask_human` for ELEVENLABS_API_KEY, write to `/app/marketing-video/.env` chmod 600 before calling subagent." This is the only friction.
- The subagent prompt has to use `source /app/marketing-video/.env && curl ...` style shell, never `--data-binary` with the key inline in the command (which would put the key in the bash command string → into the LLM context).
- The .env file persists until pod recycle. If a malicious agent ever has shell access in the same pod, it can read the file. Accepted: same threat model as any other workspace secret today.
- v1: when cortex grows a proper "ephemeral pod secret" mechanism (e.g. a tmpfs-mounted secret file the workspace can't list-and-grep), migrate to that.
