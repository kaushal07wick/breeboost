import json
import csv
import os
from datetime import datetime

INCIDENT_LOG = "incidents/log.csv"

def log_incident(alert_type, severity, notes=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, alert_type, severity, "PENDING", "OPEN", notes]

    os.makedirs("incidents", exist_ok=True)

    write_header = not os.path.exists(INCIDENT_LOG)

    with open(INCIDENT_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp","alert_type","severity","root_cause","status","notes"])
        writer.writerow(row)

    print(f"[ALERT] Incident logged: {alert_type} | Severity: {severity}")


def check_drift(report_path="reports/latest_report.json", threshold=0.20):
    if not os.path.exists(report_path):
        log_incident("Missing Report", "HIGH", "latest_report.json not found")
        return

    with open(report_path, "r") as f:
        report = json.load(f)

    drift_score = report.get("metrics", {}).get("data_drift", {}).get("drift_score", 0)

    if drift_score > threshold:
        log_incident("Data Drift", "HIGH", f"drift_score={drift_score}")
    else:
        print("No drift alert triggered.")


def check_missing_features(report_path="reports/latest_report.json"):
    with open(report_path, "r") as f:
        report = json.load(f)

    missing = report.get("metrics", {}).get("data_quality", {}).get("missing_values", 0)

    if missing > 0.05:
        log_incident("Missing Features", "MEDIUM", f"{missing*100}% missing values")


if __name__ == "__main__":
    print("Running alert checks...")
    check_drift()
    check_missing_features()
