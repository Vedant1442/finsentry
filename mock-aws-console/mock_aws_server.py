#!/usr/bin/env python3
"""
Mock AWS FinOps Environment & Real-time Live Dashboard.
Zero-dependency Python HTTP Server (runs on standard library).

Simulates:
1. AWS Cost Explorer API (monthly spend spikes & budget baselines)
2. AWS CloudWatch / Datadog Telemetry (CPU/RAM metrics & unattached volumes)
3. AWS EC2 Storage APIs (snapshotting and volume deletion)
4. Real-time HTML FinOps Dashboard with visual cost reduction feedback
"""

import http.server
import json
import os
import sys
import time
import urllib.parse
from datetime import datetime, timezone

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PORT = int(os.getenv("MOCK_AWS_PORT", 8088))
ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "assets"))

# In-Memory Cloud State
INITIAL_STATE = {
    "account_id": "1234-5678-9012",
    "environment": "staging-us-east-1",
    "budget_baseline": 24200,
    "current_monthly_spend": 42600,
    "unplanned_spike": 18400,
    "realized_monthly_savings": 0,
    "realized_annual_savings": 0,
    "eks_nodes": {
        "node_group": "staging-general-workloads",
        "instance_type": "m6i.2xlarge",
        "current_nodes": 16,
        "target_nodes": 4,
        "avg_cpu_percent": 4.2,
        "peak_ram_percent": 14.8,
        "monthly_waste": 9600,
        "remediated": False
    },
    "rds_instances": {
        "current_class": "db.r6g.2xlarge",
        "target_class": "db.r6g.large",
        "count": 4,
        "p95_cpu_percent": 6.1,
        "monthly_waste": 6400,
        "remediated": False
    },
    "volumes": [
        {"id": f"vol-0a{i:02d}b9c8d7e6f", "size_gb": 1660, "type": "gp3", "unattached_days": 24, "status": "available"}
        for i in range(1, 19)
    ],
    "snapshots": [],
    "audit_log": [
        {"timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S UTC"), "actor": "AWS EventBridge", "event": "Weekly FinOps Cron fired for staging-us-east-1"}
    ]
}

state = json.loads(json.dumps(INITIAL_STATE))

class MockAWSHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean terminal output
        return

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ("/", "/dashboard"):
            self._render_dashboard()
        elif path == "/api/state":
            self._set_headers()
            self.wfile.write(json.dumps(state).encode("utf-8"))
        elif path == "/aws/cost-explorer":
            self._handle_cost_explorer()
        elif path == "/aws/telemetry":
            self._handle_telemetry()
        elif path == "/aws/ec2/volumes":
            self._handle_volumes()
        elif path.startswith("/assets/"):
            rel = path[len("/assets/"):].replace("/", os.sep)
            file_path = os.path.join(ASSETS_DIR, rel)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                ctype = "image/png" if file_path.endswith(".png") else "image/jpeg" if file_path.endswith((".jpg", ".jpeg")) else "image/svg+xml" if file_path.endswith(".svg") else "application/octet-stream"
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Asset not found"}).encode("utf-8"))
        elif path == "/health":
            self._set_headers()
            self.wfile.write(json.dumps({"status": "healthy", "service": "Mock AWS FinOps Engine"}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/remediate/volumes":
            self._remediate_volumes()
        elif path == "/api/remediate/volumes/batch":
            self._remediate_batch_volumes()
        elif path == "/api/remediate/volume":
            self._remediate_single_volume()
        elif path == "/api/remediate/terraform":
            self._remediate_terraform()
        elif path == "/api/remediate/all":
            self._remediate_all()
        elif path == "/api/simulate":
            self._simulate_war_room()
        elif path == "/api/shell":
            self._handle_shell_command()
        elif path == "/api/reset":
            state.clear()
            state.update(json.loads(json.dumps(INITIAL_STATE)))
            self._record_log("Admin", "Reset environment back to initial unoptimized state")
            self._set_headers()
            self.wfile.write(json.dumps({"status": "reset_complete", "state": state}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Unknown POST route"}).encode("utf-8"))

    def _handle_cost_explorer(self):
        self._record_log("@auditor", "Queried AWS Cost Explorer API for trailing 30-day spend")
        response = {
            "account_id": state["account_id"],
            "period": "Trailing 30 Days",
            "budget_baseline": state["budget_baseline"],
            "current_spend": state["current_monthly_spend"],
            "variance": state["current_monthly_spend"] - state["budget_baseline"],
            "variance_percent": "+76.0%" if state["current_monthly_spend"] > state["budget_baseline"] else "0.0%",
            "top_cost_drivers": [
                {"service": "Amazon EC2 & EKS Worker Nodes", "amount": 16000, "status": "Spike"},
                {"service": "Amazon RDS PostgreSQL", "amount": 6400, "status": "Over-Provisioned"},
                {"service": "Amazon EBS Unattached Storage", "amount": 2400, "status": "Orphaned"}
            ]
        }
        self._set_headers()
        self.wfile.write(json.dumps(response, indent=2).encode("utf-8"))

    def _handle_telemetry(self):
        self._record_log("@metrics", "Cross-referenced CloudWatch & Datadog CPU/RAM metrics")
        response = {
            "eks_metrics": state["eks_nodes"],
            "rds_metrics": state["rds_instances"],
            "unattached_ebs_count": len(state["volumes"]),
            "unattached_storage_cost": len(state["volumes"]) * (2400 // 18) if state["volumes"] else 0
        }
        self._set_headers()
        self.wfile.write(json.dumps(response, indent=2).encode("utf-8"))

    def _handle_volumes(self):
        self._record_log("@coder", f"Listed available unattached EBS volumes (Count: {len(state['volumes'])})")
        self._set_headers()
        self.wfile.write(json.dumps({"volumes": state["volumes"]}, indent=2).encode("utf-8"))

    def _apply_volumes_remediation(self):
        count = len(state["volumes"])
        if count == 0:
            return 0
        for vol in state["volumes"]:
            state["snapshots"].append({
                "snapshot_id": f"snap-{vol['id'][4:]}",
                "source_volume": vol["id"],
                "created_at": datetime.now(timezone.utc).isoformat(),
                "retention": "30Days"
            })
        state["volumes"] = []
        state["current_monthly_spend"] -= 2400
        state["realized_monthly_savings"] += 2400
        state["realized_annual_savings"] += (2400 * 12)
        self._record_log("@coder", f"Created {count} safety snapshots & terminated {count} unattached EBS volumes (-$2.4k/mo)")
        return count

    def _apply_terraform_remediation(self):
        if state["eks_nodes"]["remediated"]:
            return False
        state["eks_nodes"]["current_nodes"] = 4
        state["eks_nodes"]["remediated"] = True
        state["rds_instances"]["current_class"] = "db.r6g.large"
        state["rds_instances"]["remediated"] = True
        state["current_monthly_spend"] -= 16000
        state["realized_monthly_savings"] += 16000
        state["realized_annual_savings"] += (16000 * 12)
        self._record_log("@coder", "Merged Terraform PR #482: Right-sized EKS to 4 nodes & downscaled RDS to db.r6g.large (-$16k/mo)")
        return True

    def _remediate_volumes(self):
        count = self._apply_volumes_remediation()
        self._set_headers()
        self.wfile.write(json.dumps({
            "status": "success" if count > 0 else "noop",
            "deleted_volumes": count,
            "created_snapshots": count,
            "monthly_savings": 2400 if count > 0 else 0
        }).encode("utf-8"))

    def _remediate_terraform(self):
        applied = self._apply_terraform_remediation()
        self._set_headers()
        self.wfile.write(json.dumps({
            "status": "success" if applied else "already_applied",
            "terraform_pr": "#482",
            "eks_nodes": 4,
            "rds_class": "db.r6g.large",
            "monthly_savings": 16000 if applied else 0
        }).encode("utf-8"))

    def _remediate_all(self):
        vol_count = self._apply_volumes_remediation()
        tf_applied = self._apply_terraform_remediation()
        self._record_log("@auditor", "Verified total infrastructure spend back to $24,200 baseline. Quarterly FinOps targets achieved.")
        self._set_headers()
        self.wfile.write(json.dumps({
            "status": "all_remediations_complete",
            "volumes_deleted": vol_count,
            "terraform_applied": tf_applied,
            "realized_monthly_savings": state["realized_monthly_savings"],
            "realized_annual_savings": state["realized_annual_savings"],
            "current_run_rate": state["current_monthly_spend"]
        }).encode("utf-8"))

    def _remediate_single_volume(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        try:
            req_data = json.loads(post_body.decode("utf-8"))
        except Exception:
            req_data = {}
        vol_id = req_data.get("volume_id")
        
        target = None
        for v in state["volumes"]:
            if v["id"] == vol_id:
                target = v
                break
        
        if not target and state["volumes"]:
            target = state["volumes"][0]
            vol_id = target["id"]

        if target:
            state["volumes"] = [v for v in state["volumes"] if v["id"] != vol_id]
            snap_id = f"snap-{vol_id[4:]}"
            state["snapshots"].append({
                "snapshot_id": snap_id,
                "source_volume": vol_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "retention": "30Days"
            })
            savings = round(2400 / 18)
            state["current_monthly_spend"] -= savings
            state["realized_monthly_savings"] += savings
            state["realized_annual_savings"] += (savings * 12)
            self._record_log("@coder", f"Safety snapshot {snap_id} created; purged orphaned EBS {vol_id} (-${savings}/mo)")
            self._set_headers()
            self.wfile.write(json.dumps({"status": "success", "volume_id": vol_id, "snapshot_id": snap_id}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Volume not found or already deleted"}).encode("utf-8"))

    def _remediate_batch_volumes(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        try:
            req_data = json.loads(post_body.decode("utf-8"))
        except Exception:
            req_data = {}
        volume_ids = req_data.get("volume_ids", [])
        if not volume_ids and state["volumes"]:
            volume_ids = [v["id"] for v in state["volumes"]]

        purged = []
        for vid in volume_ids:
            matching = [v for v in state["volumes"] if v["id"] == vid]
            if matching:
                purged.append(vid)
                state["snapshots"].append({
                    "snapshot_id": f"snap-{vid[4:]}",
                    "source_volume": vid,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "retention": "30Days"
                })
        
        if purged:
            state["volumes"] = [v for v in state["volumes"] if v["id"] not in purged]
            savings = round((2400 / 18) * len(purged))
            state["current_monthly_spend"] -= savings
            state["realized_monthly_savings"] += savings
            state["realized_annual_savings"] += (savings * 12)
            self._record_log("@coder", f"Batch snapshot & purge: {len(purged)} orphaned volumes terminated (-${savings}/mo)")
            self._set_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "purged_count": len(purged),
                "volume_ids": purged,
                "monthly_savings": savings
            }).encode("utf-8"))
        else:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "No valid volumes to purge"}).encode("utf-8"))

    def _simulate_war_room(self):
        """Simulate the complete autonomous multi-agent audit in sequence."""
        self._record_log("@auditor", "Initiated weekly FinOps spend audit: Detected +$18,400/mo spike across staging-us-east-1.")
        self._record_log("@metrics", "Correlated CloudWatch/Datadog: 18 unattached EBS disks, 12 idle EKS nodes (avg 4.2% CPU), over-provisioned RDS.")
        self._record_log("@coder", "Opened GitHub PR #482 (Terraform rightsizing) and prepared scripts/cleanup_orphaned_ebs.sh.")
        self._record_log("@dev", "Workload capacity verified: 38 pods safely accommodate 4 nodes with 42.5% buffer remaining.")
        self._record_log("Marcus Vance", "Engineering sign-off: Safe to proceed with zero dev velocity impact.")
        self._record_log("Elena Rostova", "Leadership sign-off: Approved $220.8k annualized savings for Q4 budget baseline.")
        self._record_log("Sarah Chen", "Lead Architect executed `!approve all` in Discord #finops-cost-optimizer.")
        vol_count = self._apply_volumes_remediation()
        tf_applied = self._apply_terraform_remediation()
        self._record_log("@auditor", "Post-remediation verification complete: spend restored to $24,200/mo baseline.")
        self._set_headers()
        self.wfile.write(json.dumps({
            "status": "simulation_complete",
            "volumes_deleted": vol_count,
            "terraform_applied": tf_applied,
            "realized_annual_savings": state["realized_annual_savings"]
        }).encode("utf-8"))

    def _handle_shell_command(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        try:
            req_data = json.loads(post_body.decode("utf-8"))
            cmd = req_data.get("command", "").strip()
        except Exception:
            cmd = ""

        output = ""
        c = cmd.lower()
        if c in ("help", "?"):
            output = (
                "AWS CloudShell (staging-us-east-1)\n"
                "Available commands:\n"
                "  aws ce get-cost-and-usage      Query Cost Explorer spend & budget baseline\n"
                "  aws ec2 describe-volumes       List unattached orphaned EBS storage volumes\n"
                "  aws eks describe-nodegroup     Check EKS worker nodes and target sizing\n"
                "  remediate volumes              Run safety snapshot & purge unattached disks\n"
                "  remediate terraform            Merge PR #482 (right-size EKS & RDS)\n"
                "  remediate all                  Execute full multi-agent remediation\n"
                "  reset                          Reset cloud state back to initial outage\n"
                "  clear                          Clear terminal window"
            )
        elif "get-cost-and-usage" in c or "cost-explorer" in c:
            output = json.dumps({
                "Dimension": "MONTHLY_SPEND",
                "Account": state["account_id"],
                "Region": state["environment"],
                "CurrentSpend": f"${state['current_monthly_spend']:,}",
                "BudgetBaseline": f"${state['budget_baseline']:,}",
                "Variance": f"+${state['current_monthly_spend'] - state['budget_baseline']:,}" if state['current_monthly_spend'] > state['budget_baseline'] else "$0",
                "RealizedAnnualSavings": f"+${state['realized_annual_savings']:,}"
            }, indent=2)
            self._record_log("CloudShell", "aws ce get-cost-and-usage executed via CloudShell")
        elif "describe-volumes" in c or "volumes" in c and not c.startswith("remediate"):
            v_list = state["volumes"]
            output = json.dumps({
                "Volumes": [
                    {"VolumeId": v["id"], "SizeGiB": v["size_gb"], "Status": v["status"], "UnattachedDays": v["unattached_days"]}
                    for v in v_list[:5]
                ],
                "TotalCount": len(v_list),
                "Note": f"{len(v_list)} unattached gp3 disks identified (>21 days inactive)" if v_list else "All orphaned volumes cleared"
            }, indent=2)
            self._record_log("CloudShell", "aws ec2 describe-volumes executed via CloudShell")
        elif "describe-nodegroup" in c or "eks" in c and not c.startswith("remediate"):
            output = json.dumps({
                "NodegroupName": state["eks_nodes"]["node_group"],
                "InstanceType": state["eks_nodes"]["instance_type"],
                "CurrentDesiredCapacity": state["eks_nodes"]["current_nodes"],
                "TargetCapacity": state["eks_nodes"]["target_nodes"],
                "Remediated": state["eks_nodes"]["remediated"],
                "AvgCpuPercent": state["eks_nodes"]["avg_cpu_percent"]
            }, indent=2)
            self._record_log("CloudShell", "aws eks describe-nodegroup executed via CloudShell")
        elif c in ("remediate volumes", "remediate-volumes"):
            count = self._apply_volumes_remediation()
            output = f"SUCCESS: Terminated {count} unattached EBS volumes. Created {count} safety snapshots tagged Retention=30Days (-$2.4k/mo)."
        elif c in ("remediate terraform", "remediate-terraform"):
            applied = self._apply_terraform_remediation()
            output = f"SUCCESS: Applied Terraform PR #482. EKS downscaled to 4 nodes, RDS resized to db.r6g.large (-$16k/mo)." if applied else "INFO: Terraform PR #482 already applied."
        elif c in ("remediate", "remediate all", "remediate-all", "!approve all"):
            vol_count = self._apply_volumes_remediation()
            tf_applied = self._apply_terraform_remediation()
            output = f"ALL REMEDIATIONS APPLIED:\n- Purged {vol_count} EBS disks with safety snapshots (-$2,400/mo)\n- Right-sized EKS & RDS via PR #482 (-$16,000/mo)\n- New Monthly Spend: ${state['current_monthly_spend']:,} (Baseline: ${state['budget_baseline']:,})\n- Realized Annual Savings: +${state['realized_annual_savings']:,} / year"
        elif c == "reset":
            state.clear()
            state.update(json.loads(json.dumps(INITIAL_STATE)))
            self._record_log("CloudShell", "Reset environment back to initial unoptimized state")
            output = "RESET COMPLETE: Environment restored to initial outage state ($42,600/mo run-rate, 18 orphaned disks, 16 EKS nodes)."
        elif c == "clear":
            output = "__CLEAR__"
        else:
            output = f"bash: {cmd}: command not found. Type 'help' for available AWS commands."

        self._set_headers()
        self.wfile.write(json.dumps({"command": cmd, "output": output}).encode("utf-8"))

    def _record_log(self, actor: str, event: str):
        state["audit_log"].insert(0, {
            "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
            "actor": actor,
            "event": event
        })
        if len(state["audit_log"]) > 15:
            state["audit_log"].pop()

    def _render_dashboard(self):
        html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.html")
        if os.path.exists(html_file):
            try:
                with open(html_file, "r", encoding="utf-8") as f:
                    content = f.read()
                self._set_headers(200, "text/html; charset=utf-8")
                self.wfile.write(content.encode("utf-8"))
                return
            except Exception as e:
                pass

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Switch FinOps — Live Cloud Environment</title>
  <style>
    :root {{
      --bg: #f2f3f3;
      --card-bg: #ffffff;
      --border: #eaeded;
      --text: #16191f;
      --text-muted: #545b64;
      --accent: #ec7211;
      --green: #037f0c;
      --red: #d13212;
      --blue: #0972d3;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
    body {{ background: var(--bg); color: var(--text); padding: 2rem; min-height: 100vh; }}
    .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; }}
    .logo-area h1 {{ font-size: 1.6rem; font-weight: 700; color: #fff; }}
    .logo-area span {{ color: var(--accent); }}
    .badge {{ background: rgba(255, 137, 94, 0.15); color: var(--accent); padding: 0.35rem 0.75rem; border-radius: 9999px; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(255, 137, 94, 0.3); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
    .card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; backdrop-filter: blur(12px); }}
    .card-title {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 0.5rem; }}
    .card-val {{ font-size: 2.2rem; font-weight: 800; }}
    .card-sub {{ font-size: 0.85rem; color: var(--text-muted); margin-top: 0.4rem; }}
    .val-red {{ color: var(--red); }}
    .val-green {{ color: var(--green); }}
    .val-orange {{ color: var(--accent); }}
    .section-title {{ font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}
    .details-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 0.5rem; }}
    th, td {{ padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.9rem; }}
    th {{ color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; }}
    .btn {{ background: var(--accent); color: #fff; border: none; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }}
    .btn:hover {{ opacity: 0.9; transform: translateY(-1px); }}
    .btn-secondary {{ background: transparent; border: 1px solid var(--border); color: var(--text-muted); margin-left: 0.5rem; }}
    .btn-secondary:hover {{ border-color: #fff; color: #fff; }}
    .log-item {{ font-size: 0.85rem; padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.04); display: flex; gap: 0.75rem; }}
    .log-time {{ color: var(--text-muted); font-family: monospace; }}
    .log-actor {{ font-weight: 600; color: var(--accent); min-width: 90px; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="logo-area">
      <h1>⚡ Switch <span>FinOps</span> War Room — Live Mock AWS Environment</h1>
      <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.3rem;">Target: staging-us-east-1 (Account: 1234-5678-9012)</p>
    </div>
    <div>
      <span class="badge">Status: Simulated Real-time Telemetry</span>
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="card-title">Live Monthly Cloud Run-Rate</div>
      <div class="card-val {'val-red' if state['current_monthly_spend'] > 30000 else 'val-green'}">${state['current_monthly_spend']:,} <span style="font-size: 1rem; font-weight: normal; color: var(--text-muted);">/ mo</span></div>
      <div class="card-sub">Budget Baseline: ${state['budget_baseline']:,} / mo</div>
    </div>

    <div class="card">
      <div class="card-title">Orphaned Unattached Volumes</div>
      <div class="card-val {'val-red' if len(state['volumes']) > 0 else 'val-green'}">{len(state['volumes'])} <span style="font-size: 1rem; font-weight: normal; color: var(--text-muted);">Disks</span></div>
      <div class="card-sub">{'$2,400 / mo Waste' if len(state['volumes']) > 0 else 'All Disks Reclaimed & Snapshot'}</div>
    </div>

    <div class="card">
      <div class="card-title">Staging Kubernetes Nodes</div>
      <div class="card-val {'val-red' if state['eks_nodes']['current_nodes'] > 4 else 'val-green'}">{state['eks_nodes']['current_nodes']} <span style="font-size: 1rem; font-weight: normal; color: var(--text-muted);">Nodes</span></div>
      <div class="card-sub">CPU Avg: {state['eks_nodes']['avg_cpu_percent']}% | Right-Sized Target: 4</div>
    </div>

    <div class="card">
      <div class="card-title">Annualized FinOps Realized Savings</div>
      <div class="card-val val-green">+${state['realized_annual_savings']:,}</div>
      <div class="card-sub">${state['realized_monthly_savings']:,} / month saved permanently</div>
    </div>
  </div>

  <div class="details-grid">
    <div class="card">
      <div class="section-title">📦 Infrastructure Resource Health</div>
      <table>
        <thead>
          <tr>
            <th>Resource Type</th>
            <th>Resource ID / Spec</th>
            <th>Metrics Telemetry</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>EKS Worker Nodes</td>
            <td>staging-general-workloads ({state['eks_nodes']['current_nodes']}x m6i.2xlarge)</td>
            <td>Avg CPU: 4.2% | Peak RAM: 14.8%</td>
            <td><span style="color: {'var(--red)' if state['eks_nodes']['current_nodes'] > 4 else 'var(--green)'};">{'⚠️ 12 Idle Nodes ($9.6k/mo)' if state['eks_nodes']['current_nodes'] > 4 else '✅ Right-Sized to 4 Nodes'}</span></td>
          </tr>
          <tr>
            <td>RDS PostgreSQL</td>
            <td>staging-app-db ({state['rds_instances']['current_class']})</td>
            <td>Active Conns: &lt;15 | p95 CPU: 6.1%</td>
            <td><span style="color: {'var(--red)' if state['rds_instances']['current_class'] == 'db.r6g.2xlarge' else 'var(--green)'};">{'⚠️ Over-Provisioned ($6.4k/mo)' if state['rds_instances']['current_class'] == 'db.r6g.2xlarge' else '✅ Downsized to large'}</span></td>
          </tr>
          <tr>
            <td>EBS Persistent Disks</td>
            <td>18 Orphaned gp3 volumes (30,000 GB)</td>
            <td>Status: available (0 I/O for 24d)</td>
            <td><span style="color: {'var(--red)' if len(state['volumes']) > 0 else 'var(--green)'};">{'⚠️ Unattached ($2.4k/mo)' if len(state['volumes']) > 0 else f'✅ Cleaned ({len(state["snapshots"])} Snapshots Created)'}</span></td>
          </tr>
        </tbody>
      </table>

      <div style="margin-top: 1.5rem; display: flex; gap: 0.5rem;">
        <button class="btn" onclick="fetch('/api/remediate/all', {{method:'POST'}}).then(()=>location.reload())">⚡ Execute All Remediations (Simulate !approve all)</button>
        <button class="btn btn-secondary" onclick="fetch('/api/reset', {{method:'POST'}}).then(()=>location.reload())">🔄 Reset to Initial Outage State</button>
      </div>
    </div>

    <div class="card">
      <div class="section-title">📜 Real-time Agent Audit Feed</div>
      <div style="max-height: 280px; overflow-y: auto;">
        {"".join([f'<div class="log-item"><span class="log-time">{log["timestamp"]}</span><span class="log-actor">{log["actor"]}</span><span>{log["event"]}</span></div>' for log in state["audit_log"]])}
      </div>
    </div>
  </div>

  <script>
    // Auto-refresh dashboard every 2.5s for live demo reaction
    setTimeout(() => location.reload(), 2500);
  </script>
</body>
</html>"""
        self._set_headers(200, "text/html; charset=utf-8")
        self.wfile.write(html.encode("utf-8"))

def run():
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), MockAWSHandler)
    print(f"==================================================================")
    print(f"  ☁️  MOCK AWS FINOPS SERVER ONLINE: http://localhost:{PORT}")
    print(f"  📊 Live FinOps Dashboard:        http://localhost:{PORT}/dashboard")
    print(f"  🔌 Cost Explorer API:            http://localhost:{PORT}/aws/cost-explorer")
    print(f"  📉 Telemetry & Metrics API:      http://localhost:{PORT}/aws/telemetry")
    print(f"  💾 EC2 Volumes API:              http://localhost:{PORT}/aws/ec2/volumes")
    print(f"==================================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Mock AWS server.")
        server.server_close()

if __name__ == "__main__":
    run()
