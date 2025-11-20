"""
features.py
ZeroTrace – Feature extraction from synthetic (or real) memory snapshots.

This module converts raw memory snapshot CSVs into ML-ready features.
"""

from __future__ import annotations
import pandas as pd
import numpy as np
from pathlib import Path
from zerotrace.config import SNAPSHOT_PATH, FEATURES_PATH


def load_snapshot(path: str | Path | None = None) -> pd.DataFrame:
    """
    Load a raw memory snapshot CSV.
    """
    if path is None:
        path = SNAPSHOT_PATH
    return pd.read_csv(path)


def compute_entropy(values: pd.Series) -> float:
    """
    Shannon entropy of a numerical distribution.
    """
    counts = values.value_counts(normalize=True)
    return float(-np.sum(counts * np.log2(counts + 1e-9)))


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts a memory snapshot dataframe into a ML feature row.
    """
    features = {}

    # === 1. Basic Metrics ===
    features["num_records"] = len(df)
    features["unique_processes"] = df["process_id"].nunique()
    features["unique_threads"] = df["thread_id"].nunique()

    # === 2. Memory Behavior Stats ===
    features["avg_mem_access"] = df["mem_access"].mean()
    features["std_mem_access"] = df["mem_access"].std()
    features["max_mem_access"] = df["mem_access"].max()

    # === 3. Kernel Call Patterns ===
    features["avg_kernel_calls"] = df["kernel_calls"].mean()
    features["suspicious_kernel_ops"] = (df["kernel_calls"] > 50).sum()

    # === 4. Entropy-Based Anomaly Detection ===
    features["mem_entropy"] = compute_entropy(df["mem_access"])
    features["kernel_entropy"] = compute_entropy(df["kernel_calls"])

    # === 5. Derived Features ===
    features["access_variation"] = (
        df["mem_access"].rolling(5).std().fillna(0).mean()
    )

    features["rapid_thread_spikes"] = (
        df["thread_id"].diff().abs().fillna(0) > 10
    ).sum()

    features["high_priv_mem_access"] = (
        df["privilege_level"] * df["mem_access"]
    ).mean()

    return pd.DataFrame([features])


def save_features(
    features_df: pd.DataFrame,
    path: str | Path | None = None
) -> str:
    """
    Save extracted feature dataframe to CSV.
    """
    if path is None:
        path = FEATURES_PATH

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)

    features_df.to_csv(out, index=False)
    return str(out)


def run_feature_pipeline() -> str:
    """
    Full load → extract → save pipeline.
    """
    df = load_snapshot()
    feat = extract_features(df)
    output_path = save_features(feat)
    print(f"[ZeroTrace] Saved extracted features to: {output_path}")
    return output_path


if __name__ == "__main__":
    run_feature_pipeline()
