# ADR 0001 — One-shot autonomous subagent (not chat-style, not multi-call)

Date: 2026-05-24
Status: Accepted

## Context

The user wants a "ProductDemoVideo" agent that builds a polished marketing demo video from a freshly-built app. The pasted reference system prompt opens with "Be event-driven. After every major step, wait for next user input — don't burn through generations on assumed approvals." That language describes a **chat-style agent** that pauses between phases for user confirmation (voice audition, storyboard sign-off, fixture audit).

Cortex's elite workflow runs subagents as **autonomous child workflows**: when a parent calls `subagent_tool`, a child elite loop is spawned with the subagent's spec, runs to completion, and returns one result blob. Verified by inspecting every existing subagent (`testing_agent_v3_fork`, `deployment_agent_sonnet_4_5`, `support_agent_sonnet_4_5`, `design_agent_v1_gemini_3_1_pro`): **none of them have `ask_human` in their toolset**. Subagents in cortex cannot pause mid-run for human input — they only have `finish` (and sometimes `test_finish`).

The retrospective the user provided identified seven failure modes that ideally need human checkpoints:
1. TTS provider/key validation
2. Voice selection (audition)
3. Fixture sanitization
4. Storyboard approval
5. Visual frame audit before final render
6. Voice density
7. Music style

## Decision

Ship as a **one-shot autonomous subagent**.

The parent agent gathers everything that needs human input *before* invocation, using its own `ask_human`:
- ElevenLabs API key (written to `/app/marketing-video/.env`)
- Voice preference (id passed in JSON; default: Brian)
- Brand accent color, target length, music mood
- 3-5 feature highlights to surface

The subagent runs autonomously to completion. Iteration on the output (re-record, fix Scene 7 overlap, change voice) happens by **re-invoking** the subagent with `previous_video_path` and `user_feedback_on_previous` populated. Re-invocations are cheap relative to the cost of building elite-workflow-level multi-call protocols.

The five quality gates that *don't* need a human (TTS validation, density, frame audit, length, fixture cleanliness) are enforced **inside the prompt** as hard checks before `finish`. The two that *do* need a human (voice audition, storyboard sign-off) are skipped in v0; the rerun loop is the substitute.

## Alternatives considered

**(a) Chat-style agent (not a subagent)**: a separate workflow type outside elite, with its own ask-question loop. Rejected: large infra change, the elite workflow's invocation model is the right level for a tool the parent calls. Standing up a new workflow type to support one feature is the wrong shape.

**(b) Multi-call subagent (parent calls it multiple times — once for storyboard, once for audition, once for render)**: rejected: parent agent isn't a human, it won't naturally pause between calls to consult the user. Adding ask_human-based pauses *between* subagent calls is just a more awkward version of the rerun-with-feedback loop.

**(c) Add `ask_human` to subagents as a one-off**: rejected: would diverge from every other cortex subagent. Touches elite-workflow ergonomics for one feature. If we later decide subagents need pauses, that's a system-wide design decision, not a per-agent hack.

## Consequences

- The subagent must make some calls without the human in the loop. Specifically: voice (use default), storyboard (don't sign off, just render).
- The rerun loop is the iteration mechanism. User-feedback string → re-invocation → new MP4. This is acceptable for the use case (one-time marketing artifact) but would be wrong for a more interactive flow.
- v1 follow-ups: voice audition mode (`mode: audition` returns 3 voice samples without rendering full video), dry-run storyboard mode (`mode: storyboard_only` returns the storyboard JSON for parent to show user via ask_human before commit).
