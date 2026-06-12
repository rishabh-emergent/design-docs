# Phase 0/1 Baseline Sweep — Raw Agent Outputs

*Workflow run wf_66554e4b-ed7, 2026-06-12. 13 agents. Source data: Redash/BigQuery prod analytics.*

---

## universe

### Summary
90-day job universe (jobs created 2026-03-14 through 2026-06-12, BigQuery DS 7, internal users excluded): 4,693,212 jobs from 3,174,166 distinct users across 4,545,588 distinct projects (fork roots) — ~1.48 jobs/user, and ~96.9% of jobs are their own project root (forking is rare and concentrated in dedicated fork_fullstack_prompt_* templates). The job mix is dominated by four template families: general_agent_v0_sonnet_4_5 (612,030 jobs, 13.0%), full_stack_app_builder_cloud_v8_sonnet_4_5 (594,570, 12.7%), expo_fullstack_v0_sonnet_4_5 (573,426, 12.2%), and free_full_stack_app_builder_cloud_v8_opus_4_7 (508,042, 10.8%). Aggregating across model/free variants: full-stack builder variants total roughly 1.47M jobs (~31%), general agent ~1.04M (~22%), Expo (mobile) ~1.03M (~22%), landing page ~450K (~10%), wingman 115,847 (2.5%), replica agent ~76K (1.6%). chat_mode is nearly uniform: 'build' = 97.4% of jobs (4,569,480); '(null)' = 2.5% (115,860 — matches the wingman prompt count almost exactly); brainstorming_requested, chat, and salesman_agent are each ≤0.1%. 12-month trend: platform grew from 433K jobs / 284K users in Jul 2025 to a peak of 1,870,366 jobs / 1,181,353 users in Mar 2026; users peaked in Apr 2026 at 1,250,176, then declined to 1,302,905 jobs / 993,801 users in May 2026; June 2026 is partial (476,043 jobs through June 12, pacing ~1.19M for the month, roughly flat vs May).

### Key numbers

- **Total jobs (2026-03-14 to 2026-06-12)**: 4,693,212
- **Distinct users (same window)**: 3,174,166
- **Distinct projects / fork roots (same window)**: 4,545,588
- **Top prompt_name: general_agent_v0_sonnet_4_5**: 612,030 jobs (13.0%)
- **chat_mode = 'build' share of jobs**: 97.4% (4,569,480 jobs)
- **Peak month jobs (Mar 2026)**: 1,870,366 jobs / 1,181,353 users
- **Peak month users (Apr 2026)**: 1,250,176 users / 1,725,915 jobs
- **May 2026 (last full month)**: 1,302,905 jobs / 993,801 users
- **'other' prompt_name bucket (beyond top 25)**: 402,279 jobs (8.6%)
- **Fork-template jobs (fork_fullstack_prompt_v2 opus 4_5+4_6+4_7)**: 111,788 jobs (2.4%)

### Jobs by prompt_name — top 25 + other (2026-03-14 to 2026-06-12)

| prompt_name | jobs | users | projects | pct_of_jobs |
|---|---:|---:|---:|---:|
| general_agent_v0_sonnet_4_5 | 612,030 | 481,093 | 612,030 | 13.0 |
| full_stack_app_builder_cloud_v8_sonnet_4_5 | 594,570 | 527,935 | 594,570 | 12.7 |
| expo_fullstack_v0_sonnet_4_5 | 573,426 | 502,102 | 573,426 | 12.2 |
| free_full_stack_app_builder_cloud_v8_opus_4_7 | 508,042 | 457,087 | 508,042 | 10.8 |
| other (all prompt_names beyond top 25) | 402,279 | 281,441 | 351,484 | 8.6 |
| free_expo_fullstack_v0_opus_4_7 | 340,693 | 307,110 | 340,693 | 7.3 |
| free_general_agent_v0_opus_4_7 | 322,177 | 273,886 | 322,177 | 6.9 |
| free_landing_page_v0_opus_4_7 | 203,969 | 184,854 | 203,969 | 4.3 |
| full_stack_app_builder_cloud_v8_opus_4_5 | 176,612 | 147,868 | 176,612 | 3.8 |
| landing_page_v1_sonnet_4_5 | 152,205 | 133,731 | 152,205 | 3.2 |
| full_stack_app_builder_cloud_v8_opus_4_7 | 128,843 | 103,454 | 128,843 | 2.7 |
| wingman | 115,847 | 105,710 | 115,847 | 2.5 |
| general_agent_v0_opus_4_7 | 71,562 | 48,223 | 71,562 | 1.5 |
| expo_fullstack_v0_opus_4_7 | 61,846 | 51,531 | 61,846 | 1.3 |
| fork_fullstack_prompt_v2_opus_4_6 | 59,014 | 11,879 | 17,097 | 1.3 |
| landing_page_v0_sonnet_4_5 | 53,855 | 49,904 | 53,855 | 1.1 |
| replica_agent_v0_sonnet_4 | 45,196 | 41,380 | 45,196 | 1.0 |
| full_stack_app_builder_cloud_v8_opus_4_6 | 40,679 | 36,673 | 40,679 | 0.9 |
| landing_page_v0_opus_4_7 | 39,668 | 30,902 | 39,668 | 0.8 |
| general_agent_v0_opus_4_5 | 34,516 | 22,913 | 34,516 | 0.7 |
| free_replica_agent_v0_opus_4_7 | 30,667 | 28,718 | 30,667 | 0.7 |
| fork_fullstack_prompt_v2_opus_4_7 | 28,991 | 9,392 | 11,751 | 0.6 |
| free_expo_fullstack_v0_opus_4_7_design | 25,873 | 23,585 | 25,873 | 0.6 |
| expo_fullstack_v0_opus_4_6 | 25,240 | 23,142 | 25,240 | 0.5 |
| fork_fullstack_prompt_v2_opus_4_5 | 23,783 | 8,743 | 10,688 | 0.5 |
| full_stack_app_builder_cloud_v8_1mil_opus_4_6 | 21,629 | 19,804 | 21,629 | 0.5 |
| **TOTAL** | **4,693,212** | **3,174,166** | **4,545,588** | **100.0** |

### Jobs by chat_mode (2026-03-14 to 2026-06-12)

| chat_mode | jobs | users | projects | pct_of_jobs |
|---|---:|---:|---:|---:|
| build | 4,569,480 | 3,122,651 | 4,425,345 | 97.4 |
| (null) | 115,860 | 105,716 | 115,860 | 2.5 |
| brainstorming_requested | 3,489 | 3,206 | 14 | 0.1 |
| chat | 2,768 | 842 | 2,768 | 0.1 |
| salesman_agent | 1,614 | 1,547 | 1,614 | 0.0 |
| brainstorm | 1 | 1 | 1 | 0.0 |

### Window totals (2026-03-14 to 2026-06-12)

| metric | value |
|---|---:|
| Total jobs | 4,693,212 |
| Distinct users | 3,174,166 |
| Distinct projects (COALESCE(fork_chain.first_job_id, job_id)) | 4,545,588 |
| Jobs per user | 1.48 |

### Monthly jobs and distinct users, Jun 2025 – Jun 2026 (whole platform, internal excluded)

| month | jobs | distinct_users |
|---|---:|---:|
| 2025-06 | 156,469 | 107,701 |
| 2025-07 | 433,264 | 284,126 |
| 2025-08 | 481,565 | 330,182 |
| 2025-09 | 836,298 | 583,772 |
| 2025-10 | 973,384 | 673,380 |
| 2025-11 | 796,243 | 555,514 |
| 2025-12 | 782,023 | 542,657 |
| 2026-01 | 1,208,072 | 798,817 |
| 2026-02 | 1,517,364 | 939,907 |
| 2026-03 | 1,870,366 | 1,181,353 |
| 2026-04 | 1,725,915 | 1,250,176 |
| 2026-05 | 1,302,905 | 993,801 |
| 2026-06 (partial, through Jun 12) | 476,043 | 389,857 |

### Caveats

- 2026-06 in the trend table is partial (Jun 1-12 only, ~12/30 of the month); naive full-month pace is ~1.19M jobs, roughly flat vs May 2026.
- Internal-user exclusion relies on a LEFT JOIN to analytics.signups_raw_dataset; jobs whose user_id has no signup row (or NULL email) are KEPT. Only '%emergent.sh' emails and the one hardcoded test user_id are excluded.
- Per-bucket 'projects' counts can overlap across prompt_name / chat_mode buckets (a fork job maps to a root project whose own job may sit in a different bucket), so the projects column does not sum to the 4,545,588 total. Equality of jobs==projects in most rows means those jobs are absent from fork_chain (not forks).
- fork_chain only contains forked jobs; root projects created BEFORE 2026-03-14 are still counted as project ids when their forks fall in the window (e.g. brainstorming_requested: 3,489 jobs collapse to just 14 root projects — these look like forks of a small set of shared/showcase templates).
- chat_mode '(null)' (115,860 jobs) aligns almost exactly with prompt_name 'wingman' (115,847 jobs) — wingman jobs apparently carry no chat_mode, so 'build' share among non-wingman jobs is ~99.8%.
- pct_of_jobs values are as returned by BigQuery ROUND(...,1); the displayed top-25 percentages sum to ~100 with rounding drift.
- prompt_name encodes template x model x free/paid variant; the 'other' bucket (402,279 jobs, 8.6%) aggregates every prompt_name beyond the top 25 and includes most remaining fork/long-tail/experimental templates (its projects < jobs indicates it contains forked jobs).
- Monthly trend counts jobs by created_at month and is whole-platform (all prompt_names/chat_modes), same exclusions; users are distinct within each month and not deduped across months.

<details><summary>Queries used</summary>

**Window totals: jobs, distinct users, distinct projects (90-day window)**

```sql
WITH base AS (
  SELECT j.id, j.user_id, COALESCE(fc.first_job_id, j.id) AS project_id
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON fc.job_id = j.id
  LEFT JOIN `analytics.signups_raw_dataset` s ON s.user_id = j.user_id
  WHERE j.created_at >= TIMESTAMP('2026-03-14')
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
    AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
)
SELECT COUNT(*) AS total_jobs, COUNT(DISTINCT user_id) AS distinct_users, COUNT(DISTINCT project_id) AS distinct_projects
FROM base
```

**Top 25 prompt_names + 'other' bucket with jobs/users/projects/pct**

```sql
WITH base AS (
  SELECT j.id, j.user_id, COALESCE(j.prompt_name, '(null)') AS prompt_name,
         COALESCE(fc.first_job_id, j.id) AS project_id
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON fc.job_id = j.id
  LEFT JOIN `analytics.signups_raw_dataset` s ON s.user_id = j.user_id
  WHERE j.created_at >= TIMESTAMP('2026-03-14')
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
    AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
),
counts AS (SELECT prompt_name, COUNT(*) AS jobs FROM base GROUP BY 1),
ranked AS (SELECT prompt_name, ROW_NUMBER() OVER (ORDER BY jobs DESC) AS rn FROM counts)
SELECT CASE WHEN r.rn <= 25 THEN b.prompt_name ELSE 'other' END AS prompt_name,
       COUNT(*) AS jobs, COUNT(DISTINCT b.user_id) AS users, COUNT(DISTINCT b.project_id) AS projects,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_jobs
FROM base b JOIN ranked r USING (prompt_name)
GROUP BY 1 ORDER BY jobs DESC
```

**chat_mode breakdown with jobs/users/projects/pct**

```sql
WITH base AS (
  SELECT j.id, j.user_id, COALESCE(j.chat_mode, '(null)') AS chat_mode,
         COALESCE(fc.first_job_id, j.id) AS project_id
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON fc.job_id = j.id
  LEFT JOIN `analytics.signups_raw_dataset` s ON s.user_id = j.user_id
  WHERE j.created_at >= TIMESTAMP('2026-03-14')
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
    AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
)
SELECT chat_mode, COUNT(*) AS jobs, COUNT(DISTINCT user_id) AS users, COUNT(DISTINCT project_id) AS projects,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_jobs
FROM base GROUP BY 1 ORDER BY jobs DESC
```

**Monthly jobs and distinct users, last 12+ months (whole platform)**

```sql
SELECT FORMAT_TIMESTAMP('%Y-%m', j.created_at) AS month,
       COUNT(*) AS jobs, COUNT(DISTINCT j.user_id) AS distinct_users
FROM `analytics.jobs_full_view` j
LEFT JOIN `analytics.signups_raw_dataset` s ON s.user_id = j.user_id
WHERE j.created_at >= TIMESTAMP('2025-06-01')
  AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
  AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
GROUP BY 1 ORDER BY 1
```

</details>


---

## ai_share

### Summary
AI-candidate share of Emergent jobs using keyword filter v1 (BigQuery DS 7, internal users excluded). Last 90 days (2026-03-14 to 2026-06-12): 867,042 of 4,693,212 jobs (18.5%) match the AI filter, created by 600,993 of 3,174,166 distinct users (18.9%), spanning 747,632 of 4,545,588 distinct projects (16.4%, project = COALESCE(fork_chain.first_job_id, job.id), AI if any job in the project matches). Weekly trend over the last 13 weeks (weeks of 2026-03-16 to 2026-06-08) shows AI project share oscillating between 14.4% and 21.9%, with no growth trend — recent weeks sit at 16-18% (week of 2026-06-01: 16.1%; partial week of 2026-06-08: 16.3%). Monthly since 2025-06 the share has been remarkably stable in a 14.6%-21.8% band (peak Oct 2025 at 21.8% and Feb 2026 at 20.3%; trough Aug 2025 at 14.6%); June 2026 partial is 16.1%. Within AI-candidate jobs last 90d, the biggest drivers are generic 'ai'-only mentions (339,764 jobs, 39.2% — matched no specific AI keyword group) and 'agent(s)' (303,452, 35.0%), both known inflators. Specific high-intent signals are smaller: gpt/chatgpt/openai 96,375 (11.1%), claude/anthropic/gemini 75,912 (8.8%), chatbot 48,721 (5.6%), rag/embedding 13,691 (1.6%), image-generation 11,172 (1.3%); tts/voice bucket is 114,845 (13.2%) but dominated by the broad 'voice' keyword. Headline: roughly 1 in 6 projects and nearly 1 in 5 users touch AI-product intent by this heuristic, but the true segment is likely meaningfully smaller pending LLM calibration since the two largest keyword buckets are the noisiest.

### Key numbers

- **AI-candidate jobs, last 90d (2026-03-14 to 2026-06-12)**: 867,042 of 4,693,212 (18.5%)
- **AI-candidate users, last 90d**: 600,993 of 3,174,166 (18.9%)
- **AI-candidate projects, last 90d (any job matches)**: 747,632 of 4,545,588 (16.4%)
- **Weekly AI project share range, last 13 weeks**: 14.4% - 21.9% (latest full week 2026-06-01: 16.1%)
- **Monthly AI project share range since 2025-06**: 14.6% (Aug 2025) - 21.8% (Oct 2025); Jun 2026 partial: 16.1%
- **Top keyword bucket: generic 'ai' only (no specific AI keyword)**: 339,764 jobs (39.2% of AI-candidate)
- **Second keyword bucket: agent(s)**: 303,452 jobs (35.0% of AI-candidate)
- **Provider-name mentions (gpt/chatgpt/openai + claude/anthropic/gemini)**: 96,375 (11.1%) and 75,912 (8.8%)

### 1) Last 90 days (2026-03-14 to 2026-06-12): AI-candidate vs non-AI

| Segment | Jobs | Share of jobs | Distinct users | Share of users | Distinct projects | Share of projects |
|---|---|---|---|---|---|---|
| AI-candidate | 867,042 | 18.5% | 600,993 | 18.9% | 747,632 | 16.4% |
| Non-AI | 3,826,152 | 81.5% | 2,758,681 | 86.9% | 3,797,956 | 83.6% |
| NULL task (counted non-AI) | 18 | 0.0% | 11 | - | 18 | - |
| Total | 4,693,212 | 100% | 3,174,166 | - | 4,545,588 | - |

Notes: user shares overlap (~185.5k users have both AI and non-AI jobs, so segment user shares sum >100%). Project rows use project-level classification (AI if any job in project matches); ~12,865 projects had both AI and non-AI jobs in-window.

### 2) Weekly trend, last 13 weeks (projects, week starting Monday)

| Week start | Total projects | AI-candidate projects | AI share % |
|---|---|---|---|
| 2026-03-16 | 367,491 | 80,380 | 21.9 |
| 2026-03-23 | 510,611 | 87,562 | 17.1 |
| 2026-03-30 | 501,643 | 77,035 | 15.4 |
| 2026-04-06 | 380,454 | 67,245 | 17.7 |
| 2026-04-13 | 403,082 | 59,300 | 14.7 |
| 2026-04-20 | 355,459 | 51,239 | 14.4 |
| 2026-04-27 | 334,784 | 50,875 | 15.2 |
| 2026-05-04 | 301,693 | 49,099 | 16.3 |
| 2026-05-11 | 302,397 | 53,181 | 17.6 |
| 2026-05-18 | 274,074 | 49,462 | 18.0 |
| 2026-05-25 | 275,845 | 47,036 | 17.1 |
| 2026-06-01 | 279,769 | 45,114 | 16.1 |
| 2026-06-08 (partial, thru 06-12) | 190,541 | 31,103 | 16.3 |

### 3) Monthly trend since 2025-06 (projects)

| Month | Total projects | AI-candidate projects | AI share % |
|---|---|---|---|
| 2025-06 | 153,347 | 26,650 | 17.4 |
| 2025-07 | 401,745 | 63,657 | 15.8 |
| 2025-08 | 446,936 | 65,458 | 14.6 |
| 2025-09 | 802,159 | 142,229 | 17.7 |
| 2025-10 | 922,869 | 201,463 | 21.8 |
| 2025-11 | 746,542 | 109,454 | 14.7 |
| 2025-12 | 717,151 | 110,024 | 15.3 |
| 2026-01 | 1,088,120 | 175,425 | 16.1 |
| 2026-02 | 1,341,011 | 272,095 | 20.3 |
| 2026-03 | 1,725,536 | 333,262 | 19.3 |
| 2026-04 | 1,685,671 | 256,730 | 15.2 |
| 2026-05 | 1,281,952 | 216,190 | 16.9 |
| 2026-06 (partial, thru 06-12) | 469,696 | 75,689 | 16.1 |

### 4) Keyword breakdown within AI-candidate jobs, last 90d (n = 867,042; buckets overlap)

| Keyword bucket | Jobs | % of AI-candidate jobs |
|---|---|---|
| Generic 'ai'/'artificial'/'intelligen*' ONLY (no other AI keyword) | 339,764 | 39.2 |
| agent(s) | 303,452 | 35.0 |
| llm / machine learning / generative / gen-ai / copilot | 146,920 | 16.9 |
| tts / voice / whisper / elevenlabs / text-to-speech | 114,845 | 13.2 |
| gpt / chatgpt / openai | 96,375 | 11.1 |
| claude / anthropic / gemini | 75,912 | 8.8 |
| chatbot / chat bot | 48,721 | 5.6 |
| rag / embedding(s) | 13,691 | 1.6 |
| image generation / text-to-image | 11,172 | 1.3 |

### Caveats

- Keyword filter v1 is a heuristic and inflates the count: the two largest buckets are generic 'ai'-only (39.2%) and 'agent(s)' (35.0%). 'agent' matches real-estate/travel/insurance/support agents, and 'ai' fires on unrelated mentions ('AI-powered builder', brand names). LLM-based calibration of true AI-product intent is planned and will likely shrink the segment materially.
- The tts/voice bucket (13.2%) is dominated by the broad keyword 'voice', which matches any voice feature, not specifically AI voice synthesis.
- Project = COALESCE(fork_chain.first_job_id, job.id); fork_chain only contains forked jobs, so unforked jobs are their own project. A project is AI-candidate if ANY of its in-window jobs matches; ~12,865 projects in the 90d window had both AI and non-AI jobs. In weekly/monthly trends a project active in multiple periods is counted in each period it has a job.
- User shares overlap: ~185,508 users created both AI and non-AI jobs in the last 90d, so AI (18.9%) + non-AI (86.9%) user shares exceed 100%.
- Filter applied to first 4,000 chars of task text only; 18 jobs with NULL task counted as non-AI.
- Internal exclusions: emails LIKE '%emergent.sh' (via signups_raw_dataset join; jobs from users without a signup row are retained) and user_id 90e9d382-f842-4e71-82eb-d008a398b7b2.
- Date windows: 90d = 2026-03-14 00:00 UTC to query time 2026-06-12 ~09:50 UTC; the week of 2026-06-08 and the month of 2026-06 are partial. Monthly trend starts 2025-06-01 (platform data starts 2025-05-26).
- jobs_full_view is not partitioned; each 90d query scanned ~10-11 GB, the monthly trend ~33 GB.

<details><summary>Queries used</summary>

**Task 1: last-90d job/user/project split by AI-candidate flag (job-level grouping)**

```sql
WITH jobs AS (
  SELECT j.id, j.user_id, COALESCE(fc.first_job_id, j.id) AS project_id,
    REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)') AS is_ai
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON j.id = fc.job_id
  LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id
  WHERE j.created_at >= TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
    AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
)
SELECT is_ai, COUNT(*) AS job_count, COUNT(DISTINCT user_id) AS distinct_users, COUNT(DISTINCT project_id) AS distinct_projects
FROM jobs GROUP BY is_ai ORDER BY is_ai DESC
```

**Task 1 totals: overall denominators + project-level AI classification (AI if any job in project matches)**

```sql
WITH jobs AS (
  SELECT j.id, j.user_id, COALESCE(fc.first_job_id, j.id) AS project_id,
    IFNULL(REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)'), FALSE) AS is_ai
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON j.id = fc.job_id
  LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id
  WHERE j.created_at >= TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
    AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
),
proj AS (SELECT project_id, LOGICAL_OR(is_ai) AS proj_is_ai FROM jobs GROUP BY project_id)
SELECT
  (SELECT COUNT(*) FROM jobs) AS total_jobs,
  (SELECT COUNT(DISTINCT user_id) FROM jobs) AS total_users,
  (SELECT COUNT(DISTINCT IF(is_ai, user_id, NULL)) FROM jobs) AS ai_users,
  (SELECT COUNT(*) FROM proj) AS total_projects,
  (SELECT COUNTIF(proj_is_ai) FROM proj) AS ai_projects_any_job
```

**Task 2: weekly trend, last 13 weeks (projects per week, AI if any job that week matches)**

```sql
WITH jobs AS (
  SELECT DATE_TRUNC(DATE(j.created_at), WEEK(MONDAY)) AS week_start, COALESCE(fc.first_job_id, j.id) AS project_id,
    IFNULL(REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)'), FALSE) AS is_ai
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON j.id = fc.job_id
  LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id
  WHERE DATE(j.created_at) >= DATE_SUB(DATE_TRUNC(CURRENT_DATE(), WEEK(MONDAY)), INTERVAL 12 WEEK)
    AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
)
SELECT week_start, COUNT(DISTINCT project_id) AS total_projects,
  COUNT(DISTINCT IF(is_ai, project_id, NULL)) AS ai_projects,
  ROUND(100 * COUNT(DISTINCT IF(is_ai, project_id, NULL)) / COUNT(DISTINCT project_id), 1) AS ai_share_pct
FROM jobs GROUP BY week_start ORDER BY week_start
```

**Task 3: monthly trend since 2025-06 (projects per month)**

```sql
WITH jobs AS (
  SELECT DATE_TRUNC(DATE(j.created_at), MONTH) AS month, COALESCE(fc.first_job_id, j.id) AS project_id,
    IFNULL(REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)'), FALSE) AS is_ai
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON j.id = fc.job_id
  LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id
  WHERE DATE(j.created_at) >= '2025-06-01'
    AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
)
SELECT month, COUNT(DISTINCT project_id) AS total_projects,
  COUNT(DISTINCT IF(is_ai, project_id, NULL)) AS ai_projects,
  ROUND(100 * COUNT(DISTINCT IF(is_ai, project_id, NULL)) / COUNT(DISTINCT project_id), 1) AS ai_share_pct
FROM jobs GROUP BY month ORDER BY month
```

**Task 4: keyword-bucket counters within AI-candidate jobs, last 90d (buckets overlap; generic-ai-only = matches generic terms and none of the specific buckets)**

```sql
WITH ai_jobs AS (
  SELECT LOWER(SUBSTR(j.task,1,4000)) AS t
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id
  WHERE j.created_at >= TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
    AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
    AND REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)')
)
SELECT COUNT(*) AS ai_candidate_jobs,
  COUNTIF(REGEXP_CONTAINS(t, r'chat\s?bot')) AS kw_chatbot,
  COUNTIF(REGEXP_CONTAINS(t, r'\bagents?\b')) AS kw_agent,
  COUNTIF(REGEXP_CONTAINS(t, r'(gpt|openai)')) AS kw_gpt_chatgpt_openai,
  COUNTIF(REGEXP_CONTAINS(t, r'(claude|anthropic|gemini)')) AS kw_claude_anthropic_gemini,
  COUNTIF(REGEXP_CONTAINS(t, r'(\brag\b|embeddings?)')) AS kw_rag_embedding,
  COUNTIF(REGEXP_CONTAINS(t, r'(image generation|text[- ]to[- ]image)')) AS kw_image_gen,
  COUNTIF(REGEXP_CONTAINS(t, r'(\btts\b|text[- ]to[- ]speech|whisper|elevenlabs|voice)')) AS kw_tts_voice,
  COUNTIF(REGEXP_CONTAINS(t, r'(\bllm\b|machine learning|generative|gen\s?ai|copilot)')) AS kw_llm_ml_generative,
  COUNTIF(REGEXP_CONTAINS(t, r'(\bai\b|\ba\.i\.|artificial|intelligen|kecerdasan buatan)') AND NOT REGEXP_CONTAINS(t, r'(chat\s?bot|gpt|openai|claude|anthropic|gemini|\bagents?\b|\brag\b|embeddings?|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|\bllm\b|machine learning|generative|gen\s?ai|copilot|voice)')) AS kw_generic_ai_only
FROM ai_jobs
```

</details>


---

## spend

### Summary
COST METHODOLOGY VALIDATED: jobs_full_view.total_credits_deducted_for_task is dead — 0 of 1,302,905 May-2026 jobs (internal excluded) have a nonzero value, and in a deterministic 20-job sample (created 2026-05-01..06-01) all 20 showed jobs_view=0 while SUM(trajectories.value_in_usd) was positive ($0.08–$25.01). Disagreement rate: 20/20 (100%). Canonical cost = SUM(trajectories.value_in_usd) GROUP BY job_id (no duplicate rows: 278,562,924 rows = 278,562,924 distinct ids since 2026-03-14). 99.6% of May jobs have positive trajectory cost, so coverage is near-complete.

90-DAY COST ANALYSIS (jobs created 2026-03-14..2026-06-12, trajectories DATE(created_at)>=2026-03-14, internal users excluded): Total attributed platform spend = $151,668,690 across 4,691,300 jobs with cost. AI-candidate jobs (keyword filter v1 on job task) are 866,627 jobs (18.5% of jobs) but $77,465,065 of spend (51.1%) — non-AI is 3,824,673 jobs at $74,203,625 (48.9%). AI jobs cost more at every percentile: median $9.94 vs $6.54 (1.5x), p75 $26.60 vs $10.11 (2.6x), p90 $152.41 vs $16.69 (9.1x), p99 $1,324 vs $202 (6.6x), mean $89.80 vs $19.50 (4.6x). The AI premium is overwhelmingly a TAIL phenomenon: above p75 AI jobs explode while non-AI stays flat.

