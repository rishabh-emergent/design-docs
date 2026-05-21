# Design Docs

Centralized design documentation for major features and changes across projects.

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
- [range-based-truncation-opus-4-7](./range-based-truncation-opus-4-7/) — Cache-TTL-aware pre-emptive truncation/summarisation for Opus 4.7 farm agents on 1M context. Avoids paying for cache invalidation twice. Works whether CAP is on or off; fully backward compatible with existing context config.
