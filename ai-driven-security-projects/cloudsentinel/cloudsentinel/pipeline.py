"""
CloudSentinel training pipeline.

In plain English:
- This script generates synthetic IAM policies.
- It analyzes each policy with the rule engine + analyzer.
- It builds a feature matrix and labels (risk levels).
- It trains a RandomForest model to predict risk level.
- It saves the model, a training report, and the feature column order.

Run from the CloudSentinel lab root with:

    python -m cloudsentinel.pipeline
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
import json

import joblib
import numpy as np
import pandas as pd

from .config import (
    BASE_DIR,
    DATA_DIR,
    RAW_DATA_PATH,
    PROCESSED_DIR,
    MODEL_PATH,
    REPORT_PATH,
    FEATURES_PATH,
)
from .analyzer import analyze_policy
from .ml import train_baseline


# -----------------------------
# Synthetic policy generation
# -----------------------------


def _make_safe_policy() -> Dict[str, Any]:
    """
    Create a mostly safe, low-risk IAM policy.

    In plain English:
    - No wildcards.
    - Read-only style actions on specific resources.
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "logs:DescribeLogGroups",
                    "logs:GetLogEvents",
                ],
                "Resource": [
                    "arn:aws:s3:::example-bucket/*",
                    "arn:aws:logs:us-east-1:111122223333:log-group:example-group:*",
                ],
            }
        ],
    }


def _make_medium_policy() -> Dict[str, Any]:
    """
    Create a medium-risk policy.

    In plain English:
    - Some wildcard resources or assume-role usage.
    - Not obviously full admin, but needs review.
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["sts:AssumeRole"],
                "Resource": "arn:aws:iam::111122223333:role/ReadOnlyRole",
            },
            {
                "Effect": "Allow",
                "Action": ["s3:ListBucket"],
                "Resource": "*",
            },
        ],
    }


def _make_high_policy() -> Dict[str, Any]:
    """
    Create a high-risk policy.

    In plain English:
    - Includes combinations that can lead to privilege escalation,
      such as iam:PassRole + ec2:RunInstances.
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "iam:PassRole",
                    "ec2:RunInstances",
                ],
                "Resource": "*",
            }
        ],
    }


def _make_critical_policy() -> Dict[str, Any]:
    """
    Create a critical-risk policy.

    In plain English:
    - Wildcard actions and wildcard resources,
      potentially for high-risk services like IAM.
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["*"],
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": ["iam:*"],
                "Resource": "*",
            },
        ],
    }


def generate_synthetic_policies(path: Path, n_samples: int = 200) -> List[Dict[str, Any]]:
    """
    Generate a mixture of synthetic IAM policies and write them to disk.

    We also return the list in memory so the training pipeline can use it
    immediately.

    The JSONL file format is:
        one JSON policy per line.
    """
    rng = np.random.default_rng(seed=42)

    policies: List[Dict[str, Any]] = []

    # We choose different policy "templates" with some probabilities,
    # so we get a mix of risk levels in the dataset.
    for _ in range(n_samples):
        r = rng.random()
        if r < 0.35:
            policy = _make_safe_policy()
        elif r < 0.55:
            policy = _make_medium_policy()
        elif r < 0.8:
            policy = _make_high_policy()
        else:
            policy = _make_critical_policy()

        policies.append(policy)

    # Make sure the raw directory exists.
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write as JSONL so it's easy to inspect or reuse later.
    with path.open("w", encoding="utf-8") as f:
        for p in policies:
            f.write(json.dumps(p))
            f.write("\n")

    return policies


def _load_policies_from_jsonl(path: Path) -> List[Dict[str, Any]]:
    """
    Load policies from a JSONL file created by generate_synthetic_policies().
    """
    policies: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            policies.append(json.loads(line))
    return policies


# -----------------------------
# Training pipeline
# -----------------------------


def run_training(raw_path: Optional[Path] = None) -> None:
    """
    Main training entrypoint.

    Steps in plain English:
    1. Generate or load synthetic IAM policies.
    2. Run the analyzer on each policy to get findings, risk level, and features.
    3. Build a feature matrix X and labels y.
    4. Train a RandomForest model with train_baseline().
    5. Save the model, report, and feature column order.
    """
    if raw_path is None:
        raw_path = RAW_DATA_PATH

    # Ensure base data directories exist.
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load or generate synthetic policies.
    if raw_path.exists():
        policies = _load_policies_from_jsonl(raw_path)
    else:
        policies = generate_synthetic_policies(raw_path, n_samples=200)

    feature_rows: List[Dict[str, Any]] = []
    labels: List[str] = []

    # 2. Run analyzer on each policy.
    for policy in policies:
        # include_features=True gives us:
        # - "risk_level" and "risk_score"
        # - "features" (numeric representation)
        result = analyze_policy(policy, include_features=True)
        feature_rows.append(result["features"])
        labels.append(result["risk_level"])

    # 3. Build X (features) and y (labels) using pandas.
    X = pd.DataFrame(feature_rows)
    y = pd.Series(labels, name="risk_level")

    # 4. Train model.
    model, report = train_baseline(X, y)

    # 5. Save artifacts.
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Save model.
    joblib.dump(model, MODEL_PATH)

    # Save training report as JSON.
    with REPORT_PATH.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Save feature column order so the API can align features at inference time.
    with FEATURES_PATH.open("w", encoding="utf-8") as f:
        json.dump(list(X.columns), f, indent=2)


if __name__ == "__main__":
    # Allow running this file as a script:
    #   python -m cloudsentinel.pipeline
    run_training()

