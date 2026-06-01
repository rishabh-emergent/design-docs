# Design Docs

Centralized design documentation for major features and changes across projects.

**Writing a design doc?** Read [CLAUDE.md](./CLAUDE.md) first — it's the style guide that keeps these docs homogeneous (section ordering, SVG colour palette, when to use callouts, post-launch update conventions).

## Structure

One folder per major feature/change:

```
design-docs/
├── {feature-slug}/
│   ├── README.md           # Index: what's inside, related PRs, supersession history
│   ├── adr/                # Architecture decision records (NNNN-title.md)
│   ├── CONTEXT.md          # Domain language, terminology (from /grill-with-docs)
│   ├── {doc-name}.html     # Self-contained HTML design docs (animations, SVG diagrams)
│   └── ...                 # PRDs, sequence diagrams, design notes
```

## Workflow

1. Create `design-docs/{feature-slug}/` for a new major feature.
2. Write docs inside (ADRs, grill-with-docs outputs, HTML designs, etc.).
3. Commit and push to this repo (separate from any consuming repo).

## Index

- [cap-margin-capture](./cap-margin-capture/) — Bill the user at as-if-cold-cache cost when CAP keeps the prompt cache alive past TTL. cortex#1411 (merged), cortex#1465 (attribution metrics, open).
- [in-loop-cap-margin-capture](./in-loop-cap-margin-capture/) — Extends cap-margin-capture to claim margin on the LLM call following a long-running tool execution. Drops the iter-1 gate, advances the eligibility window per-iter, merges in-flight in_loop pings. [cortex#1548](https://github.com/emergentbase/cortex/pull/1548).
- [range-based-truncation-opus-4-7](./range-based-truncation-opus-4-7/) — Cache-TTL-aware pre-emptive truncation/summarisation for Opus 4.7 farm agents on 1M context. Avoids paying for cache invalidation twice. Works whether CAP is on or off; fully backward compatible with existing context config.
- [truncate-or-summarize-gate](./truncate-or-summarize-gate/) — Above the operating-window top (`W_high` = `range_threshold.upper`), decide once per window-exit whether to truncate (only if it removes ≥`min_removal_frac` AND lands back in-window) or summarize immediately — instead of firing futile hard-floor truncations. Rides the same experiment as range-based-truncation; ships dark. Builds on range-based-truncation-opus-4-7 (its deferred "Tier 2").
