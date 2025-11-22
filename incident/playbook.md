# BreeBoost Incident Playbook (Concise)

This playbook is a compact, actionable guide for first-responders handling incidents detected by BreeBoost.

---

## 1. High-level triage
1. **Identify**: Check `incident/incident_log.jsonl` for latest entries.
2. **Categorize**: Is it **operational** (ingestion, schema, latency) or **model** (drift, prediction change)?
3. **Severity**: Use severity tag (P1 highest → P4 lowest).

---

## 2. First responder checklist (5–10 minutes)

### a. If ingestion / pipeline delay:
- Check ingestion logs: `logs/ingestion.log` and last modified timestamp of `monitoring/production.csv`.
- Confirm downstream consumers (dashboard/monitor) are receiving rows.
- If missing files, contact ETL owner / re-run secure upstream job.
- Mark incident notes with: `rows_missing`, `last_success_timestamp`.

### b. If missing feature / schema mismatch:
- Compare `monitoring/reference.csv` header vs `monitoring/production.csv` header.
- If column missing => escalate to Data Engineering.
- For null spike, run `python incident/rca.py --mode missing_values --top 10`.

### c. If drift / prediction distribution change:
- Run `python monitoring/report.py` and open `monitoring/reports/report.html`.
- Identify top contributing features (drift contribution).
- If drift localized to one feature (e.g., 'amount'), follow the feature-level checks.

---

## 3. Root-cause quick steps (15–30 minutes)
- Reproduce sample: extract 100 rows around the incident time (dashboard supports 'replay').
- Compare distributions (reference vs sample). Use KS / PSI values.
- Inspect raw logs for transformation errors (scaling, encoding).
- Check model inputs for invalid types (strings in numeric column).
- If model performance drop: check recent model deployment, model version, and feature changes.

---

## 4. Escalation matrix
- **P1** (data corruption / service down): Pager to on-call infra + Data Eng Lead.
- **P2** (high drift / major feature missing): Notify Model Owner + Data Eng.
- **P3** (minor drift): Triage by Analyst; add to monitoring backlog.
- **P4** (info): Log and monitor.

---

## 5. Postmortem & Prevention (after resolution)
- Add RCA summary to incident log `notes`.
- Document root cause and permanent fix (code/ETL change).
- Update this playbook with steps that saved time.
- Consider adding an automated pre-check if recurrence is possible.

---

## 6. Quick commands
- View last incidents:
  ```bash
  tail -n 20 incident/incident_log.jsonl
