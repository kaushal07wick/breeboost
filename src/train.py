import polars as pl
import numpy as np
from pathlib import Path
from sklearn.metrics import average_precision_score
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import joblib
from utils.logger import logger

# Paths
BASE = Path(__file__).resolve().parent.parent
DATA_PATH = BASE / "data" / "processed" / "paysim_cleaned.csv"
MODEL_PATH = BASE / "models" / "xgb_model.joblib"
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_data(path: Path) -> tuple[np.ndarray, np.ndarray]:
    logger.info(f"Loading processed data from {path}")
    df = pl.read_csv(path)
    Y = df["isFraud"].to_numpy()
    X = df.drop("isFraud").to_pandas()
    return X, Y

def train_model(X, Y) -> XGBClassifier:
    logger.info("Splitting dataset into train/test sets")
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

    weights = (trainY == 0).sum() / (1.0 * (trainY == 1).sum())
    logger.info(f"Class imbalance weight (scale_pos_weight): {weights:.2f}")

    clf = XGBClassifier(
        max_depth=3,
        scale_pos_weight=weights,
        n_jobs=4,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    logger.info("Training XGBoost model...")
    clf.fit(trainX, trainY)

    logger.info("Evaluating model on test set...")
    probabilities = clf.predict_proba(testX)
    auprc = average_precision_score(testY, probabilities[:, 1])
    logger.info(f"AUPRC on test set: {auprc:.4f}")
    print(f"✅ AUPRC = {auprc:.4f}")

    return clf

def save_model(model, path: Path):
    logger.info(f"Saving trained model to {path}")
    joblib.dump(model, path)

if __name__ == "__main__":
    logger.info("🚀 Training pipeline started")
    X, Y = load_data(DATA_PATH)
    model = train_model(X, Y)
    save_model(model, MODEL_PATH)
    logger.info("✅ Training complete. Model saved.")
