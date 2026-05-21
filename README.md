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

<!-- Add one line per feature folder as it's created -->
