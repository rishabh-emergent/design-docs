# Exa vs Perplexity vs Gemini — integration playbook eval

| Doc | Covers | PR |
|---|---|---|
| [eval-harness-design.md](./eval-harness-design.md) | Original 2-stage eval design (28 integrations, LLM-judge rubric, harness plumbing, smoke-test contract) | — |
| [pilot/FOUR_WAY_REPORT.md](./pilot/FOUR_WAY_REPORT.md) | **Final results** — 4-way head-to-head (Perplexity vs Exa /research/v1 vs Exa /search+Haiku vs Gemini 3.1+Grounding) over 29 integrations, all costs measured from API responses | — |
| [pilot/FULL_REPORT.md](./pilot/FULL_REPORT.md) | Intermediate report (29-int, 2-way: Perplexity vs Exa /research) | — |
| [pilot/PILOT_REPORT.md](./pilot/PILOT_REPORT.md) | Auto-generated pilot-scope report (7-int, 2-way) | — |
| [pr-348-walkthrough.html](./pr-348-walkthrough.html) | Visual code walkthrough of llm-proxy-service PR #348 with end-to-end dry run | [llm-proxy-service#348](https://github.com/emergentbase/llm-proxy-service/pull/348) (open) |

## What this is

We needed to evaluate alternatives to Perplexity `sonar-deep-research` for the
`integration_playbook_expert_v2` MCP tool — which generates the step-by-step
playbook the Emergent coding agent consumes when integrating a 3rd-party
service (Stripe, Supabase, PhonePe, etc.).

This folder holds the design, the harness, the raw playbooks generated, the
per-playbook judge scores, the aggregate reports, and the PR walkthrough that
explains the resulting llm-proxy-service code changes.

## TL;DR of the final verdict

| Provider | Quality (judge avg of 3 substance dims) | Pairwise winrate vs Perplexity | Cost/call | Cost @ 70k/mo |
|---|---|---|---|---|
| Perplexity sonar-deep-research (today) | 2.40 / 2.52 / 3.34 | — | $0.957 | $66,990 |
| Exa /research/v1 (Exa hosted research-pro) | 2.69 / 3.24 / 3.93 | 86% | $0.749 | $52,430 |
| **Exa /search + Claude Haiku 4.5** | 2.83 / 3.21 / 4.07 | 79% | $0.096 | $6,720 |
| **Gemini 3.1 Pro + google_search grounding** | **3.55 / 3.83 / 4.38** | 66% | **$0.039** | **$2,730** |

Gemini 3.1 wins on substance (3/4 dims), and is the cheapest. It only loses
pairwise comparisons because the rubric weights `citation_anchoring`
equally with correctness, and Gemini's grounding metadata doesn't surface
URLs reliably. A prod-trace investigation across 6 jobs (including one with
51 real Perplexity citations) found **zero downstream tool calls fetched any
citation URL** — citations are not used in practice, so the gap doesn't
matter operationally.

## Layout

```
exa-vs-perplexity-eval/
├── README.md                                       (this file)
├── eval-harness-design.md                          (original eval design)
├── pr-348-walkthrough.html                         (visual walkthrough of llm-proxy-service PR #348)
└── pilot/
    ├── integrations.yaml                           (7 pilot integrations — Stage-2 picks from design seed)
    ├── integrations_full.yaml                      (full 29-integration eval set)
    ├── run_pilot.py                                (Stage 1: parallel Perplexity + Exa /research calls)
    ├── run_exa_search.py                           (Stage 1: parallel Exa /search + Haiku synthesis arm)
    ├── run_gemini.py                               (Stage 1: parallel Gemini 3.1 + grounding arm)
    ├── judge.py                                    (Shape A absolute scoring via Claude Opus 4.7)
    ├── judge_three_way.py                          (incremental 4-way judge + pairwise computation)
    ├── summarize.py                                (auto-generates PILOT_REPORT.md from judge output)
    ├── PILOT_REPORT.md                             (7-int)
    ├── FULL_REPORT.md                              (29-int, 2-way)
    ├── FOUR_WAY_REPORT.md                          (29-int, 4-way — this is the canonical result)
    ├── results/                                    (raw playbook outputs as JSON, per integration)
    │   ├── I01.json … I29.json                     (each holds perplexity / exa / exa_search_haiku / gemini_31 blocks)
    │   ├── _run_summary.json                       (Stage 1 cost + latency aggregate)
    │   ├── _exa_search_summary.json
    │   └── _gemini_summary.json
    └── judge_results/
        ├── I01-perplexity.json … I29-gemini_31.json (per-playbook Opus 4.7 rubric scores + evidence)
        └── _aggregate_3way.json                    (per-dim averages + pairwise winner counts)
```

## API keys

All scripts read keys from environment variables or fall back to
`gcloud secrets versions access` on `emergent-default`:

```bash
EXA_API_KEY=...           # secret manager: EXA_API_KEY
PERPLEXITY_API_KEY=...    # secret manager: PERPLEXITY_API_KEY
ANTHROPIC_API_KEY=...     # secret manager: ANTHROPIC_API_KEY (for Haiku synthesis + Opus judge)
GEMINI_API_KEY=...        # secret manager: GEMINI_API_KEY
```

No keys are committed to this repo. The scripts will prompt
`gcloud auth login --update-adc` to be done if the gcloud token has expired.

## Reproducing the run

```bash
cd pilot/

# Stage 1 — call each provider on all 29 integrations
python3 run_pilot.py integrations_full.yaml          # ~$30 (Perplexity + Exa /research)
python3 run_exa_search.py integrations_full.yaml     # ~$3 (Exa /search + Haiku)
python3 run_gemini.py integrations_full.yaml         # ~$1 (Gemini 3.1)

# Stage 2 — judge all 4×29 = 116 playbooks via Claude Opus 4.7
python3 judge_three_way.py                           # ~$33

# Final summary
python3 -c "import json; print(json.load(open('judge_results/_aggregate_3way.json'))['pairwise'])"
```

Total run cost: ~$87. Wall-clock: ~25 min for all three Stage 1 arms in parallel + 2 min for the judge.

## Related PRs

- **llm-proxy-service** [#348](https://github.com/emergentbase/llm-proxy-service/pull/348) — adds `integration_playbook_expert_v2_exa` (Exa /search + Haiku) and `integration_playbook_expert_v2_gemini` (Gemini 3.1 + Grounding) MCP tools alongside the existing Perplexity tool.
- **cortex** [#1679](https://github.com/emergentbase/cortex/pull/1679) — pre-wires `_exa` and `_gemini` `display_name` overrides across 184 agent yamls so Unleash can swap the whitelisted tool name per cohort without further yaml changes.
- **k8-kustomize** [#7033](https://github.com/emergentbase/k8-kustomize/pull/7033) — bumps server-tools dev image tag to `v0.0.38-exa-search-haiku`.