PER-PROJECT (fork-rollup, 4,544,055 projects): classification basis matters a lot. By ROOT-job task, AI projects = 714,234 (15.7%) carrying $41.9M (27.6% of spend), p50 $9.73 / p75 $11.17 / p90 $47.14 / p99 $834. By ANY-job-in-chain matching, AI projects = 747,328 (16.4%) carrying $82.2M (54.2% of spend), p50 $9.82 / p75 $11.82 / p90 $73.01 / p99 $2,055. The ~$40M gap sits in just ~33K long fork chains whose root prompt isn't AI but where AI features appear in later prompts — i.e., AI is frequently ADDED to mature, expensive projects (also a length-bias caveat: longer chains have more chances to match keywords). True AI spend share is bracketed at roughly 28%–54%, with job-level classification landing at 51.1%.

TOP AI PROJECTS: the 10 most expensive AI-candidate projects (root-task basis) each burned $56K–$85K in 90 days. They are real, not data errors — e.g., the #8 project is a single job with 49,704 trajectory steps over 2026-04-12..06-12 consuming 11.73B prompt tokens ($57,595, ~$1.16/step). Top use cases: AI communication coach, Bitcoin trading decision engine, arxiv paper-ranking platform, creator-ops AI SaaS, gym-maintenance AI SaaS, Quran memorization app with AI recitation, and an 'AI Learning Companion' SaaS — exactly the AI-product segment under study. These whale projects suggest growth features around long-running AI app development (cost controls, dedicated AI-app templates/integrations, premium tiers).

### Key numbers

- **Validation: sampled jobs where jobs_full_view cost disagrees with trajectories sum (May 2026, n=20)**: 20/20 (100%) — jobs_view = 0 on all; traj sums $0.08–$25.01
- **May-2026 jobs with total_credits_deducted_for_task > 0 (of 1,302,905)**: 0 (0.0%) — field is unusable; canonical = SUM(trajectories.value_in_usd)
- **May-2026 jobs with trajectory cost > 0**: 1,298,327 / 1,302,905 (99.6%)
- **Duplicate check, trajectories_full_view since 2026-03-14**: 278,562,924 rows = 278,562,924 distinct ids (no dupes)
- **Total platform spend, jobs created 2026-03-14..2026-06-12**: $151,668,690 (4,691,300 jobs with cost)
- **AI-candidate share of jobs (90d)**: 866,627 / 4,691,300 = 18.5%
- **AI-candidate share of spend, job-level (90d)**: $77,465,065 / $151,668,690 = 51.1%
- **Median job cost AI vs non-AI (90d)**: $9.94 vs $6.54
- **p90 job cost AI vs non-AI (90d)**: $152.41 vs $16.69 (9.1x)
- **Avg job cost AI vs non-AI (90d)**: $89.80 vs $19.50 (4.6x)
- **AI share of project-level spend, root-task basis (90d)**: $41,881,239 = 27.6% (714,234 projects, 15.7%)
- **AI share of project-level spend, any-job-in-chain basis (90d)**: $82,188,407 = 54.2% (747,328 projects, 16.4%)
- **Most expensive AI-candidate project (90d)**: $85,088 over 329 jobs (AI social-skill coach 'RealTalk')
- **Largest single-job burn (90d)**: $57,595 in 1 job — 49,704 steps, 11.73B prompt tokens, 2026-04-12..06-12
- **Unattributed trajectory spend in window (jobs created before 2026-03-14 or internal)**: $161,528,905 raw − $151,668,690 attributed = ~$9.9M (6.1%)

### Cost methodology validation — 20 deterministic-random jobs created 2026-05-01..2026-06-01 (all 20 disagree)

| job_id | jobs_view_cost | traj_cost (USD) | n_steps | verdict |
|---|---|---|---|---|
| 068d72b1-c242-4e95-a31b-7b2e4b77d2b8 | 0 | 22.28 | 42 | jobs_view zero, traj has cost |
| 072edfce-b5e1-41fe-ba62-ebaf9a92d4e2 | 0 | 2.91 | 18 | jobs_view zero, traj has cost |
| 0c848d08-b2fc-4bf4-9224-1431c6590e71 | 0 | 8.31 | 34 | jobs_view zero, traj has cost |
| 200129b1-3c06-4037-9cdc-cd41b4729ac6 | 0 | 9.84 | 47 | jobs_view zero, traj has cost |
| 30d07034-c60e-40b5-97ff-81a5d999e0a4 | 0 | 18.53 | 33 | jobs_view zero, traj has cost |
| 57f9edbe-e092-4c1c-b31a-6f9812c26ad7 | 0 | 10.02 | 18 | jobs_view zero, traj has cost |
| 5b08c044-0535-45ad-8ec5-2268a1ad8ed4 | 0 | 1.80 | 13 | jobs_view zero, traj has cost |
| 5e11e59e-4220-4e43-8462-5ddf158574b1 | 0 | 17.18 | 32 | jobs_view zero, traj has cost |
| 6846218d-ef6a-40a9-a4ee-28d391a79de6 | 0 | 9.35 | 70 | jobs_view zero, traj has cost |
| 83c7f653-1fba-459e-a8b3-8a7a88f25fd1 | 0 | 17.43 | 24 | jobs_view zero, traj has cost |
| 8b01175f-b124-42f8-aba1-12519895b6ed | 0 | 19.22 | 25 | jobs_view zero, traj has cost |
| 8c46ca6c-3d6e-493f-ab41-c8ae341798d8 | 0 | 3.52 | 18 | jobs_view zero, traj has cost |
| 98369bc9-a5a1-474f-9508-11ba2e5055d7 | 0 | 0.08 | 2 | jobs_view zero, traj has cost |
| a12ffbb1-d698-4336-9609-2966e8d24e44 | 0 | 0.53 | 6 | jobs_view zero, traj has cost |
| a743a255-2166-4efc-a6d9-127d2b595276 | 0 | 25.01 | 39 | jobs_view zero, traj has cost |
| bbcabf90-a333-49c7-b640-bc932a1a7a77 | 0 | 10.02 | 29 | jobs_view zero, traj has cost |
| c1399673-9f04-4067-9483-064db700f92b | 0 | 8.24 | 36 | jobs_view zero, traj has cost |
| c8de5879-11a3-4b69-9609-232d83361e58 | 0 | 8.86 | 42 | jobs_view zero, traj has cost |
| da54a725-1580-4d3a-9e3b-3bc070ab2ce2 | 0 | 9.89 | 62 | jobs_view zero, traj has cost |
| f2814f53-a868-4637-bc20-12ac6cc9ee6d | 0 | 10.95 | 34 | jobs_view zero, traj has cost |

### Per-JOB cost: totals and distribution, AI-candidate vs non-AI (jobs created 2026-03-14..2026-06-12; cost = SUM trajectories.value_in_usd)

| segment | n jobs w/ cost | share of jobs | total USD | share of spend | avg | p25 | p50 | p75 | p90 | p99 |
|---|---|---|---|---|---|---|---|---|---|---|
| AI-candidate | 866,627 | 18.5% | $77,465,065 | 51.1% | $89.80 | $3.85 | $9.94 | $26.60 | $152.41 | $1,324.13 |
| non-AI | 3,824,673 | 81.5% | $74,203,625 | 48.9% | $19.50 | $0.58 | $6.54 | $10.11 | $16.69 | $201.76 |
| TOTAL | 4,691,300 | 100% | $151,668,690 | 100% | $32.33 | — | — | — | — | — |

### Per-PROJECT (fork-rollup) cost distribution, two classification bases (same window; 4,544,055 projects)

| basis | segment | n projects | total USD | share of spend | avg | p50 | p75 | p90 | p99 |
|---|---|---|---|---|---|---|---|---|---|
| root-job task | AI-candidate | 714,234 (15.7%) | $41,881,239 | 27.6% | $58.95 | $9.73 | $11.17 | $47.14 | $834.45 |
| root-job task | non-AI | 3,829,821 (84.3%) | $109,787,451 | 72.4% | $28.80 | $6.62 | $10.14 | $17.56 | $279.06 |
| any job in chain | AI-candidate | 747,328 (16.4%) | $82,188,407 | 54.2% | $110.54 | $9.82 | $11.82 | $73.01 | $2,055.11 |
| any job in chain | non-AI | 3,796,727 (83.6%) | $69,480,283 | 45.8% | $18.39 | $6.54 | $10.10 | $16.25 | $183.16 |

### Top 10 most expensive AI-candidate projects (root task matches filter; cost over 2026-03-14..2026-06-12)

| # | project root id | total cost USD | n jobs | root task (first 150 chars, truncated) |
|---|---|---|---|---|
| 1 | 6b28ff68-b0af-4569-acb5-d0efa05c69f7 | $85,088 | 329 | Logo: Speech Bubble + Handshake. Category: Social Skill & Relationship Coach. RealTalk offers guided communication coaching... |
| 2 | 19a23cc4-c95b-45d3-8b23-37aa6acf7adb | $84,004 | 6 | BUILD A PRODUCTION-GRADE BITCOIN SHORT DECISION PLATFORM. Full-stack Bitcoin SHORT decision engine and market int... |
| 3 | 00b63d16-0456-4fcd-ab0c-6566dc786c34 | $78,389 | 39 | Build a website/platform that fetches the latest scientific papers from arxiv and runs a pairwise tournament on them... |
| 4 | 618cc68e-e7cc-48c1-a22f-c6bde79e2569 | $73,148 | 78 | Build a full SaaS platform called ChamsPilot — AI ops for creators and brand deals. Production-ready app for a US LLC... |
| 5 | 4f5ad877-3cb7-439b-8bca-775b0f025f7e | $72,140 | 114 | Emergent Master Prompt — Build ObeGee (Module-by-Module, Test-Gated, No Drift)... |
| 6 | d0bcf22c-9b6e-469d-a0bc-1cc903e88448 | $68,269 | 4 | Create a premium, modern, conversion-focused SaaS website and business: GymFix AI – The Complete Gym Maintenance Platform... |
| 7 | cd89ada0-48f5-4e90-afd0-0fba6b8e9937 | $58,886 | 61 | i have a proect redeployed to my main site thedoggycompany.com; current agent is soul-concierge.preview.emergentagent.com... |
| 8 | 42becf6a-fad9-4f1b-91cd-6267fd9894cd | $57,595 | 1 | Quran memorization app (partial-ayah highlights, repetition loops, spaced repetition, AI recitation...) — 49,704 steps, 11.73B prompt tokens |
| 9 | 8bc8bbcd-163e-466b-a813-636b03351119 | $56,976 | 73 | Creer une application web et mobile universelle de prise de rendez-vous, de gestion d'activite et de pilotage financier... |
| 10 | 79e0f849-ae16-4223-a41e-f6fd873f3420 | $56,314 | 1 | Build a SaaS web app called "AI Learning Companion" — users enter any skill and it generates a structured learning r... |

### Caveats

- total_credits_deducted_for_task was validated as universally zero only for May-2026 (1.3M jobs) plus the 20-job sample; it may be populated for older periods, but it cannot be trusted anywhere — trajectories SUM(value_in_usd) is canonical throughout.
- First 20-job sample used ORDER BY RAND() inside a CTE referenced twice; BigQuery re-evaluated it per reference, producing a bogus join. Re-run deterministically with FARM_FINGERPRINT(id). Beware this pattern in future queries.
- value_in_usd is reported as-is ('ECU/USD' per spec). Whether it is fully load-bearing USD or ECU-denominated value was not independently verified against billing; absolute totals ($151.7M/90d) should be cross-checked with finance before external use.
- AI-candidate = keyword filter v1 (heuristic, not yet LLM-calibrated). Generic terms (\bagents?\b, 'intelligen', 'artificial') cause false positives; AI apps described without keywords are missed. Treat the 18.5%-of-jobs / 51.1%-of-spend numbers as a calibration-pending estimate.
- Project AI share is definition-sensitive: 27.6% of spend by root-task basis vs 54.2% by any-job-in-chain basis. The gap (~$40M in ~33K projects) reflects both real 'AI added later' behavior and length bias (longer chains have more chances to match keywords). True share is bracketed ~28%–54%.
- Distributions cover jobs/projects with at least one trajectory row in the window (inner join); ~0.4% of jobs have no positive cost and are excluded. ~$9.9M (6.1%) of raw window trajectory spend belongs to jobs created before 2026-03-14 (or internal users) and is excluded from the split.
- Jobs created near 2026-06-12 are still accruing cost; jobs created shortly after 2026-03-14 have full coverage. Per-job task text on forked jobs may include conversation context, which inflates job-level AI matching relative to root-task matching.
- Internal-user exclusion relies on signups_raw_dataset email join; jobs whose user_id has no signup row were kept (email IS NULL passes the filter).

<details><summary>Queries used</summary>

**Validation: 20 deterministic-random May-2026 jobs, jobs_view cost vs trajectories sum**

```sql
WITH sample_jobs AS (SELECT j.id, j.total_credits_deducted_for_task AS jobs_view_cost FROM `analytics.jobs_full_view` j LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id WHERE j.created_at >= TIMESTAMP('2026-05-01') AND j.created_at < TIMESTAMP('2026-06-01') AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh') AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2' ORDER BY FARM_FINGERPRINT(j.id) LIMIT 20), traj AS (SELECT t.job_id, ROUND(SUM(t.value_in_usd),4) AS traj_cost, COUNT(*) AS n_steps FROM `analytics.trajectories_full_view` t JOIN sample_jobs sj ON t.job_id = sj.id WHERE DATE(t.created_at) >= '2026-05-01' GROUP BY 1) SELECT sj.id, ROUND(sj.jobs_view_cost,4) AS jobs_view_cost, tr.traj_cost, tr.n_steps FROM sample_jobs sj LEFT JOIN traj tr ON sj.id = tr.job_id
```

**Validation at scale: all May-2026 jobs — jobs_view nonzero count vs trajectory coverage**

```sql
WITH may_jobs AS (SELECT j.id, j.total_credits_deducted_for_task AS jobs_view_cost FROM `analytics.jobs_full_view` j LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id WHERE j.created_at >= TIMESTAMP('2026-05-01') AND j.created_at < TIMESTAMP('2026-06-01') AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh') AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'), traj AS (SELECT job_id, SUM(value_in_usd) AS traj_cost FROM `analytics.trajectories_full_view` WHERE DATE(created_at) >= '2026-05-01' GROUP BY 1) SELECT COUNT(*) n_jobs, COUNTIF(tr.job_id IS NOT NULL) n_with_traj, COUNTIF(tr.traj_cost>0) n_traj_gt0, COUNTIF(mj.jobs_view_cost>0) n_jobsview_gt0 FROM may_jobs mj LEFT JOIN traj tr ON mj.id = tr.job_id
```

**Duplicate check on trajectories_full_view (90d window)**

```sql
SELECT COUNT(*) n_rows, COUNT(DISTINCT id) n_distinct_ids, ROUND(SUM(value_in_usd),0) raw_sum_usd FROM `analytics.trajectories_full_view` WHERE DATE(created_at) >= '2026-03-14'
```

**Q1+Q2: 90d totals + per-job cost distribution, AI-candidate vs non-AI**

```sql
WITH jobs AS (SELECT j.id, COALESCE(REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)'), FALSE) AS is_ai FROM `analytics.jobs_full_view` j LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id WHERE j.created_at >= TIMESTAMP('2026-03-14') AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh') AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'), costs AS (SELECT job_id, SUM(value_in_usd) AS cost FROM `analytics.trajectories_full_view` WHERE DATE(created_at) >= '2026-03-14' GROUP BY 1), job_costs AS (SELECT jobs.is_ai, c.cost FROM jobs JOIN costs c ON jobs.id = c.job_id) SELECT is_ai, COUNT(*) n_jobs, ROUND(SUM(cost),0) total_usd, ROUND(AVG(cost),2) avg_cost, ROUND(APPROX_QUANTILES(cost,100)[OFFSET(25)],2) p25, ROUND(APPROX_QUANTILES(cost,100)[OFFSET(50)],2) p50, ROUND(APPROX_QUANTILES(cost,100)[OFFSET(75)],2) p75, ROUND(APPROX_QUANTILES(cost,100)[OFFSET(90)],2) p90, ROUND(APPROX_QUANTILES(cost,100)[OFFSET(99)],2) p99 FROM job_costs GROUP BY 1
```

**Q3a: per-project distribution, AI classified by ROOT job task**

```sql
WITH jobs AS (SELECT j.id, COALESCE(fc.first_job_id, j.id) AS project_id FROM `analytics.jobs_full_view` j LEFT JOIN `analytics.fork_chain` fc ON j.id = fc.job_id LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id WHERE j.created_at >= TIMESTAMP('2026-03-14') AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh') AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'), costs AS (SELECT job_id, SUM(value_in_usd) AS cost FROM `analytics.trajectories_full_view` WHERE DATE(created_at) >= '2026-03-14' GROUP BY 1), proj AS (SELECT jobs.project_id, SUM(c.cost) AS cost, COUNT(*) n_jobs FROM jobs JOIN costs c ON jobs.id = c.job_id GROUP BY 1), root AS (SELECT r.id, COALESCE(REGEXP_CONTAINS(LOWER(SUBSTR(r.task,1,4000)), r'<AI_FILTER_V1>'), FALSE) AS is_ai FROM `analytics.jobs_full_view` r WHERE r.id IN (SELECT DISTINCT project_id FROM proj)) SELECT COALESCE(root.is_ai, FALSE) is_ai, COUNT(*) n_projects, ROUND(SUM(p.cost),0) total_usd, ROUND(AVG(p.cost),2) avg_cost, ROUND(APPROX_QUANTILES(p.cost,100)[OFFSET(50)],2) p50, ROUND(APPROX_QUANTILES(p.cost,100)[OFFSET(75)],2) p75, ROUND(APPROX_QUANTILES(p.cost,100)[OFFSET(90)],2) p90, ROUND(APPROX_QUANTILES(p.cost,100)[OFFSET(99)],2) p99 FROM proj p LEFT JOIN root ON p.project_id = root.id GROUP BY 1
```

**Q3b: per-project distribution, AI = ANY in-window job in chain matches**

```sql
WITH jobs AS (SELECT j.id, COALESCE(fc.first_job_id, j.id) AS project_id, COALESCE(REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'<AI_FILTER_V1>'), FALSE) AS is_ai FROM `analytics.jobs_full_view` j LEFT JOIN `analytics.fork_chain` fc ON j.id = fc.job_id LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id WHERE j.created_at >= TIMESTAMP('2026-03-14') AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh') AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'), costs AS (SELECT job_id, SUM(value_in_usd) AS cost FROM `analytics.trajectories_full_view` WHERE DATE(created_at) >= '2026-03-14' GROUP BY 1), proj AS (SELECT jobs.project_id, SUM(c.cost) AS cost, LOGICAL_OR(jobs.is_ai) AS any_ai FROM jobs JOIN costs c ON jobs.id = c.job_id GROUP BY 1) SELECT any_ai, COUNT(*) n_projects, ROUND(SUM(cost),0) total_usd, ROUND(AVG(cost),2) avg_cost, ROUND(APPROX_QUANTILES(cost,100)[OFFSET(50)],2) p50, ROUND(APPROX_QUANTILES(cost,100)[OFFSET(75)],2) p75, ROUND(APPROX_QUANTILES(cost,100)[OFFSET(90)],2) p90, ROUND(APPROX_QUANTILES(cost,100)[OFFSET(99)],2) p99 FROM proj GROUP BY 1
```

**Q4: top 10 most expensive AI-candidate projects with root task snippet**

```sql
WITH jobs AS (SELECT j.id, COALESCE(fc.first_job_id, j.id) AS project_id FROM `analytics.jobs_full_view` j LEFT JOIN `analytics.fork_chain` fc ON j.id = fc.job_id LEFT JOIN `analytics.signups_raw_dataset` s ON j.user_id = s.user_id WHERE j.created_at >= TIMESTAMP('2026-03-14') AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh') AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'), costs AS (SELECT job_id, SUM(value_in_usd) AS cost FROM `analytics.trajectories_full_view` WHERE DATE(created_at) >= '2026-03-14' GROUP BY 1), proj AS (SELECT jobs.project_id, SUM(c.cost) AS cost, COUNT(*) n_jobs FROM jobs JOIN costs c ON jobs.id = c.job_id GROUP BY 1) SELECT p.project_id, ROUND(p.cost,0) total_cost_usd, p.n_jobs, SUBSTR(r.task,1,150) root_task FROM proj p JOIN `analytics.jobs_full_view` r ON r.id = p.project_id WHERE COALESCE(REGEXP_CONTAINS(LOWER(SUBSTR(r.task,1,4000)), r'<AI_FILTER_V1>'), FALSE) ORDER BY p.cost DESC LIMIT 10
```

**Sanity check of largest single-job project (steps, dates, tokens)**

```sql
SELECT COUNT(*) n_steps, MIN(DATE(created_at)) first_day, MAX(DATE(created_at)) last_day, ROUND(SUM(value_in_usd),0) total_usd, ROUND(SUM(prompt_tokens)/1e9,2) prompt_tokens_B FROM `analytics.trajectories_full_view` WHERE DATE(created_at) >= '2026-03-14' AND job_id = '42becf6a-fad9-4f1b-91cd-6267fd9894cd'
```

</details>


---

## seeds_forensics

### Summary
Deep stats on 17 seed AI-product jobs (created 2026-04-25 to 2026-06-10; trajectories filtered created_at >= 2026-04-01, which covers all activity since the earliest seed is 2026-04-25). Key structural finding: NONE of the 17 seeds appear in analytics.fork_chain — every seed is its own project root, and no other job forks from any of them, so every project contains exactly 1 job (project = seed). Cost: total project cost across all 17 = $2,263.85 (SUM value_in_usd from trajectories); median $59.92, mean $133.17. One extreme outlier dominates: b2c9ae48 (team-chat-workspace, full_stack_app_builder_cloud_v8_e3_opus_4_7, Singapore marketing-agency user) cost $1,227.47 over 1,101 steps, 48 HITL interventions and 27.9 hrs — 54.2% of all seed cost. Excluding it, mean = $64.77. The two general_agent seeds are tiny ($0.63 and $5.70); the fullstack-builder seeds cluster $28-153. Engagement: 2,949 total trajectory steps (median 124), 194 HITL interventions (median 9), durations (first-to-last trajectory wall clock) range 0.0-31.9 hrs (median 2.5). Error steps: 0 across all 17 jobs (error_message never populated). Agents: all jobs use only EmergentAssistant and/or SkilledAssistant (14 use both, 3 only EmergentAssistant). Models: 13/17 claude-opus-4-7, plus claude-opus-4-8, claude-sonnet-4-6, claude-sonnet-4-5, and claude-sonnet-4-5?thinking_mode=true (1 each). Deployment: 4/17 (23.5%) deployed, all active hosted apps — team-chat-workspace.emergent.host, weekly-music-app.emergent.host, personal-growth-lab-2.emergent.host, ebook-ai-craft.emergent.host. Only b2c9ae48 has a custom domain: onebrain.team (verified) + www.onebrain.team (unverified), plus 2 unlinked typo domains (onebrain.teams). All 17 jobs have status IN_PROGRESS; all users are external (gmail/business domains, 13 countries — no @emergent.sh).

### Key numbers

- **Seeds that are forks (in fork_chain)**: 0 of 17 — all seeds are project roots
- **Jobs per project**: 1 (all 17 projects; no forks off any seed)
- **Total project cost, all 17 (traj >= 2026-04-01)**: $2,263.85
- **Median / mean project cost**: $59.92 / $133.17 (mean $64.77 excl. top outlier)
- **Top project cost (b2c9ae48, onebrain.team)**: $1,227.47 (54.2% of total)
- **Total trajectory steps / median**: 2,949 / 124
- **Total HITL interventions / median**: 194 / 9
- **Error steps (error_message IS NOT NULL)**: 0 across all 17 jobs
- **Deployed projects**: 4 of 17 (23.5%), all status=active
- **Custom-domain projects**: 1 of 17 (5.9%) — onebrain.team, verified
- **Duration range (first→last trajectory)**: 0.0–31.9 hrs, median 2.5 hrs
- **Dominant model**: claude-opus-4-7 (13/17 seeds)

### MASTER TABLE — 17 seed AI-product jobs (each seed = its own project root; n_jobs_in_project = 1 for all). Cost/steps from trajectories created_at >= 2026-04-01. Sorted by cost desc.

| seed_job_id (=root_project_id) | n_jobs | total_cost_usd | n_steps | n_hitl | n_errors | duration_hrs | deployed | last_activity |
|---|---|---|---|---|---|---|---|---|
| b2c9ae48-27f1-4b32-8ed8-31ff76c703c4 | 1 | 1227.47 | 1101 | 48 | 0 | 27.9 | Y — onebrain.team (custom, verified) + www.onebrain.team (custom, unverified) + team-chat-workspace.emergent.host (hosted); 2 unlinked typo domains (onebrain.teams) | 2026-06-12 01:18 |
| 8b0a90be-e895-42c3-8020-f41e253eb103 | 1 | 152.85 | 124 | 18 | 0 | 22.1 | N | 2026-06-08 04:50 |
| 9c3e8bab-48b6-467c-a80c-83d407d1a07d | 1 | 119.39 | 179 | 20 | 0 | 2.5 | N | 2026-06-07 05:40 |
| 310e0e8a-559d-4303-9bff-0eb24fde289e | 1 | 115.52 | 118 | 14 | 0 | 5.5 | N | 2026-06-04 13:05 |
| 309b5292-a7ef-416d-82af-83cc341c56fb | 1 | 106.71 | 167 | 4 | 0 | 1.7 | N | 2026-06-10 22:39 |
| b96b6695-47f2-44ab-a792-6a2c183e60d7 | 1 | 101.29 | 275 | 17 | 0 | 18.1 | N | 2026-06-10 11:41 |
| e8fbdd8e-9dde-4bc1-bb31-5473be113ed6 | 1 | 93.37 | 194 | 13 | 0 | 31.9 | N | 2026-06-07 15:01 |
| ea1306e8-4ba8-40f3-b742-d6f9b4107fcc | 1 | 84.31 | 136 | 9 | 0 | 11.0 | Y — ebook-ai-craft.emergent.host (hosted, active) | 2026-06-04 22:37 |
| 9bbebcec-5702-4881-92a2-912b6974bc39 | 1 | 59.92 | 118 | 6 | 0 | 0.8 | N | 2026-06-09 08:22 |
| 824ce52e-5f82-4a52-8149-dedf9cf320b0 | 1 | 47.39 | 141 | 17 | 0 | 8.5 | N | 2026-06-06 00:18 |
| d4ee18ab-e518-4c9f-98b1-8f9e22fe8361 | 1 | 43.77 | 150 | 6 | 0 | 0.9 | Y — weekly-music-app.emergent.host (hosted, active) | 2026-06-09 07:49 |
| 1a251bd8-e633-43aa-9b44-60f0608a16f2 | 1 | 38.59 | 56 | 2 | 0 | 0.7 | N | 2026-06-05 15:53 |
| dacb33b5-8b66-4288-8fb8-896f3da838c2 | 1 | 34.70 | 79 | 4 | 0 | 0.9 | Y — personal-growth-lab-2.emergent.host (hosted, active) | 2026-06-10 16:03 |
| 31fcae54-b571-443c-8c85-5b9d32608a0a | 1 | 28.50 | 59 | 3 | 0 | 0.5 | N | 2026-06-08 11:22 |
| 5a1a5743-9a33-4fa0-9294-058496fd9370 | 1 | 5.70 | 37 | 12 | 0 | 6.4 | N | 2026-06-06 22:48 |
| a7324dbd-555d-457d-8df3-a7f642a664c6 | 1 | 3.74 | 10 | 1 | 0 | 0.1 | N | 2026-04-25 15:27 |
| b488a995-01de-478f-bf07-eaeda12b7212 | 1 | 0.63 | 5 | 0 | 0 | 0.0 | N | 2026-06-05 16:46 |
| TOTAL (17) | 17 | 2263.85 | 2949 | 194 | 0 | — | 4 deployed (23.5%) | — |

