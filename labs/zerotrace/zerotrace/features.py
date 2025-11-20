"""
Feature extraction pipeline for ZeroTrace.

This script:
- Loads the synthetic process snapshot (raw memory/process info)
- Extracts numeric features the ML model will train on
- Normalizes the `label` column to integers (0..N-1) based on MODEL_CLASSES
- Saves the final feature matrix to CSV
"""

import pandas as pd
from pathlib import Path

from .config import (
    SNAPSHOT_PATH,
    FEATURES_PATH,
    FEATURE_COLUMNS,
    MODEL_CLASSES,
)

# -------------------------------------------------------
# 1. Load raw snapshot (memory/process info)
# -------------------------------------------------------

def load_snapshot() -> pd.DataFrame:
    """
    Load the synthetic snapshot CSV produced by zerotrace.synthetic.
    Ensures the 'label' column exists.
    """
    if not Path(SNAPSHOT_PATH).exists():
        raise FileNotFoundError(f"Snapshot file not found at: {SNAPSHOT_PATH}")

    df = pd.read_csv(SNAPSHOT_PATH)

    if "label" not in df.columns:
        raise ValueError(
            "Snapshot is missing the 'label' column.\n"
            "Make sure synthetic.py assigns 'label' (or family) to each process."
        )

    return df


# -------------------------------------------------------
# 2. Extract only the ML feature columns
# -------------------------------------------------------

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract numeric features from the raw snapshot.
    FEATURE_COLUMNS is defined in config.py.

    Also:
    - Converts the label column to integer class IDs based on MODEL_CLASSES.
    """

    # --- check feature columns ---
    missing = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")

    # Main numeric feature matrix
    features_df = df[FEATURE_COLUMNS].copy()

    # --- normalize label column ---
    raw_labels = df["label"]

    # If labels are strings like "benign", map them to integers via MODEL_CLASSES
    if raw_labels.dtype == object:
        family_to_label = {name: idx for idx, name in enumerate(MODEL_CLASSES)}
        labels = raw_labels.map(family_to_label)

        if labels.isna().any():
            bad_values = raw_labels[labels.isna()].unique()
            raise ValueError(
                f"Found unknown label values {bad_values}. "
                f"Expected one of: {list(family_to_label.keys())}"
            )
    else:
        # Already numeric – just ensure they're integers
        labels = raw_labels.astype(int)

    features_df["label"] = labels.values

    return features_df


# -------------------------------------------------------
# 3. Save final feature matrix
# -------------------------------------------------------

def save_features(df: pd.DataFrame, path: str = FEATURES_PATH) -> str:
    """
    Save the feature matrix (plus label) to disk.
    """
    out_path = Path(path)

    # Ensure parent directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(out_path, index=False)
    return str(out_path)


# -------------------------------------------------------
# 4. Combined pipeline (CLI entrypoint)
# -------------------------------------------------------

def run_feature_pipeline() -> None:
    """
    High-level entrypoint. Creates the feature CSV ready for ML training.
    """
    print("[ZeroTrace] Loading snapshot...")
    df = load_snapshot()

    print("[ZeroTrace] Extracting features...")
    features_df = extract_features(df)

    print(f"[ZeroTrace] Feature matrix shape: {features_df.shape}")

    out = save_features(features_df)

    print(f"[ZeroTrace] Saved features to: {out}")


if __name__ == "__main__":
    run_feature_pipeline()
