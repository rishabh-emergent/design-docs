# How to write design docs in this repo

This file is the style guide for everything under `design-docs/{feature-slug}/`. The goal is **homogeneity** — anyone opening any design doc in this repo should know where to look for the same kind of information without re-orienting themselves.

If you are writing a new design doc, start by reading three things in order:

1. This file.
2. The `README.md` of the most recently-updated sibling folder (gives you the current template).
3. The corresponding `design.html` to copy its `<style>` block verbatim.

---

## 1. What counts as a design doc

A change qualifies for a folder under `design-docs/` when **at least one** is true:

- It introduces or shifts a system boundary (new service, new storage location, new contract between services).
- It has billing, correctness, or data-loss consequences that a code reviewer cannot evaluate from the diff alone.
- It will be referenced by a future change ("this is why X is the way it is").
- A senior engineer would ask "where's the design doc?" before approving.

If none of those is true, the change belongs in a PR description and commit message, not here.

## 2. Folder layout

```
design-docs/
├── CLAUDE.md                         ← this file
├── README.md                         ← top-level index of all feature folders
└── {feature-slug}/
    ├── README.md                     ← REQUIRED: index + status table + post-launch updates
    ├── design.html                   ← REQUIRED: the canonical detailed design
    ├── adr/                          ← optional: architecture decision records (NNNN-title.md)
    ├── CONTEXT.md                    ← optional: domain language from /grill-with-docs
    ├── critique.md                   ← optional: senior-architect / security review of the design
    ├── pr-{n}-walkthrough.html       ← optional: visual walkthrough of a specific PR's diff
    └── test-cases.xlsx               ← optional: dry-run table
```

Slug rules: lowercase, hyphenated, descriptive (`cap-margin-capture`, not `cap2` or `siddharth-cap`). Slugs are permanent — if scope shifts, write a new folder and supersede the old one in its `README.md`.

## 3. The required `README.md`

Every folder has a `README.md` with this structure. Keep it short — it's an index, not the design itself.

```markdown
# {Feature Name}

| Doc | Covers | PR |
|---|---|---|
| [design.html](./design.html) | one-line description of the canonical doc | cortex#NNNN (state) |

## What this is

Two-paragraph summary. First paragraph: the problem. Second paragraph: the fix in one sentence + the trade-off.

## Code locations (cortex-only)

- **Domain**: `core/{pkg}/` — what lives here
- **Workflow**: `core/workflows/{x}/` — what lives here
- **Storage**: `internal/{backend}/{file}.go` — what lives here
- **Wiring**: `cmd/deps.go` — what env vars / clients this needs

## Status

| Change | PR | State |
|---|---|---|
| Initial feature | [cortex#NNNN](url) | Merged |
| Follow-up bugfix | [cortex#NNNN](url) | Open |

## What does NOT change

- ... (negative-space matters more than people realise — call out what stays the same)

## Post-launch updates (timeline)

| Date | PR | What shifted |
|---|---|---|
| YYYY-MM-DD | cortex#NNNN | What changed and where the design doc covers it (link the section anchor) |
```

The **Post-launch updates** table is added the first time the design ships a follow-up PR. Every subsequent PR appends a row. The corresponding section inside `design.html` should be added or updated in the same commit.

## 4. The `design.html` structure

The HTML doc is **self-contained** (no external CSS, no external JS, no CDN dependencies). Open it from disk; it just works. The `<style>` block is shared across all design docs — copy it from any existing `design.html` rather than reinventing.

### Standard section order

```
1.  TL;DR (for the impatient)
2.  Background / "Zoom out: how X works today"
3.  The problem we're solving (motivation)
4.  The solution (one paragraph + a callout)
5.  Vocabulary (precise terms — keep ≤10 entries)
6.  The rule (eligibility / decision logic)
7.  Dry runs (4 concrete scenarios with full calc tables)
8.  Data flow (sequence diagram, SVG)
9.  Storage model (what lives where, SVG)
10. Code changes (file-by-file, code-extract blocks)
11. Failure modes (tabular, every error path → behaviour)
12. Reporting (PromQL / LogQL / SQL the reader can paste verbatim)
```

Numbers are mandatory and stable — they're how reviewers refer to sections in comments. If a section doesn't apply, mark it `(n/a)` and explain in one sentence rather than omitting the number.

### Highlight major tech decisions inline

Every time a non-obvious value, store, or path is chosen, **call it out at the point of first mention** using a `<div class="callout">`. The reader should never have to ask "where does this number come from?" or "why did we pick Redis here?".

Patterns that *must* be called out:

| Pattern | Example callout text |
|---|---|
| Picking a backing store | "*here we are reading the eligibility boundary from Redis (`session:{sessionID}:meta`), not Postgres. See section 11.2 for the layout.*" |
| Hardcoded constant | "*`DefaultGlobalCacheBaseline = 26000` — picked from observed prod range 21k–28k (jobs edb67b6c-... and c302d3b2-...). Conservative bias: low values under-claim margin, never over-claim.*" |
| Defaulted behaviour on missing data | "*on `HMGET` miss we return zero-value `RuntimeMeta` and bill at `y` — never bill the user more than the no-CAP world.*" |
| Cross-service dependency | "*emergent's billing pipeline reads `cost_usd` off the PostHook payload exactly as before — no contract change.*" |
| Why NOT something | "*we did not put this in BigTable because the access pattern is hot point-read; BigTable is overkill. We did not put it in Postgres because that's the saturation we're solving for.*" |

