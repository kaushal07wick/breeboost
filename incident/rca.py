"""
Simple RCA utilities.
Provides:
 - top_n_drifted_features(reference_df, production_df)
 - basic missing value summary
 - CLI to run common modes

Dependencies: pandas, numpy, scipy (for KS)
"""

import argparse
import json
import os
from typing import List, Tuple

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

# default paths (relative)
REF_PATH = os.path.join("monitoring", "reference.csv")
PROD_PATH = os.path.join("monitoring", "production.csv")
REPORTS_DIR = os.path.join("monitoring", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def load_data(ref_path=REF_PATH, prod_path=PROD_PATH) -> Tuple[pd.DataFrame, pd.DataFrame]:
    ref = pd.read_csv(ref_path)
    prod = pd.read_csv(prod_path)
    return ref, prod


def compute_ks_per_feature(ref: pd.Series, prod: pd.Series) -> float:
    # For categorical with many unique values, fallback to PSI style; but here we use KS if numeric
    try:
        ref_clean = ref.dropna().astype(float)
        prod_clean = prod.dropna().astype(float)
        if len(ref_clean) < 2 or len(prod_clean) < 2:
            return 0.0
        stat, pvalue = ks_2samp(ref_clean, prod_clean)
        # return statistic as a measure of distribution difference (0..1)
        return float(stat)
    except Exception:
        # For non-numeric use a simple proportion difference metric
        ref_counts = ref.fillna("##MISSING##").value_counts(normalize=True)
        prod_counts = prod.fillna("##MISSING##").value_counts(normalize=True)
        all_keys = set(ref_counts.index).union(set(prod_counts.index))
        diff = sum(abs(ref_counts.get(k, 0.0) - prod_counts.get(k, 0.0)) for k in all_keys) / 2.0
        return float(diff)


def top_n_drifted_features(ref: pd.DataFrame, prod: pd.DataFrame, n: int = 10) -> List[Tuple[str, float]]:
    """
    Return top-n features with highest KS/difference score.
    """
    features = [c for c in ref.columns if c in prod.columns and c != "label"]
    scores = {}
    for f in features:
        try:
            score = compute_ks_per_feature(ref[f], prod[f])
            scores[f] = score
        except Exception:
            scores[f] = 0.0
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:n]


def missing_value_summary(prod: pd.DataFrame) -> pd.DataFrame:
    s = prod.isna().mean().sort_values(ascending=False)
    return s.reset_index().rename(columns={"index": "feature", 0: "missing_pct"})


def write_simple_report(top_drift, missing_df, out_path=None):
    out = {
        "top_drifted_features": [{"feature": f, "score": float(s)} for f, s in top_drift],
        "missing_summary": missing_df.to_dict(orient="records"),
    }
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(f"Wrote RCA summary to {out_path}")
    else:
        print(json.dumps(out, indent=2))


def cli():
    parser = argparse.ArgumentParser(description="Run quick RCA on reference vs production data.")
    parser.add_argument("--mode", choices=["top_drift", "missing_values", "summary"], default="summary")
    parser.add_argument("--n", type=int, default=10, help="Top-n features for drift")
    parser.add_argument("--out", type=str, default=None, help="Write JSON summary to file")
    args = parser.parse_args()

    ref, prod = load_data()
    if args.mode == "top_drift":
        top = top_n_drifted_features(ref, prod, n=args.n)
        for f, s in top:
            print(f"{f}\t{float(s):.4f}")
        if args.out:
            write_simple_report(top, missing_value_summary(prod), out_path=args.out)
    elif args.mode == "missing_values":
        missing = missing_value_summary(prod)
        print(missing.to_string(index=False))
        if args.out:
            write_simple_report([], missing, out_path=args.out)
    else:
        top = top_n_drifted_features(ref, prod, n=args.n)
        missing = missing_value_summary(prod)
        write_simple_report(top, missing, out_path=args.out)


if __name__ == "__main__":
    cli()