### Seed metadata — created_at, prompt_name, user, model, agents (all timestamps UTC; all jobs status=IN_PROGRESS; none present in fork_chain)

| seed_job_id | created_at | prompt_name | user_id | country | model(s) | agents used |
|---|---|---|---|---|---|---|
| a7324dbd-555d | 2026-04-25 15:21 | free_full_stack_app_builder_cloud_v8_opus_4_7 | e50e2f69-51fa | France | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| 310e0e8a-559d | 2026-06-04 07:34 | free_full_stack_app_builder_cloud_v8_opus_4_7 | 11d57183-b42d | Italy | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| ea1306e8-4ba8 | 2026-06-04 11:36 | full_stack_app_builder_cloud_v8_opus_4_7 | 9664beb9-0304 | Indonesia | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| 1a251bd8-e633 | 2026-06-05 15:12 | full_stack_app_builder_cloud_v8_opus_4_7 | 91852c29-6145 | Italy | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| 824ce52e-5f82 | 2026-06-05 15:45 | full_stack_app_builder_cloud_v8_sonnet_4_5 | fe259060-69b4 | UAE | claude-sonnet-4-5?thinking_mode=true | EmergentAssistant, SkilledAssistant |
| b488a995-01de | 2026-06-05 16:45 | general_agent_v0_opus_4_7 | bd0b4299-d90b | United States | claude-opus-4-7 | EmergentAssistant only |
| e8fbdd8e-9dde | 2026-06-06 07:06 | free_full_stack_app_builder_cloud_v8_opus_4_7 | 254e2adb-bbf0 | India | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| 5a1a5743-9a33 | 2026-06-06 16:24 | general_agent_v0_sonnet_4_5 | 37e1963a-3bd3 | United Kingdom | claude-sonnet-4-5 | EmergentAssistant only |
| 9c3e8bab-48b6 | 2026-06-07 03:10 | resume_full_stack_v2_sonnet_4_5 | 1cd13a1c-d240 | Cambodia | claude-opus-4-8 | EmergentAssistant only |
| 8b0a90be-e895 | 2026-06-07 06:40 | full_stack_app_builder_cloud_v8_opus_4_7 | ee52f0b4-ca8f | New Zealand | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| 31fcae54-b571 | 2026-06-08 10:54 | full_stack_app_builder_cloud_v8_opus_4_7 | 53454c23-85f2 | India | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| d4ee18ab-e518 | 2026-06-09 06:52 | full_stack_app_builder_cloud_v8_opus_4_7 | 7dad19eb-e1f7 | United States | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| 9bbebcec-5702 | 2026-06-09 07:35 | full_stack_app_builder_cloud_v8_opus_4_7 | c5f48c52-70a2 | United States | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| b96b6695-47f2 | 2026-06-09 17:31 | infinite_fullstack_prompt_v2_sonnet_4_6 | aa1ef20f-bc81 | India | claude-sonnet-4-6 | EmergentAssistant, SkilledAssistant |
| dacb33b5-8b66 | 2026-06-10 15:10 | free_full_stack_app_builder_cloud_v8_opus_4_7 | a5d9f0c7-999b | Sweden | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| 309b5292-a7ef | 2026-06-10 20:58 | full_stack_app_builder_cloud_v8_opus_4_7 | d662f9ea-e69c | Kenya | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |
| b2c9ae48-27f1 | 2026-06-10 21:24 | full_stack_app_builder_cloud_v8_e3_opus_4_7 | c306f97d-174d | Singapore (carrionmarketing.com) | claude-opus-4-7 | EmergentAssistant, SkilledAssistant |

### Deployment detail (analytics.deployer_db_data, all rows for seed job_ids)

| job_id | app_name | domain_name | type | status | verified | deploy created_at |
|---|---|---|---|---|---|---|
| b2c9ae48 | team-chat-workspace | onebrain.team | custom_domain | active | true | 2026-06-11 15:33 |
| b2c9ae48 | team-chat-workspace | www.onebrain.team | custom_domain | active | false | 2026-06-11 15:33 |
| b2c9ae48 | team-chat-workspace | team-chat-workspace.emergent.host | hosted | active | — | 2026-06-11 15:33 |
| b2c9ae48 | team-chat-workspace | onebrain.teams / www.onebrain.teams | unlinked_custom_domain (x2) | unlinked | — | 2026-06-11 15:33 |
| d4ee18ab | weekly-music-app | weekly-music-app.emergent.host | hosted | active | — | 2026-06-09 07:28 |
| dacb33b5 | personal-growth-lab-2 | personal-growth-lab-2.emergent.host | hosted | active | — | 2026-06-10 15:31 |
| ea1306e8 | ebook-ai-craft | ebook-ai-craft.emergent.host | hosted | active | — | 2026-06-04 22:37 (deduction 22:08) |

### Caveats

- Trajectory partition filter used was created_at >= '2026-04-01' (not '2026-03-01' as first suggested): the earliest seed was created 2026-04-25 and all 17 seeds are project roots, so no project activity can predate April; the window is lossless.
- No project has more than 1 job: none of the 17 seeds appear in fork_chain (as job_id) and no job in jobs_full_view has any of them as first_job_id. Project-level numbers therefore equal seed-job-level numbers. If 'project' should also include other independent jobs by the same user (not fork-linked), that is a different definition not computed here.
- n_errors = 0 for ALL 17 jobs (2,949 steps): error_message in trajectories_full_view appears to be very sparsely populated, so 0 should be read as 'no recorded error steps', not proof of error-free runs.
- duration_hrs is wall-clock span MIN→MAX trajectory created_at; it includes idle time waiting for user HITL responses (e.g., e8fbdd8e: 31.9 hrs for 194 steps), not active compute time.
- All 17 jobs have status IN_PROGRESS — apparently the resting state for chat-mode builder jobs, so it does not indicate active work; last_activity is the better recency signal.
- HITL definition used: steps with ARRAY_LENGTH(user_messages_array)>0 OR human_message IS NOT NULL, as specified; a single intervention spanning multiple steps could be counted more than once.
- 9c3e8bab has prompt_name resume_full_stack_v2_sonnet_4_5 but model_name claude-opus-4-8 — prompt template name and actual model can disagree.
- Deployment join was on the seed job_ids directly (equivalent to 'any job in project' since each project has exactly 1 job). Deployments may also exist under other jobs of the same user that are outside these fork chains.
- No internal users in the seed set: all 17 user emails are external (mostly gmail.com; one carrionmarketing.com); none @emergent.sh, none the excluded test user_id.

<details><summary>Queries used</summary>

**Q1: Seed job metadata + fork_chain root check (is seed a fork? first_job_id?)**

```sql
WITH seeds AS (SELECT id FROM UNNEST([...17 ids...]) AS id)
SELECT s.id AS seed_job_id, j.created_at, j.prompt_name, j.user_id, j.status,
  fc.parent_job_id, fc.first_job_id, COALESCE(fc.first_job_id, s.id) AS root_project_id
FROM seeds s
LEFT JOIN `analytics.jobs_full_view` j ON j.id = s.id
LEFT JOIN `analytics.fork_chain` fc ON fc.job_id = s.id
ORDER BY j.created_at
```

**Q2: Project membership — count jobs and distinct models per root (COALESCE(fc.first_job_id, j.id) = root)**

```sql
WITH roots AS (SELECT id FROM UNNEST([...17 ids...]) AS id),
proj_jobs AS (
  SELECT COALESCE(fc.first_job_id, j.id) AS root_id, j.id AS job_id, j.model_name, j.created_at
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON fc.job_id = j.id
  WHERE COALESCE(fc.first_job_id, j.id) IN (SELECT id FROM roots))
SELECT root_id, COUNT(DISTINCT job_id) AS n_jobs_in_project,
  STRING_AGG(DISTINCT model_name, ', ') AS models_used,
  MIN(created_at) AS first_job_created, MAX(created_at) AS last_job_created
FROM proj_jobs GROUP BY root_id
```

**Q3: Per-project trajectory aggregates — cost, steps, agents, HITL, errors, duration (partition-filtered)**

```sql
SELECT job_id, ROUND(SUM(value_in_usd),2) AS total_cost_usd, COUNT(*) AS n_steps,
  COUNT(DISTINCT agent_name) AS n_distinct_agents, STRING_AGG(DISTINCT agent_name, ', ') AS agent_names,
  COUNTIF(ARRAY_LENGTH(user_messages_array)>0 OR human_message IS NOT NULL) AS n_hitl,
  COUNTIF(error_message IS NOT NULL) AS n_errors,
  MIN(created_at) AS first_activity, MAX(created_at) AS last_activity,
  ROUND(TIMESTAMP_DIFF(MAX(created_at), MIN(created_at), MINUTE)/60.0, 1) AS duration_hrs
FROM `analytics.trajectories_full_view`
WHERE created_at >= TIMESTAMP('2026-04-01') AND job_id IN ([...17 ids...])
GROUP BY job_id ORDER BY total_cost_usd DESC
```

**Q4: Deployment check for all project job ids**

```sql
SELECT job_id, status, type, domain_name, app_name, verified, created_at, deduction_date
FROM `analytics.deployer_db_data`
WHERE job_id IN ([...17 ids...])
ORDER BY job_id, created_at
```

**Q5: Internal-user check on the 17 seed users (email domain + country)**

```sql
SELECT user_id, REGEXP_EXTRACT(email, r'@(.+)$') AS email_domain, country
FROM `analytics.signups_raw_dataset`
WHERE user_id IN ([...17 user_ids...])
```

</details>


---

## seed_users

### Summary
Profiled all 17 seed users (data window: platform start 2025-05-26 through 2026-06-12; "90d" = 2026-03-14 to 2026-06-12). PAYING: 16/17 have revenue > $0 (only jcastilla358 / c5f48c52 has $0, despite an active Standard subscription). However, 5 of those 16 have exactly $1.00 total (intro-offer-priced first month), so only 11/17 have paid more than $1. LTV: median across all 17 = $5.24; median among the 16 payers = $6.62; mean = $1,427.51; total cohort revenue = $24,267.72. Revenue is extremely concentrated: the top 4 users (c306f97d $12,970; bd0b4299 $7,410.88; ee52f0b4 $2,365; d662f9ea $1,151) hold $23,896.88 = 98.5% of cohort LTV, and topups dominate (cohort topup $22,835.37 vs subscription $1,432.35 = 94.1% topup). ACTIVITY: 17/17 created a job in the last 14 days (earliest last-job date is 2026-06-04); the cohort skews very recent — 9 of 17 signed up in May–June 2026. SUBSCRIPTIONS: 14 active Emergent Standard, 2 Standard initiated_cancellation, 1 Pro cancelled (c306f97d, cancelled 2026-01-07 but still building heavily on topups — 23 jobs and $13,000.63 platform spend in the last 90d). AI-CANDIDATE MIX: 76 of 122 cohort jobs in the last 90d match the AI-product keyword filter = 62.3%; 13/17 users have at least one AI-candidate job in 90d; the two biggest spenders are heavily AI (bd0b4299: 84.0% of 50 jobs; ee52f0b4: 43.8% of 16 jobs). 90d PLATFORM SPEND (SUM value_in_usd from trajectories): cohort total $61,003.57, led by bd0b4299 $29,196.00, c306f97d $13,000.63, ee52f0b4 $12,617.26 — note for these whales 90d platform LLM cost exceeds their all-time revenue, which deserves a margin check.

### Key numbers

- **Seed users paying (total revenue > $0, all-time to 2026-06-12)**: 16 of 17 (94.1%)
- **Seed users paying more than $1 all-time**: 11 of 17 (64.7%)
- **Median LTV across all 17**: $5.24
- **Median LTV among 16 payers**: $6.62
- **Mean LTV / total cohort revenue**: $1,427.51 / $24,267.72
- **Active in last 14 days (job created since 2026-05-29)**: 17 of 17 (100.0%)
- **Topup share of cohort revenue**: 94.1% ($22,835.37 topup vs $1,432.35 subscription)
- **Top-4 users' share of cohort LTV**: 98.5% ($23,896.88 of $24,267.72)
- **AI-candidate share of cohort 90d jobs (2026-03-14 to 2026-06-12)**: 62.3% (76 of 122 jobs)
- **Cohort 90d platform spend (SUM value_in_usd, 2026-03-14 to 2026-06-12)**: $61,003.57
- **Latest subscription state**: 14 active Standard, 2 Standard initiated_cancellation, 1 Pro cancelled

### Master table — 17 seed users (all-time through 2026-06-12; 90d = 2026-03-14 to 2026-06-12)

| User (short id) | Email | Signup | Country | Device | UTM source | Sub rev $ | Topup rev $ | Total LTV $ | Latest sub (status) | Proj all-time | Proj 90d | Jobs 90d | AI jobs 90d (share) | Last job | 90d spend $ |
|---|---|---|---|---|---|---:|---:|---:|---|---:|---:|---:|---|---|---:|
| c306f97d | arthur@carrionmarketing.com | 2025-06-26 | Singapore | Desktop | — | 1,120.00 | 11,750.00 | 12,970.00 | Pro (cancelled 2026-01-07) | 68 | 22 | 23 | 11 (47.8%) | 2026-06-10 | 13,000.63 |
| bd0b4299 | stewartlakia@gmail.com | 2026-01-06 | United States | Mobile Web | facebook | 120.88 | 7,290.00 | 7,410.88 | Standard (active) | 13 | 11 | 50 | 42 (84.0%) | 2026-06-05 | 29,196.00 |
| ee52f0b4 | enki.ea.nz@gmail.com | 2026-05-08 | New Zealand | Mobile Web | google | 25.00 | 2,340.00 | 2,365.00 | Standard (active) | 16 | 16 | 16 | 7 (43.8%) | 2026-06-09 | 12,617.26 |
| d662f9ea | doreen.zaki@gmail.com | 2026-05-31 | Kenya | Desktop | emergent-badge | 1.00 | 1,150.00 | 1,151.00 | Standard (active) | 2 | 2 | 2 | 0 (0.0%) | 2026-06-10 | 3,750.14 |
| 37e1963a | creovisualsukmarketing@gmail.com | 2026-02-17 | United Kingdom | Desktop | — | 15.00 | 300.00 | 315.00 | Standard (active) | 3 | 3 | 6 | 4 (66.7%) | 2026-06-07 | 1,338.32 |
| 11d57183 | antonio.castronuovo@gmail.com | 2025-12-28 | Italy | Mobile Web | google | 15.00 | 0.00 | 15.00 | Standard (active) | 2 | 1 | 1 | 1 (100.0%) | 2026-06-04 | 115.52 |
| 9664beb9 | dafayodigital@gmail.com | 2025-11-19 | Indonesia | Desktop | — | 15.00 | 0.00 | 15.00 | Standard (active) | 3 | 2 | 2 | 1 (50.0%) | 2026-06-04 | 84.69 |
| 53454c23 | bharathkrishna305@gmail.com | 2026-05-18 | India | Desktop | google | 2.62 | 5.37 | 7.99 | Standard (active) | 4 | 4 | 4 | 3 (75.0%) | 2026-06-08 | 182.50 |
| aa1ef20f | dhyaniumang@gmail.com | 2026-05-01 | India | Desktop | google | 5.24 | 0.00 | 5.24 | Standard (active) | 3 | 3 | 3 | 1 (33.3%) | 2026-06-09 | 209.46 |
| 91852c29 | federicosecci.ceo@gmail.com | 2026-05-29 | Italy | Desktop | tutorial | 5.00 | 0.00 | 5.00 | Standard (initiated_cancellation) | 2 | 2 | 2 | 1 (50.0%) | 2026-06-05 | 45.39 |
| 254e2adb | (null) | 2026-06-06 | India | Desktop | google | 2.61 | 0.00 | 2.61 | Standard (initiated_cancellation) | 1 | 1 | 1 | 1 (100.0%) | 2026-06-06 | 93.37 |
| a5d9f0c7 | l.a.hennix@gmail.com | 2026-06-10 | Sweden | Desktop | — | 1.00 | 0.00 | 1.00 | Standard (active) | 2 | 2 | 2 | 2 (100.0%) | 2026-06-10 | 51.78 |
| 1cd13a1c | ream34494@gmail.com | 2026-06-07 | Cambodia | Desktop | google | 1.00 | 0.00 | 1.00 | Standard (active) | 2 | 2 | 2 | 0 (0.0%) | 2026-06-07 | 119.53 |
| fe259060 | aimaganti8@gmail.com | 2026-06-05 | United Arab Emirates | Desktop | — | 1.00 | 0.00 | 1.00 | Standard (active) | 2 | 2 | 2 | 1 (50.0%) | 2026-06-07 | 59.91 |
| 7dad19eb | westoverjames6@gmail.com | 2026-06-05 | United States | Desktop | — | 1.00 | 0.00 | 1.00 | Standard (active) | 3 | 3 | 3 | 1 (33.3%) | 2026-06-09 | 51.09 |
| e50e2f69 | zarhama59@gmail.com | 2026-04-25 | France | Mobile Web | — | 1.00 | 0.00 | 1.00 | Standard (active) | 2 | 2 | 2 | 0 (0.0%) | 2026-06-07 | 28.06 |
| c5f48c52 | jcastilla358@gmail.com | 2025-09-20 | United States | — | google | 0.00 | 0.00 | 0.00 | Standard (active) | 2 | 1 | 1 | 0 (0.0%) | 2026-06-09 | 59.92 |

### Cohort aggregates

| Metric | Value | Window |
|---|---|---|
| Users paying (> $0) | 16 / 17 (94.1%) | all-time to 2026-06-12 |
| Users paying (> $1) | 11 / 17 (64.7%) | all-time to 2026-06-12 |
| Median LTV (all 17 / 16 payers) | $5.24 / $6.62 | all-time to 2026-06-12 |
| Mean LTV | $1,427.51 | all-time to 2026-06-12 |
| Total revenue (sub / topup / total) | $1,432.35 / $22,835.37 / $24,267.72 | all-time to 2026-06-12 |
| Active in last 14 days (job since 2026-05-29) | 17 / 17 (100.0%) | 2026-05-29 to 2026-06-12 |
| Total jobs / AI-candidate jobs / share | 122 / 76 / 62.3% | 2026-03-14 to 2026-06-12 |
| Users with ≥1 AI-candidate job in 90d | 13 / 17 (76.5%) | 2026-03-14 to 2026-06-12 |
| Total platform spend (SUM value_in_usd) | $61,003.57 | 2026-03-14 to 2026-06-12 |
| Signed up in May–Jun 2026 | 9 / 17 (52.9%) | — |

### Caveats

- 90d platform spend (trajectories.value_in_usd) exceeds all-time revenue for the three whales (bd0b4299: $29,196 spend vs $7,411 LTV; ee52f0b4: $12,617 vs $2,365; d662f9ea: $3,750 vs $1,151). value_in_usd is per-step cost, not user billing — either these users are heavily margin-negative or value_in_usd is denominated above raw cost; worth verifying before drawing margin conclusions.
- Five users have exactly $1.00 total revenue (intro/promo-priced first subscription month), so 'paying' is sensitive to threshold: 16/17 at >$0 but only 11/17 at >$1.
- c5f48c52 shows an active Emergent Standard subscription event (latest 2026-06-09) but $0 in user_revenue_events — likely a comped/promo subscription or a missing revenue event.
- AI-candidate classification uses the v1 keyword regex on the first 4,000 chars of the job task — heuristic, not yet LLM-calibrated; both false positives ('agents' is generic) and multilingual false negatives are possible.
- 90d spend includes trajectory steps dated 2026-03-14+ regardless of when the parent job was created, so it can include continued work on older jobs (relevant for c306f97d and bd0b4299 who have long histories).
- 254e2adb has a null email in signups_raw_dataset, so the internal-email exclusion could not be checked for that user (the user_id is not the known internal id).
- Median LTV of $5.24 is heavily skewed by the 9 users who signed up in May–June 2026 and have had little time to accrue revenue; cohort-level mean ($1,427.51) is dominated by 4 users.
- c306f97d's latest subscription is Pro cancelled (2026-01-07), but the user remains highly active funded by topups — 'cancelled' here does not mean churned.

<details><summary>Queries used</summary>

**Signup date, country, device type, utm_source, email for the 17 seed users**

```sql
SELECT user_id, CAST(created_at AS STRING) AS signup_at, country, device_type, utm_source, email FROM `analytics.signups_raw_dataset` WHERE user_id IN (<17 seed ids>)
```

**All-time revenue split subscription vs topup per user**

```sql
SELECT user_id, ROUND(SUM(CASE WHEN mode='subscription' THEN amount ELSE 0 END),2) AS subscription_rev, ROUND(SUM(CASE WHEN mode='topup' THEN amount ELSE 0 END),2) AS topup_rev, ROUND(SUM(amount),2) AS total_rev FROM `analytics.user_revenue_events` WHERE user_id IN (<17 seed ids>) GROUP BY user_id
```

**Latest subscription tier + status per user**

```sql
SELECT user_id, tier_name, status, billing_period, CAST(created_at AS STRING) AS event_at FROM `analytics.subscription_events` WHERE user_id IN (<17 seed ids>) QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) = 1
```

**Projects all-time and 90d (fork_chain rollup), 90d jobs, AI-candidate 90d jobs (keyword filter v1), last job date**

```sql
WITH jobs AS (SELECT j.id, j.user_id, j.created_at, COALESCE(fc.first_job_id, j.id) AS project_id, REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)') AS is_ai FROM `analytics.jobs_full_view` j LEFT JOIN `analytics.fork_chain` fc ON fc.job_id = j.id WHERE j.user_id IN (<17 seed ids>)) SELECT user_id, COUNT(DISTINCT project_id) AS projects_all_time, COUNT(DISTINCT IF(created_at >= TIMESTAMP('2026-03-14'), project_id, NULL)) AS projects_90d, COUNTIF(created_at >= TIMESTAMP('2026-03-14')) AS jobs_90d, COUNTIF(created_at >= TIMESTAMP('2026-03-14') AND is_ai) AS ai_jobs_90d, COUNT(*) AS jobs_all_time, CAST(MAX(created_at) AS STRING) AS last_job_at FROM jobs GROUP BY user_id
```

**90d platform spend per user from trajectories (partition-filtered)**

```sql
SELECT j.user_id, ROUND(SUM(t.value_in_usd),2) AS spend_90d_usd FROM `analytics.trajectories_full_view` t JOIN `analytics.jobs_full_view` j ON j.id = t.job_id WHERE DATE(t.created_at) >= '2026-03-14' AND j.user_id IN (<17 seed ids>) GROUP BY j.user_id
```

</details>


---

## whales

### Summary
BIG AI jobs/users analysis, DS 7 BigQuery, window = trajectories with DATE(created_at) between 2026-03-14 and 2026-06-12 (90d). Cost = SUM(value_in_usd) per job, rolled up to root project via fork_chain (verified: 1 row per job_id, no join fan-out; trajectory ids unique). HITL steps = trajectory rows with human_message IS NOT NULL (user_messages_array carries forward across steps and over-counts ~7x, so it was rejected).

(1) TOP 100 PROJECTS: combined 90d cost $5,565,893.90, range $40,301.22 (rank 100) to $158,667.55 (rank 1, a firmware-debugging project). Full table below with root job id, cost, n jobs, HITL steps, user_id, AI-candidate flag (keyword v1 on root task) and 200-char root task.

(2) AI-CANDIDATE SHARE OF TOP 100: 28 of 100 projects (28.0%) are AI-candidate by root-task keyword; they account for $1,548,287.13 of $5,565,893.90 = 27.8% of combined top-100 spend. So roughly 1 in 4 whale-project dollars already goes to AI-product builds (AI coaching apps, AI SaaS like ChamsPilot/GymFix AI/HandymanAdmin, agent directories, AI learning companions, LLM-driven market-intelligence platforms).

