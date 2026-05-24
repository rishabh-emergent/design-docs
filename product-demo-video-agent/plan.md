# product-demo-video-agent — plan

Subagent ID: `product_demo_video_v0_opus_4_7`
Display name (as seen by parent orchestrator): `product_demo_video_agent`

## Lifecycle (one-shot autonomous)

```
parent (full_stack_app_builder_cloud_v8_opus_4_7)
  │
  │  ask_human("ELEVENLABS_API_KEY?")           ──┐
  │  ask_human("voice preference?")               │ — gathered ONCE by parent
  │  ask_human("brand accent color, length, mood?")─┤
  │  ask_human("which 3-5 features to highlight?") ─┘
  │
  │  mcp_create_file /app/marketing-video/.env  ELEVENLABS_API_KEY=...   (chmod 600)
  │
  │  call subagent product_demo_video_agent with JSON contract ↓
  │
  ▼
product_demo_video_v0_opus_4_7 (this subagent)
  │
  │  Phase 1 — Pre-flight (90s budget)
  │    • validate ElevenLabs key + scopes (3-word "hello" call)
  │    • confirm ffmpeg + chromium + node present
  │    • npx -y hyperframes inside /app/marketing-video/{project}/
  │
  │  Phase 2 — Discovery (no LLM calls outside view_*)
  │    • crawl preview_url for screens / routes
  │    • view_bulk on key UI components parent named in files_of_reference
  │    • run fixture sanitization audit (DB queries, mocks)
  │
  │  Phase 3 — Storyboard (silent draft)
  │    • write 8 scene specs to /app/marketing-video/{project}/storyboard.json
  │      with: headline, sub-line, narration, animated element, screenshot need
  │    • DO NOT proceed if any scene lacks narration or visual asset
  │
  │  Phase 4 — Audio first (drives scene lengths)
  │    • generate each scene narration via ElevenLabs (one call per scene)
  │    • measure actual duration of each clip
  │    • generate / source music bed for sum-of-clip-durations + 2s tail
  │    • compute voice_density_pct
  │
  │  Phase 5 — Composition + per-scene audit
  │    • write HyperFrames composition (HTML/CSS/JS) scene-by-scene
  │    • render preview MP4 (low fps for speed)
  │    • ffmpeg -ss <scene_start> -vframes 1 → one still per scene boundary
  │    • view each still, audit for: overlap, cutoff, contrast, mock-data clutter
  │    • iterate composition until all stills pass
  │
  │  Phase 6 — Final render + mux + verification
  │    • render 1080p30 H.264
  │    • ffmpeg amix narration + music_bed (-25dB) + 1.5s fade-in / 2s fade-out
  │    • generate 720px 15s highlight GIF
  │    • verify voice_density_pct >= 90 (refuse finish if < 85)
  │    • paste verification block as final message
  │
  │  finish() ──→ parent
  ▼
parent receives:
  output_mp4 path, voice_density_pct, scenes timing table, frames_dir, issues, rerun_hints
```

## Input JSON contract (parent → subagent)

```json
{
  "project_name": "FixIt",
  "preview_url": "https://abc123.preview.emergentagent.com",
  "task_summary": "What the user originally asked for (1-2 sentences, parent paraphrases)",
  "original_problem_statement_and_user_choices_inputs": "Verbatim original user request + any user choices/inputs they made during the build",
  "files_of_reference": [
    "frontend/src/Dashboard.jsx — main scoreboard UI",
    "frontend/src/AutoFix.jsx — the wow moment, the auto-fix button",
    "frontend/src/Export.jsx — PDF export flow"
  ],
  "feature_highlights": [
    "Auto-fixes 17/20 lint warnings in one click",
    "Score climbs 39 → 81 in real time",
    "Exports compliance report PDF"
  ],
  "fixture_sanitization_notes": "DB has rows named 'test123', 'FixAll demo' — sanitize before screenshotting. Use persona names like 'Jane Doe — Stripe'.",
  "elevenlabs_key_path": "/app/marketing-video/.env",
  "voice_id": "nPczCjzI2devNBz1zQrb",
  "target_duration_seconds": 75,
  "brand_accent_color": "#3B82F6",
  "music_mood": "ambient corporate minimal piano, no drums, no vocals, like a Linear or Apple launch background",
  "agent_to_agent_context_note": "Hard build problems: the export PDF needed playwright, took 3 iterations to make stable. Worth mentioning the reliability story.",
  "previous_video_path": null,
  "user_feedback_on_previous": null
}
```

## Return contract (subagent → parent)

Final message includes the JSON below verbatim AND writes it to `/app/marketing-video/{project}/output/result.json`:

```json
{
  "status": "success",
  "output_mp4": "/app/marketing-video/FixIt/output/FixIt-final.mp4",
  "silent_mp4": "/app/marketing-video/FixIt/output/FixIt-silent.mp4",
  "voice_density_pct": 92.4,
  "total_duration_seconds": 73.2,
  "scenes": [
    {"scene": 1, "budget_s": 6, "actual_s": 5.8, "asset": "frames/scene_01.png", "narration": "..."},
    ...
  ],
  "highlight_gif": "/app/marketing-video/FixIt/output/FixIt-highlight.gif",
  "frames_dir": "/app/marketing-video/FixIt/output/frames/",
  "issues": [],
  "rerun_hints": []
}
```

## Tool budget

| Toolset | Tools |
|---|---|
| envcore mcp | execute_bash, screenshot_tool, browser_automation, view_file, view_bulk, glob_files, create_file, search_replace, bulk_file_writer, lint_javascript, lint_python, insert_text |
| server_tools mcp | web_search_tool, crawl_tool, get_assets_tool, analyze_file_tool, extract_file_tool, integration_playbook_expert_v2 |
| builtin | finish |

(Parent's whitelist ∪ testing-agent's whitelist, minus `ask_human` + `emergent_integrations_manager` — subagents cannot have those.)

## Model + policy

```yaml
model:
  provider: anthropic
  id: claude-opus-4-7
  max_tokens: 64000
  context_window: 200000
  params:
    thinking: {type: adaptive, display: summarized}
    effort: high
    task_budget: {total: 120000}

policy:
  max_iterations: 60
  max_budget_usd: 40
  scale_factor: 1.9
  timeout: 45m

context:
  squashing_strategy: bulk_checkpoint
  threshold: 0.7
  preserve_last_n: 10
  truncation_length: 150
```

## Quality gates (hard, in the prompt)

The subagent prompt encodes these as **mandatory checks before `finish`**:

1. **TTS validation** — 200 + non-zero MP3 on a 3-word "hello" call. Hard fail otherwise.
2. **Fixture sanitization** — no test data ("test", "demo", "FixAll", "123") in any rendered frame. Verified by re-screenshotting after cleanup.
3. **Voice density** — `voice_density_pct >= 90` required; 85–90 emits warning; <85 refuses to finish.
4. **Per-scene frame audit** — every scene boundary frame inspected before final render. Pass = no overlap, no cutoff, contrast ≥4.5:1, no mock-data clutter.
5. **Visual style guardrails** — single typeface (Inter or equiv), ≤3 colors on screen at once, no bounce/spin/flash, only ease-in-out / power3.out easing.
6. **Length budget** — 60s ≤ total_duration ≤ 90s. Outside window → refuse finish.

## Out-of-scope reminders for v0

- No voice audition flow
- No object-storage upload — file lives in pod fs
- No dry-run / storyboard-only mode
- No multi-aspect-ratio outputs
- No A/B variant generation
