import polars as pl
from pathlib import Path
import os
import numpy as np
from utils.logger import logger  

# Directory setup
BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw" / "PS_20174392719_1491204439457_log.csv"
PROC = BASE / "data" / "processed" / "paysim_cleaned.csv"

PROC.parent.mkdir(parents=True, exist_ok=True)

# Load the raw data
def load_raw_data(path: Path = RAW) -> pl.DataFrame:
    logger.info(f"Loading raw data from {path}")
    return pl.read_csv(path)

# Preprocess the data for fraud detection
def preprocess_data(df: pl.DataFrame, seed: int = 5) -> pl.DataFrame:
    logger.info("Starting preprocessing")
    np.random.seed(seed)

    df = df.filter(pl.col("type").is_in(["TRANSFER", "CASH_OUT"]))
    logger.info("Filtered only TRANSFER and CASH_OUT transactions")

    df = df.drop(["nameOrig", "nameDest", "isFlaggedFraud"])
    logger.info("Dropped irrelevant columns")

    df = df.with_columns([
        pl.when(pl.col("type") == "TRANSFER").then(0)
          .when(pl.col("type") == "CASH_OUT").then(1)
          .alias("type")
          .cast(pl.Int8)
    ])
    logger.info("Encoded transaction type to binary")

    condition_dest = (
        (pl.col("oldbalanceDest") == 0) &
        (pl.col("newbalanceDest") == 0) &
        (pl.col("amount") != 0)
    )
    df = df.with_columns([
        pl.when(condition_dest).then(-1).otherwise(pl.col("oldbalanceDest")).alias("oldbalanceDest"),
        pl.when(condition_dest).then(-1).otherwise(pl.col("newbalanceDest")).alias("newbalanceDest")
    ])
    logger.info("Handled suspicious destination balance zeros")

    condition_orig = (
        (pl.col("oldbalanceOrg") == 0) &
        (pl.col("newbalanceOrig") == 0) &
        (pl.col("amount") != 0)
    )
    df = df.with_columns([
        pl.when(condition_orig).then(None).otherwise(pl.col("oldbalanceOrg")).alias("oldbalanceOrg"),
        pl.when(condition_orig).then(None).otherwise(pl.col("newbalanceOrig")).alias("newbalanceOrig")
    ])
    logger.info("Handled suspicious origin balance zeros")

    df = df.with_columns([
        (pl.col("newbalanceOrig") + pl.col("amount") - pl.col("oldbalanceOrg")).alias("errorBalanceOrig"),
        (pl.col("oldbalanceDest") + pl.col("amount") - pl.col("newbalanceDest")).alias("errorBalanceDest"),
        (pl.col("amount") > 200_000).cast(pl.Int8).alias("is_large_transaction"),
        (pl.col("step") % 24).alias("hour"),
        (pl.col("step") // 24).alias("day")
    ])
    logger.info("Created engineered features")

    return df

# Save cleaned data
def save_preprocessed_data(df: pl.DataFrame, out_path: Path = PROC):
    logger.info(f"Saving preprocessed data to {out_path}")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.write_csv(out_path)
    logger.info("Data successfully saved")

if __name__ == "__main__":
    logger.info("🚀 Data preprocessing pipeline started")
    df = load_raw_data()
    df_clean = preprocess_data(df)
    save_preprocessed_data(df_clean)
    logger.info("✅ Preprocessing complete. Cleaned data saved.")
    print("✅ Preprocessing complete. Cleaned data saved to:", PROC)