(3) TOP 50 USERS: combined 90d spend $4,650,856 (top user 21e6b39e, Poland, $171,042.13). Combined revenue paid to date by these 50 users: ~$1,076,351 (range $6,253-$44,021/user). Using the literal definition (>50% of their jobs AI-candidate by keyword on each job's task), 42 of 50 whales (84.0%) are "primarily AI builders". HOWEVER this job-level flag is heavily inflated: fork-job task text contains agent-generated handoff/analysis prose that mentions "agent"/"AI" — 92.3% of fork jobs get flagged platform-wide vs only 15.7% of root jobs. Re-scoring whales on the share of their PROJECTS whose ROOT task is AI-candidate gives 10 of 50 (20.0%) primarily-AI builders. The true number lies between 20% and 84% and needs the planned LLM calibration; the root-project measure is the more trustworthy floor.

### Key numbers

- **Date window (trajectories partition filter)**: 2026-03-14 to 2026-06-12 (90 days)
- **Top-100 projects combined 90d cost**: $5,565,893.90
- **Top-100 cost range (rank 100 / rank 1)**: $40,301.22 / $158,667.55
- **AI-candidate projects in top 100 (root-task keyword)**: 28 of 100 (28.0%)
- **AI-candidate share of top-100 combined spend**: $1,548,287.13 (27.8%)
- **Top-50 users combined 90d spend**: ~$4,650,856
- **Top-50 users combined revenue paid to date**: ~$1,076,351
- **Whales primarily AI by job-level flag (>50% of jobs)**: 42 of 50 (84.0%)
- **Whales primarily AI by root-project flag (>50% of projects)**: 10 of 50 (20.0%)
- **Keyword flag rate: fork jobs vs root jobs (all costed jobs in window)**: 92.3% vs 15.7% — fork-task handoff text inflates job-level AI share
- **Top whale user**: 21e6b39e-ce89-4751-b28a-20616450c4dc: $171,042.13 spend, Poland, $40,241 revenue to date

### Top 100 projects by 90d cost (fork-rollup of SUM(value_in_usd), 2026-03-14 to 2026-06-12)

| # | root job id (project) | cost USD | n jobs | HITL steps | user_id | AI? | root task (first 200 chars, cleaned) |
|---|---|---|---|---|---|---|---|
| 1 | 002ef22d-543e-4231-8102-53193df32e13 | 158,667.55 | 28 | 3,991 | a58ff9de-8aed-4a83-a6ff-78e85643842e | no | Compare the original firmware to the one with bootloader and tell me why the new firmware does not boot up successfully |
| 2 | 1504d533-41e6-47af-9b4e-dfe48f2f5ccf | 119,967.11 | 90 | 3,072 | f8a890d0-39b5-4efb-a052-a2b6e552ac70 | no | Let's continue building my platform. Please pull up a handoff to continue building upon. |
| 3 | 03703cf1-395f-4222-b9df-9899be61c29e | 99,390.21 | 57 | 3,611 | 7aa60b28-23ef-4f2b-a205-cfc63333dc42 | no | Build me An operations management app and instruction how to set up and use. Need the week in gant view |
| 4 | 25a6efb4-4a87-428b-9503-ec180c71eb4d | 92,743.38 | 3 | 8,827 | 10738fc2-ce97-47f3-83b1-02c460212521 | no | lest fix my deployed app |
| 5 | 6b28ff68-b0af-4569-acb5-d0efa05c69f7 | 85,190.12 | 330 | 5,280 | 105a7254-f869-4ee0-8f2d-f5a7ac5dc2ec | YES | Logo: (Speech Bubble + Handshake) Category: Social Skill & Relationship Coach. Why It's Crucial: RealTalk offers guided communication coaching using generative AI and interactive scenarios |
| 6 | 19a23cc4-c95b-45d3-8b23-37aa6acf7adb | 84,003.86 | 6 | 1,317 | c7eaed00-4f57-4566-b65f-cfeacda12ec9 | YES | BUILD A PRODUCTION-GRADE BITCOIN SHORT DECISION PLATFORM. You are building a full-stack, production-grade Bitcoin SHORT decision engine and market intelligence platform. This is NOT a generic crypto |
| 7 | e66e82f0-9955-4ff5-9624-fdf0bd146ce3 | 83,799.67 | 2 | 4,281 | 1290386d-9fed-423e-9188-2b3ffecd8467 | no | Build me a foreign exchange spot and hedging app that looks like Netdana, and you can have subaccounts for clients of investment managers. |
| 8 | 00b63d16-0456-4fcd-ab0c-6566dc786c34 | 78,640.07 | 40 | 4,889 | d0f17064-8f57-48f0-b909-aeffd7f965af | YES | Build a website/platform that fetches the latest scientific papers from arxiv (sorted by different topic) and then runs a pairwise tournament on them to output a ranked list (e.g. based on Bradley-Ter |
| 9 | 9aeff7b6-f2e4-4eb2-aa51-7cee526cd96f | 78,041.75 | 9 | 2,696 | d61212ed-09be-430b-935a-73dc338de342 | no | Build RevOS - a Revenue Operating System SaaS. TECH STACK: Frontend: Next.js 14 with TypeScript; Backend: FastAPI Python; Database: PostgreSQL (Supabase); Auth: JWT |
| 10 | e6cf88a6-1d25-4bfc-9177-2b648798bdff | 77,828.00 | 106 | 3,781 | a71ccf52-d588-4962-af52-bc8ad87f3b62 | no | ich will eine App-Website diese soll folgendes koennen: Betreutes Wohnen Light-App. Fuer alleinlebende Senioren (auch ohne Pflegevertrag). Eine digitale Begleit-App fuer aeltere Menschen |
| 11 | e510f2e1-59ad-40c5-8bb7-d772912e5bc4 | 76,779.12 | 45 | 4,627 | 4bf75d3c-ed32-4e1e-ba13-b0b11fc3e829 | no | Yes. Below is a complete revised Emergent prompt that includes the new business model: Free weekly automated reports for everyone in Japan. 300 yen/month only for daily reports, scheduled custom re |
| 12 | 995ac941-a205-470c-9a17-125c8fbffd2a | 76,679.92 | 11 | 3,502 | f20389aa-75bc-4433-86ae-19c97b6c9cb3 | no | PROJE TURU: Prototype degil. Fake data degil. Mock servis degil. Gercek backend baglantili, production mantiginda, full-stack kurumsal operasyon ve B2B yonetim sistemi gelistir. |
| 13 | ecd92477-8025-48a2-8002-572efb143fbd | 73,376.80 | 41 | 4,978 | d8461c1c-9002-40aa-8648-a8b322542ec6 | no | I need you to rebuild a Field Service Management ERP as a pure Next.js web application with multi-tenant SaaS architecture that I can resell to multiple businesses. I have complete docume |
| 14 | 618cc68e-e7cc-48c1-a22f-c6bde79e2569 | 73,271.85 | 79 | 4,092 | 5a56d82a-de09-4693-9b70-38eaaa6e7a2d | YES | Build a full SaaS platform called ChamsPilot - AI ops for creators and brand deals. This is a production-ready app for a US LLC called CHAMS GLOBAL GROUP LLC |
| 15 | 4f5ad877-3cb7-439b-8bca-775b0f025f7e | 73,023.12 | 115 | 4,430 | daddf41e-b1e0-4bdf-9af0-47d2884e3f02 | YES | # Emergent Master Prompt - Build ObeGee (Module-by-Module, Test-Gated, No Drift). Copy/paste everything below into Emergent. You are the Emergent Build Agent for the |
| 16 | 2d071718-87e9-47ab-8102-846decb2ce5c | 73,000.91 | 131 | 3,531 | 6363871c-7bce-425f-a4cb-48f2b4f7fc9a | no | Oncelikle mimari kurallari oku. Ardindan, yeni portfoy olusturma sayfasinda en sonda on izleme bolumu yok. On izleme bolumu olusturulmasi lazim. |
| 17 | d0bcf22c-9b6e-469d-a0bc-1cc903e88448 | 68,269.03 | 4 | 2,294 | 1af92a1e-1dde-4b46-98d2-aaa7e0fcfb04 | YES | Create a premium, modern, conversion-focused SaaS website and business called: GymFix AI - The Complete Gym Maintenance Platform. This platform must be a one-stop shop for gym maintenance, cleaning |
| 18 | b4d97e65-2942-4ed2-ba68-fddd169b4af8 | 68,266.10 | 10 | 3,174 | 71e515fa-9427-4f08-ad7f-56d4e1f9ea58 | no | Build a complete Crew Activity Management System with the following requirements: 1. Create the following data models: RotationType, rotation_name (string), rotation_work (number) |
| 19 | f420bea8-766d-4bc4-b2fd-ab606e7552af | 65,852.90 | 44 | 2,882 | 0eac1e19-3618-4673-a6bb-7b21f9b8e386 | no | Make a plan with document, structure using this document and organised documents for react and python: Lead Management Dashboard - Comprehensive Development Plan. Executive Summary |
| 20 | aedffb39-2ac9-4adc-bdf8-5c9e9f338d28 | 63,380.60 | 1 | 4,312 | 643cabc6-8a25-4f97-a672-c1f2ffecf72b | no | Voglio creare un app anche per desktop come suzuka.app |
| 21 | 74395363-cd2a-4bd6-b761-9b7a3ec8b05b | 63,288.16 | 87 | 2,909 | bd1f78f7-f633-4871-8199-4fc6af25c301 | no | Prompt: Build a Complete Non-GRN Payment Monitoring Application (End-to-End System Design). Goal: Design a full Non-GRN Payment Monitoring Application that enables departments to upload invoices |
| 22 | e3b64117-8e1d-4940-bdc0-bd7e0b5cd014 | 62,050.91 | 106 | 4,261 | 6e10a510-62c8-43ca-b104-c46cff623ae2 | no | Build a replica of uber but to book nearby service providers instead of cabs. |
| 23 | 7c717244-0d19-4324-9b38-3c6c34f8ef5d | 59,707.43 | 6 | 2,187 | 9f1877ef-8868-476c-956a-08510c0e8809 | no | I want you to build everything as you see at https://www.zhelta.com/ Rebuild the ZHELTA homepage (zhelta.com) to match the current live version in structure, layout, and behavior |
| 24 | 47040eba-3e12-4429-bdb3-19eff3cc9133 | 59,063.95 | 40 | 2,050 | ba9f8b9f-7099-47b9-a761-1d0ece9caecc | no | Build a model to compare start ups in india |
| 25 | cd89ada0-48f5-4e90-afd0-0fba6b8e9937 | 58,921.15 | 62 | 7,776 | de9e3463-9208-4f35-b406-1e9be6d0d859 | YES | i have a proect redeployed to my main site thedoggycompany.com current agent is https://soul-concierge.preview.emergentagent.com/ thedoggycompany github.com/dipalisikand1965-blip/TDB1 |
| 26 | 42becf6a-fad9-4f1b-91cd-6267fd9894cd | 57,594.53 | 1 | 1,760 | 2bbf5c99-092e-4d12-b0da-a99f4f17916b | YES | using the following requirements to build an app. Quran memorization app (partial-ayah highlights, repetition loops, spaced repetition, AI recitation feedback). 1) Product overview. Working name |
| 27 | 8bc8bbcd-163e-466b-a813-636b03351119 | 56,975.70 | 73 | 2,138 | de92ba1d-aaf1-4f2b-a5a8-809f6647d659 | YES | Creer une application web et mobile universelle de prise de rendez-vous, de gestion d'activite et de pilotage financier, destinee a tous les auto-entrepreneurs, independants, professions liberales |
| 28 | 79e0f849-ae16-4223-a41e-f6fd873f3420 | 56,313.71 | 1 | 4,763 | eedd1b46-3a5c-41ee-9c78-131d3ac405ae | YES | Build a SaaS web app called "AI Learning Companion". The app allows users to enter any skill they want to learn and generates a structured learning roadmap with three levels: Basic, Intermediate, and |
| 29 | 48bbfcf5-4737-45c3-b9f6-6c9bca19c06d | 55,919.78 | 4 | 2,259 | 60b70787-c079-4b2f-8a19-5bb518a259a8 | no | Build a web-based CRM that reproduces and improves the provided Excel CRM. The system must support lead and project management, email ingestion to create/update leads, automated calendar events |
| 30 | a2e99b4e-c007-4ea6-a4ab-d43368f7c26a | 55,146.50 | 195 | 3,632 | a1cb3d28-7935-43b1-9995-95f217ea0cdc | no | Chat with me but don't do anything yet. I am developing an arbitrage bot. It should be capable of performing Linear and Triangular Arbitrage on the Ethereum blockchain. It should be written in N |
| 31 | 12dd4216-bbde-4a4c-8121-629e7c1ce17d | 54,427.73 | 89 | 3,485 | 4bf75d3c-ed32-4e1e-ba13-b0b11fc3e829 | YES | Core Principle (Very Important). Emergent works best when it is treated like a senior engineering team, not a single AI prompt. That means: One authoritative task at a time. Each task must be acknow |
| 32 | 3cead48f-1903-4eb5-86cb-3deb9675edf8 | 54,341.32 | 19 | 4,346 | 0997baab-7bbe-4658-8fdd-fe7711aad0e2 | no | Hi I want to build an automated trading bot using MT4 and backtest different strategies |
| 33 | 0a967cdc-6668-46ae-8a9b-8fdeb6315c9a | 54,143.26 | 35 | 2,166 | 63bf9d09-4b85-4dbc-aeef-33c8a35b432e | no | Ich moechte eine neue Website fuer "Host-On.de" mit Anhaengendem Admin Interface haben welches komplett Modular aufgebaut ist. Rechnungen sollen ueber Lexoffice erstellt werden. |
| 34 | 55a59d4c-1ba2-4714-91b4-22d40e3605bb | 53,951.83 | 90 | 3,212 | af8a4719-f6a0-4bfd-9e44-c570a235beab | no | KASPAWS - EMERGENT PHASE 1 (UI FOUNDATION ONLY). COPY/PASTE CHECKLIST (NO BACKEND, NO AUTH, NO DATA). PHASE 1 RULES (NON-NEGOTIABLE): UI layout only. No Supabase. No API calls. |
| 35 | fe0c87de-ab80-4917-b874-63901e190d05 | 53,893.36 | 1 | 2,471 | 8d25a303-8a53-4511-8ea8-521d1c20bae2 | no | Build a small business fully integrated application with point of sale, inventory management, payroll and Hr management, work order tracker with crm, accounting |
| 36 | 1c4205e2-71c3-4ecd-b8fb-b9d8dc9f87b1 | 53,247.77 | 3 | 1,955 | b54b1b95-cdc0-4bbf-a8b7-e12e8dd18a22 | no | fais moi une appli en francais a partir de ce fichier |
| 37 | 1d0a5b44-b2f8-4e25-a72e-81849227522d | 53,111.66 | 1 | 2,388 | 67707cc3-af63-481e-a9ce-db2dff9426ac | no | Project: Robelium. Feature: Command & Control Center (CCC). Request type: Internal Operations Tool (Web-only). I want to extend the existing Robelium Admin Compliance Console into a Command & Co |
| 38 | 1312cd39-6f2e-4876-b835-ab15eacc24fa | 53,111.55 | 326 | 6,999 | 4d6f01d1-2c03-4766-9010-e35be97d583d | no | Salut! Esti agentul PRO? |
| 39 | 845194cc-4e87-4346-ba9d-f933233e9f0d | 52,979.27 | 72 | 3,076 | 87eb4431-2c1c-4f48-894e-6a2c18f47dd4 | YES | Task: Set Up Python 3.13 + Node 24 Preview Runtime & Run Full Integration Test Suite. Context: This is an insurance agency CRM (AIB42) that recently migrated from MongoDB to Azure Cosmos DB NoS |
| 40 | 9493da6b-660b-4675-9949-2d03d94dc65b | 52,967.86 | 38 | 3,016 | b7a3b076-80d2-44fc-a2cc-c439c7a76a11 | no | Build a multi-tenant SaaS CRM platform specifically for martial arts schools. This must function like an agency-level system (similar to GoHighLevel): one master admin account |
| 41 | 0fcc5c04-0120-4717-8bf9-beb72296793f | 52,768.12 | 39 | 4,556 | 19e871dd-497d-4b49-abb5-033cc87056fc | YES | Here is the sales assistant i want to build check and updae me if everything is perfect so that we can start? 1. AI Model for <1 Second Response. Recommendation: Hybrid Approach |
| 42 | 3f43e5ae-de0d-4234-8f78-56d5567e3ea4 | 52,667.94 | 6 | 1,846 | faf578f4-f630-416b-9e21-bd2313bf60af | no | PRODUCT REQUIREMENT DOCUMENT: UNG DUNG TAO THE THUC GIAI DAU (VONG BANG -> KNOCK-OUT). Tong quan san pham. Muc tieu: Xay dung mot he thong (Excel-based hoac app) |
| 43 | c9e509bf-d349-475c-9c87-c6e26d7e5501 | 51,890.66 | 107 | 5,519 | d7f17f94-6bd3-4cee-9108-bb1fed59f13c | no | Como estamos de backlog? |
| 44 | 45b9b713-e76a-4eec-a316-3633cd919f4a | 51,468.56 | 1 | 2,391 | 5367b74d-00b2-4e47-8be5-95fec8408a25 | YES | <analysis>original_problem_statement: The user wants to strictly recover the "Green Assos365" mobile casino UI (www.bet1891.com) that was lost due to a local git history wipe. |
| 45 | ceec807f-918a-4db9-86ad-b073d88c0472 | 51,432.42 | 1 | 1,887 | 174d02da-90bb-4770-bfdb-c67dd2cdfeb9 | no | Build a web app MVP for a liquidation auction business. Core use case: We sell mostly one-off items through online auctions. Winners pick up locally at our warehouse. |
| 46 | a71ee6aa-8157-4e40-a870-2f9fc74d8804 | 51,397.48 | 3 | 3,988 | 012b2fc3-ad4f-4bff-9df2-eaec0ee995f8 | no | Role: You are an Expert Arbitrage & Sports Analytics Developer. We are building a high-performance NBA Player Prop Dashboard that identifies the "Best Bets" by comparing lines across the entire market |
| 47 | ef6225c5-5673-46c2-aa5c-f4ad3b9cf8e5 | 51,202.26 | 10 | 2,041 | 4b83345f-6bbb-4720-92f0-ea16fcd3963c | YES | Build a mobile-first AI strongman coaching app with the following requirements: Core purpose: Help strongman athletes generate and follow personalized training programs |
| 48 | 86a4d2e5-d934-4457-96e6-1e9230a0a9d2 | 50,990.83 | 278 | 2,715 | 402d84e2-d923-4d49-9e62-ccc762912675 | no | I want to create a work rota for a gp surgery with 2 sites. Create them in this format (template grid follows) |
| 49 | 822658df-42d4-4e63-a2ea-ce9217296ceb | 50,549.81 | 3 | 1,077 | 393ede85-3cd0-43cf-9a75-924ad983ec10 | YES | Build an elite-level web platform called "H8 Capital - Market Intelligence Machine". This is not a news app. This is a high-end macroeconomic, financial, and real estate intelligence system |
| 50 | df4f99be-75af-4e4e-bb46-cecacff1b65f | 50,156.99 | 3 | 3,732 | f4cf4e30-ac9d-465f-acae-5746a0d00111 | no | https://live-support-test.preview.emergentagent.com/AUREM-PROJECT.zip |
| 51 | e184f3b6-04ef-411f-87c3-6e1ffa8088a1 | 50,110.94 | 114 | 3,197 | 2cde2965-073a-4431-88d9-965aea52e9c4 | YES | PROJECT NAME: HandymanAdmin. PROJECT TYPE: AI-powered handyman management SaaS platform for handyman businesses. TARGET PLATFORMS: iOS, Android, Web Admin Dashboard. Build a multi-tenant S |
| 52 | d4137518-6964-490e-b717-953e9674b576 | 49,509.58 | 2 | 2,322 | fc16fdc1-6ae6-43d7-9e3b-e22ee2cd53d7 | no | You are an expert full-stack engineer. I am migrating an existing Base44 app to Emergent with Supabase as the backend (Postgres + Auth + Storage + Edge Functions). |
| 53 | af2477bf-fcd3-425b-a2d0-c900e0b0c436 | 49,135.51 | 30 | 4,720 | 3b27c47c-664a-402e-9f33-8f78a33ec8ee | no | Base on my website www.restful-awareness.com then can you build a mobile aps with excercises based on the content on my website? |
| 54 | ddebef2a-0e3c-4257-a8f8-6e2dfa1147c6 | 49,077.90 | 1 | 1,075 | 1aab4e2a-4514-45a7-a2d1-4e05386b345b | no | Je veux que tu construises une plateforme SaaS premium nommee "Marmalade - Spread your Art". Cette plateforme ne doit PAS etre un simple CRM pour galeries, ni une copie d'Artlogic. |
| 55 | 5a609c7b-e894-498c-82f6-6425341812ae | 48,883.46 | 60 | 4,118 | 64a31c4c-655d-4b5f-a37e-0b9d2c763b63 | no | can u copy paste this for me https://chromewebstore.google.com/detail/shopify-scraper/idjimkpnmipnenkoifdomonlcejhhjnn |
| 56 | 5061b61d-b1cc-4f3c-a6f2-7069b2c9bafc | 48,863.03 | 31 | 1,136 | d58cae70-ffb6-4841-ba5b-5625141dc0b7 | no | EMERGENT DAY-1 BUILD PROMPT (Single-Org GetCare 360 - NDIS Core Loop). ROLE: You are building GetCare 360 for one NDIS provider organisation (NOT multi-tenant). |
| 57 | 5d8b63ec-c040-4f98-8cbd-f4866364ec94 | 48,477.93 | 2 | 2,325 | 2294c96a-0c71-4016-accd-176b4fef6d8c | no | Can you down load the app from GitHub and analyse the code bese. It's a Torrelavega civic app. All details are in the GitHub repository. Just analyse it. |
| 58 | 74c2ae8a-88f1-4382-a66a-0879cb1ec501 | 48,443.63 | 11 | 1,698 | 45590057-3613-4779-a97b-ae771910b243 | no | could you read the entire document and plan the right method of implementation? |
| 59 | 0548d11a-49b1-42dc-98ff-5965ff88a209 | 48,079.79 | 42 | 3,243 | 37205691-96bc-4c4b-b73f-e0d46d33fda1 | YES | We want to build a professional, modern backend application for our internal operations team to manage nationwide tax searches and title orders. The system should be role-based, workflow-driven |
| 60 | f35b1007-336b-4769-b744-5cf51453ac1f | 47,992.70 | 65 | 3,693 | 4ac38357-76e9-45bc-8156-affd502e1650 | YES | New Project: Create an API using fast api or anything more suited. 1) Authentication layer, consumer of api will pass credentials and security keys. 2) Allow to send base64 of |
| 61 | df9e3c74-2347-4947-b12b-73b61886a1be | 47,969.14 | 1 | 3,535 | 52250911-cbb6-4791-8501-5d8fc5ab18f8 | YES | <analysis>original_problem_statement: The user originally provided a 5-phase blueprint to build a "Payer-Aware Orchestration Engine". Recently, the user requested a major refactor to extract the |
| 62 | a4ada122-f5cb-4eae-958f-1fbaf254d6fa | 47,734.46 | 20 | 2,419 | 5d0a27e8-e79e-42b1-8f5d-67b0d8fc7110 | no | maine ismai kuch quntals edit kiye par wo automatic ab kg mai nahi le raha and automatic calculations b nahi kar paa raha hai |
| 63 | 34229d0a-c4c7-4f88-8b64-053ec34851f8 | 47,631.54 | 3 | 3,203 | 9ac26835-d657-4121-ac6b-91edb914bf43 | no | Voici une approche structuree, methodologique et operationnelle du parcours complet, integrant ADVP, reconnaissance vocale, questionnaires, analyse semantique et aide a la decision |
| 64 | ae31bb92-db62-4331-8b74-170ecbf04157 | 47,575.58 | 56 | 3,684 | 23e63773-2192-41ea-98cb-44af8884eeb4 | no | I HAVE ATTACHED A CATALOGUE OF MY COMPANY SPARE PARTS IN MS EXCEL FORMAT. IT HAS PART NUMBER AND IMAGES FOR THOSE PARTS. ALSO I HAVE ATTACHED AN EXCEL SHEET WITH PART NUMBERS AND THEIR MRP'S. |
| 65 | e45ae51e-c9a6-4b75-94d0-e0363dd3ac2e | 47,526.76 | 39 | 2,182 | d3e01d82-bcba-40c5-abc9-9e893434b7cc | no | Analizza il file e dimmi se e fattibile |
| 66 | 3a1eb9b0-13d7-4af7-8a6e-b433428ea003 | 47,071.08 | 25 | 2,448 | dcf26f85-3eed-4d77-be84-c42ac881fbfa | YES | L'Agence de Casting de Personnalites IA. Un annuaire de "Custom GPTs" specialises pour le jeu de role ou le business. Le concept: Plutot qu'un annuaire d'outils, creez un annuaire de personnages. |
| 67 | a5714e3f-969f-41e3-a75c-06efe6b8f031 | 46,985.29 | 1 | 1,887 | 408d8140-e4cb-43fb-98bc-1ed009dceba3 | no | Crear plataforma SaaS de Facturacion Electronica para Republica Dominicana llamado FortexaFE que cumpla con Ley 32-23 de facturacion electronica, (Decreto 587-24) y normativas DGI |
| 68 | 07883f41-a328-4983-9e5b-20e06ab6c4d8 | 46,606.86 | 91 | 1,684 | 4ef7f25c-1a65-4ed6-869b-c7c57ae6404c | no | Continue from where you left off from my repo |
| 69 | 36a2d022-fc71-4873-87ef-e07f0a9aa004 | 46,563.24 | 189 | 7,549 | 9d70f61b-ec3c-4c65-b034-cdcf5242dc81 | no | Build an app that counts steps on mobile |
| 70 | 73ae3861-29ff-4f29-8260-b9db249cb046 | 46,287.75 | 11 | 982 | c2eb1a54-28f8-4840-a8fc-cf66f4029d0e | no | Can you import another app from another account |
| 71 | 436a87e2-f67d-4058-b777-9aca7c698514 | 46,278.66 | 1 | 1,981 | 8e4974a2-dc17-4c05-9a16-860a4edb2103 | no | this what I have so far... I want/need a fillable form I can send out to inspectors to do site safety inspections, then print or save as PDF. Look at what I have see what we could add or take |
| 72 | 7e1d2d23-cc0c-4392-aa89-a110ce82a4c4 | 46,074.77 | 27 | 1,449 | 42d0c72f-bd78-4ca1-97a9-374155197c12 | no | 0) Project setup and definition. 0.1 Confirm scope and modules (baseline). Task: Lock the functional scope: Clients & Subscriptions, Products (individual/grouped/addons), Orders + status flow |
| 73 | 4ada0d4f-481d-4342-9b75-ff49d8d382af | 46,027.19 | 47 | 5,951 | f81a3c59-3160-4a2d-af1d-e058fa2ea7d9 | YES | im having forking issues in my current project can you take a look at my git: https://github.com/Wilaroo/Trading-and-Analysis-Platform.git and review the last session so we can continue |
| 74 | 3a9111f5-c7c4-4820-ad14-367f4f812f10 | 45,987.70 | 1 | 3,095 | 4c960659-3896-45ff-a094-b3775d335005 | YES | <analysis>original_problem_statement: PRODUCT REQUIREMENTS: 1SOURCE & 1XCESS B2B sourcing platform with MPN verification, real-time negotiation, and bulk inventory uploads. |
| 75 | 7a6d962f-150c-4c46-9672-63d015bb6008 | 45,887.17 | 57 | 3,063 | 2d4c2994-b0f9-4787-99b7-d7d90e6beef7 | no | How complex is to make this app from base44 work? |
| 76 | c3a29276-11eb-472a-b1ac-6726c8825764 | 45,766.77 | 35 | 2,785 | f2b55a2a-1493-4275-bdad-1bb5421f7d28 | no | Build me an app for warehouse stock and inventory with customers login |
| 77 | 78a4f6b5-4d7f-4bbf-8806-c454c552cc8d | 45,158.85 | 62 | 3,714 | bf1b9378-51f4-4c60-b7a2-57088e22a249 | no | Can we continue on this project? |
| 78 | 3808ee65-88c1-4fc0-a967-de60610062ad | 44,989.25 | 45 | 3,897 | 56b10580-f6a5-4f92-8aa0-cf7e5757e4f5 | no | Hi, I want to build a logistics app. Can you help me with that? |
| 79 | cca85b02-16e9-4a52-a5c8-9e139c2ccf75 | 44,454.42 | 1 | 1,977 | 235e77f3-10a7-4fa6-8fa1-222667c45cf7 | no | Est ce que tu peux faire un site pour estimer la valeur d'un bien immobilier quelle source tu utiliseras pour ca? |
| 80 | 5cda2089-be50-4cc3-b4b0-7e30414cd8dc | 44,311.41 | 43 | 3,198 | e2554479-3a7f-4ec9-a58e-c26103e0f7eb | no | Build me a Romantasy novel generator that makes genre-perfect bestselling short romantasy novels |
| 81 | 8c4caebb-b256-4c25-b273-9055877f40c0 | 44,309.31 | 49 | 5,364 | 13fd3807-d651-4679-821f-b394a6b37661 | no | Por supuesto! Aqui tienes el prompt completo para el desarrollo de la app y el sitio web de Ross Tax Preparation, incorporando toda la informacion necesaria |
| 82 | 1d2841e3-34f4-4f04-82c6-584ea4fff58f | 44,249.13 | 1 | 1,102 | 382e2c3a-9817-4355-9dd6-237502604da1 | no | Create a production-ready private investor portal web application for a premium wealth management and private deals business focused on curated investment opportunities. |
| 83 | 3e1f86fa-f884-49f4-a88b-cfe824b8b365 | 44,118.79 | 11 | 2,200 | 1005a48b-89c9-468b-af17-3c90b791924c | no | Quiero construir un sistema POS para restaurante en Republica Dominicana, cumplimiento DGII. Funcionalidades: mapa de mesas, comandas a cocina, modificadores de platillos, division de cuentas |
| 84 | 0bb8d606-4abf-42dd-a473-408a4a3f4d47 | 43,364.17 | 1 | 2,022 | fc143432-f7e9-4d22-b61a-66ec06490442 | no | import React, useState, useEffect, useRef from 'react'; import initializeApp from 'firebase/app'; import getAuth, onAuthStateChanged, signInAnonymously, signInWithCustomToken |
| 85 | dc578095-9f24-4f44-810c-3d1497c580ff | 43,187.35 | 1 | 205 | cfb0d6ae-4ef1-4deb-bdf6-291665d9b664 | no | Pick2Play is strongest when it is positioned as: a player-first sports challenge and match ecosystem for finding opponents, creating challenges, organizing games, and powering club tournaments |
| 86 | 174ed4e1-e489-4161-88c1-6f38f78e87a9 | 42,853.96 | 86 | 2,001 | cde1511c-f4ae-4ca1-84ca-5741a04e7e51 | no | 1. Purpose: The Recipient acknowledges that the Company is developing proprietary technology, business models, and intellectual property related to the WashPros mobility-as-a-service platform |
| 87 | ab7bd4e9-b5b7-42f0-be77-538dba6254d7 | 42,662.01 | 9 | 1,764 | dcb23419-decb-4734-b967-df9f55064473 | YES | Propietaris.Cat. Ya tengo una App generada con DeepAgent de Abacus.ai que funciona bastante bien, pero quiero modificarla. La puedes ver en https//propietaris.cat |
| 88 | 7e8830b3-2b0e-4ba9-b861-375b9902ce41 | 42,477.90 | 3 | 3,313 | 4c0019fe-b0f3-448c-a681-50387b47cb39 | no | i want to create an app called Aurora Pulse - it will be used for procurement and live material tracking |
| 89 | 2667d506-65d8-434e-a40a-3729cba75b31 | 42,315.51 | 2 | 430 | fb021984-4ac4-48d8-8331-e088cdfbd72d | no | Crie um sistema web completo para analise de lucro de produtos vendidos na Amazon. Objetivo: O sistema deve permitir cadastrar produtos, inserir manualmente o preco de venda da Amazon |
| 90 | 428f73e7-1400-4248-9dcb-5611a977096f | 42,113.13 | 2 | 1,261 | c3541ca0-6d76-4b9b-a37c-fd6ffbee8a42 | no | Build an application where the admin should be able to create digital products with custom value for example 100 AFN, or 250 AFN or 500 AFN or 1000 AFN, this application will be used in Afghanistan |
| 91 | c70d9d5a-437b-486c-92f2-71b345cc99c4 | 41,976.65 | 1 | 3,284 | e2fc53ba-b0d0-4af6-99ae-8382fe609972 | YES | OK, I want to build an app that will allow my Sales agents to upload their clients information and be able to go on an order stock and also to be able to get promotional stuff |
| 92 | 6664bb58-3b3e-4d7b-8913-8d74a0421485 | 41,869.21 | 2 | 2,005 | 7c506fde-5bbd-407b-9e20-cb8ec19f43b5 | YES | Build NdorFlow Phase 6 - Stage 6.1: App Shell & Auth only. Scope: 1. Create the frontend app shell with a sidebar and top bar. 2. Create placeholder protected pages: /dashboard /jobs |
| 93 | 714e35c3-4732-4432-a26d-e1815a6a479d | 41,675.55 | 1 | 2,498 | 7fa889d0-967d-4ac0-be72-c9db38d468c7 | no | Posso parlare in italiano? |
| 94 | b9fc47f5-3ce1-4617-9a9a-1d2f11705f84 | 41,632.95 | 10 | 2,094 | 776d4cf1-bb5b-4453-a617-e93e4f7a92d5 | no | i need to build a full saas system like cliniko or jane app for practice management. can u help? |
| 95 | 750f4b3d-265f-4f73-bb0c-43abd4453608 | 41,548.80 | 4 | 2,605 | 40ae29c4-87fd-47a5-8360-90a2fd389a3d | YES | import useState, useEffect, useRef from "react"; // COSMIC INSIGHT - FULL CALCULATION ENGINES (Client-Side) |
| 96 | a5fca742-52d9-42dc-a005-dbed8957ce18 | 41,393.02 | 5 | 1,796 | 8d9c5935-dcd6-46a4-938f-fbc2f518d6ec | YES | Your FoundrRaise Emergent Build Prompt. Section 01 - Product Vision - What FoundrRaise is, the two-sided marketplace model (founders + investors + CFO co-pilots), and a competitive differentiation |
| 97 | a3e91164-9d09-4ed2-97f4-0f7d484b5ac2 | 41,230.41 | 149 | 1,766 | a9ffedec-aa47-4d21-b896-44e602246858 | no | Pls build me an erp, crm, hrms, fms with reference to the 3 files attached |
| 98 | 0f7afc70-e3c4-4925-8f2c-a35d20f80a39 | 40,965.54 | 1 | 2,698 | 8a08524b-860a-41af-bfcb-551015b957c6 | no | eu tenho 2 projetos com vc, eu consigo mesclar esses 2 ou tenho que criar do zero? |
| 99 | 68ccf2a8-ea58-48dd-90d1-4072e7900425 | 40,332.32 | 2 | 8,617 | 43463041-5c22-4f69-8e0a-0740fcd812c6 | no | (Arabic) We previously talked about a shopping app, is it still available? |
| 100 | d6471d47-49ea-4d70-9ccc-101641f2ba98 | 40,301.22 | 3 | 2,155 | b6e3fece-93c0-474d-bcaf-bba216abb694 | no | App i want to build is a trading app which takes in all the information from the world news and profiles companies and in emerging markets |

