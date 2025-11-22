# 🕵️‍♂️ BreeBoost – Real-Time Fraud Detection, Monitoring & Incident Response

![breeboost](assets/breeboost.png)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status: WIP](https://img.shields.io/badge/status-active-informational)]()
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Made with Evidently](https://img.shields.io/badge/Made%20with-Evidently-blueviolet?logo=evidently)](https://github.com/evidentlyai/evidently)

> End-to-end machine learning pipeline for fraud detection with **real-time simulation**, **data drift monitoring**, **incident response workflows**, and **interactive dashboards**.

---

## 📊 Architecture Overview

```mermaid
flowchart TD
    A[Cleaned Data] --> B[Model Inference]
    B --> C[Predictions + Probabilities]
    A --> D[Reference Data]
    C --> E[Drift Detection]
    D --> E
    E --> F[HTML Report]
    F --> G[Incident Response Layer]
    G --> H[Incident Log + Alerts]

    style A fill:#f9f,stroke:#333,stroke-width:1px
    style B fill:#bbf,stroke:#333,stroke-width:1px
    style C fill:#bfb,stroke:#333,stroke-width:1px
    style D fill:#bbf,stroke:#333,stroke-width:1px
    style E fill:#ffb,stroke:#333,stroke-width:1px
    style F fill:#fc9,stroke:#333,stroke-width:1px
    style G fill:#ffd6cc,stroke:#333,stroke-width:1px
    style H fill:#eee,stroke:#333,stroke-width:1px
````

---

## ✅ Features Implemented

### 🔍 1. **Fraud Detection Model**

* Trained XGBoost classifier for transaction-level anomaly detection
* Input validation and prediction interface
* Outputs label + fraud probability

### 💻 2. **Streamlit Dashboard**

* Real-time transaction simulation
* Drift visualization and model monitoring
* View predictions, top features, and anomaly trends

### 📈 3. **Evidently Drift Monitoring**

* Compares training vs production data
* Visualizes drift in numerical and categorical features
* Generates detailed HTML drift reports

🔗 **[View Latest Drift Report](monitoring/reports/data_drift_20250617_123717.html)**

---

## 🧯 4. **Incident Response System **

BreeBoost now includes a **production-style ML incident response module** that mimics real-world monitoring and alert handling in data pipelines.

### 🧩 Components:

* **Incident Logger:**
  Every data drift, schema mismatch, or missing feature event is logged in `incident/incident_log.jsonl` with timestamp, severity, and context.

* **Severity Mapping:**
  Automatic P1–P4 classification based on drift magnitude, data freshness, or missing data ratio.
  *(P1 = critical corruption; P4 = info-only)*

* **Root Cause Analysis (RCA):**
  Run:

  ```bash
  python incident/rca.py --mode summary
  ```

  Generates summaries of drifted features, missing value percentages, and likely sources of anomaly.

* **Incident Playbook:**
  The on-call runbook (`incident/playbook.md`) outlines:

  * First responder steps (check ingestion, compare schema)
  * RCA and triage flow
  * Escalation matrix for P1/P2/P3 levels
  * Postmortem template for prevention

* **Alert Manager (in progress):**
  Planned Slack/webhook integrations for notifying when PSI > 0.3 or key metrics degrade.

---

## 🚀 Usage

### 🔧 Install Requirements

```bash
pip install -r requirements.txt
```

### 🧠 Run Inference

```bash
python src/inference.py
```

### 🧾 Generate Reference Dataset

```bash
python src/utils/extract_ref.py
```

### 📦 Simulate Production Data

Use the dashboard or inference module to generate rows for `production.csv`.

### 📉 Run Drift Monitoring

```bash
python monitoring/report.py
```

### 🧯 Log Incidents Automatically

```bash
python src/alert_manager.py
```

### 🧪 Investigate Incidents (RCA)

```bash
python incident/rca.py --mode top_drift --n 10
```

### 🖥️ Launch Streamlit App

```bash
streamlit run app.py
```

---

## 🔢 Key Features for Drift Detection

* `amount`, `oldbalanceOrg`, `newbalanceOrig`
* `errorBalanceOrig`, `errorBalanceDest`
* `hour`, `day`, `is_large_transaction`

---

## 🛠️ Example Incident Entry

```json
{
  "timestamp": "2025-11-22T08:12:00Z",
  "incident_type": "Data Drift",
  "severity": "P2",
  "details": {
    "drift_score": 0.27,
    "affected_features": ["amount", "errorBalanceDest"]
  },
  "status": "open",
  "notes": "Potential upstream data scaling issue"
}
```

---

## 🧭 Incident Lifecycle

| Stage         | Purpose                           | Tools                     |
| ------------- | --------------------------------- | ------------------------- |
| **Detection** | Drift or anomaly found            | Evidently, PSI/KS Monitor |
| **Logging**   | Record incident context           | `incident/logger.py`      |
| **Triage**    | Severity classification (P1–P4)   | `incident/severity.py`    |
| **Response**  | Follow IRP checklist              | `incident/playbook.md`    |
| **RCA**       | Analyze drift/missingness         | `incident/rca.py`         |
| **Closure**   | Document fix + prevent recurrence | JSONL notes + postmortem  |

---

## 🛣️ Roadmap

* [x] Add incident logging and severity mapping
* [x] Implement RCA for drift/missing value reports
* [ ] Integrate Slack alerts + Prometheus metrics
* [ ] Automate IRP execution pipeline
* [ ] Add CI/CD (GitHub Actions + Docker support)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

