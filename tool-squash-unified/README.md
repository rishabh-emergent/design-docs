# tool-squash-unified

Unified `ToolSquashPolicy` — configurable rule engine for squashing tool_use args
and tool_result content during context squashing (cortex + xllm).

| Doc | Covers | Related PR |
|---|---|---|
| [pr-1519-review.html](pr-1519-review.html) | Code review of the cortex consumer PR: file-by-file explanation (simple terms), findings (F1–F5), breakage analysis, simplicity scorecard | [cortex#1519](https://github.com/emergentbase/cortex/pull/1519), consumes [xllm#200](https://github.com/emergentbase/xllm/pull/200) |

Supersedes the two in-flight PRs cortex#1499 (args truncation) and cortex#1423
(stale-restart strip), which will be closed once #1519 lands.
