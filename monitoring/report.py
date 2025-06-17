import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from datetime import datetime
import os
from pathlib import Path

# Define paths relative to this script location or project root
BASE_DIR = Path(__file__).resolve().parent.parent  # adjust if needed

REF_PATH = BASE_DIR / "monitoring" / "reference.csv"
PROD_PATH = BASE_DIR / "monitoring" / "production.csv"
REPORT_DIR = BASE_DIR / "monitoring" / "reports"

# Load data
ref = pd.read_csv(REF_PATH)
prod = pd.read_csv(PROD_PATH)

# Create and run drift report
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref, current_data=prod)

# Save report
REPORT_DIR.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_path = REPORT_DIR / f"data_drift_{timestamp}.html"
report.save_html(str(report_path))

print(f"✅ Report generated and saved to: {report_path}")
