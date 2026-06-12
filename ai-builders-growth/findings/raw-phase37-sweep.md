# Phase 3-7 Deep Research Wave — Raw Agent Outputs

*Workflow run wf_aaf70c79-b23, 2026-06-12. 13 agents: H5 retention, death-valley mechanics, Mongo S4 sampling, LTV impact model, credit exhaustion, support/churn VoC, demographics, LLM-proxy prod usage, competitor teardowns (builders + agent platforms), codebase feasibility, pricing/packaging, adversarial verification.*

---

## retention_h5

### Summary
H5 TEST (does shipping predict builder retention?): Cohort = 392,152 users whose FIRST AI-candidate root job (AI-keyword filter v1 on root task) was created 2026-02-01 to 2026-03-31, excluding emergent.sh emails and the excluded user_id. Outcome of that first AI project within 30d: 7,908 deployed (2.0%), 100,636 engaged-not-deployed (project cost >=$10; 25.7%), 283,608 shallow (<$10; 72.3%). VERDICT: H5 is SUPPORTED for builder and revenue retention, NOT supported for subscription churn. Deployers retain at ~2x the engaged non-deployers and ~3x shallow users on day-31-60 job creation (20.4% vs 10.3% vs 7.0%) and day-61-90 (14.7% vs 7.0% vs 4.6%, full-90d subcohort). Revenue retention is dramatically stratified: 44.1% of deployers make a payment in days 31-90 vs 11.5% engaged and 3.7% shallow; mean d31-90 revenue $134.70 vs $18.36 vs $4.72 per user. Multi-project expansion within 30d: deployed 44.4% vs engaged 18.0% — but shallow is anomalously high at 35.4%, indicating restarts (abandon-and-reprompt) rather than expansion. Subscription-churn overlay contradicts H5: among users with an active subscription at first-job time, deployers cancelled MORE within 60d (5.7%, 39/681) than engaged (3.7%, 87/2,327) or shallow (4.4%, 111/2,504) — possibly 'mission accomplished' churn after shipping. Note deployment is heavily confounded with engagement depth (deployers' mean 30d project cost $403.87 vs $44.68 engaged), so this is correlational, not causal.

### Key numbers

- **Cohort size (first AI root job Feb-Mar 2026)**: 392,152 users (263,740 with full 90d follow-up, first job <= 2026-03-14)
- **Deployed first AI project within 30d**: 7,908 users (2.0%)
- **Engaged-not-deployed (30d project cost >= $10)**: 100,636 users (25.7%)
- **Shallow (<$10)**: 283,608 users (72.3%)
- **Builder retention d31-60 (>=1 new job): deployed vs engaged vs shallow**: 20.4% vs 10.3% vs 7.0%
- **Builder retention d61-90 (full-90d subcohort)**: 14.7% vs 7.0% vs 4.6%
- **% paying in d31-90 (full-90d subcohort)**: 44.1% vs 11.5% vs 3.7%
- **Mean revenue d31-90 per user (incl. non-payers)**: $134.70 vs $18.36 vs $4.72
- **Mean revenue d31-90 among payers**: $305.31 vs $159.43 vs $128.11
- **2nd project started within 30d**: deployed 44.4%, engaged 18.0%, shallow 35.4% (shallow = restarts, not expansion)
- **Subscription churn within 60d (active sub at first job)**: deployed 5.7% (39/681), engaged 3.7% (87/2,327), shallow 4.4% (111/2,504)
- **Mean 30d project cost by group**: deployed $403.87, engaged $44.68, shallow $3.92

### H5: 30d outcome of first AI project vs downstream retention (cohort: first AI root job Feb-Mar 2026)

| Outcome group (30d) | N users | N full-90d | Job ret. d31-60 | Job ret. d61-90* | Paid d31-90* | Mean rev d31-90* (all) | Mean rev d31-90* (payers) | 2nd project <=30d | Active subs at job 1 | Sub churn <=60d |
|---|---|---|---|---|---|---|---|---|---|---|
| Deployed | 7,908 (2.0%) | 5,687 | 20.4% | 14.7% | 44.1% | $134.70 | $305.31 | 44.4% | 681 | 5.7% |
| Engaged, not deployed (>=$10) | 100,636 (25.7%) | 70,716 | 10.3% | 7.0% | 11.5% | $18.36 | $159.43 | 18.0% | 2,327 | 3.7% |
| Shallow (<$10) | 283,608 (72.3%) | 187,337 | 7.0% | 4.6% | 3.7% | $4.72 | $128.11 | 35.4% | 2,504 | 4.4% |

*Starred columns computed on the full-90d subcohort (first AI job <= 2026-03-14) so the day-61-90 / day-31-90 windows are complete as of 2026-06-12.

### Implications

- Shipping is the strongest retention/monetization signal we have for AI builders: deployers pay at 44.1% in days 31-90 (3.8x the engaged group) and generate $134.70/user vs $18.36 — but only 2.0% of AI-builder cohorts deploy within 30d. Moving even 2-3pp of the 100k engaged-not-deployed users into deployment is the highest-leverage growth motion.
- The engaged-not-deployed pool (100,636 users, mean $44.68 spent in 30d) is the prime target: they've proven willingness to invest but stall before shipping. Product ideas: deploy-readiness checklist for agents/chatbots, one-click 'publish your agent' with a hosted chat UI on *.emergent.host, API-key/secrets setup assistance (a known AI-app deploy blocker), and time-boxed deploy nudges around day 7-21.
- Shallow users (72.3%) churn-restart: 35.4% start a new root job within 30d but only 7.0% return after day 30. First-attempt success on AI prompts (better scaffolds/templates for chatbots, RAG, agents) matters more than re-engagement campaigns for this segment.
- Do not pitch deployment as a subscription-churn reducer: deployers actually cancel slightly more within 60d (5.7% vs 3.7%). Investigate whether this is 'project done' churn — if so, multi-project expansion hooks (deployed 44.4% already start a 2nd project) and usage-based topups matter more than retention discounts for shipped builders.
- Revenue follows shipping even among payers ($305 vs $159 mean d31-90 revenue), suggesting deployed AI products create ongoing spend (iteration + hosting). Consider post-deploy growth loops: custom domains, analytics for their agent, share/embed widgets.

### Caveats

- Correlational, not causal: deployers are self-selected heavy users (mean 30d project cost $403.87 vs $44.68 engaged); deployment likely proxies commitment as much as it drives retention. The cleanest comparison is deployed vs engaged-not-deployed, where the 2x retention and 3.8x payment gaps persist.
- AI-keyword filter v1 has ~57% precision, so roughly 4 in 10 cohort members may not actually be building AI products; results describe AI-candidate projects.
- 'Deployed' = any deployer_db_data row (created_at <= first job + 30d) on jobs in the first project's fork chain; it does not require verified=true or a live custom domain.
- Day-61-90 retention, d31-90 revenue metrics were restricted to users with first job <= 2026-03-14 (n=263,740) so windows are complete; d31-60 retention, 2nd-project, and sub-churn windows are complete for the whole cohort (latest window end 2026-05-30).
- Subscription-churn overlay has small n (681 deployed subscribers, 39 cancels); the 5.7% vs 3.7% difference is ~2pp on small samples and cancellation_snapshots coverage/retention of older cancels is unverified — treat as directional only.
- Project cost = SUM(trajectories value_in_usd) over fork-chain jobs, partition-filtered DATE(created_at) 2026-02-01..2026-05-01 and capped at first job + 30d.
- '2nd project' = any other root job (parent_job_id IS NULL) within 30d; for shallow users this largely captures abandon-and-restart behavior (35.4% > engaged 18.0%), not genuine multi-project expansion.
- Heavy queries exceeded Redash's 60s adhoc limit; per-user groups were materialized to temp_tables.h5_ai_cohort_grouped_20260612 (auto-expires 24h) and metrics computed against it. Group counts reproduced exactly across two independent runs.


---

## funnel_dropoff

### Summary
Death Valley mechanics for AI-candidate root projects (created 2026-04-01..2026-05-15, n=338,195; trajectories observed through 2026-06-12). Deployment is near-zero (<1.1%) for projects spending under $25, jumps ~9x across the $15→$50 spend range, plateaus at 9-13% from $25-200, then inflects again at $200-350 (29%) and climbs to 59% above $1,000. The engaged-but-died cohort ($10-100 spent, never deployed) is huge — 115,709 projects — and overwhelmingly dies fast: 87.6% are active on a single calendar day, despite ~99% having at least one HITL message. Reading the LAST human message of 30 sampled died projects: 63% end on a scoping answer or a bare 'proceed/yes' (the user answered the agent's clarification questionnaire or approved a plan and never came back to review the first build), 23% end mid-iteration still requesting features/design changes (feature fatigue), 10% end fighting bugs (incl. one platform OOM), 3% end asking how to download the code, 0% mention credits. Same-user signal: only 11.0% of died projects are followed by ANY new root project from the same user within 14 days (9.5% of users) — i.e., ~90% of death-valley users give up on the platform, not just the project.

### Key numbers

- **AI-candidate root projects, 2026-04-01..05-15 (after exclusions)**: 338,195
- **Deploy rate <$2 spend**: 0.04% (27/70,279)
- **Deploy rate $10-25 spend (death valley floor)**: 1.1% (1,068/93,282)
- **Deploy rate $25-100**: 10.6% (2,778/26,273)
- **Deploy rate >$500**: 52.4% (2,407/4,594)
- **First inflection of marginal-dollar curve**: $15-25 → $25-50: 0.57% → 2.86% → 9.43% (~16x from $10-15 to $25-50)
- **Plateau zone**: $25-200 stuck at 9.4-13.3% deployed
- **Second inflection**: $200-350: 13.3% → 28.9%, rising to 59.3% >$1,000
- **Engaged-but-died cohort ($10-100, not deployed)**: 115,709 projects
- **Died projects active on a single day only**: 87.6% (101,331)
- **Died projects with >=1 HITL message**: ~99%
- **Last message = scoping answer / silent abandonment (sample of 30)**: 63% (19/30)
- **Last message = unresolved bug**: 10% (3/30)
- **Last message mentioning credits/cost**: 0% (0/30)
- **Died projects followed by a new root project from same user within 14d**: 11.0% (12,659/114,911); 9.5% of 107,893 users

### 1) Funnel by project cost band (AI-candidate roots, Apr 1 - May 15 2026; cost = SUM(value_in_usd) over root+fork jobs, trajectories Apr 1 - Jun 12)

| Cost band | n projects | n deployed | % deployed | Median HITLs | Median steps |
|---|---|---|---|---|---|
| <$2 | 70,279 | 27 | 0.04% | 0 | 3 |
| $2-10 | 129,230 | 432 | 0.3% | 1 | 30 |
| $10-25 | 93,282 | 1,068 | 1.1% | 1 | 35 |
| $25-100 | 26,273 | 2,778 | 10.6% | 5 | 94 |
| $100-500 | 14,537 | 2,852 | 19.6% | 13 | 216 |
| >$500 | 4,594 | 2,407 | 52.4% | 81 | 1,227 |
| **Total** | **338,195** | **9,564** | **2.8%** | | |

### 2) Marginal-dollar curve: deploy rate by fine spend band

| Spend band | n projects | n deployed | % deployed |
|---|---|---|---|
| <$1 | 59,619 | 19 | 0.03% |
| $1-2 | 10,660 | 8 | 0.08% |
| $2-5 | 26,615 | 83 | 0.31% |
| $5-10 | 102,615 | 349 | 0.34% |
| $10-15 | 69,746 | 396 | 0.57% |
| $15-25 | 23,536 | 672 | 2.86% |
| $25-50 | 13,733 | 1,295 | 9.43% |
| $50-100 | 12,540 | 1,483 | 11.83% |
| $100-200 | 9,609 | 1,279 | 13.31% |
| $200-350 | 3,436 | 992 | 28.87% |
| $350-500 | 1,492 | 581 | 38.94% |
| $500-1000 | 2,014 | 877 | 43.55% |
| >$1000 | 2,580 | 1,530 | 59.30% |

### 3a) Engaged-but-died cohort ($10-100 spend, never deployed; n=115,709): days-active distribution (last minus first trajectory date)

| Days active | n projects | % of cohort | % with >=1 HITL |
|---|---|---|---|
| 0 (single day) | 101,331 | 87.6% | 98.9% |
| 1 | 6,370 | 5.5% | 99.8% |
| 2-3 | 2,412 | 2.1% | 100% |
| 4-7 | 1,987 | 1.7% | 99.9% |
| 8-14 | 1,234 | 1.1% | 99.9% |
| 15-30 | 1,253 | 1.1% | 100% |
| >30 | 1,122 | 1.0% | 100% |

### 3b) Tagged reason from LAST human_message (random sample of 30 died projects with >=1 HITL, FARM_FINGERPRINT-ordered)

| Apparent reason at stop | n | % | Examples |
|---|---|---|---|
| Unclear / silent abandonment — last msg is a scoping answer ('<ask_human_response>...', 'Assume Default and Proceed', 'Yes', 'C', '2a, 3b, 4b') or a plan approval, user never returns to review the build | 19 | 63% | 15 of 19 are literally answers to the agent's initial clarification questionnaire; cost mostly $10-25, HITLs=1 |
| Feature fatigue — last msg still requests new features/design changes, then user vanishes mid-iteration | 7 | 23% | 'redesign everything... more professional' ($93, 10 HITLs); 'Interview prep module...' ($72); design-tone refinement ($53); enhancement wishlists |
| Unresolved bug — last msg is bug-fix instructions or a platform failure | 3 | 10% | 'FORENSIC AUDIT... remediation plan' ($59); file-by-file bug-fix table ($10.49); platform OOM: 'Memory Limit exceeded leading to pod termination' ($70) |
| Satisfied-with-preview / exit-to-code | 1 | 3% | 'Comment télécharger le code?' ($17.87, 22 HITLs) — wanted code export, not deploy |
| Credit concern | 0 | 0% | none in sample |

### 4) Same-user restart signal (died projects with last activity <= 2026-05-29 for full 14d window)

| Metric | Value |
|---|---|
| Died projects measured | 114,911 |
| Projects followed by a new root project (same user, any topic) within 14d | 12,659 (11.0%) |
| Distinct died users | 107,893 |
| Users who started another project within 14d | 10,220 (9.5%) |
| Interpretation | ~90% gave up on the PLATFORM, not just the project |

### Implications

- The death valley is precisely $10-25: 93,282 projects (28% of all AI-candidate roots) spend real compute, median 1 HITL / 35 steps, yet deploy at 1.1%. The single dominant mechanic is NOT bugs or credits — it is users answering the kickoff questionnaire, letting the agent build, and never returning to review the first result (63% of sampled last messages). Highest-leverage fix: a first-build return loop — push/email 'your AI app is ready' with a live preview link and a one-tap next action, plus making the clarification step feel like the beginning of a session rather than the end of one.
- Deploy rate jumps ~16x between $10-15 (0.57%) and $25-50 (9.4%): getting a user to ONE more meaningful iteration (~$10-25 more spend, ~3-5 more HITLs) is worth more than anything else in the funnel. Consider an 'iteration nudge' after the first build (auto-generated punch list of 3 concrete improvements for AI apps: hook up the LLM key, add auth, test the chat flow) to pull users across the $25 line.
- The $25-200 plateau (9-13% deployed despite heavy engagement: median 5-13 HITLs, 94-216 steps) is where feature fatigue (23% of tagged stops) and unresolved bugs (10%) live. A 'ship now, iterate after' prompt — deploy the current working version before the next feature request — could convert plateau users who keep polishing and never launch; the second inflection at $200-350 shows deployment today mostly happens only after extreme persistence.
- ~90% of engaged-but-died users do not start another project within 14 days — death valley is platform churn, not project churn. Win-back should resume the EXISTING project (its preview, its chat history, its remaining credits), not prompt a fresh start; the dead project is the user's sunk asset and the natural re-entry point.
- Credit anxiety never appeared as a stated last-message reason (0/30) — pricing messaging is not the death-valley lever; product-completion loops are. Also worth noting: one persistent user (22 HITLs) abandoned at 'how do I download the code?' — a visible code-export path may retain builders who distrust hosted deploys, and a platform OOM killed another $70 project, so infra failures do show up in the long tail.

### Caveats

- AI-keyword filter v1 has ~57% precision (applied to root job task only), so ~4 in 10 'AI-candidate' projects may not truly be AI products; band-relative comparisons should be robust but absolute counts overstate the AI population.
- Deployment measured via analytics.deployer_db_data_snapshot (BASE TABLE, fresh as of 2026-06-12 11:05 UTC) because the live deployer_db_data federated view timed out repeatedly; snapshot had 507,999 rows vs 508,053 in the one successful live-view probe (~0.01% difference). 'Deployed' = project's job ever appears in deployer data (any status/type, including unverified custom domains).
- Project cost aggregates trajectories for the root job + fork_chain descendants only; subagent jobs (parent_job_id set) that are not in fork_chain are excluded — consistent across bands but may undercount true project cost.
- Trajectory observation window capped at 2026-06-12: projects created near May 15 have >=28d observation as designed, but late re-activity after Jun 12 is invisible; non-deployed status could flip later for a small tail.
- Last-message tagging is manual interpretation of 700-char truncated messages, n=30 (binomial 95% CI on the 63% bucket is roughly +/-17pp); several messages were non-English (Polish, Georgian, French, Swedish, Italian, Portuguese) and one 'last human_message' was actually a system-injected OOM recovery notice, suggesting human_message sometimes contains platform messages.
- Restart analysis counts any new ROOT job as a new project (no minimum spend on the second project), so 11% is an upper bound on meaningful retries; window anchored to last trajectory DATE (day granularity).


---

## mongo_s4

### Summary
First-ever S4 measurement: of 45 deterministically sampled deployed AI apps (active hosted deployments joined to AI-candidate root jobs created 2026-04-01..2026-06-01), 44 were successfully measured (98% coverage; 1 hard failure from a missing MONGO_URL secret). 24/45 apps (53%) have an end-user auth collection ('users' or equivalent like 'accounts'). 18/45 (40%) clear the S4 bar of >=3 registered end-users. However, signup-timestamp forensics cut this sharply: in 10 of the 24 auth apps, ALL users were created within a <60-minute burst (classic owner self-testing / seed data). Only 8/45 apps (18%) show >=3 users with signups spread over more than 24 hours — the best proxy for genuinely organic end-user adoption. The best performer reached just 54 users over 30 days (smart-photo-tools-1, an AI photo editor); no app exceeded 100 users. Among the 17 auth-less apps, lead-gen/content sites show modest but real visitor evidence: ~8 have activity (contact submissions, leads, generated plans) spread over multiple weeks, including one Telegram-bot data tool with 2,096 records over 30 days. 3 apps had a reachable Mongo cluster with zero databases — deployed but never used at all.

### Key numbers

- **Sample size (deterministic FARM_FINGERPRINT order)**: 45 apps; jobs 2026-04-01..2026-06-01; status=active, type=hosted
- **Measurement coverage**: 44/45 (97.8%); 1 failure (order-hub-288: MONGO_URL secret not found)
- **Apps with an end-user auth collection**: 24/45 (53.3%)
- **S4 bar: apps with >=3 registered end-users**: 18/45 (40.0%); 18/24 (75%) of auth apps
- **Strict organic bar: >=3 users AND signup span >24h**: 8/45 (17.8%)
- **Auth apps where all signups occurred in <60 min (self-test/seed pattern)**: 10/24 (41.7%)
- **Max end-user count observed**: 54 users / 30 days (smart-photo-tools-1); zero apps >100 users
- **Median user count among 24 auth apps**: 5.5 users
- **Apps deployed but with zero databases (never used)**: 3/45 (6.7%): lobsterbot-app, ai-startup-suite, deva-command-nexus
- **Auth-less apps with multi-week activity evidence**: ~8/17 (e.g., data-manager-sync: 2,096 records over 30 days; tour-cost-planner: 55 plans over 34 days)
- **Apps using a custom DB name (not {app}-test_database)**: 10/41 reachable (24%) — required list_databases fallback

### End-user count distribution (24 apps with users/accounts collection)

| Bucket | Apps | % of auth apps | % of 45 sampled | Examples |
|---|---|---|---|---|
| 0 users | 0 | 0% | 0% | — |
| 1-2 (likely self-test) | 6 | 25% | 13% | sugar-support (1), compliance-vault-29 (1), ai-marketing-hub-171 (1), flick-vault-system (2), agent-config-hub-2 (2), command-center-gold (2) |
| 3-10 | 12 | 50% | 27% | wear-worth-check (9), agro-connect-29 (7), crm-mobile-hub-3 (7), tarka-enroll-mvp (7), court-drafting-hub (6), quick-fast-3 (6), citizen-advisor-1 (5), video-studio-ai-24 (5), lead-magnet-finder (5), bottrader-pro-4 (4), property-forte (4), price-jackpot-finder (3) |
| 11-100 | 6 | 25% | 13% | smart-photo-tools-1 (54), agri-fintech-ng (25), aigen-workspace-1 (22), inner-wealth-2 (15), autonomous-wealth-ai (12), stratex-quant (11) |
| >100 | 0 | 0% | 0% | — |

### Signal quality: signup time-span forensics (auth apps with >=3 users, n=18)

| Pattern | Apps | Verdict |
|---|---|---|
| All signups in <60 min burst | 10 (video-studio-ai-24 26m, property-forte <1s, crm-mobile-hub-3 39m, tarka-enroll-mvp 1m, court-drafting-hub 8m, price-jackpot-finder 15m, autonomous-wealth-ai 32m, quick-fast-3 16m, command-center-gold 13m*, agent-config-hub-2 <1s*) | Self-test / seed accounts, not real adoption (*<3 users) |
| Signups spread 1-2 days | 4 (aigen-workspace-1 22u/26h, stratex-quant 11u/3d, inner-wealth-2 15u/21h, lead-magnet-finder 5u/28h) | Small launch / friends-and-family |
| Signups spread >3 days | 6 (smart-photo-tools-1 54u/30d, agri-fintech-ng 25u/3d, wear-worth-check 9u/7d, agro-connect-29 7u/35d, citizen-advisor-1 5u/5d, flick-vault-system 2u/13d) | Most credible real end-user traction |

### Auth-less apps: activity proxy (17 apps, largest business collection)

| App | Proxy collection | Docs | Date span | Read |
|---|---|---|---|---|
| data-manager-sync | records | 2,096 | 4/20-5/20 | Heavy real use (Telegram bot data tool) |
| entangled-ai | messages | 340 | n/a (no created_at) | Heavy chat use (likely owner) |
| vibe-productivity | assessments | 107 | n/a | Real assessment completions likely |
| tour-cost-planner | tour_plans | 55 | 5/3-6/6 | Sustained real use |
| learn-create-9 | messages | 28 | 5/10-5/18 | Moderate use |
| elevate-business-2 | contact_submissions | 20 | 5/14-5/27 | Real visitor inquiries |
| founder-ops-10 | leads | 19 | 5/18 (5h burst) | Single-day burst, ambiguous |
| find-your-people-4 | analytics_events (waitlist=0) | 17 | 5/30-6/2 | A few visitors, zero conversions |
| diritti-fiscali | bonuses | 15 | n/a | Seed/content data, not user activity |
| lune-healing | waitlist | 13 | 5/15-5/18 | Real waitlist signups |
| loss-calculator-1 | leads | 9 | 5/1-6/4 | Trickle of real leads |
| film-studio-ai-4 | contact_messages | 8 | 5/8-5/18 | A few real inquiries |
| web-essentials-kit | contact_messages | 6 | 5/4-6/7 | Trickle |
| creator-first-8 | newsletter_subscribers | 6 | 5/18 (same day) | Launch-day burst |
| kavion-premium | leads | 5 | 5/8 (~1h) | Likely self-test |
| ticketing-pro-7 | registrations + contacts | 4 + 1 | 5/5-5/21 | Minimal |
| striker-ai-coach-1 | analyses | 4 | 5/15 (36s) | Self-test |

### Failure modes encountered (Step 2 methodology notes)

| Failure mode | Count | Apps | Workaround |
|---|---|---|---|
| MONGO_URL secret not found | 1 | order-hub-288 | None — unmeasurable |
| Cluster reachable, 0 databases | 3 | lobsterbot-app, ai-startup-suite, deva-command-nexus | Counted as deployed-but-never-used (0 activity) |
| Custom DB name (Unauthorized on {app}-test_database) | 10 | video-studio-ai-24, property-forte, citizen-advisor-1, crm-mobile-hub-3, command-center-gold, ticketing-pro-7, ai-marketing-hub-171, striker-ai-coach-1, quick-fast-3, inner-wealth-2 | list_databases fallback worked every time |
| Transient query timeout | 1 | citizen-advisor-1 | Retry succeeded |
| Missing/nonstandard created_at field | 3 | vibe-productivity, entangled-ai, diritti-fiscali (+1 epoch-int: citizen-advisor-1) | Count obtained; no time span |

### Implications

- S4 reality check: only ~18% of deployed AI apps show organic multi-day end-user adoption, and zero in the sample crossed 100 users. The platform's growth story currently ends at 'deployed', not 'adopted' — distribution/growth features (SEO-ready landing pages, share links, launch checklists, embedded waitlists) are the bigger gap than build quality.
- The dominant failure pattern is the 'self-test burst': builders create 3-10 accounts in minutes, then traffic flatlines. An in-product 'first 10 real users' playbook (e.g., built-in analytics showing unique visitors vs. owner sessions, a 'share your app' moment after deploy) would target exactly this cliff.
- Lead-gen and waitlist apps quietly outperform: contact forms, waitlists and tool-run collections accumulate real strangers' submissions over weeks even without auth. Productizing this (native forms/waitlist/lead-inbox blocks with email notifications) is a low-cost wedge to give builders their first taste of real users.
- Built-in app analytics is a near-free retention feature: every measurement here required raw Mongo spelunking. Surfacing 'your app got N signups / N submissions this week' in the Emergent dashboard would both prove value and create a re-engagement loop.
- The 3 deployed-but-empty apps and the 41% self-test-only cohort suggest a 'post-deploy activation' email/notification sequence (day 3/7: 'your app has had 0 visitors — here's how to share it') as a cheap experiment.
- Apps with the most real traction (smart-photo-tools-1 54 users, agri-fintech-ng 25, aigen-workspace-1 22) are consumer AI tools and marketplaces — candidates for case studies and for proactive outreach to upsell custom domains and scaling.
- Methodology is now repeatable: the FARM_FINGERPRINT sample + list_databases fallback + redacted aggregate gets ~98% coverage; this S4 probe can be automated as a quarterly tracking metric.

### Caveats

- AI-keyword filter v1 has ~57% precision, so roughly 4 in 10 sampled apps are not truly AI products (e.g., kavion-premium marketing site, flick-vault-system movie tracker matched on stray keywords); S4 rates for genuinely-AI apps may differ.
- User counts are point-in-time row counts in the production DB; they cannot distinguish the owner's own account(s) from external end-users — burst-timing heuristics are a proxy, not ground truth.
- Apps whose users signed up within minutes could still be a real same-hour launch (e.g., a demo to a class); conversely multi-day spans could be one owner re-registering.
- The 3 zero-database apps may store data elsewhere (external Supabase/Firebase, frontend-only) — 'no Mongo data' is not strictly 'no users'.
- Sample covers only status='active' hosted deployments; custom-domain apps (likely the most serious builders) are excluded from this S4 cut.
- Several min/max created_at values were null due to nonstandard schemas; activity date spans are missing for 3 apps.
- One app (citizen-advisor-1) stores accounts (n=5) separately from an empty users collection — collection-name heuristics will under/over-count without per-app inspection.
- Counts capped at what the read-only tool returns; all PII was redacted server-side ($group/$project, counts and timestamps only).


---

## econ_ltv_impact

### Summary
LTV segmentation of 2,517,665 users whose first root job ran 2026-01-01..2026-03-31 confirms deployment is the strongest monetization correlate, and AI builders who deploy are the single most valuable segment: AI-builder-deployed-within-30d (n=9,522) generates mean $206.71 / median $25 revenue in the 90 days after first job with 87.1% paying, vs $13.94 mean / 17.4% paying for AI builders who engaged deeply (>=$10 first-project compute) but never deployed (n=112,306) — a $192.77/user delta. AI deployers also out-monetize non-AI deployers ($206.71 vs $160.77, +29%). However, the H5 causality story is mixed: among AI deployers who ever topped up (50.9% of group a), 73.5% made their FIRST topup BEFORE their first deployment — deployment is more often the culmination of an already-paying journey than the topup trigger. Impact model: May 2026 produced 57,401 new engaged-not-deployed AI builders; converting +5/+10/+20pp of them to deployers is worth $0.55M/$1.11M/$2.21M per monthly cohort (90d revenue) as an upper bound, or $166K/$332K/$664K under a conservative 30%-of-delta causal assumption. Whale check: the top 20 users by 90d compute consumption (2026-03-14..06-12) consumed $2.39M of internal trajectory value against only $547K lifetime revenue (23% coverage) — every one is underwater on internal-value terms; finance must confirm actual COGS per value_in_usd dollar and ECU billing conversion before treating this as negative margin.

### Key numbers

- **Group a (AI deployed <=30d): n / mean / median 90d revenue / % paying**: 9,522 / $206.71 / $25.00 / 87.1% (topup share 80.6%)
- **Group b (AI engaged >=$10, not deployed): n / mean / median / % paying**: 112,306 / $13.94 / $0 / 17.4% (topup share 71.2%)
- **Group c (AI shallow): n / mean / % paying**: 258,315 / $1.94 / 3.7%
- **Group d (non-AI deployed <=30d): n / mean / median / % paying**: 40,130 / $160.77 / $20.00 / 85.7% (topup share 81.2%)
- **Group e (non-AI engaged, not deployed): n / mean / % paying**: 498,036 / $8.97 / 12.5% (topup share 68.8%)
- **Revenue delta per user, a minus b (90d)**: $192.77
- **Group a: first topup BEFORE first deploy (of 4,846 topup users)**: 73.5% (3,561 before vs 1,285 after; 50.9% of group a ever topped up)
- **May 2026 new engaged-not-deployed AI builders**: 57,401 (of 123,929 new AI builders; only 3,199 deployed <=30d so far)
- **Upper-bound incremental revenue +5pp / +10pp / +20pp conversion**: $553K / $1.107M / $2.213M per monthly cohort (90d)
- **Conservative (30% causal share) +5pp / +10pp / +20pp**: $166K / $332K / $664K per monthly cohort (90d)
- **Top-20 whales: 90d consumption vs lifetime revenue**: $2,386,970 consumed vs $547,233 collected (23% coverage); worst user: $158,828 consumed vs $7,960 paid
- **AI deployer premium over non-AI deployer (mean 90d revenue)**: +28.6% ($206.71 vs $160.77)

### 1) 90-day LTV by builder segment (first root job 2026-01-01..2026-03-31; revenue = user_revenue_events in 90d after first job)

| Segment | n users | Mean 90d rev | Median 90d rev | % paying | Total 90d rev | Topup share |
|---|---|---|---|---|---|---|
| (a) AI builder, deployed <=30d | 9,522 | $206.71 | $25.00 | 87.1% | $1,968,268 | 80.6% |
| (b) AI engaged (>= $10 first-project cost), not deployed | 112,306 | $13.94 | $0.00 | 17.4% | $1,566,002 | 71.2% |
| (c) AI shallow | 258,315 | $1.94 | $0.00 | 3.7% | $501,785 | 62.3% |
| (d) Non-AI builder, deployed <=30d | 40,130 | $160.77 | $20.00 | 85.7% | $6,451,768 | 81.2% |
| (e) Non-AI engaged, not deployed | 498,036 | $8.97 | $0.00 | 12.5% | $4,466,834 | 68.8% |
| (f) Non-AI shallow (reference) | 1,598,930 | $0.83 | $0.00 | 1.7% | $1,329,009 | 64.5% |

### 2) Topup-after-deploy ordering, group (a) (H5 causality direction)

| Metric | Value |
|---|---|
| Group (a) users | 9,522 |
| Ever topped up (lifetime) | 4,846 (50.9%) |
| First topup BEFORE/at first deploy | 3,561 (73.5% of topup users) |
| First topup AFTER first deploy | 1,285 (26.5% of topup users) |

### 3) Impact model arithmetic (May 2026 cohort: 57,401 engaged-not-deployed AI builders; delta = $206.71 - $13.94 = $192.77/user/90d)

| Scenario | Extra deployers (57,401 x pp) | Upper bound (x $192.77) | Conservative 30%-causal (x $57.83) |
|---|---|---|---|
| +5pp | 2,870 | $553,260 | $165,981 |
| +10pp | 5,740 | $1,106,500 | $331,944 |
| +20pp | 11,480 | $2,213,000 | $663,889 |

Arithmetic: incremental_revenue = 57,401 x uplift_pp x (mean_rev_a - mean_rev_b). Upper bound assumes converted users fully adopt deployer economics (selection bias ignored); conservative variant assumes only 30% of the observed delta is causally attributable to deploying.

### 4) Whale margin check: top 20 users by trajectory consumption 2026-03-14..2026-06-12 (internal value_in_usd, NOT billed price)

| Rank | user_id (short) | 90d consumption | Lifetime revenue | Lifetime topup | Gap (rev - consumption) |
|---|---|---|---|---|---|
| 1 | 21e6b39e | $171,253 | $40,241 | $38,800 | -$131,012 |
| 2 | bf1b9378 | $158,828 | $7,960 | $6,940 | -$150,868 |
| 3 | a58ff9de | $158,813 | $25,185 | $24,380 | -$133,628 |
| 4 | 6363871c | $149,501 | $33,040 | $29,020 | -$116,461 |
| 5 | 4bf75d3c | $139,897 | $22,985 | $22,400 | -$116,912 |
| 6 | dcb23419 | $131,372 | $35,340 | $30,920 | -$96,032 |
| 7 | de9e3463 | $129,233 | $32,862 | $32,029 | -$96,371 |
| 8 | 99b4a983 | $124,728 | $33,075 | $29,025 | -$91,653 |
| 9 | f8a890d0 | $123,783 | $32,361 | $25,700 | -$91,422 |
| 10 | ba9f8b9f | $122,467 | $37,253 | $6,050 | -$85,214 |
| 11 | 45590057 | $122,061 | $15,163 | $10,953 | -$106,898 |
| 12 | 5367b74d | $115,231 | $26,991 | $21,370 | -$88,240 |
| 13 | 7aa60b28 | $99,914 | $34,157 | $1,156 | -$65,757 |
| 14 | 96ec94ce | $94,688 | $25,950 | $2,950 | -$68,738 |
| 15 | 1290386d | $93,190 | $17,376 | $15,275 | -$75,814 |
| 16 | 30131d7e | $92,939 | $13,301 | $11,900 | -$79,638 |
| 17 | 10738fc2 | $92,891 | $21,968 | $20,967 | -$70,923 |
| 18 | daddf41e | $90,703 | $28,389 | $27,160 | -$62,315 |
| 19 | 105a7254 | $88,521 | $27,807 | $24,607 | -$60,714 |
| 20 | 0eac1e19 | $86,961 | $35,829 | $30,109 | -$51,131 |
| **Total** | | **$2,386,970** | **$547,233** | **$411,711** | **-$1,839,737** |

### Implications

- Deployment is the single biggest monetization lever for AI builders: 87.1% of AI deployers pay vs 17.4% of equally-engaged non-deployers, yet only 2.5% of new AI builders (9,522/380,143) deploy within 30d. The engaged-not-deployed pool (112K/quarter, 57K in May alone) is the addressable target for deploy-completion features (one-click agent hosting, API-key onboarding, agent-specific deploy templates, share-link previews).
- H5 nuance: topups mostly PRECEDE deployment (73.5%), so deploy features likely monetize by extending the build journey and retaining already-paying users, not by triggering the first payment. Position deployment as a retention/expansion lever (post-deploy iteration, custom domains, monitoring) rather than a first-purchase trigger; the 26.5% topup-after-deploy flow (running/maintaining a live agent) is the genuinely incremental H5 revenue path.
- Even the conservative model (+5pp conversion => ~$166K per monthly cohort, ~$2M annualized) likely clears the build cost of deploy-completion features; the upper bound (+10pp => $1.1M/monthly cohort) makes this a top-3 growth bet. Recommend shipping behind an experiment to measure the true causal share (we assumed 30%).
- AI builders who deploy monetize 29% better than non-AI deployers and skew topup-heavy (80.6%) — prioritize AI/agent-specific deployment ergonomics (LLM key management, agent endpoints, usage dashboards) over generic app hosting improvements.
- Whale economics need urgent finance review: top 20 consumers used $2.39M internal value against $547K collected. If value_in_usd is within ~4x of true COGS, heavy users are loss-making — pricing/rate-limit guardrails or enterprise contracts for the >$80K-consumption tier should accompany any growth push that creates more whales.

### Caveats

- SELECTION BIAS (critical): deployers self-select — higher intent, more complete apps, more budget. The $192.77/user delta is an UPPER bound on the causal effect of getting an engaged user to deploy; the 30%-of-delta 'conservative' figure is an assumption, not a measurement. A holdout experiment on deploy-nudges is needed for a true causal estimate.
- AI keyword filter v1 precision ~57% (applied to first ROOT job task only): group (a/b/c) contains ~43% non-AI-product builders; treat AI/non-AI contrast as directional.
- Right-censoring: users with first job after 2026-03-14 have <90 observed days of revenue (min ~73 days for Mar 31 starters), slightly deflating 90d means for all groups.
- May 2026 count (57,401) is conservative/incomplete: deploy-within-30d windows for users starting after May 13 had not closed by Jun 12 (only 3,199 deployed so far vs 2.5% steady-state rate => some engaged-not-deployed users will reclassify), and first-project costs were still accruing.
- 'Deployed within 30d' = any deployer_db_data row (incl. later-deleted apps) within 30d of first root job; status/verified not filtered. 'Not deployed' groups include users who deployed after day 30 (biases group b revenue UP, making the delta slightly conservative on that axis).
- Whale check: trajectories value_in_usd is INTERNAL consumption value (list-price model value), NOT billed price and NOT Emergent's marginal cost. Finance must confirm: (1) actual provider COGS per $1 of value_in_usd (committed-use discounts, prompt caching), (2) ECU-to-USD billed conversion per tier, (3) whether top whales have enterprise/invoiced revenue outside user_revenue_events (rows 10 and 13 show large revenue not explained by topup+subscription, suggesting other payment categories exist), (4) refund treatment in user_revenue_events.
- Redash adhoc 60s timeout forced execution via direct bq CLI on project emergent-default; deployer_db_data and user_revenue_events are federated Postgres views with high latency variance (one query died with a replica 'conflict with recovery' error).
- Per-user revenue is the sum of user_revenue_events in [first_job_ts, first_job_ts+90d); medians of $0 in groups b/c/e/f mean the means are driven by a thin paying tail — model totals, not typical users.


---

## cost_shock

### Summary
Credit exhaustion is tightly coupled to the death of engaged AI projects, but it is a conversion moment as much as a friction point. Among AI-candidate root projects created 2026-04-01..2026-05-15 that died engaged ($10-100 spent, never deployed), 83.8% of their users hit a zero/negative credit balance within ±3 days of the project's last activity — vs 55.9% for users of deployed AI projects (a 28pp gap). Zero-balance is therefore strongly over-represented at the death of engaged projects, but it is not a clean differentiator: deployers hit zero too — they just pay through it (median 1.9 hours from first zero-balance to first topup; 25% top up essentially instantly). The cost of NOT paying is severe: of 251,036 AI builders who hit zero (Apr 1–May 28), 88.9% never ran another job in the following 14 days. Day-1 DAILY_CREDITS exhaustion is the norm for new AI builders (65.6% of May first-job users) and correlates with 1.8x higher 24h paid conversion (7.65% vs 4.15%) — burning the free pool signals engagement, not churn. On pricing: 1 ECU ≈ $1 of metered agent cost (validated: May 6 trajectory cost $2.03M vs 2.03M ECU of LLM_CALL debits), so the $111 median spend-to-deploy for an AI app equals ~111 ECU ≈ 1.1 months of the Standard plan's median 100 ECU monthly allocation — before the ~50-59 ECU deployment debit, which pushes a shipped AI app to ~1.6 Standard-months of credits. A $10/month Standard subscription structurally cannot finish a single AI app; the data supports a 'ship-it credit pack' offered at the zero-balance moment for projects with >$10 already invested.

### Key numbers

- **Died-engaged AI projects (Apr 1–May 15, $10-100, not deployed)**: 115,708 projects / 108,573 users
- **% of died-engaged users hitting balance <= 0 within ±3d of project last activity**: 83.8% (90,948 users; 82.1% of projects)
- **% of deployed-AI-project users hitting balance <= 0 within ±3d of last activity**: 55.9% (4,762 of 8,516 users; 54.7% of 9,564 projects)
- **Exhaustion gap, died-engaged vs deployed**: +27.9pp
- **May 2026 AI first-job users exhausting DAILY_CREDITS to zero on day 1**: 65.6% (80,809 of 123,186)
- **24h paid conversion: day-1 exhausters vs non-exhausters**: 7.65% vs 4.15% (1.8x)
- **AI builders with first topup in May 2026**: 8,540 (88.2% had hit zero first)
- **Median hours first zero-balance to first topup**: 1.9h (p25 ~0h, p75 88.5h)
- **AI builders hitting zero who never run another job in 14d**: 88.9% (223,278 of 251,036; first zero Apr 1–May 28)
- **Standard plan monthly credit grant**: 100 ECU median (avg $10.19/payment, 157,128 May grants)
- **ECU to USD metered-cost ratio**: ~1:1 (May 6: $2,029,844 trajectory cost vs 2,033,796 ECU LLM debits)
- **Standard-months of credits per deployed AI app ($111 median spend-to-deploy)**: ~1.1 months build-only; ~1.6 months incl. ~50-59 ECU deployment debit

### Zero-balance within ±3 days of project last activity (AI root projects, created 2026-04-01..2026-05-15)

| Cohort | Projects | Users | Projects hit zero ±3d | % projects | Users hit zero | % users |
|---|---|---|---|---|---|---|
| Died engaged ($10-100, not deployed) | 115,708 | 108,573 | 94,977 | 82.1% | 90,948 | 83.8% |
| Deployed (any cost) | 9,564 | 8,516 | 5,234 | 54.7% | 4,762 | 55.9% |

### Day-1 DAILY_CREDITS exhaustion vs 24h paid conversion (AI-candidate first jobs, May 2026)

| Day-1 daily pool exhausted | Users | Converted within 24h | 24h conversion |
|---|---|---|---|
| Yes | 80,809 | 6,185 | 7.65% |
| No | 42,377 | 1,758 | 4.15% |

### Topup latency and post-zero retention (AI builders, Apr-May 2026 cohort)

| Metric | Value |
|---|---|
| AI users with first topup in May | 8,540 |
| ...of which topped up after a zero-balance event | 7,532 (88.2%) |
| Median hours, first zero -> first topup | 1.9h |
| p25 / p75 hours | ~0h / 88.5h |
| AI builders hitting zero (Apr 1-May 28) | 251,036 |
| Never ran another job within 14d of first zero | 223,278 (88.9%) |

### Monthly subscription ECU grants by tier (May 2026, ecu>0)

| Tier | Grants | Median ECU | Avg ECU | Avg payment |
|---|---|---|---|---|
| Emergent Standard | 157,128 | 100 | 84.8 | $10.19 |
| Emergent Starter | 9,960 | 50 | 50.5 | $5.93 |
| Emergent Pro Lite | 792 | 200 | 160.2 | $44.86 |
| Emergent Pro | 4,249 | 750 | 654.3 | $318.12 |

### Implications

- Credit exhaustion is a major correlate of engaged-AI-project death: 5 of 6 users whose $10-100 AI project died were at zero balance within 3 days of its last activity, 28pp above the deployed baseline — this is the single clearest friction marker on the H6 path.
- The zero-balance moment is a decisive, fast-closing purchase window: payers decide in ~2 hours (median), and non-payers are 89% gone within 14 days. Rescue interventions must fire within hours, not days.
- Ship-it credit pack: a one-time, project-scoped pack (~150-200 ECU, enough to cover the remaining ~40-90 ECU to deploy plus the ~50 ECU deployment debit) offered in-product at zero-balance for projects with >$10 already sunk. Frame it as progress preservation ('your app is ~70% of the way to live').
- Repackage Standard: at 100 ECU/month vs ~160 ECU for one shipped AI app, the entry subscription guarantees mid-project exhaustion. Either add an AI-builder tier (~200-250 ECU) or bundle the first deployment fee into the first month for projects that reach deploy-readiness.
- Don't throttle the free pool: day-1 DAILY_CREDITS exhaustion converts 1.8x better — full-burn is a qualification signal. The optimization is what happens at the wall (offer, messaging, remaining-cost estimate), not preventing users from hitting it.
- Show price-to-finish: with 1 ECU ≈ $1 of metered cost, surface a live 'estimated credits to deployable' meter for AI projects so the $111 price of success is anticipated rather than a shock at zero balance.

### Caveats

- AI-keyword filter v1 has ~57% precision, so roughly 4 in 10 'AI' projects are misclassified; comparisons between cohorts are more reliable than absolute counts.
- running_balance_ecu <= 0 includes routine DAILY_CREDITS pool exhaustion (free daily credits are designed to run to zero), inflating absolute zero-balance rates in both cohorts; the 28pp died-vs-deployed gap is the meaningful signal, not the 83.8% level.
- Correlation, not causation: zero-balance near project death may co-occur with other death causes (errors, frustration); a holdout/credit-grant experiment would be needed to prove exhaustion kills projects.
- credit_ledger is only queryable from 2026-04-01 (partition filter), so 'first zero-balance' may miss earlier zero events for users active before April.
- 'Deployed' cohort includes deployed AI projects of any cost (not restricted to $10-100), per task spec; deployed projects also skew to higher-spend users who may simply have autopay/topup habits.
- ECU≈$1 of metered cost was validated on a single day (2026-05-06, 0.2% difference); topup retail pricing implies users buy ECU at a discount (avg topup $44.29 vs ~150 ECU granted), so '$111' is metered credits consumed, not necessarily cash paid.
- analytics.deployer_db_data (federated Postgres view) consistently timed out; analytics.deployer_db_data_snapshot (native, fresh to 2026-06-12 11:05) was used instead — counts could differ marginally from prior phases.
- The ±3-day window counts zero-balance events both before and after last activity; the 14d never-return metric uses root/fork jobs only (subagent jobs excluded).


---

## support_churn_voc

### Summary
Voice-of-customer analysis for AI builders (users with >=1 AI-keyword root job). Cohort: 578,341 users (574,965 emails) with an AI-candidate root job 2026-03-14..2026-06-12. Support (tickets since 2026-03-01): AI builders filed 1,089 of 5,128 tickets (21.2%) from 678 distinct emails; they over-index heavily on production/deployment pain (Production Site Errors: 45% of that cluster's tickets are AI builders vs 21% base rate) and under-index on account-deletion noise (3%). Manual tagging of 40 deterministically sampled AI-builder subjects: deployment 33%, billing/credits 15%, app-broken 13%, refund 13%, integration/keys 5%, other 23%. Churn: predict_churn classifications contain NO data after 2026-02-25, so the requested cancelled_at >= 2026-03-01 window returned zero rows; adapted to the latest available window (2025-12-01..2026-02-25) with the AI-builder job window extended back to 2025-11-01 to overlap it. AI-builder cancellations: 14,316; bad_churn 54.9% vs 50.8% for non-AI builders (+4.1pp; no 'pause' segment exists in this window — third segment is 'unclassifiable'). Cost-related reasons (pricing_perception + token_wastage + budget_constraint) account for 58% of AI-builder bad churn; product quality (agent_quality + deployment_issues) 19%; onboarding_confusion 8%. Cancellation timing: of churners whose first AI job preceded cancellation, 33% cancelled within 0-1 days of their first AI job and 49% within 7 days; 19% of AI-builder churners ran their first AI job only AFTER cancelling.

### Key numbers

- **AI-builder cohort (root AI job 2026-03-14..2026-06-12)**: 578,341 users / 574,965 distinct emails
- **Support tickets since 2026-03-01 (segment_number=1)**: 5,128 total; 1,089 from AI builders (21.2%); 678 distinct AI-builder emails of 3,772 (18.0%)
- **AI share of 'Production Site Errors and Outages' cluster**: 61/136 = 44.9% (vs 21.2% baseline)
- **AI share of 'Account Deletion Requests' cluster**: 18/603 = 3.0% (strong under-index)
- **AI-builder cancellations classified (2025-12-01..2026-02-25)**: 14,316 (bad 7,860 / good 4,403 / unclassifiable 2,053)
- **Bad-churn rate: AI builders vs non-AI**: 54.9% vs 50.8% (+4.1pp, ~8% relative)
- **Cost-driven share of AI-builder bad churn (pricing+token_wastage+budget)**: 4,588/7,860 = 58.4%
- **Cancellation within 7 days of first AI job (where job precedes cancel)**: 5,649/11,593 = 48.7% (0-1d alone: 32.7%)

### Support ticket themes — 40 deterministic-sample AI-builder subjects (manual tagging)

| Theme | Count | Share | Example subjects |
|---|---|---|---|
| Deployment (deploy fails, custom domain/DNS, prod-vs-preview sync, mobile publish, CORS) | 13 | 32.5% | "impossible to deploy app", "Attach Custom Domain", "Production deployment not syncing with Preview" |
| Billing/credits (deductions, missing credits, regeneration) | 6 | 15.0% | "again and again deducting my credits", "Concern Regarding Credits Deduction for AI Errors" |
| App-broken (errors initiating project, live app down, password-reset bug) | 5 | 12.5% | "URGENT - Backend returning 'Deployment not found' - live client app is down", "CRITICAL BUG - Admin password resets after every deployment" |
| Refund (wasted credits, failed-deploy charges, disputed receipts) | 5 | 12.5% | "Charged 50 Credits But Deployment Failed", "project destroy + use my credits 27 credits" |
| Integration/keys (signing credentials, IP whitelisting for OAuth) | 2 | 5.0% | "Need to Upload New iOS Signing Credentials", "Help Needed with All IP Whitelisting for Google Auth" |
| Other (account ownership, watermark, cancellations, vague) | 9 | 22.5% | "change ownership of account", "Watermark Removal" |

### Top support clusters for AI-builder tickets (>=2026-03-01; JSON $.cluster)

| Cluster | AI tickets | All tickets | AI share |
|---|---|---|---|
| Production Site Errors and Outages | 61 | 136 | 44.9% |
| Custom Domain Linking and DNS Configuration | 49 | 145 | 33.8% |
| Production vs Preview Discrepancies | 40 | 108 | 37.0% |
| Production Database Connection and Configuration | 38 | 93 | 40.9% |
| Deployment Build Failures | 37 | 92 | 40.2% |
| Support Ticket Follow-ups | 37 | 106 | 34.9% |
| Missing Credits and Refresh Issues | 30 | 157 | 19.1% |
| Refund Requests for Wasted Credits | 30 | 112 | 26.8% |
| Deployment Credit Charges and Refunds | 27 | 69 | 39.1% |
| Data Loss and Project Access Issues | 24 | 79 | 30.4% |
| Invoice and Receipt Requests | 24 | 98 | 24.5% |
| Complaints About Excessive Credit Consumption | 23 | 65 | 35.4% |
| Frustration with Agent Performance/Bugs | 23 | 82 | 28.0% |
| Deployment Issues and URL Requests | 23 | 81 | 28.4% |
| Account Deletion Requests | 18 | 603 | 3.0% |
| (baseline: AI builders = 21.2% of all tickets) | 1,089 | 5,128 | 21.2% |

### Churn segment split — AI builders vs non-AI (cancelled 2025-12-01..2026-02-25)

| Cohort | bad_churn | good_churn | unclassifiable | Total | Bad-churn rate |
|---|---|---|---|---|---|
| AI builders | 7,860 | 4,403 | 2,053 | 14,316 | 54.9% |
| Non-AI | 12,416 | 8,180 | 3,822 | 24,418 | 50.8% |
| Delta | — | — | — | — | +4.1pp |

Note: no 'pause' segment exists in this window; the classifier's third bucket is 'unclassifiable'.

### Churn reasons for AI builders (cancelled 2025-12-01..2026-02-25), clustered into themes

| Theme | churn_reason (segment) | Count | % of AI churners (n=14,316) |
|---|---|---|---|
| Done with project (good) | project_completed (good) | 3,889 | 27.2% |
| Cost / value perception | pricing_perception (bad) | 2,754 | 19.2% |
| Cost / value perception | token_wastage (bad) | 1,140 | 8.0% |
| Cost / value perception | budget_constraint (bad) | 694 | 4.8% |
| Cost / value perception | budget_constraint (good) | 296 | 2.1% |
| Cost / value perception | business_model_mismatch (bad) | 292 | 2.0% |
| Product quality | agent_quality (bad) | 980 | 6.8% |
| Product quality | deployment_issues (bad) | 490 | 3.4% |
| Onboarding / UX | onboarding_confusion (bad) | 663 | 4.6% |
| Competition | competitor_switch (bad) | 517 | 3.6% |
| Got value, leaving (good) | value_received (good) | 201 | 1.4% |
| Unclassifiable | unclassifiable (uncl.+bad) | 2,316 | 16.2% |

Within bad churn (7,860): cost/value = 58.4%, product quality = 18.7%, onboarding = 8.4%, competitor = 6.6%.

### Cancellation timing — days from first AI root job to cancellation (AI-builder churners, n=14,316)

| Bucket | N | % of all | % of those with job before cancel (n=11,593) | Cumulative |
|---|---|---|---|---|
| First AI job AFTER cancellation | 2,723 | 19.0% | — | — |
| 0-1 days | 3,793 | 26.5% | 32.7% | 32.7% |
| 2-3 days | 817 | 5.7% | 7.0% | 39.8% |
| 4-7 days | 1,039 | 7.3% | 9.0% | 48.7% |
| 8-14 days | 1,085 | 7.6% | 9.4% | 58.1% |
| 15-30 days | 1,951 | 13.6% | 16.8% | 74.9% |
| 31-60 days | 2,081 | 14.5% | 18.0% | 92.9% |
| 60+ days | 827 | 5.8% | 7.1% | 100% |

### 8 representative AI-builder churn quotes (deterministic sample, one per bad-churn reason, anonymized)

| Reason | Quote |
|---|---|
| agent_quality | "Not as advertised. Only creates prototype, not polished, publishable app." |
| pricing_perception | "too much for deploying the project, I mean 50 credits? you gotta be kidding me." |
| token_wastage | "bot enough credits to complete an app for a month" [sic — 'not enough'] |
| budget_constraint | "not enough credits to work for in a month" |
| deployment_issues | "The project as planned was not delivered exactly as envisioned. Anyway, thank you for the experience." |
| onboarding_confusion | (Russian, translated) "The service didn't meet expectations: too many 'summaries' instead of direct access to results, awkward to copy/export files, the interface is confusing about what gets copied, and the cost doesn't match the value received. Unsubscribing." |
| competitor_switch | "I think I will use another because I don't expert on the framework you expert" |
| business_model_mismatch | (Portuguese, translated) "A charge appeared for me today. I didn't want a fixed plan — I subscribed last month for one specific task and haven't used it since. I'd like cancellation and a refund for February. I like the platform, I just don't want a monthly subscription." |

### Implications

- Deployment is the #1 support burden for AI builders: they file 33-45% of tickets in every production/deployment cluster (site errors, build failures, prod-vs-preview drift, prod DB config) vs a 21% baseline. An 'AI-app deployment preflight' (env-var/LLM-key checks, prod-vs-preview parity diff, post-deploy smoke test) targets the densest pain.
- Charging 50 credits for deployments that then fail is a double hit appearing in both tickets ('Charged 50 Credits But Deployment Failed') and churn ('50 credits? you gotta be kidding me'). Auto-refunding credits on failed deploys / charging only on successful deploy would defuse the single most quotable grievance.
- 58% of AI-builder bad churn is cost/value (pricing, token wastage, budget). AI apps burn more credits (LLM integration debugging, agent loops). Consider AI-builder-specific value levers: credit-efficient retry on agent errors, no-charge-on-agent-fault policy, or an AI-builder plan with higher credit allotment.
- One-third of churning AI builders cancel within 0-1 days of their FIRST AI job, half within a week — the first AI-build session is the make-or-break moment. Invest in first-run success for AI prompts: working LLM-key onboarding, templates with pre-wired AI integrations, and proactive guidance when the first AI job stalls.
- AI builders rarely rage-quit the account (3% of account-deletion tickets) — they engage, hit walls, and churn on cost/quality. They are recoverable with product fixes, unlike drive-by signups.
- Integration/key issues are visible but small in tickets (5% of sampled subjects: OAuth IP whitelisting, signing credentials); bundled managed LLM keys (Emergent universal key) likely already absorb most of this — keep it default-on for AI templates.

### Caveats

- Churn data gap: predict_churn.churn_reason_classifications has NO rows with cancelled_at >= 2026-03-01 (max is 2026-02-25). All churn analyses use cancelled_at 2025-12-01..2026-02-25 instead of the requested window.
- Because the churn window predates the step-1 cohort window, AI-builder status for churn analyses uses an EXTENDED root-AI-job window (2025-11-01..2026-06-12). The support analysis uses the original step-1 cohort (jobs 2026-03-14..2026-06-12).
- AI-keyword filter v1 has ~57% precision, so roughly 4 in 10 'AI builders' may not actually be building AI products; counts for the AI cohort are inflated accordingly and deltas vs non-AI are diluted, not exaggerated.
- 'pause' churn segment does not appear in this window — the classifier emits bad_churn/good_churn/unclassifiable; 16% of AI-builder churn is unclassifiable.
- 19% of AI-builder churners ran their first AI root job after cancelling (free-tier usage post-cancel, or their earlier AI work predates the 2025-11-01 job window); timing distribution excludes them from cumulative percentages.
- Support join is on lowercase email; tickets from emails not matching a signup email (aliases, secondary addresses) are counted as non-AI. Support cluster labels are upstream LLM-generated and overlapping (many near-duplicate deployment/refund clusters).
- Churn reasons are gpt-4o-mini classifications of free-text cancellation feedback (model_version gpt-4o-mini-v1), not human-coded; quotes are verbatim user feedback truncated to 300 chars.


---

## geo_device_model

### Summary
Profiled AI-candidate builders on root projects created 2026-03-14..2026-06-12 (AI-keyword filter v1, root task only; internal users excluded). 704,660 of 4,491,140 root jobs (15.7%) are AI-candidates, built by ~575k distinct users (~18.3% of ~3.14M builders). Geography: India dominates volume (50.3% of AI builders vs 43.1% baseline); the countries that over-index for AI building are Australia (24.3% of its builders build AI), Canada (22.0%), Pakistan (21.9%), India (21.4%), UAE (21.2%), and US (20.8%), while Indonesia, Mexico, Turkey, Spain, Brazil under-index sharply (9-12%). Device: AI builders skew Desktop hard — 52.3% of AI builders signed up on Desktop vs 39.9% baseline; Mobile Web is 35.2% vs 43.1% and Mobile App 10.6% vs 15.3%. Model mix on AI root jobs is nearly identical to non-AI (Claude Opus 4.7 38.6%, Sonnet 4.5 thinking 35.4%); AI tasks slightly over-index on premium/1M-context variants. Free-prompt share is lower for AI (29.3% vs 33.0%) — AI builders are modestly more likely to start on paid prompts. H9 (AI projects iterate more via forks): weak support — among $10+ projects, 98.0% of AI projects are single-job vs 98.8% non-AI; AI projects are 1.66x more likely to be multi-job (2.01% vs 1.21%), but fork-level iteration is rare for everyone (iteration evidently happens inside jobs via chat, not forks). Language: 13% of a 200-task AI sample is non-English (French and Portuguese lead); excluding the 15% of the sample that is a duplicated English 'OpenClaw' abuse template, organic non-English share is 15.3%.

### Key numbers

- **AI-candidate root jobs (2026-03-14..06-12)**: 704,660 of 4,491,140 root jobs = 15.7%
- **AI builders (distinct users with >=1 AI root project)**: ~575k of ~3.14M builders = ~18.3%
- **Top AI-building-rate countries (% of country's builders building AI)**: Australia 24.25%, Canada 21.97%, Pakistan 21.93%, India 21.38%, UAE 21.19%, US 20.82%
- **Lowest AI-building-rate countries (top-20 volume)**: Mexico 9.13%, Türkiye 9.69%, Indonesia 10.45%, Spain 10.59%, Saudi Arabia 12.28%, Brazil 12.44%
- **Desktop signup share: AI builders vs baseline**: 52.31% vs 39.89% (+12.4pp); Mobile Web 35.19% vs 43.06%; Mobile App 10.56% vs 15.26%
- **Free prompt share (prompt_name LIKE 'free_%') on root jobs**: AI 29.26% vs non-AI 32.97%
- **Top models on AI root jobs**: claude-opus-4-7 38.57%, claude-sonnet-4-5(thinking) 35.35%, claude-opus-4-5(thinking) 8.18% — nearly identical to non-AI mix
- **Multi-job rate among $10+ projects (H9)**: AI 2.01% vs non-AI 1.21% (1.66x); avg jobs/project 1.06 vs 1.04; p50=p90=1 for both
- **$10+ projects analyzed**: 272,410 AI vs 1,030,338 non-AI
- **Non-English share of AI tasks (manual classification, n=200)**: 13.0% overall; 15.3% excluding 30 spam-template tasks. Mix: FR 9, PT 6, IT 3, ES 2, HI 2, DE 1, AR 1, RO 1, ZH 1
- **Spam contamination in AI sample**: 30/200 (15%) identical 'OpenClaw Installation' abuse template; >=2 prompt-injection/credential-leak prompts observed

### Country mix: AI builders vs platform baseline (top 15 by AI builders, 2026-03-14..06-12)

| Country | AI builders | All builders | AI share % | Baseline share % | Over-index (AI/base) | % of country building AI |
|---|---|---|---|---|---|---|
| India | 289,280 | 1,352,995 | 50.31 | 43.09 | 1.17 | 21.38 |
| United States | 48,936 | 234,993 | 8.51 | 7.48 | 1.14 | 20.82 |
| France | 20,047 | 108,828 | 3.49 | 3.47 | 1.01 | 18.42 |
| Indonesia | 17,417 | 166,672 | 3.03 | 5.31 | 0.57 | 10.45 |
| Brazil | 17,001 | 136,614 | 2.96 | 4.35 | 0.68 | 12.44 |
| Italy | 15,388 | 81,010 | 2.68 | 2.58 | 1.04 | 19.00 |
| United Kingdom | 12,965 | 67,592 | 2.25 | 2.15 | 1.05 | 19.18 |
| Pakistan | 10,980 | 50,069 | 1.91 | 1.59 | 1.20 | 21.93 |
| Canada | 9,865 | 44,898 | 1.72 | 1.43 | 1.20 | 21.97 |
| Germany | 8,951 | 54,208 | 1.56 | 1.73 | 0.90 | 16.51 |
| Spain | 7,593 | 71,671 | 1.32 | 2.28 | 0.58 | 10.59 |
| Australia | 6,847 | 28,240 | 1.19 | 0.90 | 1.32 | 24.25 |
| South Africa | 6,405 | 35,814 | 1.11 | 1.14 | 0.97 | 17.88 |
| Türkiye | 6,377 | 65,843 | 1.11 | 2.10 | 0.53 | 9.69 |
| Bangladesh | 5,461 | 30,944 | 0.95 | 0.99 | 0.96 | 17.65 |

### Device type mix at signup: AI builders vs baseline

| Device type | AI builders | All builders | AI share % | Baseline share % | Delta (pp) |
|---|---|---|---|---|---|
| Desktop | 300,775 | 1,252,316 | 52.31 | 39.89 | +12.42 |
| Mobile Web | 202,348 | 1,351,826 | 35.19 | 43.06 | -7.87 |
| Mobile App | 60,739 | 479,056 | 10.56 | 15.26 | -4.70 |
| Tablet | 5,482 | 31,505 | 0.95 | 1.00 | -0.05 |
| (unknown) | 5,622 | 24,899 | 0.98 | 0.79 | +0.19 |

### Model mix on root jobs: AI vs non-AI (top 10 by AI volume)

| model_name | AI root jobs | AI share % | Non-AI share % |
|---|---|---|---|
| claude-opus-4-7 | 271,800 | 38.57 | 38.25 |
| claude-sonnet-4-5?thinking_mode=true | 249,080 | 35.35 | 38.54 |
| claude-opus-4-5?thinking_mode=true | 57,635 | 8.18 | 9.80 |
| claude-opus-4-5-20251101?thinking_mode=true | 28,119 | 3.99 | 1.47 |
| claude-opus-4-6 | 27,934 | 3.96 | 1.55 |
| claude-opus-4-7?thinking_mode=true | 15,020 | 2.13 | 2.24 |
| claude-sonnet-4-5 | 10,723 | 1.52 | 1.43 |
| claude-sonnet-4-6 | 10,097 | 1.43 | 0.59 |
| claude-opus-4-6?thinking_mode=true | 9,649 | 1.37 | 1.24 |
| gpt-5.3-codex | 4,524 | 0.64 | 0.46 |

Free-prompt share (prompt_name LIKE 'free_%'): AI 206,211/704,660 = 29.26% vs non-AI 1,248,329/3,786,462 = 32.97%.

### Jobs-per-project distribution, projects with cost >= $10 (trajectories DATE >= 2026-03-14)

| Segment | Projects | Avg jobs | p50/p75/p90 | 1 job % | 2-3 % | 4-6 % | 7-10 % | 11-20 % | 21+ % |
|---|---|---|---|---|---|---|---|---|---|
| AI | 272,410 | 1.06 | 1 / 1 / 1 | 97.99 | 1.50 | 0.27 | 0.12 | 0.08 | 0.04 |
| Non-AI | 1,030,338 | 1.04 | 1 / 1 / 1 | 98.79 | 0.93 | 0.16 | 0.06 | 0.04 | 0.02 |

### Language mix of 200 sampled AI root tasks (manual classification)

| Language | Count | % of 200 |
|---|---|---|
| English (incl. 30 OpenClaw spam-template tasks) | 174 | 87.0 |
| French | 9 | 4.5 |
| Portuguese | 6 | 3.0 |
| Italian | 3 | 1.5 |
| Spanish | 2 | 1.0 |
| Hindi/Hinglish (romanized) | 2 | 1.0 |
| German | 1 | 0.5 |
| Arabic | 1 | 0.5 |
| Romanian | 1 | 0.5 |
| Chinese | 1 | 0.5 |

Non-English total: 26/200 = 13.0%; excluding the 30 English spam-template tasks: 26/170 = 15.3%.

### Implications

- AI builders are a desktop-first, paid-leaning audience: +12pp Desktop share and lower free-prompt usage suggest AI-product growth features (agent templates, LLM-key management, RAG scaffolding) should ship desktop-web first and can be positioned behind paid tiers without losing the core audience.
- Geography: prioritize India + English-speaking markets (US, CA, AU, UK, PK, UAE) for AI-builder campaigns — they both dominate volume and over-index on propensity (20-24% of their builders build AI). Indonesia/Brazil/Mexico/Turkey are large on the platform but under-index ~2x for AI building — localized AI-use-case content (and pt-BR/id/es onboarding) is the unlock there, consistent with the ~15% non-English organic task share led by French and Portuguese.
- Model choice is not a differentiator for AI builders (mix mirrors non-AI), so growth levers should target workflow (agent testing, API key vaults, LLM cost visibility) rather than model selection UX; slight over-index on premium/1M-context variants hints AI builders will pay for capability.
- H9 largely rejected at the fork level: even $10+ AI projects are 98% single-job. Iteration happens inside one long job, so invest in in-job iteration ergonomics (checkpoints, HITL, rollback) rather than fork-based flows; the 1.66x multi-job ratio for AI is real but tiny in absolute terms.
- Operational: the 'OpenClaw' spam template polluting ~15% of AI-candidate tasks (plus prompt-injection attempts with credential exfiltration) warrants an abuse review and a v2 keyword filter that excludes the template before this segment is used for targeting or sizing.

### Caveats

- AI-keyword filter v1 has ~57% precision, so absolute AI counts are inflated; comparisons (AI vs non-AI shares) are more robust than levels.
- Root project defined as job absent from analytics.fork_chain (job_id LEFT JOIN null); jobs-per-project counts only fork_chain descendants, NOT in-conversation follow-up messages — so 'iteration depth' here measures forking, not chat iteration. H9 may still hold at the message level (human_message/HITL), which was not measured here.
- Fork-depth cost filter sums trajectories with DATE(created_at) >= 2026-03-14 only; jobs whose spend partially predates the window are slightly undercounted, and root jobs with zero trajectory rows in the window are dropped by the inner join.
- Device/country are signup-time attributes from signups_raw_dataset, not where the building happened; users without a signup row are excluded by the join.
- Language estimate based on first 250 chars of n=200 random AI root tasks classified manually; margin of error roughly +/-4.7pp at 95% CI. Tasks with English prompt wrappers around non-English brands were counted as English.
- 15% of the AI sample is a single duplicated 'OpenClaw Installation' template (likely coordinated abuse/spam) and the sample contained prompt-injection and leaked-credential prompts — AI-candidate volume and the keyword filter are contaminated by this campaign.
- is_ai was NULL for 18 root jobs (null task); excluded from shares.


---

## llm_proxy_prod_usage

### Summary
Runtime (production) LLM usage IS distinguishable from build-time usage in the LLM Proxy Postgres (Redash DS 9, table llm_logs_partitioned). Build-time agent calls are logged as OUTBOUND requests with absolute provider URLs (api.anthropic.com, aws-external-anthropic, Azure OpenAI, Vertex) and metadata X_emergent_agent_name (EmergentAssistant ~2.65M calls/day). Runtime universal-key calls from apps are logged as INBOUND requests with relative URLs (/chat/completions, /v1/messages, /models/gemini-*:generateContent), proxy headers (X-Forwarded-For, Traceparent), and a run_id of the form '<job_uuid>_<app-defined-session-suffix>' — the embedded UUID is the app's job_id, giving per-app attribution. Sizing (June 8-11, 2026, the only ~5 days retained): inbound universal-key traffic is ~510k-563k calls/day from ~57k-64k distinct app UUIDs — but the vast majority is ephemeral build/preview-time app testing. Only 4,634 app UUIDs (7.3% of 06-11 actives) were also active 3 days earlier; this persistent 'production' cohort drove 86,341 calls on 06-11 (15.3% of inbound volume). Within it: median 10 calls/day, p90 47, only 412 apps >=50 calls/day, ~113 apps >=100 calls/day platform-wide, and the single busiest app did just 336 calls/day; zero apps exceed 1,000 calls/day and zero 429s were observed (error rate 0.2-0.8%). Cross-checking the top 60 persistent apps in BigQuery validated the heuristic: all 60 are real jobs from 60 distinct users, 51 (85%) are deployed, 37 (62%) on custom domains, 35 (58%) match the AI-keyword filter. Runtime model mix (15-min sample, n=7,655): gemini-3-flash-preview 46%, gpt-5-nano 19%, gpt-5.2 17%, claude-haiku-4-5 10%, claude-sonnet-4-5 6%. Bottom line: the 'operate' business today is a long tail of ~4.6k recurring apps with tiny per-app traffic — roughly 400 apps with meaningful (>=50 calls/day) end-user usage, not 10 whales and not thousands of high-volume apps.

### Key numbers

- **Inbound (universal-key) LLM calls per day, 2026-06-08 → 06-11**: 510,881 → 524,510 → 551,173 → 562,511 (steadily growing, +10% over 4 days)
- **Total LLM proxy log rows on 2026-06-11 (build + runtime)**: 3,476,851 (runtime inbound = ~16% of rows)
- **Distinct app UUIDs making inbound calls on 2026-06-11**: 63,831 (but 11,504 made <=2 calls; median 7 calls — mostly build/preview testing)
- **Persistent 'production' apps (active on both 06-08 and 06-11)**: 4,634 apps; 86,341 calls on 06-11 (15.3% of inbound volume)
- **Production cohort distribution (06-11)**: p50 = 10 calls/day, p90 = 47; 2,408 apps >=10 calls; 412 apps >=50 calls; busiest app = 336 calls/day; 0 apps >=1,000
- **Apps >=100 calls/day (platform-wide, 06-11)**: 113 apps, 15,131 calls combined (2.7% of inbound volume)
- **Top-60 persistent apps validation (BigQuery)**: 60/60 real jobs, 60 distinct users, 51 deployed (85%), 37 custom domains (62%), 35 AI-keyword tasks (58%)
- **Runtime error rate (status >=400)**: 0.23%-0.78% per day; 429s = 0 on all 4 days
- **Runtime model mix (sample n=7,655, 06-11 12:00-12:15 UTC)**: gemini-3-flash-preview 46.4%, gpt-5-nano 19.3%, gpt-5.2 16.9%, claude-haiku-4-5 9.6%, claude-sonnet-4-5 5.7%, opus-tier <1.5%
- **Log retention in proxy DB**: ~5 days (oldest populated partition 2026-06-08; 60d trend not possible from this source)

### Daily inbound (universal-key / runtime-path) LLM traffic — llm_logs_partitioned, url NOT LIKE 'http%'

| Day (2026) | Inbound calls | Distinct app UUIDs | Errors (>=400) | Error % | 429s |
|---|---|---|---|---|---|
| 06-08 | 510,881 | 56,750 | 1,167 | 0.23% | 0 |
| 06-09 | 524,510 | 57,970 | 2,992 | 0.57% | 0 |
| 06-10 | 551,173 | 61,872 | 2,705 | 0.49% | 0 |
| 06-11 | 562,511 | 63,831 | 4,391 | 0.78% | 0 |

### Build-time vs runtime call identification (LLM Proxy DS 9)

| Signal | Build-time (agent) | Runtime (deployed/preview app via universal key) |
|---|---|---|
| url | Absolute provider URL (api.anthropic.com, aws-external-anthropic, openai/azure, aiplatform) | Relative path: /chat/completions, /v1/messages, /models/gemini-*:generateContent |
| metadata | X_emergent_agent_name (EmergentAssistant 2.65M/day, OracleAgent 40k, SkilledAssistant 8k), X_emergent_iteration_number | X_emergent_run_id, X_emergent_request_id, X_emergent_model_name; no agent_name |
| run_id | Agent run id | '<job_uuid>_<app-defined session suffix>' (e.g. _task_focus, _v2) — UUID = app's job_id |
| headers | Provider SDK headers (X-Stainless-*, Anthropic-Version) | Ingress headers: X-Forwarded-For, Traceparent, Via; auth already swapped to provider service key at proxy |

### Production app volume distribution, 2026-06-11 (persistent cohort = active 06-08 AND 06-11)

| Segment | Apps | Calls on 06-11 |
|---|---|---|
| All persistent apps | 4,634 | 86,341 |
| >=10 calls/day | 2,408 | — |
| >=50 calls/day | 412 | 30,770 (36% of cohort volume) |
| >=100 calls/day (platform-wide incl. non-persistent) | 113 | 15,131 |
| >=1,000 calls/day | 0 | 0 |
| Busiest single app | 1 | 336 |
| Cohort median / p90 | — | 10 / 47 calls/day |

### Runtime model mix (15-min sample, 06-11 12:00-12:15 UTC, n=7,655)

| Model | Calls | Share |
|---|---|---|
| gemini-3-flash-preview | 3,555 | 46.4% |
| gpt-5-nano | 1,474 | 19.3% |
| gpt-5.2 | 1,297 | 16.9% |
| claude-haiku-4-5 | 737 | 9.6% |
| claude-sonnet-4-5 | 433 | 5.7% |
| claude-opus-4-5/4-6/4-7 | 89 | 1.2% |
| gemini-2.5-flash-lite + other | 70 | 0.9% |

### Implications

- The 'operate' business today is a long tail, not whales: ~4.6k recurring production apps but median 10 LLM calls/day, only ~400 apps with >=50 calls/day, and the busiest app does 336 calls/day. Operate-rails pricing should assume many low-volume apps (flat platform fee or generous included tier) rather than usage-tiered whale pricing — there are no whales yet.
- Zero 429s and <1% error rate mean rate-limiting/reliability is NOT the current pain; the near-term operate value props are visibility (per-app usage dashboards, spend attribution) and control (model switching, budget caps), all of which are immediately buildable since run_id already embeds the job UUID and apps already pass meaningful session names.
- 62% of top persistent apps run on custom domains and 58% are AI-keyword apps — the serious-operator segment exists and is identifiable today; a targeted beta list of the ~400 apps >=50 calls/day (or 113 >=100/day) can be generated directly from the proxy logs joined to deployer_db_data.
- Runtime traffic is growing ~10% over 4 days and is already 100% routed through the universal key proxy — the monetization/metering chokepoint is in place; what's missing is productization (usage UI, alerts, key rotation, per-end-user keys for builders who resell).
- Build-time testing dominates universal-key volume (85% of inbound calls come from same-day ephemeral jobs). Any 'production usage' metric or billing must use persistence/deployment joins, or it will overcount 14x (63.8k daily UUIDs vs 4.6k recurring apps).
- Runtime model mix skews heavily to cheap/fast models (gemini-3-flash + gpt-5-nano = 66%), suggesting builders optimize end-user cost; an operate feature exposing per-model cost/latency tradeoffs and automatic cheap-model routing aligns with observed behavior.
- 5-day log retention blocks any operate-analytics product and even internal trend tracking; ship a daily aggregate ETL (app_uuid x day x model x calls x errors) from the proxy DB to BigQuery before building anything else.

### Caveats

- 60-day trend was requested but is impossible from this source: llm_logs_partitioned retains only ~5 days (oldest populated partition 2026-06-08); a Grafana/Loki or BigQuery export would be needed for history.
- 'Production' is approximated as app UUIDs active on both 06-08 and 06-11 (3-day persistence). Multi-day build sessions can leak in; genuinely deployed apps with sporadic end-user traffic are missed. The 85%-deployed rate on the top-60 cross-check suggests the heuristic is reasonably precise at the head, less certain in the tail.
- Inbound classification = relative URL (url NOT LIKE 'http%'); a few hundred 'gemini://' scheme rows/day are included; some agent-less outbound rows (e.g. bedrock claude-haiku invocations, ~780k rows/day with null agent_name) were not classified and may include internal platform utilities.
- The proxy rewrites Authorization before logging (provider service-account keys visible, not the emergent universal key), so key-level attribution relies entirely on the run_id job-UUID embedding; per-user attribution requires the BigQuery join.
- Model mix is from a single 15-minute sample (n=7,655), not a full day; weekday-only window (Mon-Thu) may not reflect weekend traffic.
- Internal emergent.sh users could not be excluded inside DS 9 (no email column); the top-60 cross-check returned 60 distinct external-looking users, so head contamination appears low.
- Token volumes and runtime cost were not computed (response-body JSON parsing timed out at full-day scale; queries kept cheap per instructions). 06-12 was a partial day and excluded.


---

## competitors_builders

### Summary
Competitive teardown (mid-2026) of how app-builders serve users building AI products. Managed LLM keys for the BUILT app's runtime are now table stakes: Lovable (auto-managed LOVABLE_API_KEY, Gemini/OpenAI at provider cost), Replit (AI Integrations: 300+ models via managed credentials at public API price), Base44 (built-in InvokeLLM metered in integration credits), Vercel (AI Gateway, no markup, $5/mo free), and Firebase (AI Logic client SDKs, no client-side keys, billed to the user's own Blaze plan). Only Bolt.new still requires BYOK (secrets in Supabase edge functions). Integration marketplaces are converging on Stripe + auth + email/SMS, with Lovable the most consumer-polished (Stripe/Stripe Connect, Clerk, ElevenLabs voice, Twilio) and Replit the most automated (Stripe prod keys auto-wired at publish, RevenueCat for mobile). The big unsolved layer is 'operate your AI product': nobody offers turnkey end-user usage metering + resellable credits + billing rails for the builder's own customers (Base44's integration credits meter end-user actions but the builder cannot mark them up or resell them). Agent templates are nascent (Replit Agent 3 builds Slack/Telegram/scheduled automations; v0 says agents are 'coming in 2026'), WhatsApp is DIY-via-Twilio everywhere, and no competitor markets checkpointed/resumable generation. This maps cleanly to Emergent's stated user needs: parity on managed runtime LLM keys, differentiation on auth+billing+credits presets, WhatsApp-class channels, and production agent templates.

### Key numbers

- **Lovable AI free runtime allowance**: $1 of AI usage/month per workspace; thereafter pass-through at provider cost, unified in Lovable billing (402 error when balance depletes)
- **Replit AI Integrations model coverage**: 300+ models (OpenAI, Anthropic, Google, xAI, OpenRouter) with managed credentials, billed at public API price to Replit credits; paid plans only
- **Vercel AI Gateway free tier**: $5 AI Gateway credits/month, pay-as-you-go with no markup, budgets + fallbacks + usage monitoring built in
- **Base44 runtime metering**: 1 integration credit per end-user action (LLM call, image gen, email, SMS); free plan = 100 integration credits; paid $16–$160/mo
- **Bolt.new build pricing (runtime AI = BYOK)**: Free 1M tokens/mo, Pro $20/10M, Teams $50/seat/30M; built app's AI keys are user-supplied Supabase secrets
- **Firebase Studio**: Free for 3 workspaces (Premium 30); 60+ templates; runtime Gemini usage billed to builder's own Google Cloud Blaze account
- **Competitors with first-class WhatsApp channel for built AI apps**: 0 of 6 (all DIY via Twilio; Replit covers Slack/Telegram only)
- **Competitors with end-user billing/credit rails for the builder's customers**: 0 of 6 (closest: Base44 integration credits, not resellable; Replit/Lovable stop at Stripe wiring)

### AI-product affordances comparison (mid-2026)

| Capability | Lovable | Bolt.new | Replit (Agent 3) | Vercel v0 | Base44 | Firebase Studio |
|---|---|---|---|---|---|---|
| **AI/agent templates** | AI feature recipes (chat, doc Q&A, image gen) via prompt; no standalone agent templates | None first-party; prompt-driven | **Yes — Agent 3 builds agents/automations** (Slack, Telegram, email bots, scheduled workflows) with templates | AI chatbot + SaaS templates; agentic workflows announced for 2026 | None; prompt-driven with built-in InvokeLLM | **60+ templates** incl. Gemini API (Vite/Genkit/Flask) + App Prototyping agent |
| **Managed LLM key / bundled runtime inference** | **Yes** — auto-managed `LOVABLE_API_KEY`, routed via edge functions; Gemini 3 Flash default, GPT-5.5 Pro etc. | **No — BYOK** (e.g. `OPENAI_API_KEY` as Supabase secret for edge functions) | **Yes** — AI Integrations: Replit holds credentials for 300+ models, bills at public API price | **Yes** — AI SDK defaults to AI Gateway (hundreds of models, one endpoint, no key mgmt) | **Yes** — built-in LLM (auto-picks Claude Sonnet/Gemini Pro) metered in integration credits; BYOK optional | **Partial** — AI Logic client SDKs need no client key, but billing is builder's own Blaze/Cloud account |
| **AI SDK integrations** | OpenAI + Google native; others via API | Any via code (Claude powers build only) | OpenAI, Anthropic, Google, xAI, OpenRouter | OpenAI/Anthropic/Gemini + all majors via Gateway; AI SDK (TS) | OpenAI, Claude, Groq, Mistral via keys | Gemini-first via Genkit (TS/Go/Python/Dart) |
| **RAG / vector** | **Yes** — embeddings (Gemini Embedding, text-embedding-3) for semantic search/RAG | DIY (Supabase pgvector) | DIY in code; integrations help | Via marketplace: Upstash Vector, Neon, Supabase | No first-class primitive | Firestore vector search; AI Logic lacks embeddings generation |
| **Voice** | **Yes — ElevenLabs integration** (TTS, STT, Agents, Music/SFX) | DIY | Audio generation billed to credits | DIY via AI SDK | No (Twilio voice DIY) | Gemini multimodal/live via API |
| **Integration marketplace** | Premade: Stripe + **Stripe Connect**, Clerk, ElevenLabs, Twilio, PostHog | Stripe, Supabase (DB/auth), Netlify, GitHub, Figma — Supabase-centric | Stripe (prod keys auto-wired at publish), **RevenueCat** (mobile subs), Replit Auth, Slack, SendGrid, Firebase | Vercel Marketplace in v0 (Upstash, Neon, Supabase) + MCP (Stripe, Linear, Notion) — dev-grade | Built-in auth + DB + email/SMS/image-gen as credit-metered integrations; Twilio/Stripe via backend functions | Firebase Auth/Firestore + Extensions (incl. Stripe) — DIY assembly |
| **Runtime AI pricing model** | Bundled usage-based, provider cost, $1/mo free | BYOK — builder pays provider directly | Bundled pass-through at public API price (paid plans) | Gateway PAYG, no markup, $5/mo free credits | Integration credits (1/action), bundled in plan tiers | BYO Google Cloud billing (Blaze) |
| **Operate-your-AI-product features** | Workspace-level AI usage dashboard only | None | Stripe/RevenueCat monetization docs, Google Analytics; no end-user metering | Gateway budgets + usage monitoring (builder-level); Vercel analytics | **Integration credits implicitly meter end-user actions** — but not resellable/markup-able | AI Logic cost/usage monitoring, Firebase Analytics; no billing rails |

### Top 3 white-space gaps vs Emergent user needs

| # | White-space gap | Competitive evidence | Matching Emergent user need |
|---|---|---|---|
| 1 | **End-user monetization stack: metered credits + auth + billing presets.** Nobody lets a builder define credit packs, meter their end-users' AI consumption, and charge via Stripe out of the box. Base44 meters end-user actions but the credits belong to Base44's plan, not the builder's price list; Replit/Lovable stop at wiring a Stripe account. | Replit monetization docs = Stripe/RevenueCat only; Base44 integration credits non-resellable; Lovable tracks usage at workspace level only | auth+billing+credits presets; LLM key mgmt for deployed apps (parity + the missing markup/resell layer) |
| 2 | **Channels as deploy targets — especially WhatsApp.** Replit is alone in shipping Slack/Telegram agent automations; WhatsApp is DIY Twilio everywhere (Base44, Lovable). No platform treats 'deploy this AI agent to WhatsApp with managed numbers/templates' as a product. | Replit Agent 3 = Slack/Telegram/scheduled only; Base44/Lovable = Twilio backend functions DIY | Channels like WhatsApp |
| 3 | **Production agent templates + operate analytics.** Agent templates are embryonic (Replit automations are personal-workflow grade; v0 agents 'coming 2026'; Lovable/Base44 have none). And no one offers per-end-user AI usage analytics for the deployed product, nor checkpointed/resumable generation as a trust feature for long agent builds. | v0 blog: agentic workflows announced, not shipped; Firebase templates are starter code, not operated agents; zero competitors market checkpointed generation | Agent templates; checkpointed generation; usage analytics for the builder's own customers |

### Implications

- Managed LLM keys for deployed apps are now table stakes (5 of 6 competitors ship it) — Emergent should treat this as urgent parity work, priced at provider cost like Lovable/Replit/Vercel, not as a differentiator.
- The clearest differentiation is the 'operate' layer: ship auth + billing + resellable credit packs as a preset, so a builder can meter and charge THEIR end-users for AI usage in one prompt. No competitor does this; it directly monetizes Emergent's existing strength in deployed full-stack apps.
- WhatsApp-as-deploy-target is an open lane: Replit validated channel demand with Slack/Telegram, but WhatsApp (the highest-volume consumer channel) is DIY everywhere. Managed WhatsApp numbers + templates + webhook plumbing would be a first.
- Agent templates should be 'operated products', not starter code: bundle template + managed inference + channel + billing preset (e.g. 'WhatsApp support agent with credit billing') to leapfrog Replit's personal-automation framing.
- Checkpointed generation is unclaimed messaging space — no competitor markets resumable/safe long-running builds; pair it with cost transparency to counter the token-anxiety complaints visible in Bolt/Replit pricing reviews.
- Sources: https://docs.lovable.dev/integrations/ai, https://lovable.dev/blog/lovable-cloud, https://lovable.dev/pricing, https://elevenlabs.io/blog/introducing-the-elevenlabs-lovable-integration, https://docs.lovable.dev/integrations/stripe, https://support.bolt.new/integrations/supabase, https://support.bolt.new/troubleshooting/integrations-issues, https://www.banani.co/blog/bolt-new-pricing, https://docs.replit.com/replitai/replit-ai-integrations, https://docs.replit.com/core-concepts/monetization, https://docs.replit.com/replitai/agents-and-automations, https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet, https://blog.replit.com/2025-replit-in-review, https://vercel.com/docs/ai-gateway, https://vercel.com/docs/ai-gateway/pricing, https://vercel.com/blog/introducing-the-new-v0, https://vercel.com/changelog/vercel-marketplace-integrations-now-available-in-v0, https://docs.base44.com/Integrations/AI-integrations, https://docs.base44.com/Integrations/Using-integrations, https://base44.com/pricing, https://www.nocode.mba/articles/base44-pricing, https://firebase.google.com/docs/studio, https://firebase.google.com/docs/studio/pricing, https://firebase.google.com/docs/ai-logic/pricing, https://firebase.google.com/docs/ai-logic/monitoring, https://cloud.google.com/blog/products/application-development/firebase-studio-lets-you-build-full-stack-ai-apps-with-gemini

### Caveats

- Research is web-based as of June 2026; several sources are third-party reviews (banani.co, nocode.mba, superblocks) whose pricing figures may lag official changes — verify exact tier numbers before publishing externally.
- Some model names in fetched docs (e.g. Lovable's 'Gemini 3 Flash', Bolt's 'Opus 4.6') come from vendor/review pages and could not be independently cross-verified.
- Bolt.new's lack of bundled runtime inference is inferred from its support docs (BYOK via Supabase secrets) and absence of contrary evidence; a managed-key feature could exist in beta without public docs.
- Firebase Studio is still partly in preview; its pricing (free Gemini quota during preview) is explicitly temporary.
- 'Operate your AI product' findings are negative claims (absence of features) — hardest to prove; a hands-on trial of each product would strengthen them.
- v0's agent capabilities are roadmap statements from Vercel's blog, not shipped product.


---

## competitors_agents

### Summary
Mid-2026 market scan of agent platforms and AI-SaaS boilerplates. Three headline findings. (1) The agent-platform market has split into three layers: workflow-automation incumbents bolting on agents (n8n, Make, Zapier — execution/task-metered, $0–$800/mo), no-code agent-employee platforms (Lindy, Relevance AI — credit/action-metered, $19–$299/mo), and developer agent infra (LangGraph Platform, CrewAI — per-node/per-execution, free OSS up to $60k+/yr enterprise), plus a voice-agent vertical (Vapi, Retell at ~$0.05–0.07/min platform fee, $0.13–0.31/min all-in). (2) OpenClaw (ex-Clawdbot/Moltbot, by Peter Steinberger, launched Nov 2025) became the fastest-growing OSS repo ever (~9k stars in 24h, 247k by Mar 2026): a self-hosted personal agent controlled through WhatsApp/Telegram/Slack/Discord/Signal/iMessage with a skills marketplace (ClawHub, ~4k skills), cron + 'heartbeat' proactive loops, and shell/file/browser/email tools. Its virality proved two things: chat-app-as-UI is the killer distribution surface, and proactive triggers (heartbeat) make agents feel 'alive'. But it also became 2026's first agent security crisis (≈12% of ClawHub skills malicious; 7.1% leak credentials; users individually manage $5–$3,600/mo LLM keys) — exactly the gaps a hosted platform can close. (3) The boilerplate market proves strong one-time willingness-to-pay ($199–$999) for pre-wired blocks: auth, Stripe, credits/billing, chat UI, RAG, landing page, email. Emergent's unique wedge: it can generate the full-stack app + the agent + hosting + a universal LLM key in one prompt — collapsing what today requires an n8n sub + a boilerplate purchase + a Vercel deploy + per-provider API keys. Top proven template archetypes (detail in table 3): email triage, doc-QA/RAG support bot, WhatsApp/Telegram support agent, outreach autopilot, voice receptionist, social/content repurposer, meeting scheduler-recap, lead-research agent, personal heartbeat assistant, and data-analyst chat agent.

### Key numbers

- **OpenClaw GitHub stars (Mar 2026)**: 247,000 stars / 47,700 forks; 9k stars in first 24h, 100k by Feb 2
- **ClawHub skills marketplace**: ~3,984 skills; ~12% malicious (341, ClawHavoc campaign); 7.1% leak API keys/credentials (Snyk)
- **OpenClaw user LLM cost (self-managed keys)**: $5–$3,600/month depending on usage — software itself free
- **n8n cloud pricing**: €24/mo Starter (2,500 execs) → €60 Pro → €800 Business; self-host free; AI agent runs billed as normal executions
- **n8n template library**: 10,000+ workflows; >75% now use LLM integrations; AI fastest-growing category
- **Lindy pricing**: $19.99–$199.99/mo credit-metered; voice calls $0.19/min extra; 400+ native integrations, 1,000+ templates
- **Relevance AI**: Free → $19/mo Pro (30k actions/yr) → $234/mo Team; BYO API key bypasses vendor credits; 400+ agent templates
- **Zapier AI Agents**: 400 agent activities/mo free, 1,500 on Pro; Zapier Professional $29.99/mo (750 tasks)
- **LangGraph Platform**: Free dev tier (100k node execs/mo); Plus: $39/user/mo LangSmith + $0.001/node + $0.0036/min standby
- **CrewAI**: Free 50 execs/mo → $25/mo Pro (100 execs) → Enterprise est. $60k–$120k/yr
- **Voice agents (Vapi/Retell)**: Platform fee $0.05/min (Vapi) vs $0.07/min (Retell); all-in cost $0.13–$0.31/min for both
- **Boilerplate price points (one-time)**: ShipFast $199–$299; SaaS Pegasus $249–$999; supastarter ~$299–$349 lifetime; Makerkit $299
- **Enterprise agent adoption forecast**: Gartner: 40% of enterprise apps embed task-specific agents by end-2026, up from <5% in 2025

### Agent platforms — primitives, pricing, target user (mid-2026)

| Platform | Agent primitives (triggers / channels / tools) | Pricing | Target user |
|---|---|---|---|
| n8n | AI Agent node inside visual workflows; webhook/schedule/app triggers; vector stores (Pinecone, Qdrant, Supabase pgvector); native Claude/Gemini/OpenAI nodes; 10k+ templates | Self-host free; €24/€60/€800 per mo by executions; agent run = 1 execution + your LLM bill | Technical operators / automation engineers |
| Make | 3,000+ apps, visual scenario builder, Maia conversational builder, agent builder (beta); schedule + app-event triggers | Core ~$7.65/mo for 10k ops (can be 80% cheaper than Zapier) | SMB ops / no-code power users |
| Zapier | AI Agents + Copilot + MCP connectivity layered on 7k+ app triggers/actions | Free 400 agent activities/mo; 1,500 on Pro; base plans from $29.99/mo | Non-technical business users in SMB/mid-market |
| Lindy | 'AI employee' agents; email/calendar/schedule/webhook triggers; Computer Use (web navigation); phone numbers + voice; 400+ integrations, 4,000 via Pipedream | $19.99–$199.99/mo, credit-metered (1–10+ credits/task); voice $0.19/min + $10/mo per number | Founders, sales/support teams (no-code) |
| Relevance AI | Multi-agent 'AI workforce'; tools + knowledge (RAG) per agent; 400+ template marketplace (BDR outreach, research, content) | Free → $19/mo Pro → $234/mo Team; Actions + pass-through Vendor Credits; BYO API keys | Sales/ops teams, agencies building agent stacks |
| LangGraph Platform | Stateful graph agents; cron + API-invoked runs; one-click deploy, persistence, streaming endpoints; LangSmith observability | Free dev (100k node execs); $39/user/mo + $0.001/node + standby $0.0036/min; Enterprise custom | Developers/ML engineers shipping production agents |
| CrewAI | Crews (role-based multi-agent) + Flows; managed AMP cloud or self-hosted Factory; per-execution metering | OSS free; 50 execs/mo free cloud; $25/mo Pro; Enterprise ~$60k–$120k/yr | Python devs → enterprise platform teams |
| Vapi | Voice agent API: inbound/outbound calls, telephony, tool calls, BYO STT/LLM/TTS | $0.05/min platform + pass-through components; ~$0.13–$0.31/min all-in | Developers building voice products |
| Retell | Managed voice + chat agents, consolidated billing, $0.002+/msg chat agents | $0.07/min voice ($0.055 infra + components); ~$0.13–$0.31/min all-in | Teams wanting turnkey AI phone agents (receptionists, intake) |
| OpenClaw | Self-hosted personal agent: WhatsApp/Telegram/Slack/Discord/Signal/iMessage channels; shell/files/browser/email tools; skills (ClawHub, self-writable); cron + 30-min 'heartbeat' proactive loop | Free OSS; user pays own LLM API ($5–$3,600/mo) | Prosumers/hackers wanting a 24/7 personal AI on their own hardware |

### AI-SaaS boilerplate market — blocks bundled and price (proves WTP for premade blocks)

| Starter | Price (one-time) | Blocks bundled |
|---|---|---|
| ShipFast (Marc Lou) | $199 / $249 / $299 | Next.js; Google OAuth + magic-link auth; Stripe + Lemon Squeezy; MongoDB/Supabase; Mailgun/Resend email; landing page + SEO blog; unlimited projects |
| SaaS Pegasus (Django) | $249 / $449 / $999 | Auth, teams, subscriptions, e-commerce; AI app blocks: agents, tool use, image gen, LLM-agnostic chat UI, built-in chatbot |
| BuilderKit.ai | one-time (site: 'save 40+ hrs') | 17 pre-built AI apps; chat/text/image-gen modules; Supabase + Postgres; Stripe subscriptions; GPT-4/Claude/Llama/Mistral support; Vercel deploy |
| supastarter | ~$299–$349 lifetime | Next.js/Nuxt/SvelteKit; auth, payments, multi-tenancy, admin panel, i18n, AI integration/AI chatbot variant; unlimited projects |
| Makerkit | $299 lifetime (all kits) | Auth, billing, multi-tenant SaaS foundation across stacks |
| StartKit.AI | paid one-time | AI-wrapper-focused: chat, RAG, usage limits/credits, Stripe |

### Top 10 agent-template archetypes with proven demand (and where demand is evidenced)

| # | Archetype | Demand evidence |
|---|---|---|
| 1 | Email triage + auto-draft agent | Called 'the most common starter agent in 2026' (MoClaw); top n8n AI template category |
| 2 | Doc-QA / RAG knowledge bot | #1 n8n AI template class (KB chatbot w/ Pinecone/Qdrant/Supabase); SaaS Pegasus/StartKit ship RAG blocks |
| 3 | WhatsApp/Telegram support & personal agent | OpenClaw's entire viral loop = chat-app as agent UI; 280+ free n8n Telegram/WhatsApp templates |
| 4 | Outreach autopilot (BDR research → personalized sequences) | Relevance AI's flagship template category; HeyReach n8n template packs; Lindy sales agents |
| 5 | Voice receptionist / inbound call intake | Vapi/Retell whole category; Lindy charges $0.19/min voice premium; receptionist = canonical Retell use case |
| 6 | Social poster / content repurposer (blog → LinkedIn/X/newsletter) | Top-3 n8n AI template category; Relevance content-gen templates |
| 7 | Meeting scheduler + recap agent | Lindy core templates (meeting summaries ~2–5 credits); calendar triggers standard on all platforms |
| 8 | Lead/company research agent | Relevance 'prospect research' templates; Gumloop/Lindy research agents |
| 9 | Proactive personal assistant (morning briefing, monitors) | OpenClaw heartbeat pattern — 'wakes every 30 min, decides if anything matters' — widely copied/discussed |
| 10 | Data-analyst chat agent (talk to your GA/ads/DB) | Gumloop/n8n GA + Google Ads agent use cases; 'chat with your data' templates |

### Implications

- Ship an agent-template gallery mapped to the 10 proven archetypes. Every archetype above already has paid demand on n8n/Lindy/Relevance — Emergent can offer them as one-prompt full-stack apps (UI + DB + agent + hosting) instead of workflows trapped inside someone else's SaaS.
- Lean into 'OpenClaw, but hosted and safe.' OpenClaw proved demand for chat-channel agents with proactive heartbeat loops, but it ships with a security crisis (12% malicious skills, leaked keys) and a self-managed LLM bill. Emergent's hosted runtime + universal LLM key + curated tool blocks directly answers the three biggest OpenClaw pain points: setup, security, key management. (Emergent already ranks for 'what is OpenClaw' — emergent.sh/learn/what-is-openclaw — so capture that intent with a 'deploy your own' CTA.)
- Agent primitives to prioritize as platform features: (a) schedules/cron + heartbeat-style proactive triggers, (b) channel connectors (WhatsApp, Telegram, Slack, email, voice), (c) RAG/knowledge block, (d) credits/usage metering block. These are the primitives every competing platform monetizes.
- The boilerplate market proves $199–$999 one-time WTP for pre-wired auth + Stripe + credits + chat UI + RAG. Emergent can productize the same blocks as free/instant scaffolding to undercut starters, or as premium paid templates — either way it validates a paid template marketplace with rev-share for creators (Relevance: 400+ templates; n8n: 10k+).
- Pricing wedge: competitors meter executions/credits/actions on top of users' own LLM keys, creating two bills and bill-shock anxiety (Relevance even markets 'zero markup pass-through'). Emergent's universal LLM key bundled into one subscription is a genuine differentiator — market it as 'one bill, no API keys.'
- Voice is a premium-priced, underserved adjacency: $0.13–$0.31/min all-in economics mean a 'voice receptionist' template with bundled telephony could carry meaningful per-minute margin and targets non-technical SMBs that Vapi (dev-focused) ignores.

### Caveats

- Pricing figures are from third-party review/comparison sites (lindy.ai blog, checkthat.ai, pxlpeak, costbench, etc.) as much as vendor pages; tiers and credit rates change frequently — verify on vendor pricing pages before publishing externally.
- Some sources conflict: Lindy pricing is reported as both $19.99–$199.99 and $49/$299 tiers across reviews (likely plan rebrands mid-2025/26); CrewAI enterprise figures ($60k–$120k/yr) are third-party estimates, not a published rate card.
- supastarter.dev/pricing returned 404 on direct fetch; its ~$299–$349 lifetime price comes from secondary sources. BuilderKit's exact price was not retrievable from search results.
- OpenClaw is evolving fast (creator joined OpenAI Feb 2026; OpenClaw Foundation forming) — governance, security posture, and feature set may have shifted since the cited articles.
- Claim that users 'mass-installed' OpenClaw is from the task brief; internal install/usage telemetry was not checked in this scan.
- Top-10 archetype ranking is a synthesis from template-marketplace popularity and editorial round-ups, not quantitative download/revenue data per archetype.


---

## feasibility_codebase

### Summary
Feasibility sizing of 6 growth candidates against the Emergent monorepo. Headline: candidates 1, 2, and 5 are mostly content/config work on top of mature existing rails (template registry + restic snapshots, 91-playbook system, static badge HTML); candidate 3 (universal LLM key runtime for deployed apps) has surprisingly complete billing rails in integration-proxy (litellm key issuance, llmrouter proxy with auto-topup from integration_wallets into billing_ledger, budget GET/POST endpoints, GetModels) and mainly needs a public app-facing API surface + drop-in UI playbook; candidate 4 (checkpointed long-running job primitive for user apps) is the only true Large — nothing exists for user apps (cortex Temporal durability is platform-only; no CronJob/worker type in deployer's deployment generator); candidate 6 (ask-human/approval) has a complete platform-side HITL stack (ask_human tool, cortex builtin handling, interventions engine, auto-HITL service) but zero end-app primitive — a playbook-only version is Small, a hosted approval API is Medium. Note: integration-proxy providers confirmed are litellm, stripe, tigris, and ecubilling — suprsend does NOT appear anywhere in the codebase; user comms go RudderStack→MoEngage via pkg/comms.

### Key numbers

- **Integration playbooks already shipped (prompts/playbooks/*.md)**: 91 files / 88 registry entries in playbooks.yaml
- **WhatsApp/Twilio/Resend playbooks**: Already exist (BAILEYS_WHATSAPP.md, TWILIO_SMS.md, RESEND_EMAIL.md, SENDGRID.md)
- **LLM-integration playbook variants (chat, image, voice, video, files)**: 20+ (LLM_INTEGRATION_*, OPENAI_*, GEMINI_*, SORA_2, SUNO, ELEVENLABS)
- **Billing tables already live in integration-proxy**: 7 (integrations, integration_metrics, billing_tiers, integration_wallets, usage_records, billing_ledger, grace_periods)
- **Template env resolver types supporting an AI-SaaS template**: 4 (random_secret, random_hex, emergent_llm_key, job_context)
- **Playbook price already monetized per-use**: $1.50 typical playbook_price in playbooks.yaml
- **Candidates sized Small**: 3 of 6 (templates per-unit, new playbooks, white-label flag)
- **Candidates sized Large**: 1 of 6 (checkpointed long-running job primitive)

### Effort sizing summary

| # | Candidate | Effort | Services touched | Leverage level |
|---|-----------|--------|------------------|----------------|
| 1 | AI-product templates | **S per template / M for pack+gallery** | emergent (category_config row), GCS restic bucket, E1ectron (gallery surface) | Very high — full template pipeline exists |
| 2 | Premade integrations/playbooks | **S per playbook / M if metered** | prompts repo only (S); + integration-proxy seed rows (M) | Very high — 91 playbooks, registry, pricing field |
| 3 | Universal LLM key runtime block | **M** | integration-proxy (public API surface), prompts (playbook), E1ectron (settings) | High — billing/topup/models rails all exist |
| 4 | Checkpointed long-running job primitive | **L** | deployer (new manifest type), k8s, integration-proxy (billing), prompts | Low — nothing exists for user apps |
| 5 | White-label option | **S (honor-system) / M (enforced)** | app-builder templates, emergent (entitlement), deployer/CF worker if enforced | Medium — badge is static HTML, no entitlement system |
| 6 | Ask-human/approval UX for user apps | **S (playbook) / M (hosted API)** | prompts (S); + integration-proxy + notifications (M) | Medium — platform HITL complete, end-app primitive absent |

### Candidate 1 — AI-product templates: existing leverage

| Component | Location | What it does |
|---|---|---|
| Template launch flow | `emergent/app/service/template_service.py` (`start_from_template`, line 76) | Creates job from template; restic repo `gs:{TEMPLATE_RESTIC_BUCKET}:/templates/{name}`; supports per-template A/B (model+prompt swap) |
| Template registry | `category_config` Postgres table via `emergent/app/dal/default_repository.py` (`is_template_public`/`is_template_internal`, lines 75-90) | Row = template_name, config, default_env_config, env_resolver_config, public/internal flags |
| Secret auto-resolution | `emergent/agents/service/template_env_resolver.py` | Resolves `EMERGENT_LLM_KEY` (per-user LiteLLM key via IntegrationProxyClient), JWT secrets, job context into pod .env — exactly what a Claude-wrapper SaaS template needs |
| `is_template_enabled` | `emergent/app/service/job_service.py` lines 1893-1928 | Set from `is_public_template(env_image)` check on the env-image (base-image) template path — separate from code-first templates |
| Build pipeline | `.claude/skills/code-first-template/SKILL.md` + `prompts/prompts/code_first_template_full_stack_v1.md` | PRD→phased build→eval loop that produces template snapshots |
| Base env images | `app-builder/templates/` (farm, expo, nextjs, shadcn, trpc, remotion_video…) | Docker base images, not product templates |
| Plug-in point | Build the AI-SaaS app once (LLM chat + Stripe + credits via existing playbooks) → restic snapshot → insert category_config row with env_resolver_config → public=true | **No code changes to any service** |

### Candidate 2 — Integrations/playbooks: existing leverage

| Component | Location | Notes |
|---|---|---|
| Playbook corpus | `prompts/playbooks/` — 91 .md files | WhatsApp (Baileys), Twilio SMS, Resend, SendGrid, Stripe, PayPal, Razorpay, Paystack, Shopify, fal.ai, ElevenLabs, Suno, Sora-2… |
| Registry | `prompts/playbooks.yaml` (88 entries: description, file, integration_type, playbook_price, variables, testing_instructions) | Embedded into cortex via `prompts/embed.go` (go:embed) |
| Expert prompts | `prompts/prompts/integration_playbook_expert_prompt.md` (+ `auto_`, `anthropic_` variants; prompts.yaml line 819+) | Subagent that selects/applies playbooks |
| Legacy code playbooks | `emergent/agents/tools/impl/external_integration_tool.py` | Fetches `integration_playbook/{name}/playbook.py` from S3 |
| Managed-key billing | `integration-proxy/core/integrations` + schema 00007 seed rows | Tigris is the worked example of a fully metered integration |
| Adding e.g. Loops/Postmark | New .md + playbooks.yaml entry + cortex redeploy = **S**; with managed key + metering = seed integrations/metrics/tiers rows + provider collector = **M** | |

### Candidate 3 — Universal LLM key runtime: what exists vs missing

| Piece | Status | Location |
|---|---|---|
| Key issuance (litellm GenerateKey/UpdateKey) | EXISTS | `integration-proxy/core/llmkey/` + `pkg/litellm` |
| Key injected into app .env at job time | EXISTS | `template_env_resolver.py` (`emergent_llm_key` type); persists through deploy via deployer secrets (`deployer/core/secrets/`) — no deploy-time re-issuance found in deployer Go code |
| Runtime proxy + per-request budget check | EXISTS | `integration-proxy/core/llmrouter/` (LoggingTransport) |
| Auto-topup from wallet → litellm budget | EXISTS | `core/llmrouter/auto_topup.go` (MetricIDLiteLLMTopup → `billing_ledger`, idempotency-keyed) |
| Topup funding via Stripe webhooks + grace | EXISTS | `core/stripe/`, `core/billing/grace_engine.go`, `internal/billing/wallet_refiller.go` |
| Budget API | EXISTS (internal only) | `internal/httpapi/budget.go`: GET/POST `/user/{id}/budget` |
| Model list | EXISTS | `litellm.GetModels` via `core/llmkey/manager.go` |
| **Missing**: app-facing public endpoints (models + key health/balance), drop-in 'model picker + key health' UI component, playbook documenting it | GAP — the M work | New routes + auth for deployed-app callers; new playbook; optional E1ectron settings card |

### Candidates 4-6 — leverage and gaps

| Candidate | Exists | Gap | Effort rationale |
|---|---|---|---|
| 4. Checkpointed long-running job | Cortex Temporal workflows are durable/resumable (`cortex/core/workflows/` recovery.go, reset_manager.go, cancel_recovery.go) — platform-side only. Playbooks mention cron/celery ad hoc (ALPHA_VANTAGE, PAYPAL, SENDGRID, YOUTUBE). | No CronJob/worker/queue type in `deployer/core/deployment/generate.go`; user apps are web pods + CF Workers frontend (`deployer/core/deployer/deploy.go`). Minimal version = deployer-managed k8s CronJob type + manifest field + billing, or a hosted task-runner API + checkpoint-in-app-DB playbook. | **L** — new cross-service primitive (deployer manifest/k8s, billing, playbook, UI); conflicts with pod sleep/scale-down lifecycle |
| 5. White-label | Badge is static HTML `id="emergent-badge"` in `app-builder/templates/farm/frontend/public/index.html` (~line 64) and shadcn template, plus `assets.emergent.sh/scripts/emergent-main.js`; share-page branding in `E1ectron/src/routes/share-app.tsx`, `share-preview.tsx`. Subscription check pattern exists (`get_pro_and_subscription_status` in job_service.py). | No white-label entitlement anywhere; users can already hand-delete the badge. Honor-system pro flag + agent strips badge = S. Server-enforced injection (deployer/CF worker layer) = M. | **S/M** |
| 6. Ask-human/approval | Full platform HITL: `emergent/agents/tools/impl/ask_human.py`, cortex builtin handling (`cortex/core/comms/processor.go` lines 225-302), interventions engine (`cortex/core/interventions/`), `app/service/auto_hitl_service.py`, notification_service, websocket → E1ectron. | Nothing for END-USER apps. Playbook teaching apps to build approval-inbox on their own Mongo = S. Hosted approval API + notification channel (integration-proxy; comms is RudderStack→MoEngage only) = M. | **S/M** |

### Implications

- Fastest wins are content-shaped, not code-shaped: an 'AI SaaS starter' template (Claude-wrapper chat + credits + Stripe paywall) can ship with zero service changes — build once via the code-first-template skill, snapshot, add a category_config row. The env_resolver_config already auto-provisions the per-user EMERGENT_LLM_KEY, which is the hard part of an AI-SaaS starter on any other platform.
- The integration playbook system is a moat that's under-marketed: WhatsApp, Twilio, Resend, ElevenLabs, Sora-2, Suno etc. already exist with per-use pricing (playbook_price). A 'premade integrations' growth feature is largely packaging/discovery (surfacing playbooks in the UI before the user asks) rather than new engineering.
- Candidate 3 is the highest-leverage Medium: all metering/topup/grace rails exist in integration-proxy; exposing a public 'key health + model picker' API and a drop-in UI block would make deployed AI apps sticky (the app keeps billing through Emergent's universal key after deploy) — direct recurring-revenue mechanics.
- Candidate 4 (long-running checkpointed jobs) should be deprioritized or scoped down to a playbook-pattern ('checkpoint progress rows in your app DB + resume endpoint') before committing to a deployer-level primitive — the pod sleep/scale-down lifecycle makes a real primitive a Large cross-team effort.
- White-label is a classic monetization lever priced almost entirely by policy, not engineering — but since the badge is client-side HTML users can already remove, enforced white-label requires moving badge injection server-side (deployer/CF worker), so decide honor-system vs enforced before sizing the plan tier.
- Approval/ask-human for end-user apps pairs naturally with candidate 1: an 'AI agent with human approval' template would showcase a playbook-level approval inbox without any new platform primitive.

### Caveats

- Suprsend is NOT in the codebase — the task brief listed it as an integration-proxy provider, but grep finds zero references anywhere in mono; integration-proxy/pkg/comms ships events to RudderStack→MoEngage. Confirmed providers: litellm (llmkey/llmrouter), stripe (webhooks/funding), tigris (objstore), plus ecubilling.
- Two distinct 'template' systems coexist and are easy to conflate: (a) env-image base templates (app-builder/templates/ + user_env_image_template table + is_template_enabled flag in job_service.py) and (b) code-first product templates (restic snapshots + category_config table + start_from_template). Candidate 1 plugs into (b).
- Static analysis only — could not verify prod category_config rows, the litellm deployment config, or whether assets.emergent.sh/emergent-main.js re-injects the badge at runtime (script is external to the repo).
- Deployer secrets path inference: no EMERGENT_LLM_KEY handling found in deployer Go code, so the deployed app's key appears to ride along in the .env captured from the build environment; key rotation/re-issuance at deploy time looks absent (relevant to candidate 3 'key health').
- Effort sizes assume the existing teams' conventions (playbook markdown + yaml registry, category_config rows); they exclude marketing surface work (template gallery UI in E1ectron) unless noted.
- Playbook counts (91 files / 88 yaml entries) include some non-integration files (Guideline-*.md design guides are also in the playbooks dir and yaml).


---

## pricing_packaging

### Summary
Pricing/packaging evidence for AI builders (users with >=1 AI-keyword root job, Apr 1–Jun 12 2026; n=437,187 vs 2,057,267 non-AI builders; BigQuery DS7, internal users excluded). (1) AI builders subscribe at 2.2x the rate of non-AI builders (17.1% vs 7.7%) and skew 2x toward Pro among subscribers, but 82.9% still have no subscription. (2) They are heavy topup users: 5.5% ever topped up (vs 1.9%), and topups are 78.6% of all revenue from the cohort ($13.81M of $17.56M); median topup is just $20, with ~11 topup events per topping-up user — revenue arrives as many small friction-laden purchases, not committed plans. Revenue per cohort user: $40.17 (AI) vs $7.06 (non-AI), 5.7x. (3) The deploy-cost mismatch is structural: Standard grants a median 100 ECU/month (May 2026, 115,687 users), but a median deployed AI project consumes 199.4 ECU lifetime (p25=110, p75=557, p90=1,783; n=7,065 deployed AI projects) — i.e., ~2.0 Standard months; even the 25th-percentile deployed AI project overruns a full Standard month. Only Pro (750 ECU) comfortably covers it (median project = 27% of a Pro month). (4) Expansion is immediate after conversion: of AI-first-prompt users who converted within 24h (signups Apr 1–May 13), 20.46% topped up within 30 days of signup (vs 0.42% of AI-first non-converters — a 49x gap); AI-first users also convert within 24h at 8.5% vs 5.2% for non-AI-first. (5) Free-tier AI demand is large but unmonetized: 40.0% of AI root jobs (207,487 of 519,097) run on free_% prompts and deploy at 0.67%, vs 4.66% for paid-prompt AI jobs (7.0x). Net: the data supports an 'AI Builder' plan priced between Standard and Pro with ~250–300 ECU bundled (covering one shipped AI project per month), a ship-credit/deploy bundle at the moment of deployment, and auto-topup/usage commitments offered at first conversion.

### Key numbers

- **AI builders with root jobs Apr 1–Jun 12 2026**: 437,187 users (vs 2,057,267 non-AI builders)
- **Subscription rate (latest tier exists)**: AI 17.11% vs non-AI 7.72% (2.2x)
- **% on no subscription**: AI 82.89% vs non-AI 92.28%
- **Pro share among subscribers**: AI 6.6% vs non-AI 3.6% (~2x)
- **Ever topped up**: AI 5.53% (24,198) vs non-AI 1.92% (39,501)
- **Topups as % of cohort revenue**: AI 78.6% ($13.81M/$17.56M) vs non-AI 75.0% ($10.90M/$14.53M)
- **Median topup amount / events per topup user**: $20 both cohorts; AI ~11.2 events/user vs non-AI ~7.0
- **Revenue per cohort user (lifetime events)**: AI $40.17 vs non-AI $7.06 (5.7x)
- **Standard monthly ECU allocation (May 2026)**: median 100 ECU (115,687 users); Starter 50, Pro Lite 200, Pro 750
- **Median deployed AI project consumption**: 199.4 ECU = 199% of a Standard month (n=7,065; p25=110.2, p75=557.4, p90=1,783.3, avg=791.1)
- **AI-first 24h-converters who topped up within 30d**: 20.46% (3,193/15,608); non-converted AI-first: 0.42%
- **AI-first 24h conversion rate**: 8.45% vs 5.17% non-AI-first
- **AI root jobs on free prompts**: 39.97% (207,487/519,097)
- **Deploy rate: free vs paid prompt AI jobs**: 0.67% vs 4.66% (7.0x)

### 1. Latest subscription tier — AI vs non-AI builders (root jobs 2026-04-01..2026-06-12)

| Tier | AI builders | % | Non-AI builders | % |
|---|---|---|---|---|
| (no subscription) | 362,385 | 82.89% | 1,898,496 | 92.28% |
| Emergent Standard | 67,368 | 15.41% | 142,462 | 6.93% |
| Emergent Pro | 4,902 | 1.12% | 5,689 | 0.28% |
| Emergent Starter | 2,245 | 0.51% | 10,209 | 0.50% |
| Emergent Pro Lite | 286 | 0.07% | 411 | 0.02% |
| Total | 437,187 | 100% | 2,057,267 | 100% |

### 2. Topup behavior (lifetime revenue events for cohort users)

| Metric | AI builders | Non-AI builders |
|---|---|---|
| % ever topped up | 5.53% (24,198) | 1.92% (39,501) |
| Median topup amount | $20 | $20 |
| Topup events | 271,581 (~11.2/user) | 277,286 (~7.0/user) |
| Topup revenue | $13,805,517 | $10,899,134 |
| Total revenue | $17,562,362 | $14,525,967 |
| Topups as % of revenue | 78.6% | 75.0% |
| Revenue per cohort user | $40.17 | $7.06 |

### 3. Monthly ECU allocations (May 2026 grants) vs deployed AI project consumption

| Tier | Users granted (May) | Median monthly ECU | Median deployed AI project (199.4 ECU) as % of month |
|---|---|---|---|
| Emergent Starter | 7,677 | 50 | 399% |
| Emergent Standard | 115,687 | 100 | 199% |
| Emergent Pro Lite | 410 | 200 | 100% |
| Emergent Pro | 3,427 | 750 | 27% |

Deployed AI projects (deployed May 2026, n=7,065) lifetime ECU: p25=110.2, median=199.4, p75=557.4, p90=1,783.3, avg=791.1

### 4. Topup within 30d of signup, by first-prompt type and 24h conversion (signups 2026-04-01..2026-05-13)

| First prompt | Converted <24h | Users | Topup <30d | % |
|---|---|---|---|---|
| AI | Yes | 15,608 | 3,193 | 20.46% |
| AI | No | 169,018 | 708 | 0.42% |
| Non-AI | Yes | 61,681 | 12,500 | 20.27% |
| Non-AI | No | 1,132,552 | 3,305 | 0.29% |

### 5. Free vs paid prompt AI root jobs (2026-04-01..2026-06-12, project-level deploy via fork_chain)

| Prompt type | AI root jobs | Share | Deployed projects | Deploy rate |
|---|---|---|---|---|
| free_% | 207,487 | 39.97% | 1,383 | 0.67% |
| paid/other | 311,610 | 60.03% | 14,509 | 4.66% |

### Implications

- 'AI Builder' plan between Standard and Pro: Standard's 100 ECU covers only half a median deployed AI project (199 ECU), and even the p25 project (110 ECU) overruns it; Pro (750 ECU) overshoots by 3.8x. A ~250–300 ECU plan sized to 'ship one AI project per month' fills a real gap in the lineup and matches where AI builders already land (2x Pro skew shows willingness to pay up).
- Convert topup friction into committed MRR: 78.6% of AI-builder revenue arrives as topups, median $20, ~11 purchases per topping-up user — these users are repeatedly hitting paywalls mid-build. Offer auto-topup, a usage-commit discount, or larger bundled allocations at the first topup moment; predictable billing likely also reduces bad churn from bill shock.
- Ship-credit / success-based deploy bundle: deployment itself is already metered (DEPLOYMENT debits average ~57 ECU). Packaging a one-time 'ship credit' (e.g., deploy + first month of hosting/runtime inference) prices the moment of maximum perceived value and directly addresses the $111-to-deploy problem.
- Trigger expansion offers at 24h conversion: 20.5% of AI-first 24h-converters top up within 30 days (49x the non-converted rate) — the LTV expansion window opens immediately. Surface the AI Builder upgrade / auto-topup right after first payment, not later in lifecycle.
- Free-tier AI demand is a large unmonetized funnel: 40% of AI root-job attempts run on free prompts but deploy at only 0.67% (vs 4.66% paid). A deploy-gated upsell ('your agent works — ship it live with X ECU included') targets 207k attempts/quarter with a concrete value moment.
- Bundle runtime inference for AI products: AI builders' apps keep consuming LLM calls after shipping (UNIVERSAL_KEY platform-key debits already exist in the ledger). Including a monthly runtime-inference allowance in the AI Builder plan differentiates it from generic app plans and aligns price with the post-deploy cost curve that today shows up as p90 = 1,783 ECU projects.

### Caveats

- AI-keyword filter v1 has ~57% precision, applied to root-job task text only — AI-builder counts include false positives and miss users whose AI intent appears only in follow-up prompts.
- Plan mix uses the LATEST subscription_events row per user with no active-status filter — some 'tiered' users may have lapsed/cancelled; '(no subscription)' = no subscription_events row ever.
- Q3 deployed-AI-project cohort = deployments created May 2026 with AI root jobs created Apr 1–May 31; ECU = SUM of all credit_ledger DEBITs (LLM_CALL, TOOL_CALL, ENV_CREATION, DEPLOYMENT) tied to chain job_ids Apr 1–Jun 12, deduped by ledger id. Consumption after Jun 12 not counted (right-censored), so true lifetime consumption is higher.
- No clean ECU→USD conversion exists in these tables; the '$111-to-deploy' figure was not independently re-derived — the 199-ECU median vs 100-ECU Standard month is the apples-to-apples comparison.
- Topup metrics (Q2) are lifetime user_revenue_events for cohort users, not restricted to the Apr–Jun window; cohort membership itself is window-based.
- Q4 window (signups Apr 1–May 13) guarantees a complete 30d topup window; converted_within_24h covers any conversion, not necessarily AI-related spend.
- Several queries exceeded Redash's 60s adhoc timeout (jobs_full_view federates to a Postgres read replica); Q3 was narrowed to May 2026 deployments as a representative month rather than the full Apr–Jun window.
- Deploy rate counts a project as deployed if ANY job in its fork chain has a deployer_db_data row (any status, not only verified).


---

## adversarial_check

### Summary
Adversarial re-derivation of 4 headline claims (jobs 2026-03-14..2026-06-12, trajectories DATE>=2026-03-14, exclusions applied). (1) CONFIRMED with definitional caveat: AI jobs = 18.47% of jobs and 51.07% of 90d spend — but ONLY when each job is classified by its OWN task; under the documented ROOT-task rule it falls to 16.0% of jobs / 27.6% of spend. Confound is real but partial: AI jobs are 2.98x longer (123.0 vs 41.3 steps/job) AND 1.55x costlier per step ($0.726 vs $0.470); ~71% of the log cost-per-job gap is length, ~29% is per-step intensity. (2) CONFIRMED: project-level deploy rate 3.01% AI vs 1.77% non-AI; free-tier mix is NOT the confound (AI projects are actually less free-prompt: 29.3% vs 33.0%); within paid prompts the gap persists at 3.97% vs 2.40% (1.65x). (3) CONFIRMED: AI-first-prompt users convert 8.84% vs 5.32% within 24h (1.66x). Device confound exists (AI-first users are 55.0% desktop vs 36.7%) but explains a minority: Desktop-only gap is 10.34% vs 8.17% (1.27x), and the lift is even larger ratio-wise on mobile (Mobile Web 7.11% vs 3.80%); device-mix-adjusted lift ~1.55x. (4) WEAKENED: the 2.9x reproduces (51.05% AI share among universal-key users vs 18.20% all builders = 2.80x) but is substantially a denominator artifact — universal-key users average 3.3 jobs vs 1.5; against the fairer >=3-job baseline (35.72% AI) the multiplier drops to 1.84x (UK 3+ users are 65.80% AI), i.e. roughly half the headline multiplier comes from activity level, not AI-ness.

### Key numbers

- **C1: AI job share (own-task classification, jobs 3/14-6/12)**: 18.47% (867,843 / 4,697,749)
- **C1: AI spend share (90d, SUM value_in_usd)**: 51.07% ($77.54M / $151.84M)
- **C1: spec-correct ROOT-task variant**: 16.05% of jobs, 27.61% of spend ($41.93M)
- **C1: steps/job AI vs non-AI**: 123.0 vs 41.3 (2.98x)
- **C1: cost/step AI vs non-AI**: $0.7262 vs $0.4698 (1.55x)
- **C2: project deploy rate AI vs non-AI**: 3.01% (21,300/708,759) vs 1.77% (67,578/3,814,745)
- **C2: free-prompt share AI vs non-AI**: 29.3% vs 33.0% (AI less free, not more)
- **C2: paid-prompt-only deploy rate**: AI 3.97% vs non-AI 2.40% (1.65x)
- **C3: 24h conversion AI-first vs non-AI-first**: 8.84% (34,102/385,812) vs 5.32% (125,008/2,350,083)
- **C3: desktop share AI-first vs non-AI-first**: 55.0% vs 36.7%
- **C3: Desktop-only conversion**: AI 10.34% vs non-AI 8.17% (1.27x)
- **C4: AI share universal-key users vs all builders**: 51.05% vs 18.20% = 2.80x (claim said 2.9x)
- **C4: fairer baseline (>=3 jobs)**: UK 3+ users 65.80% vs all 3+ users 35.72% = 1.84x

### Verdicts summary

| # | Claim | Re-derived | Verdict | Confound finding |
|---|-------|-----------|---------|------------------|
| 1 | AI = 18.5% of jobs, 51.1% of 90d spend | 18.47% / 51.07% (exact match, own-task classification) | CONFIRMED (with caveat) | Mostly length: AI jobs 2.98x more steps; but cost/step also 1.55x higher, so not purely length. Under ROOT-task spec: only 27.6% of spend |
| 2 | AI deploy 3.0% vs non-AI 1.8% | 3.01% vs 1.77% (project-level, root-task) | CONFIRMED | Free-tier mix is NOT the explanation — AI projects are less free (29.3% vs 33.0%); paid-only gap 3.97% vs 2.40% (1.65x) survives |
| 3 | AI-first users convert 8.8% vs 5.3% | 8.84% vs 5.32% | CONFIRMED | AI-first users are much more desktop (55% vs 37%), but gap persists within every device: Desktop 1.27x, Mobile Web 1.87x, Mobile App 2.03x; mix-adjusted lift ~1.55x |
| 4 | Universal-key users 2.9x more AI | 2.80x (51.05% vs 18.20%) | WEAKENED | Denominator artifact confirmed: UK users avg 3.3 jobs vs 1.5; vs >=3-job baseline multiplier drops to 1.84x (65.80% vs 35.72%) |

### Claim 1 detail — jobs created 2026-03-14..2026-06-12, own-task classification

| Segment | Jobs | Spend (USD) | Steps | Cost/step | Steps/job | Cost/job |
|---|---|---|---|---|---|---|
| AI | 867,843 (18.47%) | $77,543,260 (51.07%) | 106,777,963 | $0.7262 | 123.0 | $89.35 |
| Non-AI | 3,829,906 (81.53%) | $74,297,878 (48.93%) | 158,154,135 | $0.4698 | 41.3 | $19.40 |
| Ratio | — | — | — | 1.55x | 2.98x | 4.61x |

### Claim 2 detail — projects (root jobs) created in window, root-task classification

| Segment | Projects | Deployed | Deploy rate | Free-prompt share | Paid deploy rate | Free deploy rate |
|---|---|---|---|---|---|---|
| AI | 708,759 | 21,300 | 3.01% | 29.3% | 3.97% (19,917/501,166) | 0.67% (1,383/207,487) |
| Non-AI | 3,814,745 | 67,578 | 1.77% | 33.0% | 2.40% (61,394/2,556,682) | 0.49% (6,184/1,257,779) |

### Claim 3 detail — signups 2026-03-14..2026-06-12 with complete 24h window, first-job task classification

| Device | AI-first users | AI conv % | Non-AI users | Non-AI conv % | Lift |
|---|---|---|---|---|---|
| Desktop | 212,042 | 10.34% | 861,779 | 8.17% | 1.27x |
| Mobile Web | 133,381 | 7.11% | 1,063,515 | 3.80% | 1.87x |
| Mobile App | 36,639 | 6.70% | 400,769 | 3.30% | 2.03x |
| Tablet | 3,750 | 6.35% | 24,020 | 4.07% | 1.56x |
| ALL | 385,812 | 8.84% | 2,350,083 | 5.32% | 1.66x |

### Claim 4 detail — user-level AI = any AI root job in window; UK = any UNIVERSAL_KEY debit in window

| Segment | Users | AI users | AI share | Avg jobs |
|---|---|---|---|---|
| All users with jobs | 3,177,764 | 578,251 | 18.20% | 1.5 |
| Universal-key users | 115,878 | 59,151 | 51.05% | 3.3 |
| All users >=3 jobs | 277,976 | 99,297 | 35.72% | 4.5 |
| UK users >=3 jobs | 35,614 | 23,435 | 65.80% | 7.7 |

### Implications

- The economics story survives red-teaming but should be re-worded: AI builders are not just 'expensive users' — they run jobs 3x longer AND pay 1.55x more per step, i.e. they are the deepest-engagement segment; pricing/credit packaging for long-running AI builds is the lever, not per-step margin.
- Quote the spec-correct root-task numbers (16% of projects, ~28% of spend) in external decks; the 51% figure depends on a classification choice that inflates AI spend share and is fragile under scrutiny.
- The AI deploy-rate advantage is genuine and not a paid-mix artifact — AI builders ship more even within paid prompts (3.97% vs 2.40%), strengthening the case for AI-product-specific deploy features (LLM-key provisioning at deploy time, agent hosting).
- The conversion lift for AI-first users is real on every device and largest ratio-wise on mobile (1.9-2.0x vs 1.27x desktop) — AI-intent onboarding flows should not be desktop-only; mobile AI-intent users are an underexploited conversion pocket.
- Downgrade the universal-key talking point from 2.9x to ~1.8x activity-adjusted; the honest framing is 'among equally active builders, universal-key users are still ~2x as likely to be building AI products', which still justifies investing in the universal key as an AI-builder retention hook (UK 3+ users average 7.7 jobs vs 4.5).

### Caveats

- Claim 1's headline (18.5%/51.1%) reproduces ONLY when each job is classified by its OWN task; the stated AI-filter spec says apply to ROOT job task only, under which the numbers are 16.0% of jobs / 27.6% of spend. The original analysis appears to have deviated from its own spec; follow-up messages mentioning AI keywords inflate the spend share.
- AI keyword filter v1 has ~57% precision, so absolute AI shares are overstated everywhere; relative comparisons assume false positives behave like true negatives.
- Spend = SUM(trajectories.value_in_usd) = internal model-cost units (~$151.8M over 90d), not revenue; treat shares, not dollar levels, as meaningful.
- Claim 2 deploy set derived from a lean EXTERNAL_QUERY (deployments JOIN apps) because analytics.deployer_db_data view consistently timed out (>60s federated query); this omits unlinked-custom-domain-only apps, a negligible sliver. Deploys are mapped to projects via fork_chain.
- Claim 4 multiplier came out 2.80x vs claimed 2.9x — within definitional wiggle room (e.g. exact UK-user window or AI-user definition); treated as a successful reproduction.
- Universal-key usage can itself be downstream of building an AI app (the key powers in-app LLM calls), so even 1.84x is correlation between two measures of the same behavior, not independent evidence.
- ~400 jobs with NULL task and ~390 jobs with NULL prompt_name excluded from respective denominators; immaterial.
- Job costs include trajectory rows dated after job creation through 2026-06-12; jobs created near window end have truncated cost accrual (affects both segments equally).
