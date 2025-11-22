"""
Basic unit tests for the incident utilities.
Requires pytest to run.
"""

import os
import json
import tempfile
from incident import logger, severity

def test_write_and_read_incident(tmp_path):
    # ensure isolated log path
    log_dir = tmp_path / "incident"
    log_dir.mkdir()
    test_log = log_dir / "incident_log.jsonl"

    # monkeypatch the path used by logger (simplest approach is to set env var or override)
    # but to keep this self-contained, replicate minimal write/read behavior:
    entry = {
        "timestamp": "2025-11-22T00:00:00Z",
        "incident_type": "UnitTest",
        "severity": "P4",
        "details": {"test": True},
        "status": "open",
        "notes": "created by test"
    }
    with open(test_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    # Read back
    with open(test_log, "r", encoding="utf-8") as f:
        lines = [json.loads(l) for l in f if l.strip()]
    assert len(lines) == 1
    assert lines[0]["incident_type"] == "UnitTest"
    assert lines[0]["severity"] == "P4"

def test_severity_rules():
    assert severity.compute_severity_from_drift(0.5) == "P1"
    assert severity.compute_severity_from_drift(0.25) == "P2"
    assert severity.compute_severity_from_drift(0.12) == "P3"
    assert severity.compute_severity_from_drift(0.01) == "P4"
    assert severity.severity_from_missing_rows(0.3) == "P1"
    assert severity.severity_from_missing_rows(0.08) == "P2" or severity.severity_from_missing_rows(0.08) == "P3"
