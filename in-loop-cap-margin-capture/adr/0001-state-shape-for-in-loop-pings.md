# ADR-0001: Separate `state.inLoopPings` slice instead of mutating `setup.Cap.Pings`

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-05-28 |
| **PR** | cortex#TBD |
| **Supersedes** | — |

## Context

In-loop CAP margin capture requires the workflow to accumulate `cap.PingRecord` rows as they are fired during a single elite run, so that subsequent iterations of the same workflow can claim margin against them. The PingRecord for each fired ping is constructed in workflow code from `RefreshRequest` (known to the workflow) + `RefreshResult` (returned by the activity).

The pre-existing structure in cortex separates two concepts:

- **`setup.Cap.Pings`** — loaded once at workflow setup from BigTable. Holds post-exit pings from prior workflow runs whose decoupling window overlaps this workflow's first iter. **Loaded once, treated as immutable for the rest of the run.** This immutability is load-bearing for replay determinism reasoning: contributors read `setup.*` and trust that values are frozen at setup time.

- **`state.*`** — mutable workflow state, evolves across iterations (messages, usage, cached anchors). Already houses similar in-flight quantities like `state.lastLLMCallTime`, `state.lastRequestID`.

We need to choose where the in-flight in-loop pings live.

## Decision

Add a new slice `state.inLoopPings` (Shape B) with an `AppendInLoopPing(p PingRecord)` mutator. At each PostHook build site, the in-loop slice is merged with the setup-loaded post-exit slice into a single `[]PingRecord` passed to `PostHookActivityInput.CapPings`:

```go
mergedPings := append(append([]cap.PingRecord{}, setup.Cap.Pings...), state.GetInLoopPings()...)
```

The merge is a temporary local; nothing about `setup.Cap.Pings` mutates.

## Consequences

- One new mutable field on `state` and one new pair of getter/Append methods, matching the existing `state.lastLLMCallTime` / `Get`/`Set` pattern.
- `setup.Cap.Pings` remains immutable — preserves the existing reader contract on `setup.*`.
- The merge cost is `O(len(post_exit) + len(in_loop))` per PostHook build, bounded by `LongRunningMaxRefreshes ≤ 4` per workflow run. Negligible.
- Tests can populate the two slices independently — `setup.Cap.Pings` for "what existed before this workflow", `state.inLoopPings` for "what this workflow fired" — making the boundary between cross-workflow and intra-workflow attribution obvious in test fixtures.

## Alternatives considered

### Shape A: Mutate `setup.Cap.Pings` in place

```go
// refreshCacheAnchorIfNeeded, after activity succeeds:
setup.Cap.Pings = append(setup.Cap.Pings, builtPingRecord)
```

**Cons:**

1. **Breaks the reader contract on `setup.*`.** Today, every reader of `setup.*` (including reviewers and future contributors) reasonably assumes those values were resolved once at workflow setup and are stable for the workflow's lifetime. Mutating one field silently in one code path erodes that contract — the next contributor who adds a setup field has no way to know which fields are mutable and which are not. The reader cost is permanent; the writer convenience is one line saved.

2. **Confuses cross-workflow vs intra-workflow semantics.** `setup.Cap.Pings` carries pings from *prior* workflow runs (loaded from BigTable). Adding in-flight pings from *this* run muddles the temporal scope of the slice. With Shape B, the boundary is structural: `setup.Cap.Pings` = "before this workflow"; `state.inLoopPings` = "during this workflow". Anyone reading the merge expression sees the boundary at the call site.

3. **Harder to reason about in replay.** Temporal replays workflows by re-running workflow code against recorded activity results. Under Shape A, on each replay, the same activity result causes the same `append` into `setup.Cap.Pings` — deterministic, but the *appearance* of mutating a setup-time-loaded slice on every replay makes the determinism argument harder to follow. Under Shape B, `state.*` is the obvious home for mutation and replay reasoning is unchanged from the existing `state.lastLLMCallTime` / `state.messages` pattern.

4. **Couples test fixtures.** A unit test that wants to exercise "iter 2 attribution with two in_loop pings fired during the run" would have to pre-load `setup.Cap.Pings` with the in_loop entries, which is exactly the wrong mental model — those pings *weren't* there at setup, they came from this run. With Shape B, the test populates `state.inLoopPings` with the expected fixtures directly.

5. **Field name lies.** `setup.Cap.Pings` was named when the slice represented the setup-time load. Repurposing it to also accumulate in-flight pings means the field name no longer describes the field. Either we accept the lie or rename the setup field (cascading rename across the codebase), neither of which is a good outcome.

### Shape C: Track `state.prevAssistantMsgAt` as a third field, advanced per iter

Considered alongside Shape B. Rejected: the "previous" value is only ever needed at the precise moment we build PostHook input. Capturing it into a local `prevAt := state.GetLastAssistantMsgAt()` immediately before `state.SetLastAssistantMsgAt(thisCallTime)` is three lines, lexically co-located, and eliminates the bug class where a future contributor adds a fourth read site of `state.prevAssistantMsgAt` and gets a value advanced into the next iter. A field that lives across the workflow run for a value with single-instant lifetime is a foot-gun. Final design uses the local — no new "Prev" field.

### Shape D: Re-read BigTable in `activityPostHook` to refresh the in-loop pool

Rejected: adds a per-iter BigTable round trip on the PostHook hot path, just to retrieve data the workflow already has in memory. The whole reason CAP runtime meta moved to Redis (cortex#1483) was to take this kind of read off the hot path.

## Notes for future contributors

- If a third source of pings is ever introduced (e.g., a "prefetch" ping fired by neo before elite starts), add a separate `state.prefetchPings` slice and extend the merge expression. Do not overload `setup.Cap.Pings`.
- The merge expression intentionally constructs a new slice (`append(append([]cap.PingRecord{}, …))`). Do not pass `state.inLoopPings` directly to the activity — Temporal serialization can mutate it on replay paths in subtle ways. Always copy.
