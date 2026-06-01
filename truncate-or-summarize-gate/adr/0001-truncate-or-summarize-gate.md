---
status: accepted
---

# Truncate-or-summarize gate at the context window boundary

## Decision

Above the operating-window top (`W_high` = the existing `range_threshold.upper`), cortex no longer truncates unconditionally every step. At the **first** finish after context exceeds `W_high` (guarded by an in-memory `armed` flag so it happens once per window-exit), a new pure decision — `xcontext.DecideBoundaryAction` — runs the pending `bulk_checkpoint` truncation for real and **truncates** only if it is *effective* (removes ≥ `min_removal_frac` of context **and** lands ≤ `W_high`); otherwise it **summarizes immediately** via the existing auto-compact pipeline. The gate is enabled solely by the presence of a new `range_threshold.min_removal_frac > 0`, so it rides the same experiment as range-based truncation and ships dark until that field is patched in.

## Why these non-obvious choices

- **Enable via `min_removal_frac` inside `range_threshold`, not a new flag.** Range-based truncation is already gated purely by structural presence (no boolean). Reusing that pattern keeps the gate "on only where range-truncation is on," lets the code ship dark, and makes rollout a single experiment field — at the cost of not being able to A/B the gate fully independently of range-truncation (acceptable: the gate is meaningless without it).

- **Summarize *immediately* at the decision point (e.g. 332K), below the 0.35 auto-compact threshold.** The PRD goal is "summarization no longer always at 0.35; the gate decides." So `maybeApplyAutoCompact` gains a `force` parameter that bypasses only its `NeedsCompact` (0.35) check. 0.35 stays untouched as a backstop and never triggers truncation, so the two cannot conflict.

- **No speculative summary pre-computation when the gate is active.** Because the gate may pick TRUNCATE above `W_high`, pre-computing a summary at a lower threshold would often be wasted LLM spend. We accept synchronous summarization latency for now and only pay for a summary when the gate actually selects SUMMARIZE. Revisitable.

- **Effectiveness is measured, not estimated (PRD R6), via an estimate-space ratio.** We run the real transform (`xllm.ApplySquash`, pure/no-I/O), take `removal_frac = (est_pre − est_post)/est_pre` as a ratio of the char/4 estimator (bias cancels), and scale the real `S` by the survival ratio for `post_trunc` — keeping it in the same real-token units as `W_high`. A true token count would need an LLM round-trip: synchronous latency + replay nondeterminism, a non-starter under Temporal.

- **`S` is the *projected* next-prompt size, not the previous input.** Use `CompactionTokenCount` (= previous input + previous output + estimated trailing tool/user messages added since the last LLM call), not `contextTokens` (input-only). Auto-compact already uses this for the same reason; using input-only would miss boundary crossings caused by the just-finished turn.

- **`forceReason` honors Truncate even when the activity's input-only predicate would skip.** The squash activity's existing `decideSquashReason` uses `contextTokens` (input-only); a `BoundaryTruncate` decision driven by projected S could be silently dropped at the activity boundary. A new `SquashConfig.ForceReason` field (plumbed via `ApplyAndPersistSquashRequest.ForceReason` → `BuildSquashRequest(forceReason)` → `applySquashing(forceReason)`) short-circuits `decideSquashReason` so the gate's decision is authoritative end-to-end. We chose this targeted bypass over a broader switch to projected tokens inside `decideSquashReason` to limit blast radius — non-gate callers keep today's exact behavior.

- **`imageOnlySquash` is a true image-only path, not a relaxation.** `Suppress` and the image-cleanup arm of `Summarize` need image-overflow removal to still fire, but must NOT re-trigger the hard-floor truncation that `Suppress` exists to prevent. The `imageOnly` flag in `BuildSquashRequest` zeros `SquashRangeThresholdPolicy` and `CompactionThreshold` on the request so the activity's `decideSquashReason` can only return `ReasonImageOverflow`. No new image-only code path is introduced — the existing image-overflow handling in `applyBulkCheckpointStrategy` is reused.

- **Tentative-disarm + re-arm-on-no-op.** The pure decision sets `armed=false` for `Truncate`/`Summarize`, but the loop caller re-arms after dispatch if the chosen action produced no effect (squash truncated nothing, or compact returned no-op). This protects against silent no-ops from activity errors, cancel signals mid-summary, exhausted truncation cutoffs, or misconfiguration — the gate retries on the next iteration instead of getting stuck disarmed above `W_high`.

- **Misconfigured `Summarize` falls back to `Proceed`.** If the gate selects Summarize but `setup.IsAutoCompactOff()` (auto-compact was never enabled for the agent), the dispatch reclassifies the action as `Proceed` and explicitly re-arms. The existing hard-floor squash takes over instead of leaving both arms inert. Logged at WARN so the misconfiguration is visible.

## Consequences

- `armed` is in-memory only; on resume it resets to true and the gate re-decides once. Harmless and self-healing.
- The gate's view of S (`CompactionTokenCount`) and the squash activity's view (`contextTokens`) deliberately differ. The `forceReason` plumbing reconciles them only when the gate has externally decided to truncate, so the rest of the squash machinery is unchanged for non-gate agents.
- Adding `ForceReason` to the `ApplyAndPersistSquashRequest` wire is forward-compatible: workers running the prior version of the request struct ignore the unknown field; workers running the new struct treat empty `ForceReason` as the default (no force).
