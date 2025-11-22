# Incident Response Plan (IRP) – BreeBoost

This IRP defines how to respond when the BreeBoost fraud monitoring system
detects anomalies, drift, pipeline delays, or system errors.

---

## 1. Alerts & Triggers

### **Data / Model Alerts**
| Alert Type | Description | Threshold |
|-----------|-------------|-----------|
| Data Drift | Drift in input distribution vs reference | > 20% drift score |
| Prediction Drift | Output distribution changes | > 15% deviation |
| Missing Features | Missing columns or NA spike | > 5% rows affected |
| Model Latency Spike | API latency jump | > 1.5× normal |

### **Operational Alerts**
| Alert Type | Description | Threshold |
|-----------|-------------|-----------|
| Pipeline Delay | Batch or real-time ingestion delay | > 10 minutes |
| API Error Spike | Failure rate | > 5% requests |
| Dashboard Failure | Monitor not updating | 2+ cycles missed |

---

## 2. First-Responder Checklist

When an alert fires:

### **Step 1 — Verify Alert**
- Check `reports/latest_report.json`
- Check Streamlit dashboard for:
  - Drift graphs
  - Error logs
  - KPI trends

### **Step 2 — Identify Category**
- **Operational issue?** (delay, API errors, ingestion failure)
- **Model issue?** (drift, missing features, anomaly spike)

### **Step 3 — Debugging Tools**
Use available tools:

| Tool | Purpose |
|------|---------|
| Evidently reports | Examine drift and data quality |
| Streamlit dashboard | Visualize KPIs and drift |
| Logs (`logs/*.log`) | Root-cause patterns |
| `alert_manager.py` | Incident creation |

---

## 3. Escalation Rules

| Condition | Escalate To |
|----------|-------------|
| Data corruption | Data Engineering |
| Unexplained drift > 30% | Model Owner |
| Sustained API error > 5% | Backend/ML Infra |
| Critical business KPI anomaly | DS Lead |

---

## 4. Incident Logging

Every alert creates an entry in:

