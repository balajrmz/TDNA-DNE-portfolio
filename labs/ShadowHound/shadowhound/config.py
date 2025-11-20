from pathlib import Path

# -------------------------------------------------------------------
# Root directory for ShadowHound
# -------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# Data directories
# -------------------------------------------------------------------
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Where our synthetic BloodHound-style edges live
RAW_GRAPH_PATH = RAW_DIR / "ad_edges.json"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------
# Files ShadowHound will read/write
# -------------------------------------------------------------------
SNAPSHOT_PATH = RAW_DIR / "ad_edges.json"
FEATURES_PATH = PROCESSED_DIR / "features.csv"

# Where ML training stores the model & report
MODEL_PATH = ROOT / "model.joblib"
REPORT_PATH = ROOT / "report.json"

# JSON file storing the list of model features
FEATURE_COLUMNS_PATH = ROOT / "feature_columns.json"

# Alias for backward compatibility (ml.py expects this name)
FEATURE_COLS_PATH = FEATURE_COLUMNS_PATH

# -------------------------------------------------------------------
# The column used as label for supervised training
# -------------------------------------------------------------------
LABEL_COLUMN = "risk_label"

# -------------------------------------------------------------------
# Random seed for reproducibility
# -------------------------------------------------------------------
RANDOM_SEED = 1337

# -------------------------------------------------------------------
# Debug helper — prints out paths when called manually
# -------------------------------------------------------------------
def describe_paths() -> None:
    print("[ShadowHound] ROOT =", ROOT)
    print("[ShadowHound] DATA_DIR =", DATA_DIR)
    print("[ShadowHound] RAW_DIR =", RAW_DIR)
    print("[ShadowHound] PROCESSED_DIR =", PROCESSED_DIR)
    print("[ShadowHound] SNAPSHOT_PATH =", SNAPSHOT_PATH)
    print("[ShadowHound] FEATURES_PATH =", FEATURES_PATH)
    print("[ShadowHound] MODEL_PATH =", MODEL_PATH)
    print("[ShadowHound] REPORT_PATH =", REPORT_PATH)
    print("[ShadowHound] FEATURE_COLUMNS_PATH =", FEATURE_COLUMNS_PATH)

if __name__ == "__main__":
    describe_paths()
