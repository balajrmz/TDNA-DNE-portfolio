"""
PacketVision configuration.

In plain English:
- This file defines important paths on disk.
- Other modules import these constants so we don't hard-code paths everywhere.
"""

from __future__ import annotations

from pathlib import Path

# BASE_DIR points to the root of this lab, e.g.:
# .../pentest-portfolio/labs/packetvision
BASE_DIR = Path(__file__).resolve().parent.parent

# All data for PacketVision lives under data/
DATA_DIR = BASE_DIR / "data"

# Raw PCAPs go here.
RAW_PCAP_DIR = DATA_DIR / "raw"

# Processed artifacts (features, model, reports) go here.
PROCESSED_DIR = DATA_DIR / "processed"
FEATURES_CSV_PATH = PROCESSED_DIR / "flow_features.csv"
MODEL_PATH = PROCESSED_DIR / "model.joblib"
REPORT_PATH = PROCESSED_DIR / "report.json"
FEATURE_COLUMNS_PATH = PROCESSED_DIR / "feature_columns.json"

