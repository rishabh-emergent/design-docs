# Ambiguous Agent Handoff v3 — Implementation Plan

**Status:** Implemented — cortex PR #1646 (branch `feat/aps-ambiguous-handoff-via-tool`)
**Branch base:** `main` (cortex repo)
**Predecessor design:** PR #1361 (closed without merging — see "Why this approach" below)

---

## As-built notes (PR #1646) — deviations from the plan below

The plan below was written against the PR #1361 branch; a few of its assumptions
were wrong against a clean `main`. What actually shipped:

- **Pod provisioning = lazy env, not eager.** Elite never provisions pods (Neo does),
  and `executeHandoff` only reuses the parent's `EnvInfo`. Build targets need
  *different* base images (web/mobile/nextjs), so the handoff stores **lazy-env**
  metadata (`envcore.StoreLazyEnv`) keyed by the job slug with the resolved build
  agent's `template_image`. envcore's `EnvEnsurer` materializes the pod with that
  image on the build agent's first envcore tool call. No pod is created at handoff.
- **No new SQL query.** The "first user message" idea became "all user messages":
  the activity uses the existing `sessionSvc.GetSessionMessages`, filters `user`
  role, and joins their text (handles multi-turn clarification). No sqlc/mockgen.
- **`executeHandoff` gained a `task string` param** (not `taskOverride`+`flow`).
  On `main` it had no `flow` param and hardcoded the task; existing callers now
  pass `""` (unchanged default `defaultHandoffTask`).
- **No `FlowAmbiguousHandoff` constant / fallback map entry** — not needed without
  the flow param.
- **`handoff_to_agent` is a builtin terminal tool** in `pkg/agentsdk/tools/builtin/`
  (executor map + `tools.yaml`), not the legacy `execute.go` path.
- **Provisioning context is stashed in session metadata by Neo** (APS classifier
  prompt name, `created_by`, `base_url`, `workspace_dir`) because none of these are
  on `elite.Request` and `ExperimentContext.PromptName` holds the *resolved* prompt
  (`ambiguous_agent_v0`), not the classifier prompt. Keys live in
  `core/workflows/elite/handoff_ambiguous.go` (`MetaKey*`).
- **Neo pod-less branch** keyed on `promptResult.PromptName == AmbiguousAgentPromptName`
  (mirrors the brainstorm branch).
- **Anti-loop**: if APS#2 re-classifies as ambiguous, fall back to
  `apsSelector.ResolveAgent(GetDefaultPrompt())`.

Files: `core/workflows/elite/{handoff.go,handoff_ambiguous.go,flow.go,workflow.go,service.go}`,
`core/workflows/neo/{workflows.go,elite.go}`, `pkg/agentsdk/tools/{handoff.go,builtin/handoff.go,builtin/executor.go,builtin/tools.yaml}`,
`resources/aps.yaml`, `resources/agents/ambiguous_agents/ambiguous_agent_v0_gpt_5_4_mini.yaml`.

---

## Goal (one paragraph)

When the APS (Auto Prompt Selector) classifies a user's initial request as ambiguous, Neo spawns the **ambiguous Elite** (pod-less, GPT-5.4-mini). That Elite asks the user to disambiguate via `ask_human` (a multiple-choice question: "Web Based app" / "Mobile App" / "Landing Page"). Once the human answers, the LLM calls a terminal tool `handoff_to_agent({ platform })`. Cortex then re-runs APS with the original user message **plus** the chosen platform as added context, gets back the right build agent (e.g. `full_stack_app_builder_cloud_v8`), and **hands off** to a new Elite at `EA-handoff-{jobID}` running that build agent — same session, fresh prompt resolution.

This document is **the entire spec** needed to implement that from scratch on a fresh `main` checkout.

---

## Why this approach (vs prior attempt in PR #1361)

PR #1361 implemented the same user-facing behavior but **reinvented the handoff mechanism**:
- Ambiguous Elite triggered a **second Neo workflow** via a custom `ActivityTriggerNeoHandoff`.
- That second Neo spawned the build Elite child at the same `EA-{jobID}` ID as the first Elite, requiring `WORKFLOW_ID_REUSE_POLICY_TERMINATE_IF_RUNNING` to win a race against the still-closing first Elite.
- Required new plumbing: `NeoTrigger` DI adapter, `NeoRequest` passthrough field on `elite.Request`, `IsFromAmbiguousHandoff` flag, anti-loop guard, JSON-safe template substitution.

Cortex **already** has an `executeHandoff` primitive (`core/workflows/elite/handoff.go`) used by:
- `auto_compact` with `target_agent_id` (e.g., fork → infinite handoff on context overflow)
- `model_upgrade` (e.g., free → paid model upgrade)

