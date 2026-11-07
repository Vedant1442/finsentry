# 📝 Flip the Switch Hackathon: Master Submission Handbook
> **Your Exact Copy-and-Paste Submission Guide for DevTools Academy & WeMakeDevs**
> **Deadline:** November 7, 2026 at 11:59 PM IST

---

## 1. Quick Submission Fields Checklist

| Form Field | Recommended Entry |
| :--- | :--- |
| **Project Name** | **Switch Sentry War Room & CreatorStudio** |
| **Tagline / Short Description** | Autonomous multi-agent swarms in Slack & Discord for zero-downtime incident response and voice-driven creative ideation, powered by Switch & Wispr Flow. |
| **Primary Track(s)** | Select both: **Track 1 (Best Business Workflow)** and **Track 2 (Best Personal or Creative Workflow)** |
| **Bounties / Side Tracks** | Select all: **Track 3 (Best Core Contribution)**, **Code with Wispr**, **Best Blog**, **#HowISwitch** |
| **Team Size** | **Up to 4 members permitted** by WeMakeDevs & DevTools Academy. You can submit with 3 teammates! |
| **Public Repository URL** | `https://github.com/Vedant1442/switch` *(or standalone repo)* |
| **Demo Video Link** | YouTube unlisted / Loom video link *(see 3-minute script below)* |
| **Blog Post Link** | Link to published post on Dev.to, Hashnode, or Medium *(content in `hackathon-showcase/blog/`)* |
| **Social Media Post Link** | Link to your Twitter/X thread or LinkedIn post *(content in `hackathon-showcase/social/`)* |
| **Wispr Flow Scorecard** | Screenshot file uploaded from `hackathon-showcase/wispr/` |

---

## 2. Long Description / Abstract (Copy & Paste)

```markdown
### What We Built
Software engineering and creative brainstorming are team sports, yet most AI tools force developers to work in isolation. 

With Switch, we turned everyday team chat platforms (Slack, Discord, Mattermost) into autonomous operational war rooms:

1. **Autonomous Cloud FinOps & Cost Optimization Room (Track 1 — Best Business Workflow):**
   A weekly automated FinOps audit in team chat that monitors multi-cloud spending, correlates telemetry across Datadog/CloudWatch, generates Terraform PRs, and reclaims $18,400/month ($220,800/year):
   - `@cost-auditor` monitors billing APIs (AWS, GCP, Azure) and detects spend spikes.
   - `@utilization-analyzer` correlates 30-day CPU/Memory metrics to identify 18 unattached EBS volumes ($2.4k/mo), 12 idle Kubernetes nodes at <5% CPU ($9.6k/mo), and 4 over-sized RDS Postgres instances ($6.4k/mo).
   - `@remediation-coder` opens Terraform PR #482, generates safe snapshot-before-delete CLI scripts, and drafts an interactive financial approval card.
   - **`@workload-advocate` (Developer's Agent):** Inspects staging CI/CD test queues and verifies pod bin-packing (42.5% headroom remaining) to ensure zero risk of pod eviction or developer velocity blockage.
   - **Cross-Team Collaboration:** The Lead Cloud Architect and Application Developer Lead both review the approval card in chat and approve via `!approve all`, realizing $220.8k/yr annualized savings with zero downtime.

2. **Incident Commander & Auto-Fix War Room (Track 1 — Best Business Workflow):**
   When an incident alert fires, an autonomous triad of agents springs into action inside Discord/Slack:
   - `@incident-investigator` parses error stack traces, executes `git blame`, and isolates the offending commit.
   - `@incident-repro` writes an isolated reproduction test in a sandbox and validates the bug with 100% fidelity.
   - `@incident-architect` implements the surgical patch, runs the test suite until 100% GREEN, and presents the Git diff to the human on-call lead.
   - The human lead confirms and deploys with a simple `!approve`. MTTR drops from 45 minutes to under 90 seconds.

3. **CreatorStudio BrainTrust (Track 2 — Best Personal/Creative Workflow):**
   A Discord/Telegram creative salon featuring 4 collaborating agents: Trend Scout (hooks), Devil's Advocate (ruthless critique), Script Architect (narrative drafting), and Visual Director (Midjourney prompts).

4. **Hands-Free Swarm Ops with Wispr Flow:**
   Every command across all workflows is voice-dictated at 160 WPM using Wispr Flow, removing keyboard friction during emergency incidents.

5. **26 Core Open-Source Contributions (Track 3):**
   To make Switch even more robust, we contributed 26 pull requests to `sandbox-quantum/switch`—including 10 enterprise service connectors (Supabase, Cloudflare, PagerDuty, GitLab, New Relic) and critical bridge fixes (Discord 2,000-char chunking, session security). All 26 PRs passed Socket Security, CLA, and Semgrep scans with 100% green status.
```

---

## 3. 3-Minute Demo Video Recording Script

> **Tips:** Record using OBS, Loom, or Screen Studio. Show Discord/Slack on one side of your screen and Switch Console / terminal on the other. Speak clearly using Wispr Flow!

