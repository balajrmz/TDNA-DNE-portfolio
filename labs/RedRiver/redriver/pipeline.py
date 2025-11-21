"""
Training pipeline for RedRiver.

This script:

1. Loads the synthetic flows CSV.
2. Computes per-flow features.
3. Saves the feature matrix to disk.
4. Trains the RandomForest model.
5. Saves the model, feature column order, and a simple metrics report.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from redriver.config import (
    FLOWS_PATH,
    FEATURES_PATH,
    MODEL_PATH,
    REPORT_PATH,
    FEATURE_COLUMNS_PATH,
    LABEL_COLUMN,
    RANDOM_SEED,
)

# ---------------------------------------------------------------------
# 1. Load raw flows
# ---------------------------------------------------------------------


def load_flows(path: Path | str = FLOWS_PATH) -> pd.DataFrame:
    print(f"[RedRiver][Pipeline] Loading raw flows from: {path}")
    return pd.read_csv(path)


# ---------------------------------------------------------------------
# 2. Compute features from flows
# ---------------------------------------------------------------------


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple feature engineering for network flows.

    Assumes df has columns:
      src_ip, dst_ip, src_port, dst_port, protocol,
      duration, bytes_sent, bytes_received, packets, label
    """

    feats = pd.DataFrame(index=df.index)

    # Basic numeric features
    feats["duration"] = df["duration"]
    feats["bytes_total"] = df["bytes_sent"] + df["bytes_received"]
    feats["pkts"] = df["packets"]

    # Ratios and flags
    feats["bytes_per_pkt"] = feats["bytes_total"] / (feats["pkts"] + 1e-3)
    feats["is_tcp"] = (df["protocol"] == "TCP").astype(int)
    feats["is_udp"] = (df["protocol"] == "UDP").astype(int)

    # Port buckets: well-known vs high ports
    feats["dst_port_high"] = (df["dst_port"] >= 1024).astype(int)
    feats["dst_port_80"] = (df["dst_port"] == 80).astype(int)
    feats["dst_port_443"] = (df["dst_port"] == 443).astype(int)

    # Copy the label column through so we can train supervised
    feats[LABEL_COLUMN] = df[LABEL_COLUMN]

    print(f"[RedRiver][Pipeline] Feature matrix shape: {feats.shape}")
    return feats


# ---------------------------------------------------------------------
# 3. Train model on features
# ---------------------------------------------------------------------


def split_features_labels(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    X = df.drop(columns=[LABEL_COLUMN])
    y = df[LABEL_COLUMN]
    return X, y


def train_model(X: pd.DataFrame, y: pd.Series):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )

    print("[RedRiver][Pipeline] Training RandomForest classifier...")
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    print(f"[RedRiver][Pipeline] Accuracy: {acc:.4f}")
    return clf, {"accuracy": acc, "classification_report": report}


# ---------------------------------------------------------------------
# 4. Save artifacts
# ---------------------------------------------------------------------


def save_artifacts(model, metrics: dict, feature_cols: list[str]) -> None:
    # Model
    joblib.dump(model, MODEL_PATH)
    # Metrics + feature list
    payload = {
        "metrics": metrics,
        "feature_columns": feature_cols,
    }
    with open(REPORT_PATH, "w") as f:
        json.dump(payload, f, indent=2)
    with open(FEATURE_COLUMNS_PATH, "w") as f:
        json.dump(feature_cols, f, indent=2)

    print(f"[RedRiver][ML] Saved model to:         {MODEL_PATH}")
    print(f"[RedRiver][ML] Saved report to:        {REPORT_PATH}")
    print(f"[RedRiver][ML] Saved feature columns:  {FEATURE_COLUMNS_PATH}")


# ---------------------------------------------------------------------
# 5. Top-level training pipeline
# ---------------------------------------------------------------------


def run_training_pipeline() -> None:
    print("[RedRiver][ML] ===== Starting Training Pipeline =====")

    # 1) Load flows
    df_flows = load_flows(FLOWS_PATH)

    # 2) Compute features
    df_feats = compute_features(df_flows)

    # 3) Save features to disk for debugging / inspection
    FEATURES_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_feats.to_csv(FEATURES_PATH, index=False)
    print(f"[RedRiver][ML] Saved feature matrix to: {FEATURES_PATH}")

    # 4) Train model
    X, y = split_features_labels(df_feats)
    feature_cols = list(X.columns)
    model, metrics = train_model(X, y)

    # 5) Save artifacts
    save_artifacts(model, metrics, feature_cols)

    print("[RedRiver][ML] ===== Training Pipeline Complete =====")


if __name__ == "__main__":
    # Allow:  python -m redriver.pipeline
    run_training_pipeline()