### Top 50 users by 90d spend (2026-03-14 to 2026-06-12), with AI-candidate shares and revenue to date

| # | user_id | 90d spend USD | n projects | n jobs | % jobs AI (keyword, inflated) | % projects AI (root task, robust) | revenue to date USD | country |
|---|---|---|---|---|---|---|---|---|
| 1 | 21e6b39e-ce89-4751-b28a-20616450c4dc | 171,042.13 | 54 | 68 | 55.9 | 33.3 | 40,241.00 | Poland |
| 2 | a58ff9de-8aed-4a83-a6ff-78e85643842e | 158,812.58 | 14 | 41 | 80.5 | 35.7 | 25,185.00 | United States |
| 3 | bf1b9378-51f4-4c60-b7a2-57088e22a249 | 157,254.67 | 72 | 194 | 77.8 | 29.2 | 7,960.00 | Spain |
| 4 | 6363871c-7bce-425f-a4cb-48f2b4f7fc9a | 149,350.67 | 41 | 236 | 85.6 | 12.2 | 33,040.00 | Germany |
| 5 | 4bf75d3c-ed32-4e1e-ba13-b0b11fc3e829 | 139,342.61 | 10 | 146 | 97.3 | 60.0 | 23,985.00 | Japan |
| 6 | dcb23419-decb-4734-b967-df9f55064473 | 130,936.34 | 16 | 43 | 95.3 | 43.8 | 35,340.00 | Spain |
| 7 | de9e3463-9208-4f35-b406-1e9be6d0d859 | 129,170.68 | 11 | 73 | 91.8 | 45.5 | 32,862.07 | India |
| 8 | 99b4a983-f5cd-4ddc-b45f-35facb0cb068 | 124,727.51 | 17 | 54 | 90.7 | 47.1 | 36,075.00 | United States |
| 9 | f8a890d0-39b5-4efb-a052-a2b6e552ac70 | 123,782.62 | 4 | 93 | 97.8 | 25.0 | 32,361.00 | United States |
| 10 | ba9f8b9f-7099-47b9-a761-1d0ece9caecc | 122,466.90 | 27 | 88 | 80.7 | 29.6 | 6,253.00 | Australia |
| 11 | 45590057-3613-4779-a97b-ae771910b243 | 121,792.77 | 24 | 46 | 69.6 | 37.5 | 15,162.94 | United Arab Emirates |
| 12 | 5367b74d-00b2-4e47-8be5-95fec8408a25 | 115,154.23 | 148 | 148 | 97.3 | 97.3 | 26,991.00 | Greece |
| 13 | 7aa60b28-23ef-4f2b-a205-cfc63333dc42 | 99,390.21 | 1 | 57 | 100.0 | 0.0 | 34,157.00 | Australia |
| 14 | 96ec94ce-f1ee-40ac-aaf0-c1b415ab308e | 94,688.30 | 13 | 116 | 96.6 | 38.5 | 25,950.00 | United States |
| 15 | 1290386d-9fed-423e-9188-2b3ffecd8467 | 92,802.17 | 6 | 7 | 57.1 | 50.0 | 17,376.00 | Australia |
| 16 | 10738fc2-ce97-47f3-83b1-02c460212521 | 92,795.53 | 4 | 6 | 50.0 | 0.0 | 21,967.50 | Switzerland |
| 17 | 30131d7e-ff08-4bc0-86fd-9a8f7359bfe1 | 92,615.28 | 27 | 30 | 23.3 | 14.8 | 13,301.00 | United Kingdom |
| 18 | daddf41e-b1e0-4bdf-9af0-47d2884e3f02 | 90,703.40 | 5 | 149 | 99.3 | 80.0 | 28,388.86 | India |
| 19 | 105a7254-f869-4ee0-8f2d-f5a7ac5dc2ec | 88,467.45 | 52 | 381 | 99.5 | 94.2 | 27,807.00 | United States |
| 20 | 0eac1e19-3618-4673-a6bb-7b21f9b8e386 | 86,688.83 | 17 | 66 | 84.8 | 35.3 | 35,829.30 | (null) |
| 21 | d61212ed-09be-430b-935a-73dc338de342 | 86,202.34 | 4 | 19 | 84.2 | 0.0 | 10,930.80 | India |
| 22 | f20389aa-75bc-4433-86ae-19c97b6c9cb3 | 86,027.29 | 27 | 37 | 40.5 | 18.5 | 14,061.00 | Turkey |
| 23 | c7eaed00-4f57-4566-b65f-cfeacda12ec9 | 85,290.40 | 4 | 9 | 77.8 | 50.0 | 27,500.00 | Switzerland |
| 24 | a6550792-618a-49c1-b46c-02678936663b | 85,104.78 | 46 | 117 | 71.8 | 19.6 | 11,252.71 | India |
| 25 | 235e77f3-10a7-4fa6-8fa1-222667c45cf7 | 83,984.74 | 17 | 17 | 52.9 | 52.9 | 14,571.00 | France |
| 26 | 98a9faf1-df98-42e1-9094-0a018e56e7b4 | 83,041.73 | 121 | 206 | 89.8 | 81.0 | 26,790.00 | United States |
| 27 | dbd09cd4-1959-4700-9aaa-289b6b060a40 | 82,944.42 | 100 | 141 | 87.9 | 81.0 | 14,001.00 | France |
| 28 | 6cc198b3-83b0-457d-affa-bcbd81a8a9f7 | 82,422.54 | 24 | 40 | 67.5 | 37.5 | 20,771.00 | United States |
| 29 | e5eebbd4-78a7-4d28-92b8-1f657a458dbd | 80,175.89 | 44 | 48 | 54.2 | 45.5 | 15,016.00 | France |
| 30 | d81cb20b-0177-497b-8eb6-f3947247b60b | 79,020.15 | 34 | 150 | 85.3 | 35.3 | 13,454.99 | Italy |
| 31 | a71ccf52-d588-4962-af52-bc8ad87f3b62 | 78,397.57 | 5 | 111 | 97.3 | 20.0 | 16,481.00 | Germany |
| 32 | d0f17064-8f57-48f0-b909-aeffd7f965af | 78,333.31 | 7 | 44 | 90.9 | 42.9 | 44,021.00 | Switzerland |
| 33 | 393ede85-3cd0-43cf-9a75-924ad983ec10 | 77,639.97 | 9 | 16 | 87.5 | 77.8 | 16,225.00 | Croatia |
| 34 | 908ffa8e-9abd-475b-996f-f78d36e78922 | 76,812.39 | 9 | 208 | 98.6 | 33.3 | 20,150.00 | Philippines |
| 35 | 70e3e616-9c82-425a-988c-057fb75c93f1 | 75,312.68 | 24 | 90 | 78.9 | 20.8 | 12,300.00 | United States |
| 36 | 2f8d5c85-30a5-417a-b711-61e782d4f449 | 74,992.04 | 12 | 14 | 42.9 | 33.3 | 13,530.00 | United States |
| 37 | 63bf9d09-4b85-4dbc-aeef-33c8a35b432e | 74,029.22 | 21 | 69 | 82.6 | 23.8 | 22,980.00 | Germany |
| 38 | d8461c1c-9002-40aa-8648-a8b322542ec6 | 73,716.89 | 3 | 44 | 97.7 | 0.0 | 23,935.00 | Canada |
| 39 | 5a56d82a-de09-4693-9b70-38eaaa6e7a2d | 73,271.98 | 3 | 81 | 98.8 | 66.7 | 14,012.00 | United States |
| 40 | 6a10f35a-de84-4c0a-9d56-9f7a528767e8 | 72,712.05 | 38 | 41 | 48.8 | 21.1 | 26,113.00 | France |
| 41 | e1dec494-92f8-4817-91b5-ca6f97b5698f | 70,432.48 | 14 | 17 | 47.1 | 35.7 | 12,350.00 | United States |
| 42 | c425d6c0-4e6c-47a8-b940-fe46c0e3e709 | 69,907.99 | 17 | 97 | 91.8 | 35.3 | 20,042.00 | Tanzania |
| 43 | f80edc9f-52f2-49b2-a498-4967340519d6 | 69,723.81 | 17 | 36 | 72.2 | 35.3 | 23,726.00 | Turkiye |
| 44 | faf578f4-f630-416b-9e21-bd2313bf60af | 68,639.98 | 21 | 27 | 44.4 | 28.6 | 14,785.00 | Vietnam |
| 45 | 1af92a1e-1dde-4b46-98d2-aaa7e0fcfb04 | 68,281.90 | 4 | 7 | 71.4 | 50.0 | 10,931.00 | United Kingdom |
| 46 | 71e515fa-9427-4f08-ad7f-56d4e1f9ea58 | 68,266.10 | 1 | 10 | 100.0 | 0.0 | 20,010.00 | South Africa |
| 47 | bdd85391-1f47-4167-9349-2baf77d5763b | 66,746.54 | 57 | 130 | 75.4 | 29.8 | 37,749.50 | Malaysia |
| 48 | 0386eb27-34e9-41aa-94a2-669e06ac3df2 | 66,066.86 | 99 | 114 | 37.7 | 27.3 | 13,500.00 | Australia |
| 49 | bd1f78f7-f633-4871-8199-4fc6af25c301 | 65,868.90 | 19 | 105 | 85.7 | 21.1 | 9,709.49 | India |
| 50 | 769bc656-4e69-4dc3-8fef-9da6d63734d7 | 65,504.63 | 73 | 107 | 88.8 | 83.6 | 15,220.00 | Australia |

### AI-candidate flag inflation evidence: keyword flag rate by job type (all costed jobs in window)

| job type | n jobs (with cost in window) | n flagged AI-candidate | % flagged |
|---|---|---|---|
| root jobs (not in fork_chain) | 4,570,139 | 717,920 | 15.7 |
| fork jobs (in fork_chain) | 203,906 | 188,297 | 92.3 |

### Caveats

