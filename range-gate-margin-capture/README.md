# Range-Gate Margin Capture via Billing Decoupling

| Doc | Covers | PR |
|---|---|---|
| [design.html](./design.html) | End-to-end design — `y/z` vocabulary, strict attribution rule, package layout (no new package), `cap` pricing reuse without duplication, composition with CAP, experiment gate, failure modes | TBD |

## What this is

When the range-gate (PR [cortex#1474](https://github.com/emergentbase/cortex/pull/1474)) fires `range_threshold_cache_invalidation`, it kills the prompt cache early to dodge a future second cache-write that TTL expiry would have caused. The user's first call after the squash pays Anthropic at the truncated-prefix cache-write rate. Today, the savings flow straight through to the user — we don't capture margin.

This doc applies CAP's billing-decoupling pattern ([cap-margin-capture](../cap-margin-capture/)): bill the user at the as-if-no-range-gate cost `z`, pay Anthropic the actual `y`, capture `z − y`. No ping cost (`x = 0`) because the range-gate doesn't make its own LLM call.

## Prerequisites assumed working

- [cortex#1474](https://github.com/emergentbase/cortex/pull/1474) — range-based truncation Tier 1
- Redis-anchor follow-up (cortex#1479) — `state.lastLLMCallTime` seeded from the Redis cross-run anchor so the gate actually fires on resume

## Code locations (cortex-only)

- **Pure attribution math**: `core/xcontext/margin.go` (NEW, same package as the trigger)
- **Pricing reuse**: imports `cap.NewPricingCalculator` + `cap.CalculateActualCost` — no new pricing helpers, no rename of cap
- **State**: `core/workflows/elite/state.go` — one new field `pendingSquashMargin *xcontext.PendingMarginEvent`
- **Integration point**: `core/workflows/elite/activities.go` — `activityPostHook` stacks the squash-margin delta after the CAP delta
- **Experiment gate**: `pkg/agentsdk/configs.FeatureRequest.RangeGateMarginEnabled` resolved via the existing elite experiments client

## What does NOT change

- No new Temporal activity. Margin is computed inside the existing `activityPostHook`.
- No new package. Margin attribution lives next to the squash decision in `xcontext`.
- No emergent-side schema change. The PostHook wire contract is unchanged; only `cost_usd` and `accumulated_cost` shift when decoupled (identical mechanism to CAP).
- No new database table, no BigTable column family. The whole margin lifecycle is in-workflow (squash → next LLM call → PostHook → cleared).
- No duplication with `core/cap/`. We import its pricing entry points; we do not copy `CalculateColdCacheCost` (different swap shape).
- No change to the legacy `bulk_checkpoint` strategy semantics for non-opted-in agents.
