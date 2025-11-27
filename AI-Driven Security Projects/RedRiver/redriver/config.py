from pathlib import Path

# Root directory for the RedRiver lab
ROOT = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# Data directories
# ------------------------------------------------------------------
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Make sure directories exist
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------
# Raw flows file (synthetic PCAP-style flows)
# ------------------------------------------------------------------
RAW_FLOWS_PATH = RAW_DIR / "flows.csv"

# Alias used by other modules (pipeline.py expects FLOWS_PATH)
FLOWS_PATH = RAW_FLOWS_PATH

# ------------------------------------------------------------------
# Files produced by the feature pipeline and ML training
# ------------------------------------------------------------------
FEATURES_PATH = PROCESSED_DIR / "features.csv"
MODEL_PATH = ROOT / "model.joblib"
REPORT_PATH = ROOT / "report.json"

# JSON file listing the feature column order the model expects
FEATURE_COLUMNS_PATH = ROOT / "feature_columns.json"

# Backwards-compatible alias (some code may import FEATURE_COLS_PATH)
FEATURE_COLS_PATH = FEATURE_COLUMNS_PATH

# ------------------------------------------------------------------
# ML configuration
# ------------------------------------------------------------------
# Name of the label column in the feature matrix
LABEL_COLUMN = "label"

# Random seed for reproducibility
RANDOM_SEED = 1337


def describe_paths() -> None:
    """Small helper to quickly print all important paths."""
    print("[RedRiver] ROOT               =", ROOT)
    print("[RedRiver] DATA_DIR           =", DATA_DIR)
    print("[RedRiver] RAW_DIR            =", RAW_DIR)
    print("[RedRiver] PROCESSED_DIR      =", PROCESSED_DIR)
    print("[RedRiver] FLOWS_PATH         =", FLOWS_PATH)
    print("[RedRiver] FEATURES_PATH      =", FEATURES_PATH)
    print("[RedRiver] MODEL_PATH         =", MODEL_PATH)
    print("[RedRiver] REPORT_PATH        =", REPORT_PATH)
    print("[RedRiver] FEATURE_COLUMNS    =", FEATURE_COLUMNS_PATH)


if __name__ == "__main__":
    # Allow quick manual check:  python -m redriver.config
    describe_paths()
