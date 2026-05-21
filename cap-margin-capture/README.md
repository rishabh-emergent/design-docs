# CAP Margin Capture via Billing Decoupling

| Doc | Covers | PR |
|---|---|---|
| [design.html](./design.html) | End-to-end design — y/z/x vocabulary, strict attribution rule, BigTable storage model, `cap.Service` architecture, failure modes, Prometheus + Loki reporting | cortex#1411 (merged) |

## What this is

When CAP (Cache Anchor Point) keeps an Anthropic prompt cache alive past its natural 5-minute TTL, the user makes an LLM call that we now serve at cache-read prices (cheap) instead of cache-creation prices (expensive). The PRD says we should keep the user's bill identical to a no-CAP world — bill them at the as-if-cold-cache cost `z`, pay Anthropic the actually-lower `y`, absorb the ping cost `x` as overhead. Margin per decoupled call = `z − y − x`.

## Code locations (cortex-only)

- **Domain**: `core/cap/` — `Service`, `Attribution`, `PingRecord`, pricing math, metrics
- **Workflow**: `core/workflows/cap/workflow.go` — CAP refresh ping activity that persists to BigTable
- **Elite integration**: `core/workflows/elite/` — `setup.go` (CapSetup bundle), `flow.go` (V2 reconcile, IterationContext), `activities.go` (activityPostHook)
- **Storage**: `internal/pgsql/cap_pings.go` — composite `CapStore` (PG for prev-msg + head usage, BT for ping rows in the `ping_data` column family on `cortex-sessions`, 7-day TTL)
- **Wiring**: `cmd/deps.go` — separate `CAP_BIGTABLE_*` env vars provision the ping-data BigTable client

## Status

| Change | PR | State |
|---|---|---|
| CAP Margin Capture v2 (the feature) | [cortex#1411](https://github.com/emergentbase/cortex/pull/1411) | Merged |
| Attribution metrics (`cap.attribution.*` OTel) | [cortex#1465](https://github.com/emergentbase/cortex/pull/1465) | Open, stacked on v2 |

**Enablement is Unleash-driven** (`cap_*` flag prefix); provider clamp restricts to Anthropic. The earlier `elite.force_cap_enabled` override has been removed — Unleash is the single source of truth.

## What does NOT change

- No emergent-side schema change. The audit blob initially planned for `trajectories.traj_payload.cap` was dropped in favour of cortex-local telemetry (Loki + Prometheus).
- No change to the cortex→emergent PostHook contract beyond the swapped `cost_usd` / `accumulated_cost` values.
- No new Temporal activities. Attribution lives in pure functions on `cap.Service`, invoked from existing `activityPostHook`.