- value_in_usd magnitudes are implausibly large as raw provider cost (top project $158.7k; top-50 users' 90d 'spend' $4.65M vs only ~$1.08M revenue paid to date by the same users). Trajectory ids and fork_chain rows were verified unique (no double counting), so use these figures for RANKING and relative shares, not absolute unit economics, until the value_in_usd denomination is confirmed.
- AI-candidate flag is keyword heuristic v1. On FORK jobs the task field contains agent-generated handoff/<analysis> text that almost always mentions 'agent'/'AI': 92.3% of fork jobs flag vs 15.7% of root jobs. Hence '% jobs AI-candidate' for whales (42/50 >50%) is heavily inflated; the root-task project-level measure (10/50 >50%) is the more reliable floor. Both are reported; LLM calibration is planned.
- Some root tasks themselves start with <analysis> handoff blocks (cross-account/project imports, e.g. ranks 44, 61, 74), so even the root-task flag can misfire on those rows.
- HITL steps = count of trajectory rows where human_message IS NOT NULL. user_messages_array was rejected because it carries forward across steps (~7x over-count on probe job b878e6a3). human_message has ~10% repeated texts on probed jobs, so HITL counts may be slightly inflated.
- Cost is attributed to the 90d window only: jobs/projects started before 2026-03-14 include only their steps inside the window; n_jobs per project counts only jobs with >=1 costed step in the window.
- Internal users excluded only via signups email NOT LIKE '%emergent.sh' plus the one hardcoded user_id; users absent from signups_raw_dataset were kept (could not be screened).
- Project owner = root job's user_id in the projects table; in the users table each job's cost is attributed to the job's own user (a fork by a different user would split between tables).
- One whale (0eac1e19) has NULL country in signups_raw_dataset.

<details><summary>Queries used</summary>

**Task 1: Top 100 projects by 90d cost with fork rollup, HITL steps (human_message), AI-candidate flag and root-task snippet**

```sql
WITH costs AS (
  SELECT job_id, SUM(value_in_usd) AS cost, COUNTIF(human_message IS NOT NULL) AS hitl_steps
  FROM `analytics.trajectories_full_view`
  WHERE DATE(created_at) >= '2026-03-14'
  GROUP BY job_id
),
jobmap AS (
  SELECT j.id, COALESCE(fc.first_job_id, j.id) AS project_id
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON fc.job_id = j.id
),
proj AS (
  SELECT jm.project_id, SUM(c.cost) AS total_cost, COUNT(DISTINCT c.job_id) AS n_jobs, SUM(c.hitl_steps) AS n_hitl_steps
  FROM costs c JOIN jobmap jm ON jm.id = c.job_id
  GROUP BY jm.project_id
),
su AS (SELECT user_id, ANY_VALUE(email) AS email FROM `analytics.signups_raw_dataset` GROUP BY user_id)
SELECT p.project_id, ROUND(p.total_cost,2) AS total_cost_usd, p.n_jobs, p.n_hitl_steps, r.user_id,
       REGEXP_CONTAINS(LOWER(SUBSTR(r.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)') AS ai_candidate,
       SUBSTR(r.task,1,200) AS root_task_200
FROM proj p
JOIN `analytics.jobs_full_view` r ON r.id = p.project_id
LEFT JOIN su ON su.user_id = r.user_id
WHERE (su.email IS NULL OR su.email NOT LIKE '%emergent.sh')
  AND r.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
ORDER BY p.total_cost DESC
LIMIT 100
```

**Task 2: AI-candidate count and spend share within the top 100 projects**

```sql
-- same CTEs as Task 1 ending in top100 AS (SELECT project_id, total_cost, ai_candidate ... ORDER BY total_cost DESC LIMIT 100)
SELECT COUNT(*) AS n_projects, COUNTIF(ai_candidate) AS n_ai_projects,
       ROUND(SUM(total_cost),2) AS total_spend,
       ROUND(SUM(IF(ai_candidate,total_cost,0)),2) AS ai_spend,
       ROUND(100*SUM(IF(ai_candidate,total_cost,0))/SUM(total_cost),1) AS ai_spend_pct
FROM top100
-- result: 100 projects, 28 AI, $5,565,893.90 total, $1,548,287.13 AI (27.8%)
```

**Task 3: Top 50 users by 90d spend with job-level AI share, revenue to date, country**

```sql
WITH costs AS (
  SELECT job_id, SUM(value_in_usd) AS cost FROM `analytics.trajectories_full_view`
  WHERE DATE(created_at) >= '2026-03-14' GROUP BY job_id
),
jobs AS (
  SELECT j.id, j.user_id, COALESCE(fc.first_job_id, j.id) AS project_id,
         REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)') AS ai_candidate
  FROM `analytics.jobs_full_view` j LEFT JOIN `analytics.fork_chain` fc ON fc.job_id = j.id
),
user_agg AS (
  SELECT jb.user_id, SUM(c.cost) AS spend, COUNT(DISTINCT jb.project_id) AS n_projects,
         COUNT(DISTINCT jb.id) AS n_jobs, COUNT(DISTINCT IF(jb.ai_candidate, jb.id, NULL)) AS n_ai_jobs
  FROM costs c JOIN jobs jb ON jb.id = c.job_id GROUP BY jb.user_id
),
rev AS (SELECT user_id, ROUND(SUM(amount),2) AS revenue_to_date FROM `analytics.user_revenue_events` GROUP BY user_id),
su AS (SELECT user_id, ANY_VALUE(email) AS email, ANY_VALUE(country) AS country FROM `analytics.signups_raw_dataset` GROUP BY user_id)
SELECT u.user_id, ROUND(u.spend,2) AS spend_90d_usd, u.n_projects, u.n_jobs, u.n_ai_jobs,
       ROUND(100*u.n_ai_jobs/u.n_jobs,1) AS pct_jobs_ai_candidate,
       COALESCE(r.revenue_to_date,0) AS revenue_to_date_usd, su.country
FROM user_agg u
LEFT JOIN rev r ON r.user_id = u.user_id
LEFT JOIN su ON su.user_id = u.user_id
WHERE (su.email IS NULL OR su.email NOT LIKE '%emergent.sh')
  AND u.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
ORDER BY u.spend DESC LIMIT 50
```

**Task 3 robustness: project-level AI share per whale (root-task flag on each distinct project of the 50 hardcoded whale user_ids)**

```sql
WITH whales AS (SELECT user_id FROM UNNEST([/* 50 whale user_ids from previous query */]) AS user_id),
costs AS (SELECT job_id FROM `analytics.trajectories_full_view` WHERE DATE(created_at) >= '2026-03-14' GROUP BY job_id),
user_projects AS (
  SELECT DISTINCT j.user_id, COALESCE(fc.first_job_id, j.id) AS project_id
  FROM `analytics.jobs_full_view` j
  JOIN whales w ON w.user_id = j.user_id
  JOIN costs c ON c.job_id = j.id
  LEFT JOIN `analytics.fork_chain` fc ON fc.job_id = j.id
)
SELECT up.user_id, COUNT(*) AS n_projects,
       COUNTIF(REGEXP_CONTAINS(LOWER(SUBSTR(r.task,1,4000)), r'(\bai\b|...keyword v1...)')) AS n_ai_projects,
       ROUND(100*COUNTIF(REGEXP_CONTAINS(LOWER(SUBSTR(r.task,1,4000)), r'(\bai\b|...keyword v1...)'))/COUNT(*),1) AS pct_projects_ai
FROM user_projects up JOIN `analytics.jobs_full_view` r ON r.id = up.project_id
GROUP BY up.user_id ORDER BY pct_projects_ai DESC
```

**Caveat quantification: keyword flag rate on root vs fork jobs (shows fork-task handoff inflation: 92.3% vs 15.7%)**

```sql
WITH costs AS (SELECT job_id, SUM(value_in_usd) AS cost FROM `analytics.trajectories_full_view` WHERE DATE(created_at) >= '2026-03-14' GROUP BY job_id)
SELECT (fc.job_id IS NOT NULL) AS is_fork_job, COUNT(*) AS n_jobs,
       COUNTIF(REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|...keyword v1...)')) AS n_ai_flagged,
       ROUND(100*COUNTIF(REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|...keyword v1...)'))/COUNT(*),1) AS pct_flagged
FROM costs c
JOIN `analytics.jobs_full_view` j ON j.id = c.job_id
LEFT JOIN `analytics.fork_chain` fc ON fc.job_id = j.id
GROUP BY is_fork_job
```

**Data integrity probes: fork_chain uniqueness (863,062 rows = 863,062 distinct job_ids), trajectory id uniqueness (8,194,730 = 8,194,730 on 3-day sample), and HITL definition check (user_messages_array carries forward; human_message ~= distinct messages)**

```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT job_id) AS n_distinct_jobs FROM `analytics.fork_chain`;
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT id) AS n_ids FROM `analytics.trajectories_full_view` WHERE DATE(created_at) BETWEEN '2026-05-01' AND '2026-05-03';
SELECT job_id, COUNTIF(human_message IS NOT NULL) AS rows_with_human_msg, COUNT(DISTINCT human_message) AS distinct_human_msgs FROM `analytics.trajectories_full_view` WHERE DATE(created_at) >= '2026-03-14' AND job_id IN ('f1f71b32-2bf0-490c-95e6-4468f43f74e6','4eebb99c-ad40-4d04-a04a-95f45042e617') GROUP BY job_id
```

</details>


---

## integration_proxy

### Summary
The Integration Proxy DB (Redash DS 18, Postgres, 15 tables) is NOT a per-request proxy log — it is an integration registry + provisioning + metering/billing store. It contains no request-level rows, no status codes, and no error data, so per-provider call volume and error rates cannot be derived from it. What it does capture: (1) Universal LLM key issuance — every user gets one LiteLLM virtual key (api_keys: 2,120,408 rows, all provider='litellm', all active; emergent_keys mirrors this with is_paid flag: 357,989 paid-active vs 1,751,641 free-active, key_config.llm.allowed_providers is almost always ["claude","openai","gemini"]). (2) Universal-key monetization via billing_ledger metric 'litellm_topup' (ECU units): in the last 30 days (2026-05-13→06-12) 30,473 ledger entries totaling 175,954.57 ECU across 2,239 distinct users; last 90 days 56,752 entries / 348,394.46 ECU / 3,626 users; modal topup is 5 ECU (46,861 of 56,752 entries), negatives are reversals. Monthly trend: Apr (from 04-17) 82,828 ECU/926 users, May 212,883/2,551, Jun 1-12 52,805/922 — these ~2.2-2.5k users/month are deployed apps actively consuming LLM through Emergent's universal key, the strongest production-AI-app signal in this DB. (3) Stripe adoption: app_integrations is 100% 'stripe' — 131,767 distinct apps since 2025-07-06, 15,845 in last 30d, 39,042 in last 90d. (4) Tigris object storage: 95,370 users provisioned orgs+buckets; the only active 'proxy mode' integration; usage_records (9.4M rows since 2026-04-17) is daily polled usage, ~79.7k users polled/day; 56,689 distinct users stored >0 GB in last 30d; storage billing is negligible (662 ECU/30d). (5) Push notifications via SuprSend: only 352 apps since 2026-05-22 (new/nascent). For actual per-provider LLM call volumes and failures of AI builders' apps, use LLM Proxy Postgres (DS 9) or credits_db.credit_ledger reference_type='UNIVERSAL_KEY' instead; this DB best serves as the roster of WHO has paid universal keys and WHO tops up (i.e., shipped AI products with real usage).

### Key numbers

- **Universal LLM keys issued (api_keys, provider=litellm, all-time to 2026-06-12)**: 2,120,408 users (1 key per user, 100% active)
- **Paid universal keys (emergent_keys is_paid=true, active)**: 357,989 users (16.9% of 2,119,127 keys)
- **LiteLLM topup volume, last 30d (2026-05-13→06-12)**: 30,473 entries, 175,954.57 ECU, 2,239 distinct users
- **LiteLLM topup volume, last 90d (2026-03-14→06-12; data starts 04-17)**: 56,752 entries, 348,394.46 ECU, 3,626 distinct users
- **Modal topup amount (90d)**: 5 ECU (46,861 of 56,752 entries, 82.6%)
- **Apps with Stripe integration (all-time since 2025-07-06)**: 131,767 distinct apps; 15,845 last 30d; 39,042 last 90d
- **Tigris storage users provisioned (storage_orgs)**: 95,370 users
- **Users storing >0 GB on Tigris, last 30d**: 56,689 distinct users
- **Integration wallets with positive balance**: 4,806 of 687,619 (0.7%); total balance 231,034.28 ECU
- **Apps with push notifications (SuprSend, since 2026-05-22)**: 352 apps

### Schema: 15 tables in Integration Proxy DB (DS 18)

| Table | Rows | Date range | Purpose |
|---|---|---|---|
| integrations | 2 | Apr 2026 | Catalog: tigris (storage, proxy, active, request_audit=true), litellm (llm_router, proxy, INACTIVE status) |
| integration_metrics | 4 | Apr 2026 | gb_stored / requests_class_a / requests_class_b (tigris), litellm_topup (litellm, ECU) |
| api_keys | 2,120,408 | 2025-07-25 → now | One LiteLLM virtual key per user (key=secret). All provider='litellm', status='active' |
| emergent_keys | 2,119,127 | 2025-07-25 → now | Universal Emergent key per user; is_paid, key_config {llm.allowed_providers, auto_topup, auto_topup_amount} |
| app_integrations | 131,767 | 2025-07-06 → now | app_uuid → integration; 100% 'stripe', 1 row per app |
| user_integrations | 102,904 | 2026-04-17 → now | All tigris, all active |
| integration_wallets | 687,619 | 2026-04-17 → now | Per-user ECU wallet for integrations |
| billing_ledger | 2,669,732 | 2026-04-17 → now | ECU debits/credits per metric (gb_stored overage + litellm_topup) |
| usage_records | 9,428,094 | 2026-04-17 → now | Daily polled tigris usage per user per metric |
| billing_tiers | 3 | — | gb_stored pricing: free ≤0.2GB, paid ≤2GB free, then 0.03/GB |
| storage_orgs / storage_buckets | 95,370 / 95,368 | 2026-02-24 → now | Tigris org+bucket per user (creds=secret) |
| push_apps / push_apps_suprsend | 352 | 2026-05-22 → now | SuprSend push provisioning per app slug |
| integration_grace_periods | small | — | Grace deadlines for unpaid integration usage |

### Sample rows (secrets redacted)

| Table | Sample (latest rows, 2026-06-12) |
|---|---|
| app_integrations | app=844bdcc1-36aa-...-df89942e89aa, integration='stripe', created_at=2026-06-12T09:48:40Z (all 5 sampled rows: stripe) |
| api_keys | provider='litellm', status='active', key='<redacted>' — 1 row per user |
| emergent_keys | is_paid=false, status='active', emergent_key='<redacted>', key_config keys = [llm, auto_topup, auto_topup_amount]; paid keys: llm.allowed_providers=["claude","openai","gemini"] (16,384 of 16,407 keys created last 7d), auto_topup=true, auto_topup_amount=1 |
| usage_records | user=a5fc7ee1-..., period=2026-06-10, value=0.026 (gb_stored) / 56 (requests), created_at=2026-06-11 — daily poll batch |
| push_apps | app_id='trip-logger-app' / 'scam-spotter-5' / 'cycle-companion-59', provider='suprsend', push_key='<redacted>' |

### Per-integration usage, last 30d (2026-05-13→06-12) and 90d (2026-03-14→06-12)

| Integration / metric | 30d records | 30d value | 30d distinct users | 90d records | 90d value | 90d distinct users |
|---|---|---|---|---|---|---|
| litellm_topup (billing, ECU) | 30,473 | 175,954.57 | 2,239 | 56,752 | 348,394.46 | 3,626 |
| tigris gb_stored (billing, ECU) | 1,865,040 | 662.02 | n/a (timeout) | 2,612,980 | 803.88 | n/a |
| tigris gb_stored (usage, GB-days) | 2,391,866 | 67,957.6 | 56,689 (value>0) | 3,142,698 | 85,305.5 | n/a |
| tigris requests_class_a (usage) | 2,391,866 | 2,806,717 | n/a | 3,142,698 | 3,576,477 | n/a |
| tigris requests_class_b (usage) | 2,391,866 | 16,756,001 | n/a | 3,142,698 | 26,178,244 | n/a |
| stripe (app registrations) | 15,845 apps | — | — | 39,042 apps | — | — |

### LiteLLM topup monthly trend (billing_ledger, metric=litellm_topup)

| Month | Entries | Net ECU | Distinct users |
|---|---|---|---|
| 2026-04 (from 04-17) | 12,299 | 82,828.23 | 926 |
| 2026-05 | 37,540 | 212,882.99 | 2,551 |
| 2026-06 (through 06-12) | 6,918 | 52,805.14 | 922 |

### Caveats

- This DB has NO per-request log table and NO status/error columns anywhere — per-provider call volume, latency, and error rates are not derivable here. integrations.request_audit=true exists for tigris but the audit data is not stored in this DB. Use LLM Proxy Postgres (DS 9) or credits_db.credit_ledger (reference_type='UNIVERSAL_KEY') for actual LLM call telemetry.
- billing_ledger.amount and wallet balances are in ECU (Emergent Credit Units), per integration_metrics.unit='ECU' — not confirmed to be USD 1:1; do not report as dollars.
- Internal/test user exclusion was NOT applied: this DB has no email column; user_id values would need joining to analytics.signups_raw_dataset (BigQuery) to exclude *@emergent.sh and the known test user.
- usage_records/billing_ledger/user_integrations data only starts 2026-04-17 (wallets/metering launch), so '90-day' windows effectively cover 2026-04-17→06-12. app_integrations starts 2025-07-06; api_keys/emergent_keys start 2025-07-25.
- Three aggregate queries (joined COUNT DISTINCT over 9.4M-row usage_records and 2.7M-row billing_ledger) hit Redash's 60s timeout; distinct-user counts for tigris request metrics and gb_stored billing were skipped. Workarounds shown in queries section.
- The 'litellm' integration row has status='inactive' in the integrations catalog, yet litellm_topup billing entries flow daily — the status flag appears to control catalog visibility, not the topup pipeline. Interpret with care.
- app_integrations contains ONLY 'stripe' — other integrations users wire up (SendGrid, Twilio, OpenAI-direct, etc.) are not registered in this DB at all.
- June 2026 monthly figures are partial (through 2026-06-12).

<details><summary>Queries used</summary>

**Full schema listing (15 tables + columns)**

```sql
-- via mcp__redash__get_schema {dataSourceId: 18}
```

**Table row counts and date ranges**

```sql
SELECT 'api_keys' AS t, COUNT(*) n, MIN(created_at) min_ts, MAX(created_at) max_ts FROM api_keys UNION ALL SELECT 'app_integrations', COUNT(*), MIN(created_at), MAX(created_at) FROM app_integrations UNION ALL SELECT 'billing_ledger', COUNT(*), MIN(created_at), MAX(created_at) FROM billing_ledger UNION ALL SELECT 'emergent_keys', COUNT(*), MIN(created_at), MAX(created_at) FROM emergent_keys UNION ALL SELECT 'integration_wallets', COUNT(*), MIN(created_at), MAX(created_at) FROM integration_wallets UNION ALL SELECT 'usage_records', COUNT(*), MIN(created_at), MAX(created_at) FROM usage_records UNION ALL SELECT 'user_integrations', COUNT(*), MIN(created_at), MAX(created_at) FROM user_integrations UNION ALL SELECT 'push_apps', COUNT(*), MIN(created_at), MAX(created_at) FROM push_apps UNION ALL SELECT 'storage_orgs', COUNT(*), MIN(created_at), MAX(created_at) FROM storage_orgs UNION ALL SELECT 'storage_buckets', COUNT(*), MIN(created_at), MAX(created_at) FROM storage_buckets UNION ALL SELECT 'integration_metrics', COUNT(*), MIN(created_at), MAX(created_at) FROM integration_metrics
```

**Integrations catalog (only 2 rows: tigris active, litellm inactive)**

```sql
SELECT id, name, display_name, provider_key, category, mode, status, request_audit, default_topup, low_budget_threshold, created_at FROM integrations ORDER BY created_at
```

**app_integrations breakdown — 100% stripe, 1 row per app**

```sql
SELECT integration, COUNT(*) AS rows, COUNT(DISTINCT app) AS distinct_apps, MIN(created_at) AS first_seen, MAX(created_at) AS last_seen FROM app_integrations GROUP BY integration ORDER BY rows DESC
```

**Stripe app adoption 30/90d**

```sql
SELECT COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '30 days') AS stripe_apps_30d, COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '90 days') AS stripe_apps_90d, COUNT(*) AS stripe_apps_all FROM app_integrations
```

**Universal LLM key issuance (all litellm, all active)**

```sql
SELECT provider, status, COUNT(*) AS n, COUNT(DISTINCT user_id) AS distinct_users, MIN(created_at) AS first_seen, MAX(created_at) AS last_seen FROM api_keys GROUP BY provider, status ORDER BY n DESC
```

**Paid vs free universal keys**

```sql
SELECT is_paid, status, COUNT(*) AS n, COUNT(DISTINCT user_id) AS users FROM emergent_keys GROUP BY 1,2 ORDER BY n DESC
```

**Metric ID -> integration mapping**

```sql
SELECT m.id, m.key, i.name AS integration, m.unit FROM integration_metrics m JOIN integrations i ON i.id = m.integration_id
```

**Usage volume per metric, 30d (swap 30->90 for 90d; group-by-id only to avoid 60s Redash timeout)**

```sql
SELECT metric_id, COUNT(*) AS records, SUM(value) AS total_value FROM usage_records WHERE created_at >= NOW() - INTERVAL '30 days' GROUP BY 1
```

**Billing volume per metric, 30d (swap 30->90 for 90d)**

```sql
SELECT metric_id, COUNT(*) AS entries, ROUND(SUM(amount)::numeric,2) AS total_amount FROM billing_ledger WHERE created_at >= NOW() - INTERVAL '30 days' GROUP BY 1
```

**Distinct users topping up universal LLM key, 30/90d**

```sql
SELECT COUNT(DISTINCT user_id) FILTER (WHERE created_at >= NOW() - INTERVAL '30 days') AS litellm_topup_users_30d, COUNT(DISTINCT user_id) AS litellm_topup_users_90d FROM billing_ledger WHERE metric_id = 'e0b2351d-60f1-4f5b-9452-a092e51c63ec' AND created_at >= NOW() - INTERVAL '90 days'
```

**Distinct users with non-zero Tigris storage, 30d**

```sql
SELECT COUNT(DISTINCT user_id) AS tigris_storing_users_30d FROM usage_records WHERE metric_id = '30ff33f9-c058-4bf9-aef5-15f765fdc775' AND created_at >= NOW() - INTERVAL '30 days' AND value > 0
```

**Topup amount distribution (modal = 5 ECU; negatives = reversals)**

```sql
SELECT amount, COUNT(*) AS n FROM billing_ledger WHERE metric_id = 'e0b2351d-60f1-4f5b-9452-a092e51c63ec' AND created_at >= NOW() - INTERVAL '90 days' GROUP BY 1 ORDER BY n DESC LIMIT 10
```

**Monthly litellm topup trend**

```sql
SELECT DATE_TRUNC('month', created_at)::date AS month, COUNT(*) AS topup_entries, ROUND(SUM(amount)::numeric,2) AS net_amount, COUNT(DISTINCT user_id) AS users FROM billing_ledger WHERE metric_id = 'e0b2351d-60f1-4f5b-9452-a092e51c63ec' GROUP BY 1 ORDER BY 1
```

**Wallet balances**

```sql
SELECT COUNT(*) AS wallets, COUNT(*) FILTER (WHERE balance > 0) AS wallets_positive, ROUND(SUM(balance)::numeric,2) AS total_balance, ROUND(AVG(balance)::numeric,4) AS avg_balance FROM integration_wallets
```

**key_config structure without exposing secrets (allowed_providers, auto_topup)**

```sql
SELECT key_config->'llm'->>'allowed_providers' AS allowed_providers, COUNT(*) AS n FROM emergent_keys WHERE is_paid = true AND created_at >= NOW() - INTERVAL '7 days' GROUP BY 1 ORDER BY n DESC LIMIT 10
```

**Provider breakdowns for push/storage provisioning**

```sql
SELECT provider, COUNT(*) AS n FROM push_apps GROUP BY 1; SELECT provider, COUNT(*) AS n, COUNT(DISTINCT user_id) AS users FROM storage_orgs GROUP BY 1
```

**Tigris storage pricing tiers**

```sql
SELECT t.segment, t.up_to, t.unit_price, t.flat_fee, m.key AS metric FROM billing_tiers t JOIN integration_metrics m ON m.id = t.metric_id ORDER BY m.key, t.sort_order
```

</details>


---

## deploy_funnel

### Summary
Build-to-deploy funnel for projects whose root job was created 2026-03-14 to 2026-06-12 (window: last 90 days; deployments as of snapshot 2026-06-12 09:02 UTC; internal users excluded). Of 4,519,055 projects, 708,023 (15.7%) are AI-candidate by the v1 keyword filter. AI projects deploy MORE often, not less: 21,265 of 708,023 AI projects deployed (3.0%) vs 67,448 of 3,811,014 non-AI (1.8%) — a 1.7x relative lift, refuting the hypothesis that AI builds deploy less. The lift holds within every top-10 job template, so it is not just composition (e.g., paid fullstack opus_4_7: AI 11.8% vs non-AI 10.8%; expo: 1.7% vs 1.2%). Custom-domain attach among deployed projects is also slightly higher for AI: 4,764 (22.4% of deployed AI) vs 14,172 (21.0% of deployed non-AI). Deploy rate varies hugely by template: full_stack_app_builder_cloud_v8_opus_4_7 deploys at 11.1% while free tiers deploy at 0.2-0.7% and general_agent at 0.2-0.4%. Cost separates deployers sharply: median AI deployed project cost $111.47 (p25 $37.52, p75 $397.68, mean $661.11) vs $9.43 median for non-deployed AI projects (p25 $1.99, p75 $10.92, mean $27.51) — deployed AI projects cost ~11.8x more at the median, i.e., S3 (deploy) is reached almost exclusively by users who invest heavily in iteration.

### Key numbers

- **Projects with root job created in window (2026-03-14 to 2026-06-12, excl. internal)**: 4,519,055
- **AI-candidate projects (keyword filter v1 on root task)**: 708,023 (15.7% of projects)
- **AI deploy rate**: 3.0% (21,265 / 708,023)
- **Non-AI deploy rate**: 1.8% (67,448 / 3,811,014)
- **AI vs non-AI deploy-rate lift**: 1.7x (3.0% vs 1.8%)
- **Custom domain among deployed, AI**: 4,764 (22.4% of deployed AI)
- **Custom domain among deployed, non-AI**: 14,172 (21.0% of deployed non-AI)
- **Median cost, deployed AI projects (trajectories >= 2026-03-14)**: $111.47
- **Median cost, non-deployed AI projects**: $9.43
- **Deployed vs non-deployed AI median cost ratio**: 11.8x
- **Highest-deploying template (paid fullstack opus_4_7)**: 11.1% overall; AI 11.8% vs non-AI 10.8%

### 1+2) Build-to-deploy funnel, AI vs non-AI (root job created 2026-03-14 to 2026-06-12)

| Segment | Projects | Deployed (any status) | Deploy rate | Custom domain | Custom domain % of deployed |
|---|---:|---:|---:|---:|---:|
| AI-candidate | 708,023 | 21,265 | 3.0% | 4,764 | 22.4% |
| Non-AI | 3,811,014 | 67,448 | 1.8% | 14,172 | 21.0% |
| (null task, unclassifiable) | 18 | 0 | 0.0% | 0 | — |
| Total | 4,519,055 | 88,713 | 2.0% | 18,936 | 21.3% |

### 3) Deploy rate by root prompt_name — top 10 by project count (same window)

| prompt_name | Projects | Deployed | Deploy rate | AI projects | AI deploy rate | Non-AI deploy rate |
|---|---:|---:|---:|---:|---:|---:|
| general_agent_v0_sonnet_4_5 | 612,035 | 2,633 | 0.4% | 85,699 | 0.5% | 0.4% |
| full_stack_app_builder_cloud_v8_sonnet_4_5 | 594,588 | 5,662 | 1.0% | 97,118 | 1.4% | 0.9% |
| expo_fullstack_v0_sonnet_4_5 | 573,445 | 7,488 | 1.3% | 85,357 | 1.7% | 1.2% |
| free_full_stack_app_builder_cloud_v8_opus_4_7 | 508,185 | 2,709 | 0.5% | 91,664 | 0.7% | 0.5% |
| free_expo_fullstack_v0_opus_4_7 | 340,796 | 1,866 | 0.5% | 54,084 | 0.7% | 0.5% |
| free_general_agent_v0_opus_4_7 | 322,248 | 581 | 0.2% | 26,418 | 0.3% | 0.2% |
| free_landing_page_v0_opus_4_7 | 204,033 | 1,835 | 0.9% | 20,596 | 1.1% | 0.9% |
| full_stack_app_builder_cloud_v8_opus_4_5 | 176,612 | 5,710 | 3.2% | 26,205 | 5.2% | 2.9% |
| landing_page_v1_sonnet_4_5 | 152,205 | 3,159 | 2.1% | 14,647 | 3.0% | 2.0% |
| full_stack_app_builder_cloud_v8_opus_4_7 | 128,861 | 14,277 | 11.1% | 33,950 | 11.8% | 10.8% |

### 4) Project cost (SUM trajectories.value_in_usd, 2026-03-14 to 2026-06-12), AI projects: deployed vs non-deployed

| AI projects | n | p25 cost | Median cost | p75 cost | Mean cost |
|---|---:|---:|---:|---:|---:|
| Deployed | 21,265 | $37.52 | $111.47 | $397.68 | $661.11 |
| Not deployed | 686,758 | $1.99 | $9.43 | $10.92 | $27.51 |

### Caveats

- Used `analytics.deployer_db_data_snapshot` (BASE TABLE, 507,778 rows, refreshed 2026-06-12 09:02 UTC) instead of `analytics.deployer_db_data`: the latter is a federated VIEW that times out (>60s) in Redash even on LIMIT 5. Schemas are identical; deploy counts reflect the snapshot moment.
- AI classification is the heuristic keyword filter v1 on the root job's task (first 4,000 chars), not LLM-calibrated; multilingual coverage is partial. Expect both false positives (e.g., 'agents' in real-estate contexts) and false negatives.
- Project = root job (not present as job_id in fork_chain) created >= 2026-03-14; forks are attached via fork_chain.first_job_id. Deployments whose fork-chain root predates the window are excluded by construction.
- Deployed = any row in deployer data for any job in the project, ANY status (active/deleted/unlinked) and any type; this measures 'ever deployed', not 'currently live'.
- Right-censoring: roots created near the end of the window have had less time to deploy; this depresses absolute deploy rates equally for both segments but the AI vs non-AI comparison should be unbiased.
- 18 root projects had NULL task and could not be classified (none deployed); excluded from the AI/non-AI split but included in totals.
- Cost uses SUM(trajectories.value_in_usd) per job aggregated to project, partition-filtered to >= 2026-03-14; complete for in-window roots since trajectories cannot predate job creation. Projects with zero trajectory rows counted as $0. Medians via APPROX_QUANTILES (approximate).
- Cost gap (11.8x) is correlation, not causation: deployers iterate more (more forks/HITL), and bigger spenders are likelier to deploy; do not read as 'spending causes deployment'.
- The 90-day project count (4.5M) means most projects are single-job (fork_chain has only 863K forked jobs all-time); deploy rate per project is therefore close to deploy rate per root job.

<details><summary>Queries used</summary>

**Parts 1+2: funnel — projects, deployed, deploy rate, custom-domain split, AI vs non-AI (BigQuery DS 7)**

```sql
WITH internal_users AS (
  SELECT DISTINCT user_id FROM `analytics.signups_raw_dataset` WHERE email LIKE '%emergent.sh'
),
roots AS (
  SELECT j.id AS project_id,
    REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)') AS is_ai
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON j.id = fc.job_id
  WHERE j.created_at >= TIMESTAMP('2026-03-14')
    AND fc.job_id IS NULL
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
    AND j.user_id NOT IN (SELECT user_id FROM internal_users)
),
deployed_projects AS (
  SELECT COALESCE(fc.first_job_id, d.job_id) AS project_id,
    LOGICAL_OR(d.type = 'custom_domain') AS has_custom_domain
  FROM `analytics.deployer_db_data_snapshot` d
  LEFT JOIN `analytics.fork_chain` fc ON d.job_id = fc.job_id
  GROUP BY 1
)
SELECT r.is_ai, COUNT(*) AS n_projects,
  COUNTIF(dp.project_id IS NOT NULL) AS n_deployed,
  ROUND(100 * COUNTIF(dp.project_id IS NOT NULL) / COUNT(*), 1) AS deploy_rate_pct,
  COUNTIF(dp.has_custom_domain) AS n_custom_domain,
  ROUND(100 * COUNTIF(dp.has_custom_domain) / NULLIF(COUNTIF(dp.project_id IS NOT NULL),0), 1) AS custom_domain_pct_of_deployed
FROM roots r
LEFT JOIN deployed_projects dp ON r.project_id = dp.project_id
GROUP BY r.is_ai ORDER BY r.is_ai DESC
```

**Part 3: deploy rate by root prompt_name, top 10 by project count, with AI/non-AI split (BigQuery DS 7)**

```sql
WITH internal_users AS (
  SELECT DISTINCT user_id FROM `analytics.signups_raw_dataset` WHERE email LIKE '%emergent.sh'
),
roots AS (
  SELECT j.id AS project_id, j.prompt_name,
    REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)') AS is_ai
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON j.id = fc.job_id
  WHERE j.created_at >= TIMESTAMP('2026-03-14')
    AND fc.job_id IS NULL
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
    AND j.user_id NOT IN (SELECT user_id FROM internal_users)
),
deployed_projects AS (
  SELECT COALESCE(fc.first_job_id, d.job_id) AS project_id
  FROM `analytics.deployer_db_data_snapshot` d
  LEFT JOIN `analytics.fork_chain` fc ON d.job_id = fc.job_id
  GROUP BY 1
)
SELECT COALESCE(r.prompt_name, '(null)') AS prompt_name,
  COUNT(*) AS n_projects,
  COUNTIF(dp.project_id IS NOT NULL) AS n_deployed,
  ROUND(100 * COUNTIF(dp.project_id IS NOT NULL) / COUNT(*), 1) AS deploy_rate_pct,
  COUNTIF(r.is_ai) AS n_ai_projects,
  COUNTIF(r.is_ai AND dp.project_id IS NOT NULL) AS n_ai_deployed,
  ROUND(100 * COUNTIF(r.is_ai AND dp.project_id IS NOT NULL) / NULLIF(COUNTIF(r.is_ai),0), 1) AS ai_deploy_rate_pct,
  ROUND(100 * COUNTIF(NOT r.is_ai AND dp.project_id IS NOT NULL) / NULLIF(COUNTIF(NOT r.is_ai),0), 1) AS nonai_deploy_rate_pct
FROM roots r
LEFT JOIN deployed_projects dp ON r.project_id = dp.project_id
GROUP BY 1 ORDER BY n_projects DESC LIMIT 10
```

**Part 4: median/quartile project cost (SUM trajectories.value_in_usd), deployed vs non-deployed AI projects (BigQuery DS 7)**

```sql
WITH internal_users AS (
  SELECT DISTINCT user_id FROM `analytics.signups_raw_dataset` WHERE email LIKE '%emergent.sh'
),
ai_roots AS (
  SELECT j.id AS project_id
  FROM `analytics.jobs_full_view` j
  LEFT JOIN `analytics.fork_chain` fc ON j.id = fc.job_id
  WHERE j.created_at >= TIMESTAMP('2026-03-14')
    AND fc.job_id IS NULL
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
    AND j.user_id NOT IN (SELECT user_id FROM internal_users)
    AND REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)')
),
project_jobs AS (
  SELECT project_id, project_id AS job_id FROM ai_roots
  UNION ALL
  SELECT r.project_id, fc.job_id FROM ai_roots r JOIN `analytics.fork_chain` fc ON fc.first_job_id = r.project_id
),
job_costs AS (
  SELECT job_id, SUM(value_in_usd) AS cost
  FROM `analytics.trajectories_full_view`
  WHERE DATE(created_at) >= '2026-03-14'
  GROUP BY job_id
),
project_costs AS (
  SELECT pj.project_id, COALESCE(SUM(jc.cost), 0) AS project_cost
  FROM project_jobs pj LEFT JOIN job_costs jc ON pj.job_id = jc.job_id
  GROUP BY 1
),
deployed_projects AS (
  SELECT DISTINCT COALESCE(fc.first_job_id, d.job_id) AS project_id
  FROM `analytics.deployer_db_data_snapshot` d
  LEFT JOIN `analytics.fork_chain` fc ON d.job_id = fc.job_id
)
SELECT dp.project_id IS NOT NULL AS deployed, COUNT(*) AS n_projects,
  ROUND(APPROX_QUANTILES(pc.project_cost, 100)[OFFSET(25)], 2) AS p25_cost_usd,
  ROUND(APPROX_QUANTILES(pc.project_cost, 100)[OFFSET(50)], 2) AS median_cost_usd,
  ROUND(APPROX_QUANTILES(pc.project_cost, 100)[OFFSET(75)], 2) AS p75_cost_usd,
  ROUND(AVG(pc.project_cost), 2) AS avg_cost_usd
FROM project_costs pc
LEFT JOIN deployed_projects dp ON pc.project_id = dp.project_id
GROUP BY 1 ORDER BY 1 DESC
```

</details>


---

## conversion

### Summary
Window: signups 2026-03-14 → 2026-06-12 (last 90 days), BigQuery analytics.conversions_dataset, internal users excluded (3,965,561 signups). ACQUISITION MIX: Fullstack Builder is the dominant first-prompt type (1,644,637 signups, 41.5%), followed by no-first-job/uncategorized (1,255,040, 31.6%), General Agent (623,378, 15.7%), Landing Page (310,053, 7.8%); everything else (Other, Replica/Portfolio Agent, etc.) is <2% each. Expo Builder did not appear at all in the last 90 days. CONVERSION BY PROMPT TYPE (24h, complete-window users only; overall baseline 4.5% = 175,983/3,924,138): Fullstack Builder 4.9%, Landing Page 4.6%, Replica Agent 4.4%, Portfolio Agent 3.5%, General Agent only 2.4%, Other 2.0%. DEVICE: Desktop converts 6.9% (38.4% of signups) vs Mobile Web 3.1% (44.7% of signups) and Mobile App 2.6% (16.0%) — a 2.2-2.7x desktop premium. COUNTRY: India is 40.3% of signups but converts at 2.4%; US is 7.8% of signups at 11.5%; UK 9.2%, Brazil 9.1%, France 5.9%, Mexico 5.4%; Indonesia worst of top-10 at 1.5%. H3 TEST (AI-intent first prompt): joining every signup's first job in jobs_full_view and applying the AI-product keyword filter v1: 389,391 signups (9.8% of all; 14.1% of the 2.76M who created a job) had an AI-candidate first prompt. Their 24h conversion is 8.8% (34,062/385,327) vs 5.3% (124,864/2,347,499) for non-AI first prompts and 1.4% for no-first-job users — a 1.66x lift over other job creators and ~2x the overall baseline. H3 is SUPPORTED: AI-intent users are a high-converting acquisition segment, and they already contribute 19.4% of all 24h conversions (34,062/175,983) from only 9.8% of signups.

### Key numbers

- **Signups last 90 days (2026-03-14 to 2026-06-12, internal excluded)**: 3,965,561
- **Overall 24h signup→paid conversion (complete-window users)**: 4.5% (175,983 / 3,924,138)
- **Top prompt_type: Fullstack Builder share / conv rate**: 41.5% of signups / 4.9%
- **General Agent share / conv rate (worst major type)**: 15.7% of signups / 2.4%
- **Desktop vs Mobile Web conv rate**: 6.9% vs 3.1%
- **India share / conv rate**: 40.3% of signups / 2.4%
- **US share / conv rate**: 7.8% of signups / 11.5%
- **AI-first-prompt signups (keyword filter v1 on first job)**: 389,391 (9.8% of signups; 14.1% of job creators)
- **H3: 24h conv AI-first vs non-AI-first vs no-job**: 8.8% vs 5.3% vs 1.4% (1.66x lift over non-AI job creators)
- **Share of all 24h conversions from AI-first-prompt users**: 19.4% (34,062 / 175,983)

### 1+2) Prompt_type distribution & 24h conversion — signups 2026-03-14 to 2026-06-12 (conv rate on has_complete_24h_window=1)

| prompt_type | signups | % of signups | complete-window users | conversions 24h | conv rate 24h |
|---|---:|---:|---:|---:|---:|
| Fullstack Builder | 1,644,637 | 41.5% | 1,626,985 | 79,558 | 4.9% |
| (no first job / uncategorized) | 1,255,040 | 31.6% | 1,241,035 | 63,497 | 5.1% |
| General Agent | 623,378 | 15.7% | 617,921 | 14,797 | 2.4% |
| Landing Page | 310,053 | 7.8% | 306,297 | 14,042 | 4.6% |
| Other | 62,115 | 1.6% | 62,031 | 1,242 | 2.0% |
| Replica Agent | 47,235 | 1.2% | 46,783 | 2,047 | 4.4% |
| Portfolio Agent | 22,784 | 0.6% | 22,784 | 792 | 3.5% |
| Auto Selector | 299 | 0.0% | 282 | 8 | 2.8% |
| Prototype Agent | 17 | 0.0% | 17 | 0 | 0.0% |
| Frontend Builder | 2 | 0.0% | 2 | 0 | 0.0% |
| Import | 1 | 0.0% | 1 | 0 | 0.0% |
| **Total** | **3,965,561** | **100%** | **3,924,138** | **175,983** | **4.5%** |

### 3a) 24h conversion by device_type — same window

| device_type | signups | % of signups | complete-window users | conversions 24h | conv rate 24h |
|---|---:|---:|---:|---:|---:|
| Mobile Web | 1,771,242 | 44.7% | 1,749,974 | 54,768 | 3.1% |
| Desktop | 1,521,392 | 38.4% | 1,501,869 | 103,670 | 6.9% |
| Mobile App | 633,452 | 16.0% | 633,240 | 16,255 | 2.6% |
| Tablet | 39,475 | 1.0% | 39,055 | 1,290 | 3.3% |

### 3b) 24h conversion by top-10 country (by signups) — same window

| country | signups | % of signups | complete-window users | conversions 24h | conv rate 24h |
|---|---:|---:|---:|---:|---:|
| India | 1,596,702 | 40.3% | 1,580,884 | 38,533 | 2.4% |
| United States | 308,124 | 7.8% | 304,043 | 35,039 | 11.5% |
| Indonesia | 223,273 | 5.6% | 219,308 | 3,255 | 1.5% |
| Brazil | 150,126 | 3.8% | 149,024 | 13,503 | 9.1% |
| France | 130,737 | 3.3% | 128,762 | 7,624 | 5.9% |
| Italy | 96,453 | 2.4% | 95,702 | 3,860 | 4.0% |
| Spain | 90,536 | 2.3% | 89,845 | 4,356 | 4.8% |
| United Kingdom | 80,161 | 2.0% | 79,412 | 7,287 | 9.2% |
| Türkiye | 71,102 | 1.8% | 70,451 | 2,027 | 2.9% |
| Mexico | 68,629 | 1.7% | 67,961 | 3,654 | 5.4% |

### 4) H3: AI keyword filter v1 on first-job task vs 24h conversion (full join, not sampled) — same window

| segment | signups | % of signups | complete-window users | conversions 24h | conv rate 24h |
|---|---:|---:|---:|---:|---:|
| non_ai_first_prompt | 2,371,168 | 59.8% | 2,347,499 | 124,864 | 5.3% |
| no_first_job | 1,205,002 | 30.4% | 1,191,312 | 17,057 | 1.4% |
| ai_first_prompt | 389,391 | 9.8% | 385,327 | 34,062 | **8.8%** |

### Caveats

- AI-candidate classification uses keyword filter v1 (heuristic, multilingual-ish); not yet LLM-calibrated — expect some false positives (e.g. 'agent' in real-estate-agent prompts) and false negatives in non-Latin languages.
- Conversion rates computed only on has_complete_24h_window=1 (3,924,138 of 3,965,561 signups), so the most recent ~24h of signups are excluded from rate denominators.
- prompt_type NULL (31.6%) is not identical to 'created no job': the jobs_full_view join finds 50,038 NULL-prompt_type users who did create a first job. The NULL group converts at 5.1% while true no-first-job users convert at 1.4% — suggesting prompt_type categorization misses some job creators (likely pay-before-first-free-job users), so per-prompt_type rates are slightly understated for categorized types.
- First job identified as earliest jobs_full_view row per user with created_at >= 2026-03-14; valid because all signups are >= that date, but jobs include forks/follow-ups only after the true first job so ordering is safe.
- Internal exclusion: emails LIKE '%emergent.sh' and the one flagged user_id removed via signups_raw_dataset join; signups without an email row in signups_raw_dataset are dropped by the inner join (counts may differ slightly from raw conversions_dataset).
- Country/device rates are overall (not per prompt_type) as requested; India+Indonesia = 45.9% of signups at <2.5% conversion heavily depresses the blended 4.5% baseline.
- Bonus query scanned 11.2 GB (jobs_full_view task column is unpartitioned); full-population join used, no sampling needed.

<details><summary>Queries used</summary>

**Q1+Q2: prompt_type distribution (all signups, last 90d) and 24h conversion by prompt_type (complete-window only)**

```sql
WITH base AS (
  SELECT c.user_id, c.prompt_type, c.converted_within_24h, c.has_complete_24h_window
  FROM `analytics.conversions_dataset` c
  JOIN `analytics.signups_raw_dataset` s ON s.user_id = c.user_id
  WHERE DATE(c.signup_timestamp) >= '2026-03-14'
    AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
    AND c.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
)
SELECT COALESCE(prompt_type, '(no first job / uncategorized)') AS prompt_type,
  COUNT(*) AS signups,
  ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_signups,
  COUNTIF(has_complete_24h_window = 1) AS users_complete_window,
  COUNTIF(has_complete_24h_window = 1 AND converted_within_24h = 1) AS conversions_24h,
  ROUND(100 * COUNTIF(has_complete_24h_window = 1 AND converted_within_24h = 1) / NULLIF(COUNTIF(has_complete_24h_window = 1), 0), 1) AS conv_rate_24h_pct
FROM base GROUP BY 1 ORDER BY signups DESC
```

**Q3a: 24h conversion by device_type (same base CTE)**

```sql
WITH base AS ( /* same base as Q1, plus device_type */ SELECT c.device_type, c.converted_within_24h, c.has_complete_24h_window FROM `analytics.conversions_dataset` c JOIN `analytics.signups_raw_dataset` s ON s.user_id = c.user_id WHERE DATE(c.signup_timestamp) >= '2026-03-14' AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh') AND c.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2')
SELECT COALESCE(device_type,'(unknown)') AS device_type, COUNT(*) AS signups,
  ROUND(100*COUNT(*)/SUM(COUNT(*)) OVER (),1) AS pct_of_signups,
  COUNTIF(has_complete_24h_window=1) AS users_complete_window,
  COUNTIF(has_complete_24h_window=1 AND converted_within_24h=1) AS conversions_24h,
  ROUND(100*COUNTIF(has_complete_24h_window=1 AND converted_within_24h=1)/NULLIF(COUNTIF(has_complete_24h_window=1),0),1) AS conv_rate_24h_pct
FROM base GROUP BY 1 ORDER BY signups DESC
```

**Q3b: 24h conversion by top-10 country_name by signups (same base CTE)**

```sql
WITH base AS ( /* same base as Q1, plus country_name */ SELECT c.country_name, c.converted_within_24h, c.has_complete_24h_window FROM `analytics.conversions_dataset` c JOIN `analytics.signups_raw_dataset` s ON s.user_id = c.user_id WHERE DATE(c.signup_timestamp) >= '2026-03-14' AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh') AND c.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2')
SELECT COALESCE(country_name,'(unknown)') AS country_name, COUNT(*) AS signups,
  ROUND(100*COUNT(*)/SUM(COUNT(*)) OVER (),1) AS pct_of_signups,
  COUNTIF(has_complete_24h_window=1) AS users_complete_window,
  COUNTIF(has_complete_24h_window=1 AND converted_within_24h=1) AS conversions_24h,
  ROUND(100*COUNTIF(has_complete_24h_window=1 AND converted_within_24h=1)/NULLIF(COUNTIF(has_complete_24h_window=1),0),1) AS conv_rate_24h_pct
FROM base GROUP BY 1 ORDER BY signups DESC LIMIT 10
```

**Q4 (H3): join each signup's first job from jobs_full_view, apply AI keyword filter v1 to SUBSTR(task,1,4000), compare 24h conversion across ai_first_prompt / non_ai_first_prompt / no_first_job**

```sql
WITH signups AS (
  SELECT c.user_id, c.converted_within_24h, c.has_complete_24h_window
  FROM `analytics.conversions_dataset` c
  JOIN `analytics.signups_raw_dataset` s ON s.user_id = c.user_id
  WHERE DATE(c.signup_timestamp) >= '2026-03-14'
    AND (s.email IS NULL OR s.email NOT LIKE '%emergent.sh')
    AND c.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
),
first_jobs AS (
  SELECT user_id, task_head FROM (
    SELECT j.user_id, SUBSTR(j.task,1,4000) AS task_head,
      ROW_NUMBER() OVER (PARTITION BY j.user_id ORDER BY j.created_at) AS rn
    FROM `analytics.jobs_full_view` j
    WHERE DATE(j.created_at) >= '2026-03-14'
      AND j.user_id IN (SELECT user_id FROM signups)
  ) WHERE rn = 1
)
SELECT
  CASE WHEN fj.user_id IS NULL THEN 'no_first_job'
       WHEN REGEXP_CONTAINS(LOWER(fj.task_head), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)') THEN 'ai_first_prompt'
       ELSE 'non_ai_first_prompt' END AS segment,
  COUNT(*) AS signups,
  ROUND(100*COUNT(*)/SUM(COUNT(*)) OVER (),1) AS pct_of_signups,
  COUNTIF(sc.has_complete_24h_window=1) AS users_complete_window,
  COUNTIF(sc.has_complete_24h_window=1 AND sc.converted_within_24h=1) AS conversions_24h,
  ROUND(100*COUNTIF(sc.has_complete_24h_window=1 AND sc.converted_within_24h=1)/NULLIF(COUNTIF(sc.has_complete_24h_window=1),0),1) AS conv_rate_24h_pct
FROM signups sc LEFT JOIN first_jobs fj USING (user_id)
GROUP BY 1 ORDER BY signups DESC
```

</details>


---

## universal_key

### Summary
Universal LLM Key adoption, last 90 days (2026-03-14 → 2026-06-12, internal users excluded, ledger deduped). (1) Scale: 408,325 UNIVERSAL_KEY debit transactions from 123,104 distinct users totaling 2,998,599 ECU. Weekly trend: rapid ramp to a peak of 15,492 users in week of 2026-03-30, then user counts drifted down to ~7-9k/week by June while weekly ECU held roughly flat (~185k-260k ECU/week) — ECU per weekly user roughly doubled from ~17 to ~28, i.e. fewer but heavier users. (2) Context: UNIVERSAL_KEY is the 4th-largest debit type by ECU but only 1.5% of all debit ECU (2.99M of 201.2M; LLM_CALL dominates at 161.2M ECU / 3.18M users). By user reach, UNIVERSAL_KEY's 123k users ≈ 3.9% of the 3.18M users with LLM_CALL debits. (3) AI overlap — the H6 headline: 62,678 of 123,104 universal-key users (50.9%) match the AI-candidate keyword filter on jobs in the same 90d window (54.1% of the 115,804 UK users who created any job). Baseline among ALL job-creating users: 600,993 of 3,174,166 = 18.9% AI-candidate. So universal-key users are ~2.9x more likely to be AI-product builders than the average builder — strong support that the universal key is disproportionately an AI-builder feature, consistent with H6 (though direction of causality is not established: AI builds may require the key rather than the key inducing AI builds). (4) Spend per universal-key user over 90d is small and skewed: p50 = 5 ECU, p90 = 25 ECU, p99 = 228.9 ECU, mean 24.4 ECU, max 95,830 ECU; median user has just 1 UNIVERSAL_KEY transaction (p90 = 4). Interpretation: adoption is broad-but-shallow — a large AI-skewed user base touches the key lightly, with revenue concentrated in a small heavy tail; as an activation lever the key reaches the right segment, but per-user monetization is currently minimal (median 5 ECU ≈ rounding error vs. typical build costs).

### Key numbers

- **UNIVERSAL_KEY total ECU (90d: 2026-03-14→2026-06-12)**: 2,998,599 ECU
- **UNIVERSAL_KEY transactions (90d)**: 408,325
- **UNIVERSAL_KEY distinct users (90d)**: 123,104
- **UNIVERSAL_KEY share of all DEBIT ECU (90d)**: 1.5% (2.99M / 201.2M ECU)
- **UK users as share of LLM_CALL-active users (90d)**: 3.9% (123,104 / 3,182,751)
- **UK users matching AI-candidate job filter (90d)**: 62,678 / 123,104 = 50.9% (54.1% of the 115,804 UK users with ≥1 job)
- **Baseline AI-candidate share among all job-creating users (90d)**: 18.9% (600,993 / 3,174,166)
- **AI-candidate lift for UK users vs baseline**: ~2.9x (54.1% vs 18.9%)
- **Per-user UNIVERSAL_KEY spend p50 / p90 (90d)**: 5 ECU / 25 ECU (mean 24.4, p99 228.9, max 95,830)
- **Median UNIVERSAL_KEY transactions per user (90d)**: 1 (p90 = 4)
- **Peak weekly UK users**: 15,492 (week of 2026-03-30); ~7-9k/week by June

### Weekly UNIVERSAL_KEY trend (week starting Monday; first row covers only Mar 14-15, last row partial through Fri Jun 12)

| week_start | users | transactions | total_ecu |
|---|---|---|---|
| 2026-03-09* | 2,865 | 7,394 | 46,494.52 |
| 2026-03-16 | 10,423 | 30,317 | 188,369.54 |
| 2026-03-23 | 13,019 | 32,126 | 221,108.33 |
| 2026-03-30 | 15,492 | 37,688 | 263,542.07 |
| 2026-04-06 | 12,334 | 31,250 | 246,825.34 |
| 2026-04-13 | 11,018 | 31,709 | 239,985.30 |
| 2026-04-20 | 11,072 | 31,151 | 232,564.83 |
| 2026-04-27 | 11,831 | 30,456 | 236,077.89 |
| 2026-05-04 | 11,216 | 27,718 | 227,865.56 |
| 2026-05-11 | 11,423 | 28,649 | 221,107.44 |
| 2026-05-18 | 9,089 | 24,895 | 193,432.76 |
| 2026-05-25 | 8,330 | 28,115 | 249,303.49 |
| 2026-06-01 | 9,054 | 39,202 | 248,506.76 |
| 2026-06-08* | 7,197 | 27,657 | 183,424.97 |

### All DEBIT reference_types, 90d (2026-03-14→2026-06-12)

| reference_type | transactions | distinct_users | total_ecu | % of debit ECU |
|---|---|---|---|---|
| LLM_CALL | 266,256,087 | 3,182,751 | 161,248,024.67 | 80.1% |
| DEPLOYMENT | 331,173 | 109,246 | 17,408,600.00 | 8.7% |
| EXPIRED | 166,156 | 112,832 | 12,846,041.56 | 6.4% |
| UNIVERSAL_KEY | 408,325 | 123,103 | 2,998,598.79 | 1.5% |
| EXPIRY_MANUAL | 42,332 | 42,332 | 2,847,820.68 | 1.4% |
| SUPPORT | 21,355 | 19,492 | 1,972,379.34 | 1.0% |
| ENV_CREATION | 4,579,951 | 3,125,156 | 915,303.80 | 0.5% |
| TOOL_CALL | 2,310,701 | 208,656 | 527,728.96 | 0.3% |
| BOOST_EXPIRED | 3,983 | 3,983 | 231,989.06 | 0.1% |
| MONGO_SUBSCRIPTION | 244 | 151 | 157,600.00 | 0.1% |
| POD_UPGRADE | 45,654 | 42,405 | 44,819.00 | 0.0% |
| TOTAL | 274,165,961 | — | 201,198,905.86 | 100% |

### H6 test: UNIVERSAL_KEY users vs AI-candidate job set (90d) + per-user spend distribution

| metric | value |
|---|---|
| UK users total | 123,104 |
| UK users with ≥1 job in window | 115,804 (94.1%) |
| UK users with ≥1 AI-candidate job | 62,678 (50.9% of all UK; 54.1% of UK w/ jobs) |
| All job-creating users (baseline) | 3,174,166 |
| Baseline AI-candidate share | 600,993 (18.9%) |
| Lift: UK vs baseline | ~2.9x |
| Per-user UK ECU: p50 / p90 / p99 / mean / max | 5 / 25 / 228.85 / 24.36 / 95,830 |
| Per-user UK transactions: p50 / p90 | 1 / 4 |

### Caveats

- AI-candidate filter is the v1 keyword heuristic on SUBSTR(task,1,4000) — pending LLM calibration; it overcounts (e.g. 'agent' in non-AI contexts) and undercounts (AI features described without keywords).
- Overlap measures correlation, not causation: AI-product apps mechanically require an LLM key at runtime, so AI builders self-select into UNIVERSAL_KEY usage; this does not prove the key activates AI builds (H6 direction untested).
- Internal-user exclusion (email NOT LIKE '%emergent.sh') only applies to user_ids present in analytics.signups_raw_dataset; ledger rows for users missing from signups are retained.
- Distinct UK user count varies by 1 across queries (123,103 vs 123,104) — queries ran minutes apart on live data; immaterial.
- Weekly trend: first bucket (week_start 2026-03-09) covers only Mar 14-15; last bucket (2026-06-08) is partial through Jun 12 (~5 of 7 days).
- Context table includes non-usage debit types not in the documented enum (EXPIRED, EXPIRY_MANUAL, BOOST_EXPIRED = credit expirations; SUPPORT, MONGO_SUBSCRIPTION); excluding expirations, UNIVERSAL_KEY is 1.6% of usage-debit ECU.
- credit_ledger deduped via QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY created_at)=1 per known duplication issue; ECU figures are credits, not USD.
- jobs_full_view is not partitioned; the 90d job filter used created_at >= TIMESTAMP('2026-03-14') and per-user aggregation to control scan size (~28.5 GB scanned).