The rule of thumb: **if a future maintainer would have to git-blame to figure out why a line of code looks the way it does, that "why" belongs in the design doc, not in a code comment.**

### Visualizations

| When | What to draw | How |
|---|---|---|
| Two or more processes interact across time | Sequence diagram (lifelines + arrows + colour-coded phases) | inline `<svg>` with `viewBox`, no external assets |
| Data lives in multiple stores | Storage model — boxes per store, fields inside, GC/TTL annotations | inline `<svg>` |
| A decision has branching outcomes | State diagram OR table with `(condition) → (outcome)` rows | inline `<svg>` or HTML table |
| Cost / token math | `<table class="calc-table">` with formula column and value column | reuse the shared CSS classes |
| A 5-minute timeline (cache TTL, idle windows) | Time-axis SVG with rect overlays for "alive" vs "dead" zones | inline `<svg>` |

All SVGs must:
- Have an explicit `viewBox` (no fixed pixel sizes).
- Use the shared colour palette: `#0b6bcb` (accent / user-flow), `#b06a00` (CAP / background-flow), `#1b7a3f` (success / decoupled), `#b3251b` (failure), `#555` (neutral DB / passive lifeline), `#666` (axis).
- Include a `<div class="caption">` below — italic, explains what the reader should take away. The caption is not optional; the SVG without the caption is half a diagram.

### Code blocks

`<pre><code>` for code extracts. **Abridge aggressively** — the goal is to point the reader at the right file, not to inline 200 lines. Keep extracts under 30 lines. Always cite the file path on the first line as a comment:

```html
<pre><code>// core/cap/global_cache.go
const DefaultGlobalCacheBaseline = 26000

func EffectiveGlobalCacheBaseline(measured int) int {
    if measured > 0 { return measured }
    return DefaultGlobalCacheBaseline
}</code></pre>
```

### Callout colour vocabulary

| Class | When |
|---|---|
| `<div class="callout">` (blue) | A neutral "you should read this" pointer to another section or a non-obvious detail. |
| `<div class="callout good">` (green) | Property we want the reader to internalise as a guarantee ("user is never overbilled because…"). |
| `<div class="callout warn">` (amber) | Operational caveat, post-launch update, gotcha. |
| `<div class="callout bad">` (red) | Anti-pattern, the wrong-thing-don't-do-this. Rare. |

## 5. Post-launch updates: how to amend a shipped doc

When a follow-up PR changes a property of the system the doc describes:

1. **Do not delete the original.** The historical design is part of the doc's value.
2. Add a row to the **Post-launch updates** table in `README.md`.
3. Inside `design.html`, add a `<div class="callout warn">` at the top of the affected section pointing to a new sub-section (or a new top-level section) that documents the change. Title it with the PR number and date.
4. Update the **Status** table.
5. If the change introduces a new storage location, a new dependency, or a new failure mode, you must add a new section in the standard order (Storage model, Failure modes, Reporting) — do not bury operational consequences in a callout.

Example (from `cap-margin-capture/design.html` section 10):

```html
<div class="callout warn">
<h4>Post-launch update (PR cortex#1483, 2026-05-23)</h4>
<p>v2 originally read X from Postgres on every workflow setup. That saturated cortex-db. Both reads now live in Redis. <strong>See section 11 for the full design and visualization.</strong></p>
</div>
```

## 6. The "homogeneity test"

Before you commit a new or updated design doc, open two existing design docs side-by-side with yours. Ask:

- Does the section order match? (TL;DR first, vocabulary before dry runs, dry runs before data flow, etc.)
- Are the SVGs using the same colour palette?
- Is the README structure identical?
- Are major tech decisions called out at point-of-first-mention with a callout?
- Are the table headers the same? (e.g., Failure modes always uses `| Failure | Behavior |`)
- Is every section numbered, and are subsections numbered `N.M`?

If any answer is no, fix yours — the goal is that someone can read three design docs in an afternoon without context-switching.

## 7. Anti-patterns

| Anti-pattern | Why it's bad |
|---|---|
| Multi-paragraph callouts that should be a section | Callouts are for pointers, not for content. If it's longer than 4 lines, promote it. |
| External CSS or JS (`<link>`, `<script src>`) | Breaks the open-from-disk property. Inline everything. |
| Code extracts longer than 30 lines | The reader can `git blob` the file. Show only the shape; cite the path. |
| Numbered sections without an `id` attribute | Reviewers cannot link to a section. Always `<section id="slug">`. |
| Markdown-only design (no HTML) for a multi-flow feature | If you have ≥2 lifelines or ≥2 stores, you owe the reader an SVG. |
| Storing implementation status anywhere except the Status table | Single source of truth. PR ⇄ row. |
| "TODO: explain later" left in the committed doc | Either explain it now or delete it. Don't ship gaps. |

## 8. Quick checklist before commit

- [ ] `README.md` has Status table updated for the PR(s) that motivated this revision.
- [ ] `README.md` has a Post-launch updates row if this is not the first version.
- [ ] `design.html` opens in a browser standalone (no console errors, no missing fonts).
- [ ] Every section has an `id`.
- [ ] Every SVG has a `<div class="caption">`.
- [ ] Every hardcoded number / store choice / fallback is justified in a callout.
- [ ] The doc is self-contained — no link to internal Notion / Slack thread as a substitute for content.
- [ ] You can read your own doc cold a week later and still understand the decisions.
