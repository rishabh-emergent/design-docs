# Range-Based Truncation for Opus 4.7 (275k Farm Agents)

| Doc | Covers | PR |
|---|---|---|
| [design.html](./design.html) | End-to-end design — token bands, cache-TTL prediction, decision flow, architecture, code changes, backward compatibility, failure modes, metrics, architect-critique trail | TBD |

## What this is

Today, Opus 4.7 farm agents squash at exactly 275k tokens. Anthropic's prompt cache has a 5-minute TTL and is prefix-based — every squash invalidates the cache and forces a fresh `cache_creation` charge. If a TTL expiry lands just before 275k, we pay for cache invalidation **twice** (once on the post-expiry call, once on the post-squash call). This design adds a cache-TTL-aware trigger that squashes pre-emptively when the cache is predicted to die within a configured range, so we absorb only one `cache_creation` instead of two.

## Hard contracts (v0.2)

- **Works without CAP.** Prediction uses `state.LastLLMCallTime` as the primary anchor. CAP ping data is consumed opportunistically if available, but is not a dependency. Opt-in does not require CAP to be enabled.
- **Fully backward compatible.** Existing `threshold`, `overflow_threshold`, `auto_compact[]` semantics are untouched for non-opted-in agents. Opt-in is a single new YAML block (`range_based_truncation:`) with no interaction with existing fields.

## Code locations (cortex-only)

- **Schema**: `pkg/agentsdk/context.go` — new `RangeBasedTruncation` pointer field on `Context`, plus `Tier1Spec` / `Tier2Spec`
- **Decision**: `core/xcontext/rangebased.go` (NEW, ~80 LoC) — single pure function `DecideRangeAction` that folds prediction + action policy
- **Dispatch**: `core/workflows/elite/flow.go` — switch added around the existing squash block (~line 541) behind a Temporal version gate
- **Tier 2 plumbing**: `core/workflows/elite/compact.go` — `maybeApplyAutoCompact` gains one `force *AutoCompactConfig` parameter; existing callers pass `nil` and see no behaviour change
- **Setup**: `core/workflows/elite/setup.go` — populate `setup.RangeBasedTruncation` from `agentConfig.Context.RangeBasedTruncation`
- **Metrics**: `core/workflows/elite/metrics.go` — `recordRangeBasedDecision` emits two histograms
- **Opt-in**: 7 Opus 4.7 farm-agent YAMLs in `resources/agents/farm_agents/`

**Total non-test: ~110 LoC.** No new packages. No new Temporal activities. No extraction refactors.

## What this does NOT change

- No change to the `bulk_checkpoint` strategy. Tier 1 reuses `applySquashing` byte-for-byte.
- No change to `activityGenerateSummary` / `activitySaveCompactMessage`. Tier 2 invokes them via the existing `maybeApplyAutoCompact` pipeline.
- No change for any non-opted-in agent or non-Opus-4.7 model.
- No change to CAP behaviour, intervals, or attribution. CAP ping data is read; CAP code is not modified.
- No emergent-side schema change. No new metrics namespace.

## Status

| Change | Branch | State |
|---|---|---|
| Design (v0.2, post-critique) | — | Draft |
| Implementation | TBD | Not started |

## Dependency

The optional CAP ping consumption (`setup.Cap.Pings`) was introduced by [cortex#1411 CAP Margin Capture](../cap-margin-capture/). If `setup.Cap` is nil (CAP not deployed, BigTable client missing, provider clamp rejected the workflow), the feature degrades cleanly to using `state.LastLLMCallTime` alone. Opting in does not block on cortex#1411 — the design uses CAP as a signal-improving optional input.

## Architect debate

The final design was synthesised from three competing architect proposals (minimal-diff, modular sub-package, CAP-owned) followed by a software-architect critique pass that removed two files and one extraction refactor without dropping any PRD requirement. The trail is documented inline in `design.html` §11.
