# CAP Margin Capture via Billing Decoupling

| Doc | Covers | PR |
|---|---|---|
| [design.html](./design.html) | End-to-end design — y/z/x vocabulary, strict attribution rule, BigTable storage model, `cap.Service` architecture, failure modes, Prometheus + Loki reporting | cortex#1411 (merged) |

## What this is

When CAP (Cache Anchor Point) keeps an Anthropic prompt cache alive past its natural 5-minute TTL, the user makes an LLM call that we now serve at cache-read prices (cheap) instead of cache-creation prices (expensive). The PRD says we should keep the user's bill identical to a no-CAP world — bill them at the as-if-cold-cache cost `z`, pay Anthropic the actually-lower `y`, absorb the ping cost `x` as overhead. Margin per decoupled call = `z − y − x`.

## Code locations (cortex-only)

- **Domain**: `core/cap/` — `Service`, `Attribution`, `PingRecord`, pricing math, metrics, `global_cache.go` (hardcoded fallback)
- **Workflow**: `core/workflows/cap/workflow.go` — CAP refresh ping activity that persists to BigTable + writes to Redis runtime meta
- **Elite integration**: `core/workflows/elite/` — `setup.go` (CapSetup bundle), `flow.go` (V2 reconcile, IterationContext), `activities.go` (activityPostHook), `request.go` (RecordCacheBaseline trigger)
- **Storage**: `internal/pgsql/cap_pings.go` — BigTable client for ping rows in the `ping_data` column family on `cortex-sessions`, 7-day TTL
- **Runtime meta**: `internal/redis/runtimemeta/store.go` — Redis-backed implementation of `sessions.RuntimeMetaStore` (PR #1483 — replaces the two hot Postgres queries with a single `HMGET`)
- **Wiring**: `cmd/deps.go` — separate `CAP_BIGTABLE_*` env vars provision the ping-data BigTable client; `REDIS_ADDR` provisions the runtime-meta store

## Status

| Change | PR | State |
|---|---|---|
| CAP Margin Capture v2 (the feature) | [cortex#1411](https://github.com/emergentbase/cortex/pull/1411) | Merged |
| Attribution metrics (`cap.attribution.*` OTel) | [cortex#1465](https://github.com/emergentbase/cortex/pull/1465) | Merged |
| Runtime meta → Redis (kill Postgres CPU saturation) | [cortex#1483](https://github.com/emergentbase/cortex/pull/1483) | Merged |
| Hardcoded global-cache fallback (26000 tokens) | [cortex#1485](https://github.com/emergentbase/cortex/pull/1485) | Merged |
| CAP ping caching-policy fix (post-1411 regression) | [cortex#1487](https://github.com/emergentbase/cortex/pull/1487) | Merged |

**Enablement is Unleash-driven** (`cap_*` flag prefix); provider clamp restricts to Anthropic. The earlier `elite.force_cap_enabled` override has been removed — Unleash is the single source of truth.

## What does NOT change

- No emergent-side schema change. The audit blob initially planned for `trajectories.traj_payload.cap` was dropped in favour of cortex-local telemetry (Loki + Prometheus).
- No change to the cortex→emergent PostHook contract beyond the swapped `cost_usd` / `accumulated_cost` values.
- No new Temporal activities. Attribution lives in pure functions on `cap.Service`, invoked from existing `activityPostHook`.

## Post-launch updates (timeline)

| Date | PR | What shifted |
|---|---|---|
| 2026-05-21 | [cortex#1411](https://github.com/emergentbase/cortex/pull/1411) | v2 shipped with two Postgres reads on every workflow setup (`GetPreviousAssistantMessageTime`, `GetHeadMessageCacheReadTokens`). Cortex-db CPU saturated at 70–90% within hours. Hot-fix [cortex#1482](https://github.com/emergentbase/cortex/pull/1482) commented out the call site; CAP attribution went dark. |
| 2026-05-23 | [cortex#1483](https://github.com/emergentbase/cortex/pull/1483) | Both hot reads moved to a Redis hash `session:{sessionID}:meta`. One `HMGET` per workflow setup. `system_prompt_cache_read_tokens` written only on system-prompt context boundaries (init / handoff). CAP attribution re-enabled. **Design section 11 below covers this in full.** |
| 2026-05-23 | [cortex#1485](https://github.com/emergentbase/cortex/pull/1485) | When the Redis baseline is missing/zero (existing pre-Redis sessions, write miss), `EffectiveGlobalCacheBaseline` returns a hardcoded fallback of `26000` tokens (picked from observed prod values 21k–28k). Existing sessions decouple instead of degrading to bill-at-`y`. |
| 2026-05-24 | [cortex#1487](https://github.com/emergentbase/cortex/pull/1487) | PR #1411 also dropped the explicit `OptionCaching` line in `cap/workflow.go`. That regressed cache_control breakpoints + `body.thinking` placement on Opus-4-7 adaptive-thinking pings, producing a 2% 500-error cascade. Restored. Unrelated to billing math. |
