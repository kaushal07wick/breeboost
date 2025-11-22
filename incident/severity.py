"""
Severity helpers and simple rules mapping metrics -> severity.
Keep this deterministic and easy to expand.
"""

from typing import Dict, Any


def compute_severity_from_drift(drift_score: float) -> str:
    """
    Map a numeric drift score into severity levels:
     - P1: Critical (very high drift / data corruption)
     - P2: Major (high drift)
     - P3: Minor (noticeable drift)
     - P4: Info (low/non-actionable drift)
    """
    if drift_score is None:
        return "P4"
    if drift_score >= 0.4:
        return "P1"
    if drift_score >= 0.2:
        return "P2"
    if drift_score >= 0.1:
        return "P3"
    return "P4"


def severity_from_missing_rows(missing_pct: float) -> str:
    if missing_pct is None:
        return "P4"
    if missing_pct >= 0.25:
        return "P1"
    if missing_pct >= 0.10:
        return "P2"
    if missing_pct >= 0.03:
        return "P3"
    return "P4"


def decide_severity(event: Dict[str, Any]) -> str:
    """
    Generic decision based on available event keys.
    event may contain: {'drift_score': 0.2, 'missing_pct': 0.05, ...}
    """
    if "drift_score" in event:
        return compute_severity_from_drift(event.get("drift_score"))
    if "missing_pct" in event:
        return severity_from_missing_rows(event.get("missing_pct"))
    return "P4"
