# FinSentry

A team of AI agents in Discord that guard your cloud spending, ask for permission, and fix waste.

---

## Why we built this

Every company using AWS wastes money on cloud bills. People spin up test servers for a project, forget to delete them, leave unattached storage volumes sitting around, and provision oversized staging databases. 

The problem is that engineers live in Discord or Slack, not in the AWS Cost Explorer console. By the time finance notices the spike at the end of the month, thousands of dollars are already gone.

We built **FinSentry** to bring cloud cost monitoring directly into team chat. Instead of a lone dashboard nobody checks, four AI teammates run in your Discord channel, investigate waste together, verify that downsizing won't break your apps, and apply the fix when you give the green light.

---

## How it works

The workflow runs entirely inside a Discord channel (`#finops-staging-us-east-1`):

1. **`@auditor` spots the spike:** Notices that staging spend jumped by $18,400/month over baseline and alerts the team.
2. **`@metrics` checks the data:** Pulls CloudWatch and Datadog stats to see what is actually being used. Finds 18 unattached EBS disks (0 activity), 12 idle Kubernetes nodes (4% CPU), and 4 oversized RDS databases.
3. **`@coder` prepares the fix:** Writes the Terraform right-sizing code, sets up automated backup snapshots for the disks before deleting them, and posts an approval card in chat.
4. **`@dev` safety check:** Checks Kubernetes pod allocations to make sure downsizing from 16 to 4 nodes won't crash any running services. Confirms 42.5% headroom buffer remaining.
5. **Human approval:** The lead engineer types `@coder approve all`. Coder applies the changes, deletes the orphaned volumes, and confirms the bill dropped back to normal.

---

## Live AWS Console

The repo includes a local mock AWS dashboard (`mock-aws-console/`) so you can watch changes happen in real time:

- **Before:** Spend shows **$42,600 / month**, amber alert banner, 18 unattached storage volumes.
- **After approval:** When `@coder` runs the remediation, spend drops to **$24,200 / month**, saving **$18,400/mo ($220,800/yr)**, and the dashboard turns green.

---

## Project Structure

```text
finsentry/
├── README.md                                  # You are here
├── workflows/
│   ├── finops-cost-optimizer.template.yaml    # Switch agent workflow definition
│   └── teammate-dev-agent.template.yaml       # Dev advocate agent definition
└── mock-aws-console/
    ├── mock_aws_server.py                     # Local mock AWS API server (port 8088)
    └── dashboard.html                         # Real-time browser console
```

---

## How to run it locally

### 1. Start the mock AWS dashboard
```bash
cd mock-aws-console
python mock_aws_server.py
```
Open [http://localhost:8088/dashboard](http://localhost:8088/dashboard) in your browser.

### 2. Run the Switch workflow
```bash
switch template apply workflows/finops-cost-optimizer.template.yaml
```

### 3. Test in Discord
In your channel, type:
```text
@auditor run weekly finops audit for staging-us-east-1
```
After the agents inspect the metrics and `@dev` gives the green light, approve the changes:
```text
@coder approve all. Execute the remediation and tag auditor for verification.
```
Watch the dashboard at `http://localhost:8088/dashboard` update to green in real time.

---

## Voice dictation (Wispr Flow)

You can also run this completely hands-free using Wispr Flow. Instead of typing the commands, press your Wispr shortcut and speak:
- *"At auditor run weekly finops audit for staging-us-east-1"*
- *"At coder approve all. Execute the remediation and tag auditor for verification."*

---

## License

Apache 2.0
