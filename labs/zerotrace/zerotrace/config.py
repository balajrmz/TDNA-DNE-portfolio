from pathlib import Path

# Root directory = labs/zerotrace/
ROOT = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Files we write/read
SNAPSHOT_PATH = RAW_DIR / "memory_snapshots.csv"
FEATURES_PATH = PROCESSED_DIR / "features.csv"   # new
FEATURES_CSV_PATH = FEATURES_PATH                # <- add this alias
MODEL_PATH = ROOT / "model.joblib"
FEATURE_COLUMNS_PATH = ROOT / "feature_columns.json"
REPORT_PATH = ROOT / "report.json"


# Feature columns the model will use
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

MODEL_CLASSES = [
    "benign",
    "infostealer_like",
    "ransomware_like",
    "injected_loader",
]

NUM_PROCESSES = 800
SEED = 1337