| Timestamp | Screen Display | Narration / Action |
| :--- | :--- | :--- |
| **0:00 - 0:25** | Webcam / Discord channel `#finops-cost-optimizer` | "Hi everyone! I'm Vedant. Today, most AI assistants isolate you in an IDE. But real engineering happens in team chat. Today, I'm excited to present our **Autonomous Cloud FinOps War Room** and **CreatorStudio**, built with **Switch** and powered by **Wispr Flow**." |
| **0:25 - 1:15** | Discord showing weekly FinOps scheduled audit | Show `@cost-auditor` detecting the $18,400 monthly cloud spend spike.<br>Show `@utilization-analyzer` correlating Datadog metrics to 18 unattached EBS volumes, 12 idle K8s nodes (<5% CPU), and 4 over-provisioned RDS instances.<br>Show `@remediation-coder` opening Terraform PR #482 and posting the interactive Financial Approval Card. |
| **1:15 - 1:55** | Discord showing approval & execution | Show the Lead Cloud Architect confirming with `!approve all` (dictated via Wispr Flow!).<br>Show `@remediation-coder` merging the Terraform PR and running the snapshot-before-delete script, reclaiming $220,800/yr.<br>Quickly highlight the Incident Commander war room resolving a production 500 error under 90s. |
| **1:55 - 2:25** | Discord channel `#creator-braintrust` | Switch to the CreatorStudio channel.<br>*(Speak via Wispr Flow):* *"Team, give me 3 high-retention video angles on multi-agent systems."*<br>Show the Trend Scout proposing angles, Devil's Advocate critiquing the clichés, and Visual Director generating Midjourney prompts. |
| **2:25 - 2:45** | GitHub browser tab showing 26 PRs | "Finally, to give back to the open-source ecosystem, I authored and submitted **26 pull requests** to the Switch core repository—spanning 10 enterprise connectors and critical bridge stability fixes, all 100% green on CI." |
| **2:45 - 3:00** | Project README / Outro | "Thank you to WeMakeDevs, DevTools Academy, and Switch for hosting this hackathon. Check out our repository and let's flip the switch together!" |

---

## 4. Track 3 PR Submission Appendix

If the submission form asks for your PR numbers or links, paste this complete list:

1. **PR #1409:** `feat(connections): add Supabase service connector (#827)` — https://github.com/sandbox-quantum/switch/pull/1409
2. **PR #1400:** `feat(connections): add Cloudflare service connector (#828)` — https://github.com/sandbox-quantum/switch/pull/1400
3. **PR #1398:** `feat(connections): add PagerDuty service connector (#825)` — https://github.com/sandbox-quantum/switch/pull/1398
4. **PR #1389:** `feat(connections): add New Relic service connector (#823)` — https://github.com/sandbox-quantum/switch/pull/1389
5. **PR #1377:** `feat(connections): add Box connector (#832)` — https://github.com/sandbox-quantum/switch/pull/1377
6. **PR #1375:** `feat(connections): add Bitbucket service connector (#818)` — https://github.com/sandbox-quantum/switch/pull/1375
7. **PR #1374:** `feat(connections): add GitLab service connector (#816)` — https://github.com/sandbox-quantum/switch/pull/1374
8. **PR #1371:** `feat(connections): add Intercom service connector (#842)` — https://github.com/sandbox-quantum/switch/pull/1371
9. **PR #1369:** `fix(discord): record thread message map on root_id (#318)` — https://github.com/sandbox-quantum/switch/pull/1369
10. **PR #1368:** `fix(gateway): show actual key prefix instead of hash prefix (#455)` — https://github.com/sandbox-quantum/switch/pull/1368
11. **PR #1334:** `feat(connections): add ServiceNow connector investigation (#1175)` — https://github.com/sandbox-quantum/switch/pull/1334
12. **PR #1333:** `fix(rooms): validate visibility pair in create_room (#453)` — https://github.com/sandbox-quantum/switch/pull/1333
13. **PR #1332:** `fix(auth): derive session cookie max_age from JWT_EXPIRY_HOURS (#454)` — https://github.com/sandbox-quantum/switch/pull/1332
14. **PR #1331:** `fix(deeplinks): make switchdash scheme and host comparison case-insensitive (#471)` — https://github.com/sandbox-quantum/switch/pull/1331
15. **PR #1330:** `fix(claude): exclude connector MCP tools from sessionSettings allow list (#1103)` — https://github.com/sandbox-quantum/switch/pull/1330
16. **PR #1328:** `fix(mattermost): catch only not-found in get_external_user_id (#452)` — https://github.com/sandbox-quantum/switch/pull/1328
17. **PR #1325:** `fix(slack): include forwarded message content from share attachments (#1320)` — https://github.com/sandbox-quantum/switch/pull/1325
18. **PR #1319:** `feat(commands): add !get-document command (#1097)` — https://github.com/sandbox-quantum/switch/pull/1319
19. **PR #1318:** `feat(commands): add !briefing command (#706)` — https://github.com/sandbox-quantum/switch/pull/1318
20. **PR #1317:** `fix(mattermost): resolve reply to thread root (#1158)` — https://github.com/sandbox-quantum/switch/pull/1317
21. **PR #1316:** `feat(connections): add Zoom Meetings service connector (#1173)` — https://github.com/sandbox-quantum/switch/pull/1316
22. **PR #1315:** `feat(connections): add LaunchDarkly service connector (#1172)` — https://github.com/sandbox-quantum/switch/pull/1315
23. **PR #1314:** `feat(connections): add Grafana service connector (#826)` — https://github.com/sandbox-quantum/switch/pull/1314
24. **PR #1311:** `feat(connections): add Calendly service connector (#1147)` — https://github.com/sandbox-quantum/switch/pull/1311
25. **PR #1310:** `feat(connections): add Miro service connector (#1174)` — https://github.com/sandbox-quantum/switch/pull/1310
26. **PR #1284:** `fix(discord): stay under 2000 cap on long lines in code blocks (#1226)` — https://github.com/sandbox-quantum/switch/pull/1284
