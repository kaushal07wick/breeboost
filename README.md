
# 🕵️‍♂️ Fraud Detection & Monitoring Project

This project builds a machine learning pipeline to detect fraudulent transactions and monitor data drift using [Evidently](https://github.com/evidentlyai/evidently).

---

## 📁 Project Structure

```

breeboost/
├── src/
│   ├── inference.py            # Model inference logic
│   ├── utils/
│   │   └── logger.py           # Logging utility
│   └── ...
├── monitoring/
│   ├── reference.csv           # Historical reference data
│   ├── production.csv          # New data with model predictions
│   ├── report.py               # Drift detection script
│   └── reports/                # HTML reports saved here
├── data/
│   └── processed/
│       └── paysim\_cleaned.csv  # Cleaned dataset used for training/reference
└── README.md

```

---

## ✅ What Has Been Implemented

### 1. **Model Inference**
- `inference.py` loads a trained XGBoost model and predicts fraud labels and probabilities.
- Ensures inputs match training schema exactly.
- Can be run as a standalone script for test predictions.

### 2. **Reference Data Creation**
- Script extracts a clean `reference.csv` from the main dataset.
- Renames target column (`isFraud` → `is_fraud`) if needed.
- Saves the reference data in the correct format with required columns.

### 3. **Production Data Simulation**
- `production.csv` includes:
  - Input features
  - Model prediction (`prediction`)
  - Probability of fraud (`fraud_proba`)
- Mimics what the model would see in a production pipeline.

### 4. **Monitoring with Evidently**
- `report.py` runs a drift report comparing reference vs. production data.
- Uses `DataDriftPreset` from Evidently.
- Generates and saves an HTML report with timestamp.
- Reports stored in `monitoring/reports/`.

---

## 🧪 How to Run

1. **Run model inference:**
   ```bash
   python src/inference.py
    ```

2. **Create reference data (one-time):**
   ```bash
   python src/utils/extract_ref.py
   ```

3. **Add predictions to production data**
   (Use inference module on new samples and save as `production.csv`)

4. **Generate monitoring report:**

   ```bash
   python monitoring/report.py
   ```

5. **View report:**
   Open the generated HTML in `monitoring/reports/` in your browser.

---

## 🛠️ Requirements

* Python 3.8+
* `pandas`
* `xgboost`
* `joblib`
* `evidently`
* `scipy`

Install with:

```bash
pip install pandas xgboost joblib evidently scipy
```

---

## 🚀 Next Steps

* [ ] Automate inference + production CSV generation
* [ ] Add concept/performance drift monitoring
* [ ] Set alerts for severe drift
* [ ] Dockerize and deploy

---

## 📌 Notes

* Be sure that `src` is in your Python path (or run scripts from the project root).
* Fix any drift-related warnings in data by examining the generated report.

---

> *This project is a work-in-progress and designed for educational and experimental purposes.*

```

Let me know if you'd like this in a downloadable file, or expanded with diagrams, badges, etc.
```
