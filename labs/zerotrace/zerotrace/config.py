"""
ZeroTrace Configuration

Defines paths and constants used across the ZeroTrace memory forensics project.
"""

from pathlib import Path

# Root directory = labs/zerotrace/
ROOT = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Where snapshots are stored
SNAPSHOT_PATH = RAW_DIR / "memory_snapshots.csv"

# ML artifacts
MODEL_PATH = ROOT / "model.joblib"
FEATURE_COLUMNS_PATH = ROOT / "feature_columns.json"
REPORT_PATH = ROOT / "report.json"

# Features used by the model
FEATURE_COLUMNS = [
    "pid",
    "ppid",
    "num_modules",
    "num_unsigned_modules",
    "num_rwx_regions",
    "avg_entropy",
    "has_network_connection",
    "num_connections",
    "listening_ports",
    "high_entropy_strings",
    "cpu_usage",
    "memory_usage_mb",
]

# Default model classes
MODEL_CLASSES = [
    "benign",
    "infostealer_like",
    "ransomware_like",
    "injected_loader",
]

# Synthetic generation settings
NUM_PROCESSES = 800  # synthetic amount
SEED = 1337
