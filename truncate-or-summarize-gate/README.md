# Truncate-or-Summarize Gate at the Context Window Boundary

| Doc | Covers | PR |
|---|---|---|
| [design.html](./design.html) | End-to-end design — token bands, measured (not estimated) effectiveness, dry runs, data flow, file-by-file code changes, failure modes, reporting. | [cortex#1594](https://github.com/emergentbase/cortex/pull/1594) |
| [CONTEXT.md](./CONTEXT.md) | Domain glossary (operating window, W_high/W_low, effective truncation, the two arms). | — |
| [adr/0001-truncate-or-summarize-gate.md](./adr/0001-truncate-or-summarize-gate.md) | The recorded decision + non-obvious trade-offs (gating, forced summarize, no pre-computation, estimate-space math, per-iteration re-decision). | — |

## What this is

Above the top of the operating window (`W_high` = the existing `range_threshold.upper`, 0.325 ≈ 325K on a 1M window), cortex today fires its hard-floor truncation every single step. When the surviving context is itself already above `W_high`, those truncations reclaim almost nothing but still re-process the full prompt — wasted work that just delays the summarization actually needed.

This adds a **truncation-gain optimization**: on every finish where context exceeds `W_high`, it runs the pending truncation *for real* (pure `xllm.ApplySquash`), measures what it removes, and chooses — **truncate** if effective (removes ≥ `gain_threshold` of context **and** lands back ≤ `W_high`), otherwise **summarize immediately**. The trade-off: summarization (a synchronous LLM call) can now fire earlier and is not pre-computed, in exchange for eliminating the futile-truncation churn.

## Code locations (cortex-only)

- **Schema**: `pkg/agentsdk/context.go` — one new field `RangeThresholdConfig.GainThreshold` (presence > 0 is the enable signal).
- **Decision**: `core/xcontext/truncation_gain.go` (NEW) — pure `DecideGainAction`; `core/xcontext/tiered.go` carries `GainThreshold` onto the resolved policy.
- **Wiring**: `core/workflows/elite/setup.go` — copies the field onto `SquashRangeThresholdPolicy`; `IsTruncationGainOptimizationActive()` helper.
- **Loop dispatch**: `core/workflows/elite/flow.go` — calls the gate, dispatches to existing truncate/summarize paths; force-truncate signal honors the gate's decision regardless of the input-only predicate; skips speculative summary pre-computation when active.
- **Forced summarize**: `core/workflows/elite/compact.go` — `maybeApplyAutoCompact` gains a `force bool` that bypasses only its 0.35 `NeedsCompact` check (still respects `HasEnoughMessages`).
- **State**: no new state. The gate is a pure function of the current iteration's inputs.
- **Persistence**: `internal/pgsql/agents.go` — new field rides the existing `range_threshold` jsonb round-trip.

**No new Temporal activity. No emergent-side or wire-contract change.**

## Status

| Change | PR | State |
|---|---|---|
| Truncate-or-summarize gate (this design) | [cortex#1594](https://github.com/emergentbase/cortex/pull/1594) | Review |

## What does NOT change

- **At or below `W_high`** behaviour is byte-for-byte unchanged — the cache-aware range gate inside `[W_low, W_high)` and the legacy threshold for non-opted agents are untouched.
- No change to *how* truncation or summarization is performed internally — the gate only arbitrates *which one* fires above `W_high`.
- No change for any job without `range_threshold` + `gain_threshold` (ships dark; rollout is one experiment field).
- `auto_compact.threshold` (0.35) is left in place purely as a backstop; it never triggers truncation, so it cannot conflict with the hard floor.
- No new storage and no new in-memory state. The gate is purely derived from the iteration's current inputs.

## Open items (to validate in prod)

- Initial values `gain_threshold=0.10`, `W_high=0.325`, `W_low=0.14` are starting points; tune from the `action` split (§12).
- Synchronous summarization latency accepted for now; revisit pre-computation if the SUMMARIZE rate near the boundary is high.
