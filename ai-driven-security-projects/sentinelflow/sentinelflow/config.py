"""
Central place for simple configuration values.

Having a config module makes it easy to change file paths
or constants in one place instead of hunting through
multiple files.
"""

from pathlib import Path

# Base project directory (assumes we run commands from the project root:
# labs/sentinelflow)
BASE_DIR = Path(__file__).resolve().parents[1]

# Paths for data and model artifacts
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "sentinelflow_synthetic.csv"
PROCESSED_DIR = DATA_DIR / "processed"

# Trained model and metrics
MODEL_PATH = PROCESSED_DIR / "model.joblib"
REPORT_PATH = PROCESSED_DIR / "report.json"

# NEW: where we store the exact feature column order used during training.
# This lets the API align incoming requests to match the trained model.
FEATURES_PATH = PROCESSED_DIR / "feature_columns.json"
