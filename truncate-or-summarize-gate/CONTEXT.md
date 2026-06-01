# Truncate-or-Summarize Gate — Context

Domain language for the gate that, once a session's context leaves the operating
window, decides **once** whether to truncate or summarize instead of letting
truncation fire ineffectively. Scoped to cortex's elite workflow + `xcontext`.
Builds directly on [range-based-truncation-opus-4-7](../range-based-truncation-opus-4-7/).

## Language

**Operating window**:
The context-size band a session is steered to stay within, `[W_low, W_high]`.
Defined in cortex as fractions of the model context window via the existing
`range_threshold.lower` / `range_threshold.upper`.
_Avoid_: "context budget", "healthy range".

**W_high (upper bound)**:
Top of the operating window. Maps to existing `range_threshold.upper` (e.g. 0.325
≈ 325K on a 1M window). The point above which the gate makes its decision.
_Avoid_: "overflow threshold" (that is a separate, higher stop-gate), "compaction threshold".

**W_low (lower bound)**:
Bottom of the operating window. Maps to existing `range_threshold.lower` (e.g. 0.14
≈ 140K). Drives the existing cache-invalidation truncation arm; the gate's own
decision math never reads it.

**Boundary gate**:
The truncate-or-summarize decision made at the first step-finish after context
exceeds `W_high`. Not a new trigger — it arbitrates which of the two existing
mechanisms (truncation vs summarization) fires.
_Avoid_: "tier 2", "summarization trigger" (the gate may pick either arm).

**Effective truncation**:
A pending truncation that BOTH (a) removes ≥ `min_removal_frac` of current context
AND (b) lands post-truncation context ≤ `W_high`. The gate truncates only when
truncation is effective; otherwise it summarizes.

**min_removal_frac**:
Configurable minimum fraction of current context a truncation must remove to count
as effective (initial 0.10). New field on `range_threshold`; its presence (> 0) is
the gate's enable signal — gate is dark when absent, preserving today's behavior.

**Per-iteration re-decision**:
The gate re-evaluates on every step finish — no `armed` flag, no `Suppress` action.
The effectiveness check itself prevents wasteful repeated truncation: if a fresh
truncation can no longer remove ≥ `min_removal_frac` of context or land back ≤
`W_high`, the gate flips to **Summarize**. So a session above `W_high` may run
several Truncate steps in a row (each one making real progress), and the moment
Truncate stops being effective the gate switches to Summarize. The
`auto_compact.threshold` (0.35) stays as a far-side safety backstop.

**Truncate arm**:
The existing `bulk_checkpoint` squash on its hard-floor path (`rangeThresholdHardFloor`).

**Summarize arm**:
The existing `auto_compact` pipeline (`maybeApplyAutoCompact`), **forced** to run
the instant the gate selects it — even below its own `auto_compact.threshold`
(0.35). It summarizes at the current size (e.g. 332K), not deferred to 0.35. The
0.35 threshold is left untouched as a pure backstop and never triggers truncation,
so it cannot conflict with the hard-floor. Nothing summarizes at or below `W_high`.

**Pending-truncation floor (`locked_floor + tail`)**:
The post-truncation context size the PRD subtracts from `S`. In cortex it is measured
by actually running pure `xllm.ApplySquash` with the pending bulk cutoff on the
current messages — never a guessed fraction (PRD R6).

**S (projected next-prompt size)**:
Real-token size of the prompt the agent is about to send, *not* the size of the
previous LLM call's input. Computed via `CompactionTokenCount(messages,
systemPrompt, lastUsage)` = previous input + previous output + estimated trailing
tool/user messages added since the last LLM call. Using input-only would miss
boundary crossings caused by the just-finished turn (e.g. large tool result that
landed after `lastUsage` was sampled).

**`forceReason` (Truncate signal)**:
The gate's projected-S view diverges from the squash activity's input-only
`decideSquashReason`. When the gate picks Truncate, the dispatch sets
`forceReason = ReasonRangeThresholdHardFloor` on the squash request; the activity
treats it as the authoritative reason and bypasses its own token check, so the
gate's decision is honoured end-to-end.

**`imageOnly` squash**:
A squash request with `RangeThreshold` and `CompactionThreshold` zeroed so the
activity's `decideSquashReason` can *only* return `ReasonImageOverflow`. Used by
the **Boundary gate** under Summarize when image-overflow cleanup is needed but
the hard-floor truncation must NOT re-fire.

## Relationships

- The **Boundary gate** intercepts only the **Truncate arm**'s hard-floor case
  (`S > W_high`); the cache-invalidation arm inside `[W_low, W_high)` is unchanged.
- A gate decision selects exactly one of **Truncate arm** XOR **Summarize arm**.
- **min_removal_frac** present ⇒ **Boundary gate** active ⇒ requires `range_threshold`
  present (so the gate only runs where range-based truncation runs).
- **Effective truncation** false ⇒ **Summarize arm**; true ⇒ **Truncate arm**.

## Flagged ambiguities

- "summarization at 0.35" — the existing `auto_compact.threshold`, distinct from
  `W_high` (0.325). The gate can force the **Summarize arm** *below* 0.35; 0.35
  remains only as a backstop. Resolved: gate is the authority above `W_high`.
- "overflow_threshold" (0.34 stop-gate) vs `W_high`/`range_threshold.upper` (0.325)
  vs `auto_compact.threshold` (0.35) are three different numbers — kept distinct.
