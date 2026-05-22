# Senior-architect critique — range-gate-margin-capture v1

## Summary

The core mechanism (snapshot pre-squash cache prefix at squash time, re-price at PostHook by adding `avoided` back into `CacheCreationInputTokens`, stack delta on top of CAP) is sound and the CAP-mirroring scope discipline (no new package / activity / column / table) is the right call. But the doc has at least one blocker (`PreSquashCachedPrefix` is computed against the wrong baseline), one near-blocker (the FeatureRequest plumbing claim is factually incorrect), and several edge cases that quietly produce wrong numbers or wrong attribution — most notably composition with `bulk_checkpoint`, auto-compact handoff, and the layering choice that puts an elite-specific resolver into `core/xcontext/`.

## Issues

### [BLOCKER] `PreSquashCachedPrefix` is read from the wrong call's Usage
- **Where**: §6 ("Computing avoided_tokens precisely"), §9.1 `PendingMarginEvent`, §9.2 row 1 ("populate in `ApplySquash` from `state.LastUsage`")
- **What**: The doc says `pendingMargin.PreSquashCachedPrefix = lastUsage.CacheCreationInputTokens + lastUsage.CacheReadInputTokens`. In `runIteration` (flow.go:562–568) the squash decision uses `state.LastUsage()`, which `flow.go:1022` only updates *after* the LLM call returns. So at squash time `state.LastUsage` is the usage of the LLM call **two iterations back** (iter N-1's call), not "the prior call's Usage" as the doc claims in Scenario A. On a fresh resume — the headline case in §7 Scenario A — `state.LastUsage` is whatever Setup loaded (`setup.go:329`), which is the *last persisted* usage from the prior run. That may be a tool-result iteration where the prefix grew further, or where cache was rebuilt — not the cached size that the gate is dodging.
- **Why it matters**: `avoided = PreSquash − postSquashCacheCreate` directly drives the dollar swap. If `PreSquash` is the wrong call's number, the swap is wrong in either direction — and gate 5 (`avoided > 0`) silently masks under-billing while still firing the swap if avoided happens to be positive. In Scenario A the 452k figure is presented as "snapshotted from prior call's Usage" with no acknowledgement that on a resume there *is* no prior call in this run.
- **Fix**: Source `PreSquashCachedPrefix` from the *same input the gate uses* — i.e., `tokens` as computed by `contextTokens(...)` in `xcontext.decideSquashReason`, which already encapsulates "best estimate of the prompt size right now". Plumb that out of `ApplySquash` and into `ApplySquashResult.PreSquashTotalTokens int`. Drop the "cache_create + cache_read" shortcut entirely — it's not equivalent on resume.

### [BLOCKER] FeatureRequest is not the experiments-resolved flag surface
- **Where**: §13.2 "Resolved at workflow start by the experiments client … same path as every other elite experiment", §9.2 row 7
- **What**: `pkg/agentsdk/configs.FeatureRequest` (features.go:44) is **user-requested feature opt-ins** sent in the job payload (`Context`, `ThinkingMode`, `BeastMode`, etc.). The example given — `IsParallelToolExecution` — does **not** live on `FeatureRequest`; it lives on `Request.Metadata` as a free-form `map[string]any` (request.go:345–351). The experiments client writes into `Request.Metadata` / agent config patches, not into `FeatureRequest`. Adding `RangeGateMarginEnabled` to `FeatureRequest` would make it a **client-controlled** flag (any caller can set `range_gate_margin_enabled: true` in the job JSON and force decoupling on themselves), which is the opposite of a gradual server-side rollout.
- **Why it matters**: A misnamed knob in the wrong layer is how you ship a billing feature that the customer can disable from curl. Also: the experiment is never actually resolved by the experiments client because `FeatureRequest` isn't part of the resolved config patch — it's the *input*.
- **Fix**: Either (a) thread it through `Request.Metadata["range_gate_margin_enabled"]` and resolve it the same way `IsParallelToolExecution` is set today, or (b) put it on `SetupResult` populated by the experiment resolver and add a getter. Don't touch `FeatureRequest`.

### [SHOULD-FIX] Composition with `bulk_checkpoint` is undefined
- **Where**: §11 ("Composition with CAP"); not discussed for the squash-strategy axis
- **What**: `core/xcontext/squash.go:258–270` routes `bulk_checkpoint` through `applyBulkCheckpointStrategy`, which can return `WasApplied=true` with `reason = ReasonRangeThresholdCacheInvalidation` *only when* `BulkTruncateBeforeIndex` finds a viable cutoff. If it doesn't (≤ `preserve_last_n` tool results), `applyBulkCheckpointStrategy` returns `(false, …, "")` — squash didn't apply but the *gate* still wanted to fire. The doc never says whether to set the pending event in that case; reading §8 literally, it depends on `result.WasApplied`, so no event — which means the legitimate "range gate fired, bulk strategy declined" call still leaks margin.
- **Why it matters**: `bulk_checkpoint` is the production strategy (see `cortex/CLAUDE.md`). The exact case the gate exists to catch (long resumed runs with thin tool-result lists) is precisely when bulk decline-to-cut is most likely.
- **Fix**: Make the pending event keyed on *the gate firing*, not on `WasApplied`. Either (a) record pending when `decideSquashReason == ReasonRangeThresholdCacheInvalidation` regardless of bulk's verdict, or (b) document that this path is intentionally excluded and add a metric for it (`squashmargin.attribution.skipped_total{reason=bulk_strategy_declined}`).

### [SHOULD-FIX] Auto-compact handoff silently drops the pending event
- **Where**: §8 data flow, §12 failure modes ("Workflow restart between squash and PostHook")
- **What**: Between squash (flow.go:564) and PostHook, `maybeApplyAutoCompact` runs (flow.go:579) and can return `ShouldHandoff = true`, exiting the iteration before the LLM call ever happens. The pending event is now stuck in `state.pendingSquashMargin` of a workflow that's terminating into a child handoff. The child workflow (`compact.go`) starts fresh — `state.pendingSquashMargin` is never carried over.
- **Why it matters**: Range-gate-cache-invalidation fires on big prompts; auto-compact also fires on big prompts. The two paths overlap exactly where margin is most lucrative. The "pending event lives exactly one iteration" property the doc relies on for correctness is violated by handoff.
- **Fix**: Either drain the event by emitting a `squashmargin.attribution.skipped_total{reason=handoff_before_posthook}` metric on handoff (and pass nothing to the child), or — better — refuse to set the pending event when `compactOutcome.ShouldHandoff` is true (run the auto-compact pre-check before the squash, or check it after squash and unset). The current design will look correct in tests and quietly under-attribute in production.

### [SHOULD-FIX] Layering: `core/xcontext/margin.go` is wrong-package
- **Where**: §9.1, §10 ("Why not extract pricing into a neutral `core/billing/`?")
- **What**: `core/xcontext/` is the *deterministic, side-effect-free* squashing decision engine (per `core/xcontext/CLAUDE.md`: "standalone functions … threshold checks"). The proposed file imports `cortex/core/cap` for pricing, `cortex/pkg/agentsdk/io` for `TokenUsage`, and pulls in experiment-eligibility logic. That is elite-workflow billing logic dressed as a context-management primitive. It also creates a `xcontext → cap` dependency edge that today does not exist, and inverts the layering implied by `core/cap/` being a billing infrastructure peer of xcontext.
- **Why it matters**: Once `xcontext` imports `cap`, the next "small" reuse (e.g., neo workflow also wants margin attribution) will force another package to depend on the same edge, and the package boundary breaks. The doc rejects `core/billing/` as a "rename PR touching every CAP call site" — but you don't need a rename; you need the new resolver in either `core/workflows/elite/margin.go` (where it's actually used, only one consumer today) or `core/cap/margin.go` (next to the pricing primitives it reuses, since you're already importing them).
- **Fix**: Put the resolver in `core/workflows/elite/margin.go`. It's a workflow-internal attribution rule, not a context-management primitive. Move `PendingMarginEvent` and `MarginInput`/`MarginAttribution` with it. Keep `xcontext` pure.

### [SHOULD-FIX] Pricing-calculator allocation per call + missing pricing-model passthrough
- **Where**: §9.1 `ResolveMarginAttribution` body (`calc := cap.NewPricingCalculator(ctx)`); §10
- **What**: `cap.NewPricingCalculator(ctx)` constructs a fresh `pricing.Calculator` every invocation (cap/pricing.go:14). CAP's `ResolveAttribution` already pays this cost once per PostHook (cap/service.go:102); now squash-margin pays it *again*. More importantly: `cap.CalculateActualCost` honours `usage.PricingModel` for tier selection — but the design's `cloneWithAddedCacheCreate` is hand-written and is not specified to preserve `PricingModel`, `ReasoningTokens`, or `OutputTokens`. If any of those drop, `z` is silently mis-priced on multi-tier or batch-priced models.
- **Why it matters**: On Anthropic batch / tier-discounted pricing the swap could over- or under-bill by 25–50%. Silent. Worse than no swap.
- **Fix**: (a) Pass the calculator allocated by CAP into the resolver (one extra arg), don't allocate twice; (b) implement the clone as `usageCopy := *in.CurrentUsage; usageCopy.CacheCreationInputTokens += int64(avoided)` and pass the copy by pointer — copying the struct preserves every field, no field-listing risk.

### [SHOULD-FIX] `z > y` math-sanity gate is correct only because pricing is monotone today
- **Where**: §6 gate 6, §9.1 `EligibilityMathSanityFailed`
- **What**: Gate 6 demands `z > y` strictly. Suppose Anthropic introduces a "bulk cache-create" discount where the marginal cost-per-token decreases past 1M tokens (already the structure on input tokens). Then adding 302k cache-create on top of an existing 150k could push the call into a discount tier where `z` is *not* strictly greater than `y` — and the swap correctly should still fire. The doc treats `z ≤ y` as math-sanity-failure but it's actually a legitimate pricing structure.
- **Why it matters**: First time Anthropic ships tiered cache pricing, this whole feature silently degrades to "skipped_total{reason=math_sanity_failed}" on the biggest calls — the ones where margin is largest.
- **Fix**: Soften to `z >= y` (equal allowed, just no margin captured — bill at y). For *negative* delta, log loudly and skip. Don't conflate "no margin available" with "pricing table corrupt".

### [CONSIDER] Tier-2 extension path is hand-waved
- **Where**: §15 non-goals ("design generalises but the gates only admit `range_threshold_cache_invalidation`")
- **What**: Tier 2 is summarisation, which costs an extra LLM call. That's an `x > 0` margin (like CAP). The current `MarginInput` has no field for `PingCostUSD` or its summarisation analogue, and `PendingMarginEvent` doesn't record the summarisation LLM-call cost. When tier-2 lands, the resolver signature changes and every caller updates. Either declare that explicitly, or add a `RealizationCostUSD float64` field to `PendingMarginEvent` now (zero for tier-1) so the formula generalises.
- **Fix**: Add the field now or explicitly say "tier 2 will refactor this struct". Don't claim "design generalises" without naming the seam.

### [CONSIDER] Metric cardinality and reporting
- **Where**: §14
- **What**: `squashmargin.attribution.skipped_total{model, provider, reason}` with 8 reason values × ~10 models × 3 providers = 240 series. Fine. But `squashmargin.attribution.billable_distribution` as a histogram per `{model, provider}` is high-cardinality if observed across all variants. Also, no `agent_id` label means you can't slice rollout by the per-agent opt-in surface (§13.1).
- **Fix**: Add `agent_id` to the *counter* labels but **not** to the histogram. Drop `provider` from labels — `model` implies provider.

## Things the design got right

- The discipline of "no new package, no new activity, no new column, no rename" is exactly right for a CAP-clone v1 — kudos for resisting the urge to refactor pricing into a neutral package.
- `cap_delta` and `rg_delta` stacking math in §11 is correct: both reference the same `y` baseline; the disjoint-mechanism argument holds (cache-stayed-alive vs cache-killed-deliberately).
- "Bias toward under-billing on every uncertain gate" is the right philosophy and is explicitly stated in §12 — that's the kind of thing future maintainers will be tempted to "fix" and the doc preempts them.
- Scenario B (hard-floor not eligible) correctly identifies that `range_threshold_hard_floor` defers but does not *avoid* a cache_create — the reason gate 2 needs to filter on the specific reason string.

## Verdict

**Needs another iteration before implementation.** The two BLOCKERs (wrong-baseline snapshot, wrong-layer experiment flag) will produce incorrect numbers and a user-controllable billing knob respectively — neither is a "ship-then-fix" risk. The bulk_checkpoint and auto-compact-handoff gaps will silently zero out a chunk of margin in exactly the cases this feature targets. Address those four, queue the layering and pricing-clone items for the same PR (~30 lines of churn), defer the tier-2 generalisation and metric-cardinality items to v1.1.
