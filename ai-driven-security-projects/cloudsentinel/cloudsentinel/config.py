"""
CloudSentinel configuration.

In plain English:
- This file just defines important paths on disk.
- Other modules import these constants so we don't hard-code file paths
  everywhere.
"""

from __future__ import annotations

from pathlib import Path

# BASE_DIR points to the root of the CloudSentinel lab, e.g.:
# .../pentest-portfolio/labs/cloudsentinel
BASE_DIR = Path(__file__).resolve().parent.parent

# All data for this lab lives under data/
DATA_DIR = BASE_DIR / "data"

# Raw (synthetic) IAM policies will be stored here as JSONL (one policy per line).
RAW_DATA_PATH = DATA_DIR / "raw" / "synthetic_policies.jsonl"

# Processed artifacts (model, reports, features) live here.
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_PATH = PROCESSED_DIR / "model.joblib"
REPORT_PATH = PROCESSED_DIR / "report.json"
FEATURES_PATH = PROCESSED_DIR / "feature_columns.json"

