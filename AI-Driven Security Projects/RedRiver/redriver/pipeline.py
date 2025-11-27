# redriver/pipeline.py

"""
End-to-end training pipeline for RedRiver.

This script:

1. Generates synthetic flow data (flows.csv)
2. Computes per-flow features (features.csv)
3. Trains the RandomForest model
4. Saves model + metrics + feature column metadata

Usage:

    python -m redriver.pipeline
"""

from __future__ import annotations

from redriver.synthetic import run_synthetic_pipeline
from redriver.features import run_feature_pipeline
from redriver.ml import run_training_pipeline


def run_full_pipeline() -> None:
    print("[RedRiver][Pipeline] ===== Starting Full Pipeline =====")

    # 1) Generate synthetic flows
    run_synthetic_pipeline()

    # 2) Compute features from flows
    run_feature_pipeline()

    # 3) Train model on features
    run_training_pipeline()

    print("[RedRiver][Pipeline] ===== Full Pipeline Complete =====")


if __name__ == "__main__":
    run_full_pipeline()
