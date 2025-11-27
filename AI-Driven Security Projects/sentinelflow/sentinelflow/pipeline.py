"""
Training pipeline for SentinelFlow.

This script:
1. Generates a synthetic dataset that looks like network traffic.
2. Builds ML features from that data.
3. Trains a baseline RandomForest model.
4. Saves the model, metrics, and feature column order to disk.

Run with:
    python -m sentinelflow.pipeline
"""

from pathlib import Path
import json
from typing import Optional

import numpy as np
import pandas as pd
import joblib

from .config import (
    RAW_DATA_PATH,
    MODEL_PATH,
    REPORT_PATH,
    DATA_DIR,
    PROCESSED_DIR,
    FEATURES_PATH,
)
from .features import build_features, load_raw
from .models import train_baseline


def generate_synthetic_data(path: Path, n_samples: int = 5000) -> None:
    """
    Create a synthetic dataset that looks like network flow data.
    """

    rng = np.random.default_rng(seed=42)

    src_ips = [f"10.0.0.{i}" for i in range(1, 21)]
    dst_ips = [f"192.168.1.{i}" for i in range(1, 21)]

    df = pd.DataFrame(
        {
            "src_ip": rng.choice(src_ips, n_samples),
            "dst_ip": rng.choice(dst_ips, n_samples),
            "src_port": rng.integers(1024, 65535, n_samples),
            "dst_port": rng.choice([22, 80, 443, 3389, 8080, 53], n_samples),
            "protocol": rng.choice(["TCP", "UDP"], n_samples),
            "bytes_in": rng.exponential(8000, n_samples).astype(int),
            "bytes_out": rng.exponential(8000, n_samples).astype(int),
            "packet_count": rng.poisson(15, n_samples),
        }
    )

    df["label"] = "normal"

    scan_idx = rng.choice(df.index, size=int(0.06 * n_samples), replace=False)
    df.loc[scan_idx, "packet_count"] *= 5
    df.loc[scan_idx, "label"] = "scan"

    remaining_idx = df.index.difference(scan_idx)
    dos_idx = rng.choice(remaining_idx, size=int(0.04 * n_samples), replace=False)
    df.loc[dos_idx, "bytes_in"] *= 10
    df.loc[dos_idx, "label"] = "dos"

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def run_training(raw_path: Optional[Path] = None) -> None:
    """
    Main training function.
    """
    if raw_path is None:
        raw_path = RAW_DATA_PATH

    if not raw_path.exists():
        generate_synthetic_data(raw_path)

    df = load_raw(str(raw_path))
    X, y = build_features(df)

    model, report = train_baseline(X, y)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    # NEW — SAVE FEATURE COLUMNS
    with open(FEATURES_PATH, "w") as f:
        json.dump(list(X.columns), f, indent=2)


if __name__ == "__main__":
    run_training()
