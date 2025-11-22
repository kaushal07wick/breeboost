"""
Simple incident logger: append JSON lines to incident/incident_log.jsonl
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

LOG_PATH = os.path.join("incident", "incident_log.jsonl")
os.makedirs("incident", exist_ok=True)


def _utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def write_incident(incident_type: str, severity: str, details: Dict[str, Any], status: str = "open", notes: str = "") -> None:
    """
    Append an incident as a JSON line.

    incident_type: short name (e.g., "Data Drift", "Missing Feature")
    severity: one of P1,P2,P3,P4
    details: arbitrary dict with metrics (drift_score, features, etc.)
    status: open | resolved | mitigated
    notes: free text
    """
    entry = {
        "timestamp": _utc_now_iso(),
        "incident_type": incident_type,
        "severity": severity,
        "details": details,
        "status": status,
        "notes": notes,
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    # Also print to console for the on-call/CI visibility
    print(f"[INCIDENT LOGGED] {entry['timestamp']} | {incident_type} | {severity}")


def read_incidents(limit: int = 100):
    """Read last `limit` incidents (most recent last)."""
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [json.loads(l.strip()) for l in lines if l.strip()]
    return lines[-limit:]
