# eval.py

import joblib
import polars as pl
from sklearn.metrics import classification_report, confusion_matrix, average_precision_score
from sklearn.model_selection import train_test_split
from pathlib import Path
from utils.logger import logger

# Paths
BASE = Path(__file__).resolve().parent
DATA_PATH = (BASE / ".." / "data" / "processed" / "paysim_cleaned.csv").resolve()
MODEL_PATH = (BASE / ".." / "models" / "xgb_model.joblib").resolve()

def load_data():
    logger.info("📥 Loading and splitting dataset...")
    df = pl.read_csv(DATA_PATH)

    y = df["isFraud"].to_numpy()
    X = df.drop("isFraud").to_pandas()

    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

def evaluate_model(model, X_test, y_test):
    logger.info("🧪 Evaluating model performance...")

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    logger.info("📊 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    logger.info("🧾 Classification Report:")
    print(classification_report(y_test, y_pred))

    auprc = average_precision_score(y_test, y_proba)
    logger.info(f"🔍 Average Precision Score (AUPRC): {auprc:.4f}")

if __name__ == "__main__":
    logger.info("🚀 Starting evaluation script")
    model = joblib.load(MODEL_PATH)
    _, X_test, _, y_test = load_data()
    evaluate_model(model, X_test, y_test)
