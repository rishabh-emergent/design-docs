---
status: accepted
---

# Truncate-or-summarize gate at the context window boundary

## Decision

Above the operating-window top (`W_high` = the existing `range_threshold.upper`), cortex no longer truncates unconditionally every step. On every finish where context exceeds `W_high`, a new pure decision — `xcontext.DecideBoundaryAction` — runs the pending `bulk_checkpoint` truncation for real and **truncates** only if it is *effective* (removes ≥ `min_removal_frac` of context **and** lands ≤ `W_high`); otherwise it **summarizes immediately** via the existing auto-compact pipeline. The gate is enabled solely by the presence of a new `range_threshold.min_removal_frac > 0`, so it rides the same experiment as range-based truncation and ships dark until that field is patched in.

## Why these non-obvious choices

- **Enable via `min_removal_frac` inside `range_threshold`, not a new flag.** Range-based truncation is already gated purely by structural presence (no boolean). Reusing that pattern keeps the gate "on only where range-truncation is on," lets the code ship dark, and makes rollout a single experiment field — at the cost of not being able to A/B the gate fully independently of range-truncation (acceptable: the gate is meaningless without it).

- **Summarize *immediately* at the decision point (e.g. 332K), below the 0.35 auto-compact threshold.** The PRD goal is "summarization no longer always at 0.35; the gate decides." So `maybeApplyAutoCompact` gains a `force` parameter that bypasses only its `NeedsCompact` (0.35) check. 0.35 stays untouched as a backstop and never triggers truncation, so the two cannot conflict.

- **No speculative summary pre-computation when the gate is active.** Because the gate may pick TRUNCATE above `W_high`, pre-computing a summary at a lower threshold would often be wasted LLM spend. We accept synchronous summarization latency for now and only pay for a summary when the gate actually selects SUMMARIZE. Revisitable.

- **Effectiveness is measured, not estimated (PRD R6), via an estimate-space ratio.** We run the real transform (`xllm.ApplySquash`, pure/no-I/O), take `removal_frac = (est_pre − est_post)/est_pre` as a ratio of the char/4 estimator (bias cancels), and scale the real `S` by the survival ratio for `post_trunc` — keeping it in the same real-token units as `W_high`. A true token count would need an LLM round-trip: synchronous latency + replay nondeterminism, a non-starter under Temporal.

- **`S` is `contextTokens` (input-only) — same view as the squash activity.** Earlier revisions used `CompactionTokenCount` (previous input + output + trailing) to catch boundary crossings caused by the just-finished turn, but that diverged from the activity's own `decideSquashReason` and required a `ForceReason` bypass to honour the gate's decision end-to-end. Aligning the gate to the activity's view removes that whole plumbing chain. Trade-off: a sudden output + trailing spike that pushes the next prompt above `W_high` in one iteration is not caught this turn; the gate catches it on the iteration AFTER (when `LastUsage` reflects the bigger call). Worst case: one oversized LLM call (~+65K tokens at the boundary). Acceptable in exchange for a single-view architecture with no force-bypass plumbing.

- **`imageOnlySquash` is a true image-only path, not a relaxation.** The image-cleanup arm of `Summarize` needs image-overflow removal to still fire, but must NOT re-trigger the hard-floor truncation that the gate just decided to *not* run. The `imageOnly` flag in `BuildSquashRequest` zeros `SquashRangeThresholdPolicy` and `CompactionThreshold` on the request so the activity's `decideSquashReason` can only return `ReasonImageOverflow`. No new image-only code path is introduced — the existing image-overflow handling in `applyBulkCheckpointStrategy` is reused.

- **Per-iteration re-decision, no `armed` flag.** An earlier revision gated the decision behind an in-memory `armed` flag so it fired once per window-exit. The effectiveness check already filters wasteful truncations (an ineffective Truncate flips to Summarize), so `armed` was defense-in-depth without a concrete failure mode it protected against. Dropping it removed a state field, accessor pair, `BoundarySuppress` action, and a re-arm-on-no-op switch in the caller.

- **Misconfigured `Summarize` falls back to today's hard-floor squash.** If the gate selects Summarize but `setup.IsAutoCompactOff()` (auto-compact was never enabled for the agent), the dispatch leaves `runSquash=true` so the existing input-only predicate fires the bulk truncation as it would today. Logged at WARN so the misconfiguration is visible. No special force-bypass needed because the activity's predicate already agrees with the gate's S.

## Consequences

- No new in-memory or persisted state, no force-bypass plumbing across the activity wire. The gate is a pure function of the current iteration's inputs.
- Gate's S aligns with the squash activity's S (both `contextTokens`), so BoundaryTruncate is honoured naturally. No risk of the activity silently overriding the gate.
- Sudden one-iteration spikes (large output + trailing in a single turn) cost one oversized LLM call before the gate reacts. Self-corrects.