Both call `w.executeHandoff(exec, req, setup, targetAgentID, flow)` → spawns a new Elite at `EA-handoff-{jobID}`, same session, `IsHandoff=true`, `IsInitRequest=true`, fire-and-forget (matches Neo's pattern). No second Neo. No workflow ID race. No new plumbing.

The new approach: **add a third flow `FlowAmbiguousHandoff` to the existing primitive.** The only genuinely new code is: (a) the tool schema change, (b) a new SQL query for "first user message", (c) a new activity that wraps APS + message-store lookup, and (d) the terminal-tool branch in `flow.go` that ties them together.

---

## Architecture

### High-level flow

```
1. User submits job  ──▶  Neo workflow starts at  neo-{jobID}
2. Neo runs APS #1   ──▶  classifies as "ambiguous_agent_v0"
3. Neo spawns ambiguous Elite (pod-less) at  EA-{jobID}
4. Ambiguous Elite runs:
     - LLM asks_human → user picks platform
     - LLM emits  handoff_to_agent({ platform: "Web Based app" })
5. Elite's terminal-tool branch:
     a. Dispatch  ActivityResolveAmbiguousHandoff
        - Activity loads first user message for session_id from DB
        - Activity calls APS #2 with task = first_user_msg + "\n(User selected platform: <platform>)"
        - Activity returns { target_agent_id, resolved_task }
     b. Call  w.executeHandoff(exec, req, setup, target_agent_id, FlowAmbiguousHandoff, resolved_task)
        - Starts build Elite at  EA-handoff-{jobID}
        - Same SessionID (continuity)
        - IsHandoff=true, IsInitRequest=true (re-resolves prompt)
        - Fire-and-forget
     c. Ambiguous Elite returns  iterationResult{ stopReason: StopReasonHandoff }
6. Build Elite runs the resolved build agent end-to-end. Done.
```

### Workflow ID layout

| Workflow | ID | Lifecycle |
|---|---|---|
| Neo | `neo-{jobID}` | Fire-and-forget. Exits after spawning ambiguous Elite. |
| Ambiguous Elite | `EA-{jobID}` | Lives until LLM emits `handoff_to_agent`, then exits with `StopReasonHandoff`. |
| Build Elite | `EA-handoff-{jobID}` | Spawned by `executeHandoff`. Runs the resolved build agent. |

**Single session ID** shared across all three Elite-phase rows — FE sees one continuous chat. The handoff workflow ID convention (`EA-handoff-{jobID}`) is already understood by `core/workflows/manager.go` and `core/workflows/elite/recovery.go`.

### What changes vs current main

- **NEW** SQL query, NEW activity, NEW flow constant, NEW tool schema (handoff_to_agent takes `{platform}` only).
- **EXTEND** existing `executeHandoff` signature with an optional `taskOverride` parameter (only used by `FlowAmbiguousHandoff`; other callers pass `""` for back-compat).
- **NEW** terminal-tool branch in `core/workflows/elite/flow.go` for `handoff_to_agent`.
- **NEW** ambiguous_agent_v0 YAML config + entry in `resources/agents/aps.yaml`.
- **NEW** ambiguous agent prompt + JSON-format APS prompts in the prompts repo.

---

## Files to create / modify

### cortex repo

| Path | Action | Purpose |
|---|---|---|
| `internal/pgsql/rawqueries/messages.sql` | edit | Add `GetFirstUserMessageBySessionID` query |
| `internal/pgsql/queries/messages.sql.go` | regenerate | `make sqlc` |
| `internal/pgsql/mocks/mock_querier.go` | regenerate | `mockgen -source=queries/querier.go ...` |
| `internal/pgsql/messages.go` | edit | Domain wrapper for new query |
| `core/workflows/elite/request.go` | edit | Add `FlowAmbiguousHandoff` constant + map entry |
| `core/workflows/elite/handoff.go` | edit | Extend `executeHandoff` signature with `taskOverride string` |
| `core/workflows/elite/activities.go` | edit | Register new `ActivityResolveAmbiguousHandoff` |
| `core/workflows/elite/handoff_ambiguous.go` | NEW | `handleAmbiguousHandoff` method + the new activity body |
| `core/workflows/elite/flow.go` | edit | Add terminal-tool branch for `handoff_to_agent` |
| `core/workflows/elite/setup.go` (or `service.go`) | edit | Inject `messageStore` + `apsSelector` for new activity |
| `pkg/agentsdk/tools/builtin/tools.yaml` | edit | New tool schema: `handoff_to_agent({ platform })` |
| `pkg/agentsdk/tools/handoff.go` | NEW | Constant `ToolNameHandoffToAgent` + (no parser needed if schema is just platform) |
| `pkg/agentsdk/tools/execute.go` | edit | Tool handler — passthrough; no business logic |
| `resources/agents/ambiguous_agents/ambiguous_agent_v0_gpt_5_4_mini.yaml` | NEW | Agent YAML — model=gpt-5.4-mini, tools=[ask_human, handoff_to_agent], no `context:` block |
| `resources/agents/aps.yaml` | edit | Add `ambiguous_agent_v0` → `ambiguous_agent_v0_gpt_5_4_mini` mapping |
| `pkg/agentsdk/configs/loader.go` (or `loader_test.go`) | edit | Add `ambiguous_agents/` to auto-compact exemption list |
| `cmd/server.go` or `cmd/deps.go` | edit | Wire `messageStore` + `Selector` into elite Workflow constructor |

### prompts repo (separate PR)

| Path | Action | Purpose |
|---|---|---|
| `prompts/auto_prompt_selector_paid.md` | NEW or update | JSON output format `{"agent": "...", "reason": "..."}` + ambiguous detection rules |
| `prompts/auto_prompt_selector_free.md` | NEW or update | Same for free tier |
| `prompts/ambiguous_agent_prompt_v0.md` | NEW | System prompt for ambiguous agent: ask_human MCQ → then `handoff_to_agent({platform})` |

---

## Step-by-step implementation

Each step is independently verifiable. Run `go build ./... && go test ./...` after each.

### Step 1 — Branch off main

```bash
cd cortex
git checkout main && git pull
git checkout -b aps-v3-handoff-tool
git submodule update --init --recursive   # for cassettes/
```

**Verify:** `git log -1 --oneline` matches `origin/main` HEAD.

---

### Step 2 — SQL: first user message by session

Add to `internal/pgsql/rawqueries/messages.sql`:

```sql
-- name: GetFirstUserMessageBySessionID :one
-- Returns the content_ref of the first user-role message in a session (ordered by created_at ASC).
-- Used by ambiguous handoff to retrieve the user's original task.
SELECT content_ref
FROM messages
WHERE session_id = $1 AND role = 'user'
ORDER BY created_at ASC
LIMIT 1;
```

Run:
```bash
cd internal/pgsql && sqlc generate
mockgen -source=queries/querier.go -destination=mocks/mock_querier.go -package=mocks
```

Add a domain wrapper in `internal/pgsql/messages.go`:
```go
func (s *Store) GetFirstUserMessage(ctx context.Context, sessionID string) (string, error) {
    ref, err := s.q.GetFirstUserMessageBySessionID(ctx, sessionID)
    if err != nil {
        if errors.Is(err, pgx.ErrNoRows) {
            return "", nil
        }
        return "", fmt.Errorf("get first user message: %w", err)
    }
    // content_ref may be BigTable key OR inline JSON (see CLAUDE.md storage modes).
    // For ambiguous handoff we want the user's original text; if it's a BigTable key,
    // fetch from BT. If inline JSON, parse and extract text block.
    return s.resolveContentToText(ctx, ref)
}
```

**Verify:** `go build ./...` clean. Unit test with both inline-JSON and BigTable-ref content.

> **Note on content storage:** Per `cortex/CLAUDE.md`, message content is in BigTable when `sessions_bigtable.enabled: true`, else inline JSON in `content_ref`. The helper must handle both. If `resolveContentToText` doesn't already exist on the store, model it after how `LoadThread` activity reads messages (`core/workflows/elite/activities.go` — search for `ActivityLoadThread`).

---

### Step 3 — Add `FlowAmbiguousHandoff` constant

Edit `core/workflows/elite/request.go`. Find the existing `Flow*Handoff` constants (around line 35) and add:

```go
const (
    FlowModelUpgradeHandoff = "model_upgrade_handoff"
    FlowAutoCompactHandoff  = "auto_compact_handoff"
    FlowAmbiguousHandoff    = "ambiguous_handoff"   // NEW: post-ambiguous-agent classification handoff to resolved build agent
    FlowSubagent            = "subagent"
)

var defaultInitialMessageFallback = map[string]string{
    FlowModelUpgradeHandoff: "",
    FlowAutoCompactHandoff:  "Please use ask_human tool and confirm your plan now.",
    FlowAmbiguousHandoff:    "",  // ambiguous handoff ALWAYS passes a non-empty taskOverride; this default is defensive only
    FlowSubagent:            "...", // existing value
}
```

**Verify:** unit test `TestDefaultInitialMessageFallback` covers the new key.

---

### Step 4 — Extend `executeHandoff` signature

Edit `core/workflows/elite/handoff.go`. Add an optional `taskOverride` parameter:

```go
func (w *Workflow) executeHandoff(
    exec WorkflowExecutor,
    req *Request,
    setup *SetupResult,
    targetAgentID string,
    flow string,
    taskOverride string,   // NEW: when non-empty, used as Task; else DefaultInitialMessageFallback(flow)
) (string, error) {
    log := exec.Logger()

    task := taskOverride
    if task == "" {
        task = DefaultInitialMessageFallback(flow)
    }

    handoffReq := Request{
        JobID:             req.JobID,
        UserID:            req.UserID,
        AgentID:           targetAgentID,
        AgentType:         req.AgentType,
        Task:              task,                                  // CHANGED
        SessionID:         req.SessionID,
        PromptVariables:   setup.State.GetPromptVariables(),
        EnvInfo:           setup.State.GetEnvInfo(),
        IsInitRequest:     true,
        IsHandoff:         true,
        ExperimentContext: req.ExperimentContext,
        Metadata:          req.Metadata,
        HasCustomMCP:      req.HasCustomMCP,
        Version:           req.Version,
        FeatureRequest:    setup.FeatureRequest,
    }
    // ... rest unchanged
}
```

Update the two existing callers in `core/workflows/elite/compact.go` (~line 635) and `core/workflows/elite/flow.go` (~line 835) to pass `""` as the new last arg.

**Verify:** existing `TestHandoffWorkflowID` and any handoff tests still pass.

---

### Step 5 — New activity `ActivityResolveAmbiguousHandoff`

Create `core/workflows/elite/handoff_ambiguous.go`:

```go
package elite

import (
    "context"
    "fmt"
    "strings"

    "cortex/core/aps"
    "cortex/pkg/agentsdk/tools"
)

const ActivityResolveAmbiguousHandoff = "elite.ResolveAmbiguousHandoff"

type ResolveAmbiguousHandoffRequest struct {
    JobID             string
    SessionID         string
    UserID            string
    ModelName         string
    Platform          string
    ExperimentContext aps.ExperimentContext
}

type ResolveAmbiguousHandoffResult struct {
    TargetAgentID string
    ResolvedTask  string  // first_user_msg + "\n(User selected platform: <platform>)"
}

// Activity body. Runs in a Temporal activity context (has access to real ctx, can do DB I/O).
func (w *Workflow) activityResolveAmbiguousHandoff(ctx context.Context, req ResolveAmbiguousHandoffRequest) (*ResolveAmbiguousHandoffResult, error) {
    firstMsg, err := w.messageStore.GetFirstUserMessage(ctx, req.SessionID)
    if err != nil {
        return nil, fmt.Errorf("load first user message: %w", err)
    }
    if firstMsg == "" {
        return nil, fmt.Errorf("no user message found in session %s", req.SessionID)
    }

    task := firstMsg
    if req.Platform != "" {
        task = fmt.Sprintf("%s\n\n(User selected platform: %s)", strings.TrimSpace(firstMsg), req.Platform)
    }

    // Pick APS prompt by tier (paid/free) — read from experiment context or default to paid.
    apsPromptName := selectAPSPromptName(req.ExperimentContext)

    apsResult, err := w.apsSelector.SelectAndResolve(ctx, aps.SelectAndResolveInput{
        Task:              task,
        UserID:            req.UserID,
        JobID:             req.JobID,
        ModelName:         req.ModelName,
        APSPromptName:     apsPromptName,
        ExperimentContext: req.ExperimentContext,
    })
    if err != nil {
        return nil, fmt.Errorf("aps re-classify: %w", err)
    }

    // Anti-loop: if APS classifies as ambiguous AGAIN (rare), fall back to default agent.
    if apsResult.AgentID == ambiguousAgentID {
        log := activity.GetLogger(ctx)
        log.Warn("APS re-classified as ambiguous; falling back to default agent",
            "session_id", req.SessionID, "platform", req.Platform)
        apsResult.AgentID = apsResult.DefaultAgentID  // available on SelectResult — verify field name
    }

    return &ResolveAmbiguousHandoffResult{
        TargetAgentID: apsResult.AgentID,
        ResolvedTask:  task,
    }, nil
}
```

Register the activity in `core/workflows/elite/activities.go` (find the existing `RegisterActivityWithOptions` block and add):

```go
wr.RegisterActivityWithOptions(w.activityResolveAmbiguousHandoff, activity.RegisterOptions{
    Name: ActivityResolveAmbiguousHandoff,
})
```

**Inject `messageStore` + `apsSelector` into the Workflow struct** if they aren't already there:
- Add fields to `Workflow` struct in `core/workflows/elite/workflow.go`.
- Add constructor parameters in `NewWorkflow(...)`.
- Wire in `cmd/server.go` (or wherever the elite Workflow is constructed) — pass the existing `messageStore` (already used by `LoadThread`) and the `aps.Selector` (constructed in cmd/server for Neo's use).

> If the APS Selector isn't accessible at the elite construction site without an import cycle, define a small `apsSelector` interface in `core/workflows/elite/interfaces.go`:
> ```go
> type apsSelector interface {
>     SelectAndResolve(ctx context.Context, input aps.SelectAndResolveInput) (*aps.SelectResult, error)
> }
> ```
> The concrete `*aps.Selector` satisfies it structurally.

**Verify:** unit test with mock `messageStore` + mock `apsSelector` returning a deterministic agent ID.

---

### Step 6 — Tool schema change in `tools.yaml`

Edit `pkg/agentsdk/tools/builtin/tools.yaml`. Replace the existing handoff_to_agent block (if it exists from a prior branch) with:

```yaml
  - name: handoff_to_agent
    builtin_type: handoff_to_agent
    definition:
      name: handoff_to_agent
      description: |
        Terminal tool used ONLY by the ambiguous_agent_v0. Call exactly ONCE after
        the user answers your ask_human MCQ. This is your FINAL action — do NOT
        emit any text after this tool call. The build agent is selected from the
        chosen platform automatically; this call ends the current turn and the
        appropriate build environment is provisioned on the same job.
      input_schema:
        type: object
        properties:
          platform:
            type: string
            enum: ["Web Based app", "Mobile App", "Landing Page"]
            description: The user's chosen platform mapped from their ask_human answer.
        required:
          - platform
```

Create `pkg/agentsdk/tools/handoff.go`:

```go
package tools

const ToolNameHandoffToAgent = "handoff_to_agent"
```

Edit `pkg/agentsdk/tools/execute.go` — add `"handoff_to_agent"` to the dispatch switch as a passthrough (it doesn't execute logic; the Elite workflow inspects the tool call from the LLM result):

```go
case ToolNameHandoffToAgent:
    // Marker tool — actual handoff dispatch happens in Elite's terminal-tool branch.
    // Just return a successful tool_result so the LLM iteration completes cleanly.
    return ToolResult{Content: "handoff initiated"}, nil
```

**Verify:** `go test ./pkg/agentsdk/...` passes; tool registers in the agent SDK without schema errors.

---

### Step 7 — Terminal-tool branch in `flow.go`

Edit `core/workflows/elite/flow.go`. Find the post-tool-execution block (search for `TerminalToolName` — there's an existing switch around line 758). Add a branch:

```go
if toolExecResult.TerminalToolName == tools.ToolNameHandoffToAgent {
    if result, fired := w.handleAmbiguousHandoff(exec, req, setup, llmResult); fired {
        return result
    }
    // If handoff failed to fire, fall through to end_turn so the iteration completes.
}
```

Add `handleAmbiguousHandoff` to `handoff_ambiguous.go`:

```go
func (w *Workflow) handleAmbiguousHandoff(
    exec WorkflowExecutor,
    req *Request,
    setup *SetupResult,
    llmResult LLMCallResult,
) (iterationResult, bool) {
    log := exec.Logger()

    platform := extractPlatformFromToolCalls(llmResult)
    if platform == "" {
        log.Error("handoff_to_agent: missing platform in tool args; falling through",
            "job_id", req.JobID)
        return iterationResult{}, false
    }

    var resolved ResolveAmbiguousHandoffResult
    err := exec.ExecuteActivity(ActivityResolveAmbiguousHandoff, ResolveAmbiguousHandoffRequest{
        JobID:             req.JobID,
        SessionID:         req.SessionID,
        UserID:            req.UserID,
        ModelName:         req.ModelName,
        Platform:          platform,
        ExperimentContext: req.ExperimentContext,
    }).Get(&resolved)
    if err != nil {
        log.Error("handoff_to_agent: APS re-classify failed", "error", err)
        return buildErrorResultWithErr(err), true
    }

    wfID, err := w.executeHandoff(exec, req, setup, resolved.TargetAgentID, FlowAmbiguousHandoff, resolved.ResolvedTask)
    if err != nil {
        log.Error("handoff_to_agent: failed to spawn build Elite", "error", err)
        return buildErrorResultWithErr(err), true
    }

    log.Info("handoff_to_agent: scheduled build Elite",
        "target_agent", resolved.TargetAgentID, "workflow_id", wfID, "platform", platform)

    return iterationResult{
        stopReason:     StopReasonHandoff,
        shouldContinue: false,
        handoff:        &HandoffInfo{AgentID: resolved.TargetAgentID, WorkflowID: wfID},
    }, true
}

func extractPlatformFromToolCalls(llmResult LLMCallResult) string {
    if llmResult.Outcome == nil {
        return ""
    }
    for _, tc := range llmResult.Outcome.ToolCalls {
        if tc.Name != tools.ToolNameHandoffToAgent {
            continue
        }
        var args map[string]any
        if err := json.Unmarshal([]byte(tc.Arguments), &args); err != nil {
            continue
        }
        if p, ok := args["platform"].(string); ok {
            return p
        }
    }
    return ""
}
```

**Verify:** `go test ./core/workflows/elite/...` passes including new branch coverage.

---

### Step 8 — Ambiguous agent YAML

Create `resources/agents/ambiguous_agents/ambiguous_agent_v0_gpt_5_4_mini.yaml`:

```yaml
name: ambiguous_agent_v0_gpt_5_4_mini
spec:
  model:
    id: gpt-5.4-mini
    provider: openai
    params:
      temperature: 0.1
      max_tokens: 4096
  prompts:
    - name: ambiguous_agent_prompt_v0
      type: system
  tools:
    - name: ask_human
    - name: handoff_to_agent
  policy:
    max_iterations: 5
    timeout: 5m
  # NO context block — this is a pod-less, short-lived agent.
  # NO auto_compact — single-turn clarification, never needs compacting.
```

Edit `resources/agents/aps.yaml` to add the mapping:
```yaml
ambiguous_agent_v0: ambiguous_agent_v0_gpt_5_4_mini
```

Edit `pkg/agentsdk/configs/loader.go` (or the test that enforces auto-compact requirement) to exempt the `ambiguous_agents/` directory from `agentYAMLRequiresPromptLevelAutoCompact`:

```go
func agentYAMLRequiresPromptLevelAutoCompact(path string) bool {
    if strings.Contains(path, "/ambiguous_agents/") {
        return false
    }
    // ... existing exemptions
}
```

**Verify:** `go test ./pkg/agentsdk/configs/...` passes — the YAML loads without requiring `auto_compact`.

---

### Step 9 — Skip pod provisioning in Neo when agent is ambiguous

Neo currently calls `CreateEnvironment` after APS resolves the agent. For pod-less agents (ambiguous, brainstorm), skip pod creation.

Edit `core/workflows/neo/workflows.go` — find the call after APS resolves the agent. Add a guard:

```go
if isPodlessAgent(promptResult.AgentID) {
    log.Info("skipping pod provisioning for pod-less agent", "agent_id", promptResult.AgentID)
} else {
    // existing CreateEnvironment call
}

func isPodlessAgent(agentID string) bool {
    return strings.HasPrefix(agentID, "ambiguous_agent_") ||
           strings.HasPrefix(agentID, "brainstorm_") ||
           strings.HasPrefix(agentID, "general_agent_")
}
```

> Verify this list against what's already pod-less in current main — `brainstorm_v0` may already have a code path skipping pod creation. Reuse it if present.

**Verify:** unit test for the routing rule + manual e2e check that ambiguous job doesn't provision a pod.

---

### Step 10 — Prompts (separate PR in prompts repo)

Three prompt files needed:

#### a) `auto_prompt_selector_paid.md`

JSON output format. Structure:
```
You are a classifier that picks the right build agent for a user request.

Allowed agents:
- replica_agent_v0: clone an existing website
- landing_page_v0: build a one-page landing page
- full_stack_app_builder_nextjs: Next.js full-stack web app
- full_stack_app_builder_cloud_v8: cloud-hosted full-stack web app (DEFAULT for ambiguous web requests)
- expo_fullstack_v0: React Native mobile app via Expo
- ambiguous_agent_v0: user request is ambiguous about platform (web vs mobile vs landing); ask for clarification
- brainstorm_v0: user wants to discuss ideas, not build yet
- general_agent_v0: other / unclear intent

Rules:
- If the request mentions "mobile app" / "iOS" / "Android" / "Expo" → expo_fullstack_v0
- If the request is "make me a landing page for X" → landing_page_v0
- If the request is "clone <url>" / "make a copy of <site>" → replica_agent_v0
- If the request is a vague "build me an app" with no platform hint → ambiguous_agent_v0
- Default for unambiguous web app requests → full_stack_app_builder_cloud_v8

Task: {task_description}

Respond ONLY with JSON: {"agent": "<agent_name>", "reason": "<one sentence>"}
```

Template variables: `{task_description}` (substituted by `getAutoAgentConfig` in `core/aps/llm.go`).

Configuration kwargs:
```
model: gpt-5.4-mini  (or whatever current paid APS uses)
default_agent: full_stack_app_builder_cloud_v8
default_env: fastapi_react_mongo_shadcn_base_image
allowed_agents: [replica_agent_v0, landing_page_v0, full_stack_app_builder_nextjs, full_stack_app_builder_cloud_v8, expo_fullstack_v0, ambiguous_agent_v0, brainstorm_v0, general_agent_v0]
```

#### b) `auto_prompt_selector_free.md`

Same structure but for free-tier users. Allowed agents typically a subset.

#### c) `ambiguous_agent_prompt_v0.md`

```
You are the ambiguous-request clarifier. The user submitted a vague build request and we need to figure out what platform they want.

Your job: ONE turn.
1. Call ask_human with a multiple-choice question listing exactly these options:
   - "Web Based app"
   - "Mobile App"
   - "Landing Page"
2. When the user picks one, immediately call handoff_to_agent with their chosen platform.
3. Do NOT emit any text after handoff_to_agent. That tool call ends your turn.

The user's original request was:
{user_prompt}

Default suggestion if user is unsure: "Web Based app".
```

> Note: `{user_prompt}` here is substituted at prompt-fetch time by APS's `getAutoAgentConfig` — same pattern as `{task_description}` in the APS prompts. The cortex code passes the original Neo `req.Task` as the substitution value.

**Verify:** prompt renders without missing variables when fetched via LangSmith.

---

### Step 11 — Tests

#### Unit
- `TestExtractPlatformFromToolCalls` — covers valid args, missing platform, malformed JSON
- `TestHandleAmbiguousHandoff_Success` — mocks activity returning a target agent, asserts executeHandoff called with right args
- `TestHandleAmbiguousHandoff_APSFailure` — activity returns error → returns error iterationResult
- `TestHandleAmbiguousHandoff_LoopGuard` — APS returns ambiguous again → fallback to default agent
- `TestActivityResolveAmbiguousHandoff` — mocks messageStore + apsSelector
- `TestGetFirstUserMessageBySessionID` — both inline-JSON and BigTable-ref content
- `TestExecuteHandoff_WithTaskOverride` — new optional param
- `TestDefaultInitialMessageFallback_AmbiguousFlow` — returns empty string

#### Integration
- Modify `core/workflows/elite/recovery_test.go` to also recognize `EA-handoff-{jobID}` as a valid post-ambiguous handoff target (it already does for auto_compact).
- E2E harness recording of a full ambiguous flow if VCR cassettes are practical.

```bash
make check
go test ./...
go test -tags=integration ./core/workflows/elite/... -timeout 10m
```

---

### Step 12 — Eph deploy + manual smoke

1. Push branch, deploy to a fresh eph (e.g., `aps-v3`).
2. Seed `cortex_aps-v3` DB with the three new prompts (`auto_prompt_selector_paid`, `auto_prompt_selector_free`, `ambiguous_agent_prompt_v0`) via the `transfer-prod-job` / `debug-job` skill or direct `psql` upsert into the `prompts` table (schema: `prompt_name TEXT PK, file_name TEXT, content TEXT, variables JSONB, kwargs JSONB, version TEXT`).
3. Set `auto_prompt_selector` row content = paid prompt v3 (so default tier picks paid).
4. Submit an ambiguous job via the eph API:
   ```bash
   curl -X POST https://api.aps-v3.emergent.test/jobs/v0/submit-queue/ \
     -H "Authorization: Bearer $TOKEN" \
     -d '{ "id":"smoke-1", "payload": { "task": "build me an app" } }'
   ```
5. Verify in Temporal UI:
   - One Neo workflow at `neo-smoke-1`
   - One ambiguous Elite at `EA-smoke-1`
   - After human picks "Web Based app", one build Elite at `EA-handoff-smoke-1`
   - All three share one session_id in `cortex.sessions`
6. Verify in emergent FE: single continuous chat (user message → ambiguous's MCQ → user's pick → build agent's response).

---

## Open architectural decisions (locked in)

| # | Decision | Rationale |
|---|---|---|
| 1 | APS#2 runs in an activity (`ActivityResolveAmbiguousHandoff`), not inside the tool handler. | Keeps `pkg/agentsdk/tools/` decoupled from `core/aps`. Tool stays a thin marker; activity owns the dispatch. |
| 2 | Tool schema is `{ platform }` only — no `user_prompt` field. Original user task is fetched from messages DB. | LLM doesn't need to echo back the user's message; reading from DB is authoritative and avoids prompt-template substitution complexity. |
| 3 | Build Elite spawns at `EA-handoff-{jobID}` (existing `HandoffWorkflowID` convention), NOT `EA-{jobID}`. | Reuses the existing handoff primitive used by auto_compact + model_upgrade. No workflow ID collision. No `TERMINATE_IF_RUNNING` race-fix needed. |
| 4 | Same `session_id` across ambiguous and build Elites. | Single continuous chat in FE. Matches how auto_compact handoff preserves session. |
| 5 | Anti-loop guard: if APS#2 returns `ambiguous_agent_v0` again, fall back to `default_agent` from APS config + log warn. | Defensive. Should never fire in practice since platform info should disambiguate. |
| 6 | `executeHandoff` gets an optional `taskOverride string` param; existing callers pass `""`. | Minimal-blast-radius change to an existing primitive. Single-line addition for each existing caller. |
| 7 | First-user-message lookup is a new SQL query, not in-memory filter. | O(1) DB hit, predictable, no full-thread load. |
| 8 | Ambiguous agent YAML has no `context:` block (no auto_compact). | Single-turn agent, never compacts. Loader test exempts the directory. |
| 9 | Neo skips pod provisioning when APS resolves to a pod-less agent (ambiguous, brainstorm, general). | Ambiguous Elite needs no pod. Build Elite (post-handoff) handles its own env via `executeHandoff`'s env-setup path. |
| 10 | APS extractor parses BOTH JSON `{"agent","reason"}` (new v3 prompts) AND XML `<agent>/<reason>` (legacy). | Already on main if PR for APS JSON support landed; otherwise add per the existing `extractAgentAndReason` pattern. |

---

## Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| `executeHandoff`'s build Elite needs a pod, but ambiguous Elite is pod-less (no env exists yet) | Medium | The build Elite's setup path calls `CreateEnvironment` itself (verify: read `setup.go` for IsHandoff branch). If env creation is gated on `IsHandoff=false`, add an `IsHandoff && needsEnv(agent)` branch that provisions on first iteration. |
| First user message returned is empty/junk (e.g., FE sent a tool_use first) | Low | Activity returns error, `handleAmbiguousHandoff` returns error iterationResult, job fails with clear log. Acceptable: this is a malformed-input case. |
| APS#2 takes >5s and ambiguous Elite hits iteration timeout | Low | Ambiguous YAML has `timeout: 5m`. APS is normally ~2s. Plenty of headroom. |
| `prompts` repo PR not deployed before cortex PR → cortex calls APS with prompt that returns XML, but new code expects JSON | Medium | Deploy prompts PR first. Or: keep XML fallback parser (already exists in `extractAgentAndReason`). |
| FE doesn't render the second Elite's messages because workflow ID changed | Low | FE subscribes by session_id, not workflow_id. Verify in `E1ectron` job-detail page. |

---

## Done criteria

- [ ] All 12 steps complete; all unit + integration tests pass.
- [ ] `make check` clean (gofmt + goimports + lint).
- [ ] Eph smoke test: ambiguous job runs end-to-end, build Elite is the right resolved agent, single session row, one continuous chat in FE.
- [ ] PR opened against `main` with this doc linked in the description.
- [ ] Prompts repo PR merged and deployed to eph DB before cortex PR merges to main.

---

## References

- Existing handoff primitive: `core/workflows/elite/handoff.go` (used by auto_compact + model_upgrade)
- Existing handoff caller (auto_compact): `core/workflows/elite/compact.go:615-650`
- Existing handoff caller (model_upgrade): `core/workflows/elite/flow.go:820-840`
- APS Selector: `core/aps/resolver.go` (`SelectAndResolve`) + `core/aps/llm.go` (`selectWithLLM`)
- Neo entry: `core/workflows/neo/workflows.go` (APS#1 + Elite child spawn)
- Workflow ID conventions: `core/workflows/workflows.go` (`EliteWorkflowID`, `HandoffWorkflowID`)
- Message storage modes: `cortex/CLAUDE.md` → "Storage Modes" section
- Activity naming + DI patterns: `cortex/CLAUDE.md` → "Architecture Principles"
- Versioning policy (no GetVersion guards): `cortex/CLAUDE.md` → "Workflow Versioning Policy"
- Prior attempt: PR #1361 (closed)