<details><summary>Queries used</summary>

**Q1 totals: UNIVERSAL_KEY debits last 90d — transactions, distinct users, total ECU (deduped, internal excluded)**

```sql
WITH ledger AS (
  SELECT id, user_id, created_at, ecu
  FROM `credits_db.credit_ledger`
  WHERE DATE(created_at) >= '2026-03-14'
    AND transaction_type = 'DEBIT'
    AND reference_type = 'UNIVERSAL_KEY'
  QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY created_at) = 1
),
internal AS (
  SELECT DISTINCT user_id FROM `analytics.signups_raw_dataset`
  WHERE email LIKE '%emergent.sh'
),
clean AS (
  SELECT l.* FROM ledger l
  LEFT JOIN internal i ON l.user_id = i.user_id
  WHERE i.user_id IS NULL
    AND l.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
)
SELECT COUNT(*) AS n_transactions,
       COUNT(DISTINCT user_id) AS distinct_users,
       ROUND(SUM(ecu), 2) AS total_ecu
FROM clean
```

**Q1 weekly trend: users, transactions, ECU per week (Monday weeks)**

```sql
-- same ledger/internal/clean CTEs as above, then:
SELECT DATE_TRUNC(DATE(created_at), WEEK(MONDAY)) AS week_start,
       COUNT(DISTINCT user_id) AS users,
       COUNT(*) AS n_transactions,
       ROUND(SUM(ecu), 2) AS total_ecu
FROM clean
GROUP BY week_start
ORDER BY week_start
```

**Q2 context: all DEBIT reference_types last 90d — ECU + distinct users per type**

```sql
WITH ledger AS (
  SELECT id, user_id, created_at, ecu, reference_type
  FROM `credits_db.credit_ledger`
  WHERE DATE(created_at) >= '2026-03-14'
    AND transaction_type = 'DEBIT'
  QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY created_at) = 1
),
internal AS (
  SELECT DISTINCT user_id FROM `analytics.signups_raw_dataset`
  WHERE email LIKE '%emergent.sh'
),
clean AS (
  SELECT l.* FROM ledger l
  LEFT JOIN internal i ON l.user_id = i.user_id
  WHERE i.user_id IS NULL
    AND l.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
)
SELECT reference_type, COUNT(*) AS n_transactions,
       COUNT(DISTINCT user_id) AS distinct_users,
       ROUND(SUM(ecu), 2) AS total_ecu
FROM clean
GROUP BY reference_type
ORDER BY total_ecu DESC
```

**Q3 overlap: UK users joined to AI-candidate keyword filter on jobs_full_view (90d), with all-job-user baseline**

```sql
WITH internal AS (
  SELECT DISTINCT user_id FROM `analytics.signups_raw_dataset`
  WHERE email LIKE '%emergent.sh'
),
uk_users AS (
  SELECT DISTINCT l.user_id
  FROM `credits_db.credit_ledger` l
  LEFT JOIN internal i ON l.user_id = i.user_id
  WHERE DATE(l.created_at) >= '2026-03-14'
    AND l.transaction_type = 'DEBIT'
    AND l.reference_type = 'UNIVERSAL_KEY'
    AND i.user_id IS NULL
    AND l.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
),
job_users AS (
  SELECT j.user_id,
         MAX(CAST(REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)') AS INT64)) AS is_ai_candidate
  FROM `analytics.jobs_full_view` j
  LEFT JOIN internal i ON j.user_id = i.user_id
  WHERE j.created_at >= TIMESTAMP('2026-03-14')
    AND i.user_id IS NULL
    AND j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
  GROUP BY j.user_id
)
SELECT
  (SELECT COUNT(*) FROM uk_users) AS uk_users_total,
  (SELECT COUNT(*) FROM uk_users u JOIN job_users j ON u.user_id = j.user_id) AS uk_users_with_jobs,
  (SELECT COUNT(*) FROM uk_users u JOIN job_users j ON u.user_id = j.user_id AND j.is_ai_candidate = 1) AS uk_users_ai_candidate,
  (SELECT COUNT(*) FROM job_users) AS all_job_users,
  (SELECT COUNTIF(is_ai_candidate = 1) FROM job_users) AS all_job_users_ai_candidate
```

**Q4 spend distribution: per-user UNIVERSAL_KEY ECU and transaction percentiles (90d)**

```sql
-- same ledger/internal CTEs as Q1, then:
WITH per_user AS (
  SELECT l.user_id, SUM(l.ecu) AS uk_ecu, COUNT(*) AS uk_tx
  FROM ledger l
  LEFT JOIN internal i ON l.user_id = i.user_id
  WHERE i.user_id IS NULL
    AND l.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
  GROUP BY l.user_id
)
SELECT COUNT(*) AS n_users,
       ROUND(AVG(uk_ecu), 2) AS avg_ecu,
       ROUND(APPROX_QUANTILES(uk_ecu, 100)[OFFSET(50)], 2) AS p50_ecu,
       ROUND(APPROX_QUANTILES(uk_ecu, 100)[OFFSET(90)], 2) AS p90_ecu,
       ROUND(APPROX_QUANTILES(uk_ecu, 100)[OFFSET(99)], 2) AS p99_ecu,
       ROUND(MAX(uk_ecu), 2) AS max_ecu,
       ROUND(APPROX_QUANTILES(uk_tx, 100)[OFFSET(50)], 1) AS p50_tx,
       ROUND(APPROX_QUANTILES(uk_tx, 100)[OFFSET(90)], 1) AS p90_tx
FROM per_user
```

</details>


---

## errors_baseline

### Summary
Error-signature baseline on AI-candidate jobs, trajectories window 2026-04-14 → 2026-06-12 (~60d), internal users excluded. (1) Scale: AI-candidate jobs generated 63.45M trajectory steps across 489,184 jobs, with 12,387 error steps (steps with non-empty error_message). The top friction signature by far is the generic "Something went wrong, Internal server error" — 4,703 error steps across 2,172 jobs and 1,880 distinct users, 38.0% of all AI error steps. Next: Cloud Build failures (3 retry-prefix variants totaling ~2,380 steps / ~1,185 jobs), frontend health-check failures (824 steps / 423 jobs), a template-prep "dynamic_manifest" error (699 steps but only 120 jobs — highly concentrated, likely one broken template path), "Failed to restart environment" (694 steps / 413 jobs / 408 users — almost 1 error per user, a wide-blast-radius signature), context-limit errors (616 steps / 238 jobs), and "failed to fetch envs from source pod" (543 steps / 432 jobs). (2) AI vs non-AI step-level error rates are nearly identical: 0.0195% (12,387/63,452,498) for AI vs 0.0209% (21,859/104,746,279) for non-AI — AI jobs are NOT intrinsically more error-prone per step. However, at the job level, 1.14% of AI jobs hit at least one error vs 0.43% of non-AI jobs (2.6x), driven by AI jobs being far longer: ~129.7 steps/job vs ~45.9 steps/job. So AI builders accumulate more error exposure per project simply through session length. (3) Agent attribution: errors on AI jobs are almost entirely from EmergentAssistant (12,071 error steps, 97.4% of total, 0.0226% rate over 53.46M steps); SkilledAssistant contributes 316 (0.0032% rate over 9.98M steps); no other agent_name produced errors. Headline for Phase 4: the biggest AI-segment friction is platform/infra (generic 500s, Cloud Build, env restart/fetch), not model-side; the context-limit signature (616 steps, 238 jobs) is the most AI-segment-relevant product fix since long AI builds hit it via session length.

### Key numbers

