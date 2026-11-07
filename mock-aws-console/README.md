# ☁️ Mock AWS Management Console & Live FinOps Simulation Engine
> **Zero-Dependency High-Fidelity AWS Simulation for the Flip the Switch Hackathon**

This directory provides a **Mock AWS Cloud & Telemetry Engine** built entirely on Python's standard library. It renders an authentic, pixel-perfect **AWS Management Console (AWS Cloudscape Light Mode `#f2f3f3` / `#ffffff` with Squid Ink `#161e2e` Navigation Bar & Dark Mode Toggle)** and exposes full REST APIs for AWS Cost Explorer, CloudWatch telemetry, EC2/EBS storage, and CloudShell terminal.

Teammates and hackathon judges can open the interface in any web browser and watch the cloud spend drop from **$42,600/mo to $24,200/mo in real-time** as Switch agents work — **without incurring real AWS charges or requiring cloud credentials**!

---

## 🎨 Authentic AWS Cloudscape Design System (`https://cloudscape.design`)

The dashboard replicates the official **AWS Management Console (Cloudscape Design System - Light Theme Default)**:

1. **Official Cloudscape Visual Refresh Tokens:**
   - **Container Border Radius:** 16px (`--aws-border-radius-container: 16px;`) on all cards, charts, and table containers.
   - **Color Palette:** Authentic light canvas (`#f2f3f3`), pure white surface (`#ffffff`), border lines (`#eaeded` / `#d5dbdb`), Squid Ink header (`#161e2e`), AWS Smile orange (`#ff9900` / `#ec7211`).
   - **Typography:** Amazon Ember typography hierarchy, heading font-weights, and secondary label sizing.

2. **Official Cloudscape Status Indicators (`awsui-status-indicator`):**
   - Replaced generic badges with authentic inline Cloudscape Status Indicators with SVG iconography:
     - 🟢 **Success:** Circular green checkmark (`#00802f`) for `Optimal`, `Baseline`, `Running`, `Completed (100%)`.
     - 🟡 **Warning:** Amber triangle with exclamation (`#855900`) for `Action Required`, `12 Idle Nodes`, `Downsize Opportunity`.
     - 🔴 **Error:** Red circular exclamation mark (`#d13212`) for `Over Budget`, `18 Orphaned Volumes`.
     - 🔵 **In-Progress:** Circular spinning SVG indicator (`#006ce0`) during remediation.

3. **Cloudscape Collection Preferences Modal (`⚙️ Preferences`):**
   - Gear icon button in table headers opens a modal allowing users to customize:
     - **Page Size:** 10, 25, or 50 resources per page.
     - **Content Density:** Comfortable vs. Compact view.
     - **Text Wrapping:** Toggle line wrapping inside table data cells.

4. **Multi-Select Batch Remediation Toolbar:**
   - Checkboxes on the Orphaned EBS Volumes table with an active blue selection banner (`#eff6ff` / `#1e40af`) calculating instantaneous savings for selected items.

5. **Cloudscape Confirmation Modals & Toast Flashbars:**
   - Action confirmation dialogs for single and batch operations.
   - Stacked toast notifications with automatic dismissal.

6. **AWS CloudShell Drawer & 6-Month Stacked Spend Graph:**
   - Slide-up terminal drawer supporting interactive CLI queries (`aws ce get-cost-and-usage`, `aws ec2 describe-volumes`, `remediate all`).
   - SVG stacked bar chart visualizing monthly costs across EKS compute, RDS databases, EBS storage, and base infrastructure.

---

## 🌐 Public Sharing Tunnel

A live Cloudflare tunnel is running to allow instant sharing with teammates and judges without port forwarding:

- **Public URL:** [https://pink-walnut-flowers-celebration.trycloudflare.com/dashboard](https://pink-walnut-flowers-celebration.trycloudflare.com/dashboard)
- **Local URL:** [http://127.0.0.1:8088/dashboard](http://127.0.0.1:8088/dashboard)

---

## ⚡ Mock REST API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `GET /` or `/dashboard` | `GET` | Renders the AWS Management Console UI |
| `GET /api/state` | `GET` | Returns the complete real-time JSON cloud state (polled every 1.5s by UI) |
| `GET /aws/cost-explorer` | `GET` | Simulates AWS Cost Explorer spend report and budget baseline |
| `GET /aws/telemetry` | `GET` | Simulates Datadog & CloudWatch 30-day CPU/RAM utilization metrics |
| `GET /aws/ec2/volumes` | `GET` | Returns list of available unattached EBS storage volumes |
| `POST /api/remediate/volumes` | `POST` | Creates 18 snapshots and terminates orphaned volumes (-$2.4k/mo) |
| `POST /api/remediate/volume` | `POST` | Safely snapshots and terminates an individual volume by ID |
| `POST /api/remediate/terraform`| `POST` | Merges PR #482: rightsizes EKS (16➔4) and RDS (db.r6g.large) (-$16k/mo) |
| `POST /api/remediate/all` | `POST` | Executes all remediations at once (simulates `!approve all` in chat) |
| `POST /api/simulate` | `POST` | Triggers the complete autonomous multi-agent war room audit sequence |
| `POST /api/shell` | `POST` | Interactive AWS CloudShell command handler |
| `POST /api/reset` | `POST` | Resets the cloud environment back to initial over-budget outage state |
| `GET /aws/telemetry` | `GET` | Simulates Datadog & CloudWatch 30-day CPU/RAM utilization metrics |
| `GET /aws/ec2/volumes` | `GET` | Returns list of available unattached EBS storage volumes |
| `POST /api/remediate/volumes` | `POST` | Creates 18 snapshots and terminates orphaned volumes (-$2.4k/mo) |
| `POST /api/remediate/terraform`| `POST` | Merges PR #482: rightsizes EKS (16➔4) and RDS (db.r6g.large) (-$16k/mo) |
| `POST /api/remediate/all` | `POST` | Executes all remediations at once (simulates `!approve all` in chat) |
| `POST /api/reset` | `POST` | Resets the cloud environment back to initial over-budget outage state |

---

## 🚀 How to Run in 2 Seconds

### 1. Launch the Mock AWS Console:
```powershell
python hackathon-showcase/workflows/finops-cost-optimizer/demo/mock_aws/mock_aws_server.py
```
Open your browser to: **`http://localhost:8088/dashboard`**

### 2. Trigger the Autonomous Multi-Agent Audit:
In a second terminal window (or triggered from Discord via webhook):
```powershell
python hackathon-showcase/workflows/finops-cost-optimizer/demo/simulate_finops_audit.py
```

### 3. Watch Live Real-Time Reaction:
As `@auditor`, `@metrics`, `@coder`, `@dev`, and human teammates (@Sarah Chen, @Marcus Vance, @Elena Rostova) approve the remediation:
- The AWS banner turns from amber **Warning** to emerald **Success**.
- The spend counter drops smoothly from **$42,600** to **$24,200**.
- The realized annual savings ticks up to **+$220,800/yr**.
- 12 idle EKS worker instances transition to `terminated`.
- 18 safety snapshots populate in the Snapshots tab.
- 0 page reload / 0 screen flicker (smooth DOM updates via background fetch).
