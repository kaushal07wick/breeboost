import pandas as pd
from pathlib import Path
import joblib

# Paths
DATA_PATH = Path("../breeboost/data/processed/paysim_cleaned.csv").resolve()
REFERENCE_PATH = Path("../breeboost/monitoring/reference.csv").resolve()
MODEL_PATH = Path("../breeboost/models/xgb_model.joblib").resolve()

# Feature columns expected by model
columns_needed = [
    "step",
    "type",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "errorBalanceOrig",
    "errorBalanceDest",
    "is_large_transaction",
    "hour",
    "day",
]

# Load raw data
df = pd.read_csv(DATA_PATH)

# Check missing columns
missing = [col for col in columns_needed if col not in df.columns]
if missing:
    print(f"⚠️ Missing columns in dataset: {missing}")
    exit(1)

# Extract features (take first 500 rows)
df_features = df[columns_needed].head(500).copy()

# Load model
model = joblib.load(MODEL_PATH)

# Predict
predictions = model.predict(df_features)
probabilities = model.predict_proba(df_features)[:, 1]

# Add prediction columns
df_features["prediction"] = predictions
df_features["fraud_proba"] = probabilities

# Reorder columns exactly as you want
final_cols = columns_needed + ["prediction", "fraud_proba"]
df_features = df_features[final_cols]

# Save CSV
REFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
df_features.to_csv(REFERENCE_PATH, index=False)

print(f"✅ reference.csv saved to: {REFERENCE_PATH}")
