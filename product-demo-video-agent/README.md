# product-demo-video-agent

A cortex subagent that produces a polished 60–90s marketing demo MP4 (voiceover + music bed + per-scene frames + highlight GIF) for a freshly-built app. Wired as the 5th subagent into `full_stack_app_builder_cloud_v8_opus_4_7`, alongside testing/design/support/deployment.

Related PR: TBD.

## What's in this folder

| File | Purpose |
|---|---|
| `README.md` | This index. |
| `plan.md` | The full design: lifecycle, JSON contract, tool budget, render pipeline, quality gates. |
| `adr/0001-one-shot-autonomous-subagent.md` | Why we're shipping this as a single autonomous run, not a chat-style or multi-call agent. |
| `adr/0002-elevenlabs-key-via-pod-file.md` | Why the parent agent writes ELEVENLABS_API_KEY to `/app/marketing-video/.env` instead of passing it through the subagent's LLM context. |

## Decisions at a glance

| Branch | Decision | Rationale |
|---|---|---|
| Lifecycle | One-shot autonomous subagent | Matches every other cortex subagent (testing, design, deployment). Elite workflow already supports it. Subagents have no `ask_human`. |
| Input | Dense JSON in subagent description, parent fills | Same pattern as `testing_agent_v3_fork`. Parent owns all human interaction upfront. |
| ElevenLabs key | Parent's `ask_human` → write to `/app/marketing-video/.env` chmod 600 → subagent receives path only | Raw key never enters subagent's LLM context. |
| Voice audition | Skip in v0 (default voice Brian); user iterates by re-invoking with `voice_id` override | Subagent can't pause for audio playback. Audition is a v1 follow-up. |
| Storyboard sign-off | Skip in v0; iterate via `previous_video_path` + `user_feedback_on_previous` on re-invocation | Parent can't show the storyboard to the user without a UI. |
| Output destination | Pod fs at `/app/marketing-video/{project}/output/*.mp4` | User downloads from the file browser UI. Object-storage upload is v1. |
| HyperFrames install | `npx -y hyperframes` inside `/app/marketing-video/{project}/` per run | Doesn't pollute `/app/frontend|backend`. Cold start ~30s. Visible in file browser. |
| System binaries | None to install — preview pod has ffmpeg + chromium + Playwright pre-installed | Confirmed via the `preview_support_agent.md` docs. |
| Model | claude-opus-4-7, adaptive thinking, 200k context, task_budget 120000 | Match testing agent. |
| Iterations / timeout / budget | max_iterations 60, timeout 45m, max_budget_usd 40 | Lower iterations than testing (fewer rounds), higher wall time (render is slow). |
| Tools | Parent's whitelist ∪ testing-agent's whitelist, minus `ask_human` + `emergent_integrations_manager` (subagents can't have them) | User asked for at-least-parent's-tool-set. |
| Invocation cue | Dense `description:` field + matching block in the parent prompt | User wants explicit parent-prompt hint. |

## Lessons captured (from the manual video-build retrospective)

Each lesson maps to a concrete enforcement in the subagent prompt:

| Lesson from retrospective | Where it's enforced |
|---|---|
| Validate TTS provider + key scope BEFORE writing composition code | Mandatory pre-flight phase — 3-word "hello" call. Hard fail if 401. |
| Sanitize fixtures before screenshotting | Phase 2 fixture-sanitization gate. Subagent inspects DB / mocks state before any `screenshot_tool` call. |
| Voice length drives scene length (≥90% density) | Phase 4 audio-first generation. Phase 6 hard gate: `voice_density_pct >= 90`. Refuse to `finish` if below 85. |
| Per-scene visual audit BEFORE final render | Phase 5 frame-export-per-scene-boundary, AI-audit each. Re-edit composition before going to final render. |
| Voice audition | Out of scope for v0. Default voice locked. |
| Music bed in v1, not afterthought | Phase 3 composes audio + music at -25dB simultaneously. |
| Track density %, not absolute length | Verification block surfaces density, not duration. |

## How a user triggers this

1. User builds app with cortex (normal flow).
2. User says something like *"make a launch video"* / *"create a demo reel"* / *"build me a promo clip for this app"*.
3. Parent agent detects the intent, calls `ask_human` to collect ElevenLabs API key + voice + brand color + target length + which features to highlight.
4. Parent writes `/app/marketing-video/.env` with `ELEVENLABS_API_KEY=...` (chmod 600).
5. Parent invokes `product_demo_video_agent` with the full JSON contract.
6. Subagent runs autonomously (~15–30 min wall time).
7. Subagent returns `/app/marketing-video/{project}/output/{project}-final.mp4`. User downloads from the file browser.
8. If user wants changes, parent re-invokes with `previous_video_path` + `user_feedback_on_previous`.

## Files touched (cortex side)

| File | Change |
|---|---|
| `cortex/resources/agents/common_agents/subagents-product_demo_video_v0_opus_4_7.yaml` | NEW — agent spec |
| `cortex/prompts/prompts/product_demo_video_v0.md` | NEW — subagent system prompt |
| `cortex/prompts/prompts.yaml` | Add `product_demo_video_v0` entry |
| `cortex/resources/agents/farm_agents/full_stack_app_builder_cloud_v8_opus_4_7.yaml` | Add 5th `subagent` toolset + override |
| `cortex/prompts/prompts/full_stack_app_builder_cloud_v8_opus_4_6.md` | Add "when to call product_demo_video_agent" block |

## Out of scope for v0

- Voice audition (sample 2-3 voices, user picks)
- Object-storage upload (persistent URL instead of pod-fs file)
- Dry-run / storyboard-only mode for sign-off before render
- Multi-aspect-ratio outputs (vertical for social, square for grid)
- A/B variant generation (two videos, user picks)
- Caching `node_modules/hyperframes` across reruns (it's cached per pod, fine)
