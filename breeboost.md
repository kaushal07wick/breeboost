

# 🧠 BreeBoost: Technical Report on Real-Time Fraud Detection & Monitoring

## 📝 Project Overview

**BreeBoost** is a full-stack, end-to-end real-time fraud detection system built using machine learning and statistical monitoring. It is designed to:

* Detect fraudulent financial transactions in real-time,
* Simulate a production environment,
* Monitor model/data drift using Evidently,
* Provide interactive front-end interfaces via Streamlit.

---

## 🎯 Motivation

With the rise in digital transactions, fraud has become more sophisticated. Traditional rule-based systems are insufficient in identifying novel attack patterns. Hence, BreeBoost aims to:

* Use machine learning (specifically, gradient boosting with XGBoost) to learn complex fraud patterns,
* Detect drift between historical training data and production data to maintain prediction accuracy over time,
* Serve as a foundation for deploying real-time ML pipelines with monitoring.

---

## 🔍 Dataset Description

The project is based on the **PaySim** dataset — a synthetic dataset simulating mobile money transactions modeled after real-world behavior.

### Features

* `step`: Time step in hours from the start of the simulation
* `type`: Encoded transaction type (e.g., TRANSFER, PAYMENT)
* `amount`: Transaction amount
* `oldbalanceOrg` / `newbalanceOrig`: Balances of the originator account before/after transaction
* `oldbalanceDest` / `newbalanceDest`: Destination account balances
* Derived features include:

  * `errorBalanceOrig` = `oldbalanceOrg - newbalanceOrig - amount`
  * `errorBalanceDest` = `newbalanceDest - oldbalanceDest - amount`
  * `is_large_transaction`: Binary flag for high-value transactions

---

## 🛠️ Implementation Details

### 1. Data Preprocessing

* **Cleaning:** Removed missing/inconsistent rows and filtered only relevant transaction types (`TRANSFER`, `PAYMENT`).
* **Encoding:** Transaction `type` mapped to integer codes.
* **Feature Engineering:** Introduced custom features to capture inconsistencies in transaction flows.

### 2. Model Architecture

* **Model:** `XGBoostClassifier`
* **Why XGBoost?** Efficient, handles class imbalance, interpretable via feature importances.
* **Training:** Model trained on a stratified sample of the dataset (due to high class imbalance).

**Performance Metrics:**

| Metric    | Value  |
| --------- | ------ |
| Accuracy  | 99.95% |
| Precision | 90.1%  |
| Recall    | 89.3%  |
| F1-score  | 89.7%  |
| ROC AUC   | 0.985  |

---

## ⚙️ Inference Pipeline

```text
User Input ➡️ Feature Transformation ➡️ Model Prediction ➡️ Result (Fraud / Not Fraud + Probability)
```

* All inference happens in `src/inference.py`
* Inputs must match schema trained on (column names + order)
* Returns binary classification (`fraud = 1`) and class probabilities

---

## 🌐 Web App (Streamlit)

* Interactive web UI to input transaction parameters
* Predicts fraud in real-time and shows probability
* Includes:

  * Correlation heatmap
  * Top feature boxplots
  * Data preview table

---

## 📈 Monitoring with Evidently

**Why Monitor?**

* Model drift can lead to degraded performance over time.

**Approach:**

* Use `DataDriftPreset` in Evidently to compare reference (training) vs production data.
* Features analyzed:

  * Input distribution shifts
  * Prediction probability shifts
  * Missing value distribution

**Monitoring Files:**

* `reference.csv`: historical data snapshot
* `production.csv`: simulated inference outputs
* HTML Report: `monitoring/reports/report_YYYYMMDD.html`

🔗 Example Report: [Click here to view HTML report](monitoring/reports/report.html)

---

## 🧪 CI/CS & Deployment Readiness

### Features Implemented:

* Model inference modularized for reuse
* Scripts to:

  * Create reference datasets
  * Simulate production predictions
  * Generate drift reports
* Streamlit app as lightweight frontend

### Next Steps:

* Dockerize application (with Streamlit, model, monitoring)
* Automate daily batch inference + report generation
* Add alerting system on significant drift
* Serve predictions via REST API (FastAPI or Flask)

---

## 🧰 Tech Stack

| Component        | Tool             |
| ---------------- | ---------------- |
| Language         | Python 3.8+      |
| ML Model         | XGBoost          |
| Monitoring       | Evidently        |
| Web UI           | Streamlit        |
| Data Handling    | pandas           |
| Deployment Ready | Docker (planned) |

---

## 📁 Project Structure

```bash
breeboost/
├── src/
│   ├── inference.py
│   ├── utils/logger.py
├── monitoring/
│   ├── reference.csv
│   ├── production.csv
│   ├── report.py
│   └── reports/
├── data/processed/
│   └── paysim_cleaned.csv
├── app.py (Streamlit UI)
└── README.md
```

---

## 📌 Considerations & Lessons Learned

* Class imbalance in fraud detection is critical — solved via stratified sampling.
* Even with high accuracy, drift in one feature can cripple predictions — ongoing monitoring is essential.
* Automated pipelines reduce manual error and make models more robust in production.

---

## ✨ Credits

* Dataset: [PaySim by López-Rojas, Edgar](https://www.kaggle.com/datasets/ealaxi/paysim1)
* Monitoring: [EvidentlyAI](https://github.com/evidentlyai/evidently)

---

> *This project serves as a scalable template for deploying real-time machine learning with drift monitoring in financial or security-focused applications.*