- **AI-candidate error steps (2026-04-14 to 2026-06-12)**: 12,387 of 63,452,498 steps (0.0195%)
- **Non-AI error steps, same window**: 21,859 of 104,746,279 steps (0.0209%)
- **Job-level error incidence: AI vs non-AI**: 1.14% (5,579/489,184) vs 0.43% (9,871/2,283,150) — 2.6x
- **Avg steps per job: AI vs non-AI**: 129.7 vs 45.9
- **#1 signature: 'Something went wrong, Internal server error'**: 4,703 steps / 2,172 jobs / 1,880 users (38.0% of AI error steps)
- **#2 family: Cloud Build failed (3 retry-nesting variants)**: ~2,380 steps / ~1,185 jobs
- **Context-limit errors on AI jobs**: 616 steps / 238 jobs / 202 users
- **EmergentAssistant share of AI-job errors**: 12,071 / 12,387 = 97.4% (rate 0.0226%); SkilledAssistant 316 (0.0032%)

### Top 25 normalized error signatures on AI-candidate jobs (trajectories 2026-04-14 → 2026-06-12; first 80 chars, ids/uuids/numbers stripped)

| # | Signature (truncated @80) | Error steps | Distinct jobs | Distinct users |
|---|---|---|---|---|
| 1 | Something went wrong, Internal server error. Please try again in some time. If i | 4,703 | 2,172 | 1,880 |
| 2 | not retryable: not retryable: Cloud Build failed: cloud build: build failed: | 1,695 | 700 | 585 |
| 3 | not retryable: frontend health check failed after <n> attempts | 824 | 423 | 316 |
| 4 | not retryable: prepare template files: get template data: dynamic_manifest enabl | 699 | 120 | 111 |
| 5 | Failed to restart environment | 694 | 413 | 408 |
| 6 | not retryable: not retryable: not retryable: Cloud Build failed: cloud build: bu | 654 | 469 | 435 |
| 7 | You have reached the context limit. To continue either Rollback and Erase messag | 616 | 238 | 202 |
| 8 | not retryable: failed to fetch envs from source pod: failed to get template name | 543 | 432 | 397 |
| 9 | not retryable: nginx template mismatch detected: app URL returns nginx welcome p | 199 | 131 | 120 |
| 10 | We couldn't process your request because it was blocked by our content filtering | 172 | 70 | 64 |
| 11 | not retryable: there has been an error with this deployment. Please fork the ses | 172 | 170 | 120 |
| 12 | not retryable: copy files from pod: copy code: failed to extract tar archive: ex | 137 | 66 | 61 |
| 13 | not retryable: failed to list source databases: failed to execute command: comma | 68 | 26 | 22 |
| 14 | We couldn't process your request due to a server overload. Please try again afte | 65 | 58 | 58 |
| 15 | not retryable: ensure-environment request failed: Post "https://as.int.apis.emer | 64 | 56 | 56 |
| 16 | The image you provided is too large. Please reduce the image size to meet the li | 61 | 12 | 12 |
| 17 | not retryable: backend health check failed after <n> attempts | 55 | 39 | 35 |
| 18 | not retryable: external MongoDB connection test failed: failed to ping MongoDB: | 54 | 28 | 26 |
| 19 | not retryable: failed to get cluster by name: ERROR: column "federated_db" does | 53 | 52 | 52 |
| 20 | not retryable: failed to fetch envs from source pod: failed to copy env files fr | 50 | 44 | 44 |
| 21 | not retryable: copy files from pod: copy code: failed to get pod: pods "agent-en | 46 | 41 | 40 |
| 22 | not retryable: copy files from pod: copy supervisord.conf: failed to stream tar | 46 | 15 | 13 |
| 23 | not retryable: failed to list source databases: failed to get pod: pods "agent-e | 38 | 31 | 30 |
| 24 | not retryable: copy files from pod: copy code: failed to get pod: Get "https://<n> | 37 | 37 | 37 |
| 25 | not retryable: not retryable: Cloud Build failed: failed to get build status: fa | 31 | 16 | 12 |

### Error-step rate: AI vs non-AI jobs (steps 2026-04-14 → 2026-06-12)

| Segment | Total steps | Error steps | Error-step rate | Jobs w/ steps in window | Jobs w/ ≥1 error | Job-level error rate | Steps/job |
|---|---|---|---|---|---|---|---|
| AI-candidate | 63,452,498 | 12,387 | 0.0195% | 489,184 | 5,579 | 1.14% | 129.7 |
| Non-AI | 104,746,279 | 21,859 | 0.0209% | 2,283,150 | 9,871 | 0.43% | 45.9 |
| (null task) | 17 | 0 | 0% | 12 | 0 | 0% | 1.4 |

### Errors by agent_name on AI-candidate jobs (2026-04-14 → 2026-06-12)

| Agent | Total steps | Error steps | Error-step rate | Jobs w/ errors | Share of AI error steps |
|---|---|---|---|---|---|
| EmergentAssistant | 53,461,000 | 12,071 | 0.0226% | 5,407 | 97.4% |
| SkilledAssistant | 9,984,161 | 316 | 0.0032% | 210 | 2.6% |
| (null) | 7,337 | 0 | 0% | 0 | 0% |

### Caveats

- AI-candidate classification is the heuristic keyword filter v1 on jobs.task (first 4,000 chars), not yet LLM-calibrated; expect some false positives ('agents' as travel/real-estate agents) and misses.
- 'Error step' = trajectory row with non-empty error_message. The status column is only ACTIVE/INACTIVE (lifecycle, not errors), so silent/unlogged failures and job-level failures without trajectory error_message are not counted.
- Signatures are normalized to the first 80 chars with uuids/hex/digits stripped; truncation merges some distinct root causes (especially the generic 'Internal server error' bucket) and splits Cloud Build failures into 3 retry-nesting variants (rows 2, 6, 25 are one family, ~2,380 steps).
- Window applies to trajectory created_at (2026-04-14 → 2026-06-12); jobs of any creation date are included if they had steps in the window. jobs_full_view is unpartitioned, so the job side is a full-table classify (no date cut).
- Job-level error-rate gap (1.14% vs 0.43%) is largely a session-length effect (AI jobs run ~2.8x more steps), not per-step fragility — per-step rates are statistically near-identical.
- Internal users excluded via signups email NOT LIKE '%emergent.sh' plus the known test user_id; jobs whose user has no signup row are retained.
- Step counts include all agent steps (HITL turns, tool calls, etc.); error-step rate is therefore diluted by the huge denominator — per-job incidence is the more user-felt metric.

<details><summary>Queries used</summary>

**Probe: confirm status values and define 'error step' (status is ACTIVE/INACTIVE only; error_message presence is the error indicator)**

```sql
SELECT status, COUNT(*) AS steps, COUNTIF(error_message IS NOT NULL AND TRIM(error_message) != '') AS steps_with_error_msg
FROM `analytics.trajectories_full_view`
WHERE DATE(created_at) >= '2026-04-14'
GROUP BY status ORDER BY steps DESC
```

**Top 25 normalized error signatures on AI-candidate jobs (count, distinct jobs, distinct users)**

```sql
WITH excl AS (
  SELECT DISTINCT user_id FROM `analytics.signups_raw_dataset` WHERE email LIKE '%emergent.sh'
),
jobs_ai AS (
  SELECT j.id AS job_id, j.user_id
  FROM `analytics.jobs_full_view` j
  WHERE j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
    AND j.user_id NOT IN (SELECT user_id FROM excl)
    AND REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)')
),
err AS (
  SELECT t.job_id, jb.user_id,
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(SUBSTR(TRIM(t.error_message),1,80),
      r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', '<id>'),
      r'\b[0-9a-fA-F]{12,}\b', '<id>'), r'\d+', '<n>'), r'\s+', ' ') AS sig
  FROM `analytics.trajectories_full_view` t
  JOIN jobs_ai jb ON t.job_id = jb.job_id
  WHERE DATE(t.created_at) >= '2026-04-14'
    AND t.error_message IS NOT NULL AND TRIM(t.error_message) != ''
)
SELECT sig, COUNT(*) AS error_steps, COUNT(DISTINCT job_id) AS distinct_jobs, COUNT(DISTINCT user_id) AS distinct_users
FROM err GROUP BY sig ORDER BY error_steps DESC LIMIT 25
```

**Error-step rate AI vs non-AI (step- and job-level)**

```sql
WITH excl AS (
  SELECT DISTINCT user_id FROM `analytics.signups_raw_dataset` WHERE email LIKE '%emergent.sh'
),
jobs AS (
  SELECT j.id AS job_id,
    REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)') AS is_ai
  FROM `analytics.jobs_full_view` j
  WHERE j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
    AND j.user_id NOT IN (SELECT user_id FROM excl)
)
SELECT jb.is_ai,
  COUNT(*) AS total_steps,
  COUNTIF(t.error_message IS NOT NULL AND TRIM(t.error_message) != '') AS error_steps,
  ROUND(SAFE_DIVIDE(COUNTIF(t.error_message IS NOT NULL AND TRIM(t.error_message) != ''), COUNT(*)) * 100, 4) AS error_step_rate_pct,
  COUNT(DISTINCT t.job_id) AS distinct_jobs,
  COUNT(DISTINCT IF(t.error_message IS NOT NULL AND TRIM(t.error_message) != '', t.job_id, NULL)) AS jobs_with_errors
FROM `analytics.trajectories_full_view` t
JOIN jobs jb ON t.job_id = jb.job_id
WHERE DATE(t.created_at) >= '2026-04-14'
GROUP BY jb.is_ai
```

**Errors by agent_name on AI-candidate jobs**

```sql
WITH excl AS (
  SELECT DISTINCT user_id FROM `analytics.signups_raw_dataset` WHERE email LIKE '%emergent.sh'
),
jobs_ai AS (
  SELECT j.id AS job_id
  FROM `analytics.jobs_full_view` j
  WHERE j.user_id != '90e9d382-f842-4e71-82eb-d008a398b7b2'
    AND j.user_id NOT IN (SELECT user_id FROM excl)
    AND REGEXP_CONTAINS(LOWER(SUBSTR(j.task,1,4000)), r'(\bai\b|\ba\.i\.|gpt|chatgpt|claude|gemini|\bllm\b|openai|anthropic|chat\s?bot|copilot|\bagents?\b|\brag\b|embeddings?|machine learning|generative|gen\s?ai|image generation|text[- ]to[- ](speech|image|video)|\btts\b|whisper|elevenlabs|intelligen|artificial|kecerdasan buatan)')
)
SELECT COALESCE(t.agent_name, '(null)') AS agent_name,
  COUNT(*) AS total_steps,
  COUNTIF(t.error_message IS NOT NULL AND TRIM(t.error_message) != '') AS error_steps,
  ROUND(SAFE_DIVIDE(COUNTIF(t.error_message IS NOT NULL AND TRIM(t.error_message) != ''), COUNT(*)) * 100, 4) AS error_step_rate_pct,
  COUNT(DISTINCT IF(t.error_message IS NOT NULL AND TRIM(t.error_message) != '', t.job_id, NULL)) AS jobs_with_errors
FROM `analytics.trajectories_full_view` t
JOIN jobs_ai jb ON t.job_id = jb.job_id
WHERE DATE(t.created_at) >= '2026-04-14'
GROUP BY agent_name ORDER BY error_steps DESC LIMIT 15
```

</details>


---

## seed_deployments (dep probe)

### Summary
For the 17 seed jobs, fork-chain expansion via analytics.fork_chain found zero additional jobs — none of the 17 seeds appear in fork_chain as either job_id or first_job_id, so each seed is its own chain. Querying analytics.deployer_db_data for those 17 job IDs (data as of 2026-06-12) returned 8 deployment rows belonging to only 4 of the 17 jobs: b2c9ae48 (team-chat-workspace, 5 rows: hosted on team-chat-workspace.emergent.host plus active custom domain onebrain.team / www.onebrain.team and two unlinked rows for the typo'd onebrain.teams), d4ee18ab (weekly-music-app.emergent.host, hosted, active), dacb33b5 (personal-growth-lab-2.emergent.host, hosted, active), and ea1306e8 (ebook-ai-craft.emergent.host, hosted, active). The other 13 seed jobs (309b5292, 310e0e8a, 5a1a5743, b488a995, 9bbebcec, a7324dbd, e8fbdd8e, 31fcae54, 9c3e8bab, 824ce52e, b96b6695, 8b0a90be, 1a251bd8) have no deployment records at all. All 8 found rows have status 'active' except the 2 'unlinked' rows; only 1 job (team-chat-workspace) ever attached a custom domain.

### Key numbers

- **Seed jobs checked (incl. fork chains)**: 17 (chains added 0 extra jobs)
- **Seed jobs with at least one deployment**: 4 of 17 (23.5%)
- **Deployment rows found**: 8
- **Jobs with custom domain**: 1 (b2c9ae48, onebrain.team)
- **Seed jobs with no deployments**: 13 of 17 (76.5%)

### Deployments for seed jobs and their fork chains (analytics.deployer_db_data, as of 2026-06-12)

| job_id | app_name | domain_name | type | status |
|---|---|---|---|---|
| b2c9ae48-27f1-4b32-8ed8-31ff76c703c4 | team-chat-workspace | onebrain.team | custom_domain | active |
| b2c9ae48-27f1-4b32-8ed8-31ff76c703c4 | team-chat-workspace | www.onebrain.team | custom_domain | active |
| b2c9ae48-27f1-4b32-8ed8-31ff76c703c4 | team-chat-workspace | team-chat-workspace.emergent.host | hosted | active |
| b2c9ae48-27f1-4b32-8ed8-31ff76c703c4 | team-chat-workspace | onebrain.teams | unlinked_custom_domain | unlinked |
| b2c9ae48-27f1-4b32-8ed8-31ff76c703c4 | team-chat-workspace | www.onebrain.teams | unlinked_custom_domain | unlinked |
| d4ee18ab-e518-4c9f-98b1-8f9e22fe8361 | weekly-music-app | weekly-music-app.emergent.host | hosted | active |
| dacb33b5-8b66-4288-8fb8-896f3da838c2 | personal-growth-lab-2 | personal-growth-lab-2.emergent.host | hosted | active |
| ea1306e8-4ba8-40f3-b742-d6f9b4107fcc | ebook-ai-craft | ebook-ai-craft.emergent.host | hosted | active |

### Caveats

- None of the 17 seed jobs appear in analytics.fork_chain (verified both as job_id and first_job_id), so 'seed + fork chain' reduces to the 17 seeds; if a fork relationship exists outside fork_chain (e.g., chat_mode forks not captured by the view) it would be missed.
- analytics.deployer_db_data is a snapshot/sync of the deployer DB; very recent deployments may not yet be reflected.
- The two 'unlinked' rows (onebrain.teams / www.onebrain.teams) look like a TLD typo of onebrain.team that was later corrected — same app, same job.
- Queries against deployer_db_data + fork_chain repeatedly hit the Redash 60s adhoc timeout; the successful run took 81.7s, so re-runs may need the saved-query path or retries.

<details><summary>Queries used</summary>

**Find all deployments for the 17 seed jobs plus any jobs in their fork chains (spec pattern: descendants of seeds-as-roots, plus roots of seeds-as-forks)**

```sql
WITH seeds AS (
  SELECT id FROM UNNEST(['dacb33b5-8b66-4288-8fb8-896f3da838c2','b2c9ae48-27f1-4b32-8ed8-31ff76c703c4','309b5292-a7ef-416d-82af-83cc341c56fb','310e0e8a-559d-4303-9bff-0eb24fde289e','5a1a5743-9a33-4fa0-9294-058496fd9370','b488a995-01de-478f-bf07-eaeda12b7212','9bbebcec-5702-4881-92a2-912b6974bc39','a7324dbd-555d-457d-8df3-a7f642a664c6','e8fbdd8e-9dde-4bc1-bb31-5473be113ed6','31fcae54-b571-443c-8c85-5b9d32608a0a','9c3e8bab-48b6-467c-a80c-83d407d1a07d','824ce52e-5f82-4a52-8149-dedf9cf320b0','ea1306e8-4ba8-40f3-b742-d6f9b4107fcc','d4ee18ab-e518-4c9f-98b1-8f9e22fe8361','b96b6695-47f2-44ab-a792-6a2c183e60d7','8b0a90be-e895-42c3-8020-f41e253eb103','1a251bd8-e633-43aa-9b44-60f0608a16f2']) AS id
),
chain AS (
  SELECT id AS job_id FROM seeds
  UNION DISTINCT
  SELECT job_id FROM `analytics.fork_chain` WHERE first_job_id IN (SELECT id FROM seeds)
  UNION DISTINCT
  SELECT first_job_id FROM `analytics.fork_chain` WHERE job_id IN (SELECT id FROM seeds)
)
SELECT d.job_id, d.app_name, d.domain_name, d.type, d.status
FROM `analytics.deployer_db_data` d
JOIN chain c ON d.job_id = c.job_id
ORDER BY d.job_id, d.type, d.domain_name
```

**Verify the full chain membership (seeds resolved to roots, then all descendants of those roots) — returned exactly the 17 seeds, confirming no fork-chain siblings/descendants exist**

```sql
WITH seeds AS (
  SELECT id FROM UNNEST([/* 17 seed ids */]) AS id
),
roots AS (
  SELECT id AS root FROM seeds
  UNION DISTINCT
  SELECT fc.first_job_id FROM `analytics.fork_chain` fc JOIN seeds s ON fc.job_id = s.id
)
SELECT root AS job_id FROM roots
UNION DISTINCT
SELECT fc.job_id FROM `analytics.fork_chain` fc JOIN roots r ON fc.first_job_id = r.root
```

</details>


---

## seed_mongo_probe (end-user counting validation)

### Summary
VERDICT: App-Mongo end-user counting is FEASIBLE and already works in prod via the deployer MCP (mcp__deployer__run_mongo_query), with zero special flags needed — all queries ran read-only against live prod app databases on 2026-06-12. Tested 3 of the 4 active seed apps. (1) team-chat-workspace (job b2c9ae48, custom domain onebrain.team): 13 collections incl. users/messages/chats/workspaces/billing_events; 64 end-users (63 of 64 email-verified), signups spanning 2026-06-10 21:29 UTC to 2026-06-12 06:50 UTC (i.e., still signing up the morning of this analysis), plus 164 chat messages — genuine third-party adoption (sample redacted emails: a***@sonrie.ai, s***@gmail.com). (2) personal-growth-lab-2 (job dacb33b5): 2 collections (users, scores); only 2 users, both created within 2 minutes on 2026-06-10 and both t***@lifescore.app — almost certainly the builder's own test accounts, illustrating that raw user counts need an own-account/test-account filter. (3) ebook-ai-craft (job ea1306e8): NO users collection at all — single 'ebooks' collection with 3 documents (2026-06-04 to 2026-06-05, Indonesian AI-prompt ebooks); auth-less apps have no end-user registry, so adoption must fall back to activity-document counts. IDENTIFIER ANSWER: run_mongo_query requires app_name (it resolves the app's MONGO_URL secret from the name, even for deleted apps); fetch_app_details accepts app name, app ID, or custom domain, and the app ID equals the job_id. So the scale pipeline is: job_id -> app_name via analytics.deployer_db_data -> run_mongo_query(app_name). Each app has exactly one DB named '{app_name}-test_database' (template default name persists in prod), so DB naming is predictable but should be confirmed via list_databases. PII handling: users docs contain email and password_hash; redaction was done server-side inside the aggregation $project (building 'a***@domain'), so raw PII never left Mongo — this pattern should be mandatory for Phase 3 step 43.

### Key numbers

- **team-chat-workspace end-users (users collection)**: 64 (63 email-verified)
- **team-chat-workspace user created_at range**: 2026-06-10 21:29 UTC to 2026-06-12 06:50 UTC
- **team-chat-workspace messages (engagement)**: 164
- **personal-growth-lab-2 end-users**: 2 (both t***@lifescore.app, created 2026-06-10 15:23-15:25 UTC; likely builder self-test)
- **ebook-ai-craft users collection**: ABSENT (auth-less app)
- **ebook-ai-craft activity proxy (ebooks docs)**: 3 (2026-06-04 to 2026-06-05)
- **apps tested / apps where user counting succeeded**: 3 / 2 (third needed activity-count fallback)
- **databases per app**: 1, named '{app_name}-test_database'

### Per-app Mongo adoption validation (read live 2026-06-12)

| app_name | job_id / app ID | DB name | collections | users count | user created_at range (UTC) | notes |
|---|---|---|---|---|---|---|
| team-chat-workspace | b2c9ae48-27f1-4b32-8ed8-31ff76c703c4 | team-chat-workspace-test_database | 13: users, messages, chats, chat_summaries, workspaces, memberships, invites, mention_notifications, attachments, audit_log, billing_events, plan_configs, password_resets | 64 (63 verified) | 2026-06-10 21:29 -> 2026-06-12 06:50 | Real adoption: 164 messages; custom domain onebrain.team; diverse email domains (sonrie.ai, gmail.com) |
| personal-growth-lab-2 | dacb33b5-8b66-4288-8fb8-896f3da838c2 | personal-growth-lab-2-test_database | 2: users, scores | 2 | 2026-06-10 15:23 -> 2026-06-10 15:25 | Both users t***@lifescore.app within 2 min — likely builder self-test, not real adoption |
| ebook-ai-craft | ea1306e8-4ba8-40f3-b742-d6f9b4107fcc | ebook-ai-craft-test_database | 1: ebooks | n/a (no users collection) | n/a (ebooks: 2026-06-04 -> 2026-06-05) | Auth-less app; fallback signal = 3 ebook docs (Indonesian AI-prompt ebooks); user count unmeasurable |

### Sample user docs (PII redacted server-side in $project; no raw emails retrieved)

| app | created_at (UTC) | email (redacted) | email_verified |
|---|---|---|---|
| team-chat-workspace | 2026-06-10T21:29:07 | a***@sonrie.ai | true |
| team-chat-workspace | 2026-06-10T21:29:07 | s***@gmail.com | true |
| personal-growth-lab-2 | 2026-06-10T15:23:34 | t***@lifescore.app | n/a (field absent) |
| personal-growth-lab-2 | 2026-06-10T15:25:41 | t***@lifescore.app | n/a (field absent) |

User-doc schemas observed: team-chat-workspace = {_id, id, email, display_name, password_hash, created_at, email_verified, notification_prefs}; personal-growth-lab-2 = {_id, email, name, password_hash, created_at}.

### Failure modes and mitigations for Phase 3 step 43 (scaled counting)

| failure mode | seen on | mitigation |
|---|---|---|
| No 'users' collection (auth-less app) | ebook-ai-craft | list_collections first; fall back to counting primary activity collection(s); report 'unmeasurable' tier |
| Builder self-test accounts inflate counts | personal-growth-lab-2 (2 users in 2 min, same domain) | Heuristics: min user threshold, signup-time spread, email-domain diversity, exclude builder's own email |
| PII in users docs (email, password_hash) | both apps with users | Mandatory server-side $project redaction; never find() raw docs; never project password_hash/tokens |
| Schema heterogeneity (field names differ: name vs display_name; email_verified optional) | both | Discover field names via $objectToArray keys-only probe before projecting |
| created_at stored as ISO string, not BSON date | all 3 apps | String min/max is safe for ISO-8601; do not assume $dateToString works |
| run_mongo_query needs app_name (not job_id) | all | Map job_id -> app_name via analytics.deployer_db_data (or fetch_app_details, which accepts app ID = job_id, name, or custom domain) |
| One MCP call per app, 1000-doc cap | all | Use $count/$group aggregations only (no doc dumps); batch sequentially; expect some apps unreachable (none hit in this sample) |

### Caveats

- Sample size is 3 apps from one user's seed set; the 2/3 'users collection exists' rate and adoption levels are not generalizable without a larger run.
- Counts are live point-in-time reads on 2026-06-12 (team-chat-workspace was still gaining signups during the analysis window); re-running will give different numbers.
- Database is always named '{app_name}-test_database' in this sample (template default carried to prod) — predictable but should still be confirmed via list_databases per app rather than hardcoded.
- user counts conflate real end-users with the builder's own test accounts (personal-growth-lab-2 shows 2 'users' that are almost certainly self-tests); a quality filter is required before using counts as an adoption metric.
- For auth-less apps, activity-document counts (e.g., 3 ebooks) cannot distinguish 1 user from many; end-user counting is strictly unmeasurable there.
- run_mongo_query enforces read-only (list/find/aggregate) and a 1000-doc cap; only count/group/keys-only aggregations were used and emails were redacted inside the Mongo pipeline, so no raw PII entered this analysis.
- Did not test the 4th app (weekly-music-app) or any deleted/suspended app, so the 'unreachable Mongo / missing secret' failure mode remains unexercised (the tool docs claim app_name works even for deleted apps).
- The 'fourth' identifier path — querying by custom domain — was validated only for fetch_app_details (onebrain.team resolved), not for run_mongo_query, which strictly requires app_name or a raw connection string.

<details><summary>Queries used</summary>

**Confirm each app exists and resolve identifiers (accepts app name, app ID, or custom domain; returned app ID == job_id)**

```sql
MCP mcp__deployer__fetch_app_details {identifier: 'team-chat-workspace' | 'ebook-ai-craft' | 'personal-growth-lab-2'}
```

**Discover the app's database name (always '{app_name}-test_database' in this sample)**

```sql
MCP mcp__deployer__run_mongo_query {operation: 'list_databases', app_name: '<app>'}
```

**Discover collections per app (users present in 2/3 apps)**

```sql
MCP mcp__deployer__run_mongo_query {operation: 'list_collections', app_name: '<app>', database: '<app>-test_database'}
```

**Count end-users**

```sql
Mongo aggregate on <db>.users: [{"$count": "user_count"}]
```

**Probe user-doc field names WITHOUT reading values (PII-safe schema discovery)**

```sql
Mongo aggregate on <db>.users: [{"$limit": 2}, {"$project": {"_id": 0, "field_names_only": {"$map": {"input": {"$objectToArray": "$$ROOT"}, "as": "kv", "in": "$$kv.k"}}}}]
```

**User created_at range + verified count (team-chat-workspace variant; personal-growth-lab-2 same without verified)**

```sql
Mongo aggregate on <db>.users: [{"$group": {"_id": null, "min_created": {"$min": "$created_at"}, "max_created": {"$max": "$created_at"}, "verified_count": {"$sum": {"$cond": ["$email_verified", 1, 0]}}, "total": {"$sum": 1}}}]
```

**Fetch 2 sample user docs with email redacted SERVER-SIDE (raw PII never leaves Mongo)**

```sql
Mongo aggregate on <db>.users: [{"$sort": {"created_at": 1}}, {"$limit": 2}, {"$project": {"_id": 0, "created_at": 1, "email_verified": 1, "email_redacted": {"$concat": [{"$substrCP": ["$email", 0, 1]}, "***@", {"$arrayElemAt": [{"$split": ["$email", "@"]}, 1]}]}}}]
```

**Engagement signal proving real adoption on team-chat-workspace**

```sql
Mongo aggregate on team-chat-workspace-test_database.messages: [{"$count": "message_count"}] -> 164
```

**Activity-count fallback for auth-less app (ebook-ai-craft has no users collection)**

```sql
Mongo aggregate on ebook-ai-craft-test_database.ebooks: [{"$count": "ebook_count"}] -> 3; plus [{"$sort": {"created_at": 1}}, {"$project": {"_id": 0, "created_at": 1, "topic": 1, "language": 1, "audience": 1, "chapter_count": 1}}]
```

</details>
