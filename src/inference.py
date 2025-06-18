import joblib
import pandas as pd
from pathlib import Path
from utils.logger import logger

BASE = Path(__file__).resolve().parent
MODEL_PATH = (BASE / ".." / "models" / "xgb_model.joblib").resolve()
INPUT_PATH = (BASE / ".." / "data" / "input_data.csv").resolve()
OUTPUT_PATH = (BASE / ".." / "monitoring" / "production.csv").resolve()

def load_model():
    logger.info(f"Loading model from {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def predict(model, data: pd.DataFrame):
    logger.info("Making prediction...")
    pred = model.predict(data)
    proba = model.predict_proba(data)
    return pred, proba

if __name__ == "__main__":
    logger.info("Running batch inference for monitoring...")

    try:
        new_data = pd.read_csv(INPUT_PATH)
        logger.info(f"Loaded input data from {INPUT_PATH}, shape: {new_data.shape}")
    except FileNotFoundError:
        logger.error(f"Input file not found: {INPUT_PATH}")
        exit()

    model = load_model()
    y_pred, y_proba = predict(model, new_data)

    new_data["prediction"] = y_pred
    new_data["fraud_proba"] = y_proba[:, 1]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    new_data.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"Saved predictions to {OUTPUT_PATH}")
