# In-Loop CAP Margin Capture

Extension of [cap-margin-capture](../cap-margin-capture/) to claim margin on the LLM call following a long-running tool execution. CAP keeps the cache alive while the tool runs (in-loop pings, already shipped); this doc covers the **attribution layer** that makes that margin bookable.

| Doc | Covers | PR |
|---|---|---|
| [design.html](./design.html) | End-to-end design — what's already shipped vs the two attribution gaps, the unified per-iter window, race-condition analysis, code changes, failure modes | [cortex#1548](https://github.com/emergentbase/cortex/pull/1548) |
| [adr/0001-state-shape-for-in-loop-pings.md](./adr/0001-state-shape-for-in-loop-pings.md) | Why `state.inLoopPings` slice (Shape B) instead of mutating `setup.Cap.Pings` (Shape A) | — |
| [in-loop-cap-qa-test-cases.xlsx](./in-loop-cap-qa-test-cases.xlsx) | Manual-QA test scenarios (15 cases, P0–P2), Cloud Run / Loki / BigTable / Postgres queries cheat sheet, log-field glossary | [cortex#1548](https://github.com/emergentbase/cortex/pull/1548) |

## What this is

When the agent fires a long-running tool (sandbox build, deploy, test suite), the LLM side goes idle for minutes. If the tool runs past Anthropic's 5-minute cache TTL, the next LLM call pays cache-write again — an avoidable cost that today flows straight through to the user. CAP already mitigates this on the cache side via in-loop refresh pings (`core/workflows/elite/cap.go:capRefreshLoop`), but the margin attribution path was scoped to post-exit pings only (terminal-state CAP). Iter 2+ of any elite workflow hits a hard `IsFirstIteration` gate and bills `y` regardless of in-loop activity.

This change unifies the two paths: drop the iter-1 gate, advance the eligibility window per-iter, and merge in-flight `in_loop` pings into the attribution input. Same `z − y − x` math, same Unleash experiment, no new flag, no schema change. **5 file changes, +20 / −10 lines net.**

## Code locations (cortex-only)

- **Firing (already shipped, unchanged)**: `core/workflows/elite/cap.go:capRefreshLoop` + `refreshCacheAnchorIfNeeded`. Gated on `CapConfig.ShouldRefreshLongRunning(elapsed, cacheTokens, refreshCount)` (config in `core/cap/config.go`).
- **Attribution math (unchanged)**: `core/cap/attribution.go:DecideEligibility` + `BuildAttribution` — same `z − y − x` machinery as terminal-state.
- **State (new)**: `core/workflows/elite/state.go` — adds `lastAssistantMsgAt` field + `inLoopPings` slice with getters/setters.
- **Wiring**: `core/workflows/elite/flow.go` — read-advance-merge at every PostHook build site.
- **Result shape**: `core/cap/refresh.go` — adds `FiredAt time.Time` to `RefreshResult` so the workflow can construct a `PingRecord` deterministically after the activity returns.

## What does NOT change

- No new Temporal activity. Refresh and PostHook activities exist already.
- No new Unleash flag. Reuses `cap_enable_refresh`; an additional patch in the same experiment toggles `LongRunningMaxRefreshes > 0` to enable in-loop firing.
- No emergent-side schema or PostHook contract change. Only `cost_usd` / `accumulated_cost` shift on decoupled iters — same as terminal-state.
- No new metrics. The existing `cap_attribution_total{reason, ping_source}` histogram already carries the source label from `PingRecord.Source` — in-loop attributions surface as `ping_source="in_loop"` rows on the same Grafana panels.
- No change to BigTable read path. `LoadCapPings` keeps its post-exit filter — only setup-time loads need it; in-flight in_loop pings are merged from in-memory state, not re-read from BT.

## Status

| Change | PR | State |
|---|---|---|
| In-loop attribution (this design) | [cortex#1548](https://github.com/emergentbase/cortex/pull/1548) | Open |

## Post-launch updates (timeline)

| Date | PR | What shifted |
|---|---|---|
| — | — | — |
