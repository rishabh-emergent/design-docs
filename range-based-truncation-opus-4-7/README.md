# Range-Based Truncation for Opus 4.7 (Tier 1)

| Doc | Covers | PR |
|---|---|---|
| [design.html](./design.html) | End-to-end design — token bands, cache-TTL prediction, decision flow, architecture, code changes, backward compatibility, failure modes, metrics, open risks. **Truncation only.** | [cortex#1474](https://github.com/emergentbase/cortex/pull/1474) |

## What this is

Today, Opus 4.7 farm agents squash at exactly 275k tokens via the legacy `context.threshold` gate. Anthropic's prompt cache has a 5-minute TTL — if it expires near the 275k mark, we pay `cache_creation` once on the post-expiry call and again a few calls later when the squash fires. This design adds a **cache-TTL-aware range gate** that pre-emptively truncates when the cache is predicted to be invalid inside a configurable range below the legacy threshold, so we absorb only one `cache_creation` charge.

## Scope

**Truncation (Tier 1) only.** Summarisation (Tier 2) — the upper range that fires the auto-compact pipeline — is deferred to a separate stacked PR. This design covers the squash-side range gate exclusively.

## Hard contracts

- **Works whether CAP is on or off.** The TTL anchor is `state.LastLLMCallTime`. CAP refreshes already update this field via `core/workflows/elite/cap.go:85`, so the range gate piggybacks on a shared anchor without explicit CAP plumbing.
- **Fully backward compatible.** Agents without the new `range_threshold` field see zero behaviour change. For opted-in agents, the legacy `context.threshold` gate is **bypassed entirely** — the range gate is the sole truncation trigger.

## Code locations (cortex-only)

- **Schema**: `pkg/agentsdk/context.go` — `RangeThresholdConfig` field on `Context`. Cross-field validation enforces `overflow_threshold > range_threshold.upper`.
- **Decision**: `core/xcontext/squash.go` (`decideSquashReason`) + `core/xcontext/tiered.go` (`RangeThresholdPolicy`, `rangeThresholdOutcome`). Single shared decision function used by both `NeedsSquashing` (pre-flight) and `applyBulkCheckpointStrategy` (in-activity).
- **Wiring**: `core/workflows/elite/setup.go` builds `setup.SquashRangeThresholdPolicy` from agent config + `cap.CacheTTL`. `core/workflows/elite/flow.go:557` captures `squashEvalTime := exec.Now()` once and threads it through gate + activity.
- **Persistence**: `internal/pgsql/agents.go` jsonb writer + reader updated to round-trip the new field.
- **Opt-in**: `resources/agents/farm_agents/full_stack_app_builder_cloud_v8_opus_4_7.yaml` adds `range_threshold` and bumps `overflow_threshold` to 0.34.

**Total: ~700 LoC (incl. tests + PRDs).** One new package file (`core/xcontext/tiered.go`). No new Temporal activities.

## What this does NOT change

- No change to the `bulk_checkpoint` strategy. The range gate only changes **when** truncation fires, not what content survives.
- No change to `auto_compact` or summarisation behaviour. Tier 2 is a separate follow-up.
- No change for any non-opted-in agent.
- No change to CAP refresh behaviour. CAP continues to update `state.LastLLMCallTime`; the range gate reads it.

## Status

| Change | PR | State |
|---|---|---|
| Tier 1 truncation (this design) | [cortex#1474](https://github.com/emergentbase/cortex/pull/1474) | Open |
| Tier 2 summarisation | [cortex#1475](https://github.com/emergentbase/cortex/pull/1475) | Open (stacked on #1474) |
| YAML opt-in for Tier 2 | TBD | Pending |

## Supersession history

| Version | Date | Notes |
|---|---|---|
| v0.1 (dual-spec, action enum) | 2026-05-22 | Initial design — dedicated `range_based_truncation` block with twin `truncate_range`/`summarise_range` sub-structs and a 3-value action enum. **Superseded.** |
| v0.2 (post-critique, simplified enum) | 2026-05-22 | Renamed types, trimmed comments, added fire logs. Still dual-spec. **Superseded.** |
| **v1.0 (truncation only, generic gate)** | **2026-05-22** | **Current.** Single generic `RangeThresholdConfig` bolted onto `Context`. Bypasses legacy threshold for opted-in agents. Matches cortex#1474. |

The earlier proposals (cortex#1472 alt design) were closed in favour of cortex#1474's approach: smaller surface, generic gate reusable for Tier 2, idiomatic cortex extension pattern.
