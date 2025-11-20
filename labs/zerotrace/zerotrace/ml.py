"""
ml.py

ZeroTrace – Model training module.

In plain English:
- Load the processed features (X) and labels (y).
- Split into train and validation sets.
- Train a RandomForest classifier to detect suspicious processes.
- Save the model, feature column order, and a training report to disk.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# Import paths and feature definitions from our config file
from .config import (
    FEATURES_PATH,
    MODEL_PATH,
    FEATURE_COLUMNS_PATH,
    FEATURE_COLUMNS,
    REPORT_PATH,
)

# Reuse the feature pipeline so we can regenerate features if needed
from .features import run_feature_pipeline


def load_features(path: str | Path | None = None) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Load features and labels from the CSV file.

    In plain English:
    - Read the processed features CSV we created earlier.
    - Split it into:
      * X: numeric feature columns used by the model.
      * y: the label column (0 = benign, 1 = suspicious, etc.).
    """
    if path is None:
        path = FEATURES_PATH

    path = Path(path)

    # If the features file does not exist yet, run the feature pipeline first.
    if not path.exists():
        print("[ZeroTrace] Features file not found – running feature pipeline...")
        run_feature_pipeline()

    df = pd.read_csv(path)

    # X = feature matrix (only the columns we declared in FEATURE_COLUMNS)
    X = df[FEATURE_COLUMNS].copy()

    # y = labels – we saved them under the 'label' column
    if "label" not in df.columns:
        raise ValueError("Features file is missing the 'label' column.")
    y = df["label"].copy()

    print(f"[ZeroTrace] Loaded features from: {path}")
    print(f"[ZeroTrace] Feature matrix shape: {X.shape}")
    return X, y


def train_model(
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[RandomForestClassifier, dict]:
    """
    Train a RandomForest classifier on ZeroTrace features.

    Steps:
    1. Load X (features) and y (labels).
    2. Split into train and validation sets.
    3. Fit a RandomForest model.
    4. Evaluate it and build a training report dictionary.

    Returns:
    - model: the trained RandomForestClassifier instance.
    - report: a Python dict with metrics and metadata.
    """
    X, y = load_features()

    # --- 1. Train/validation split ---
    # We use stratify=y so class balance is preserved in both sets.
    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    print(f"[ZeroTrace] Training samples: {len(y_train)}")
    print(f"[ZeroTrace] Validation samples: {len(y_val)}")

    # --- 2. Define the model ---
    # RandomForest is a solid, interpretable baseline for tabular data.
    model = RandomForestClassifier(
        n_estimators=200,        # number of trees
        n_jobs=-1,               # use all CPU cores
        class_weight="balanced", # handle class imbalance
        random_state=random_state,
    )

    # --- 3. Train the model ---
    print("[ZeroTrace] Training RandomForest model...")
    model.fit(X_train, y_train)

    # --- 4. Evaluate on validation set ---
    y_pred = model.predict(X_val)

    # classification_report gives precision/recall/F1 per class
    clf_report = classification_report(
        y_val,
        y_pred,
        output_dict=True,
        zero_division=0,
    )

    # confusion_matrix shows how many samples are confused between classes
    cm = confusion_matrix(y_val, y_pred).tolist()

    # --- 5. Build a training report dict ---
    report: dict = {
        "n_samples": int(len(y)),
        "n_features": len(FEATURE_COLUMNS),
        "classes": sorted([int(c) for c in np.unique(y)]),
        "classification_report": clf_report,
        "confusion_matrix": cm,
        "feature_importances": {
            name: float(imp)
            for name, imp in zip(FEATURE_COLUMNS, model.feature_importances_)
        },
    }

    return model, report


def save_artifacts(model: RandomForestClassifier, report: dict) -> None:
    """
    Save the trained model, feature column order, and training report to disk.

    In plain English:
    - model.joblib           -> the fitted RandomForest model.
    - feature_columns.json   -> list of feature names in the order the model expects.
    - report.json            -> metrics + feature importance for documentation.
    """
    # Ensure parent directories exist
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEATURE_COLUMNS_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 1) Save model
    joblib.dump(model, MODEL_PATH)
    print(f"[ZeroTrace] Saved model to: {MODEL_PATH}")

    # 2) Save feature column order
    with open(FEATURE_COLUMNS_PATH, "w", encoding="utf-8") as f:
        json.dump(FEATURE_COLUMNS, f, indent=2)
    print(f"[ZeroTrace] Saved feature columns to: {FEATURE_COLUMNS_PATH}")

    # 3) Save training report
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"[ZeroTrace] Saved training report to: {REPORT_PATH}")


def run_training_pipeline() -> None:
    """
    High-level helper: run the full training pipeline.

    Steps:
    - Load features.
    - Train the model.
    - Save all artifacts.
    """
    model, report = train_model()
    save_artifacts(model, report)
    print("[ZeroTrace] Training pipeline complete.")


if __name__ == "__main__":
    # Allow running via:
    #   python -m zerotrace.ml
    run_training_pipeline()
