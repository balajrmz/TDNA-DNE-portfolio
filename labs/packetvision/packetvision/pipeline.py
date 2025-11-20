"""
Training pipeline for PacketVision.

In plain English:
- This script generates synthetic flow data for different traffic behaviors.
- It turns those flows into numeric features.
- It trains a RandomForest classifier to recognize those behaviors.
- It saves the model and metadata (feature columns, training report) to disk.

This gives us a repeatable way to build a model WITHOUT needing real PCAPs
in the repository.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

import json
import random
import time

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from .config import (
    PROCESSED_DIR,
    FEATURES_CSV_PATH,
    MODEL_PATH,
    REPORT_PATH,
    FEATURE_COLUMNS_PATH,
)
from .features import build_features
from .ml import (
    train_packetvision_model,
    save_model,
    save_feature_columns,
)


# ---------------------------------------------------------------------------
# Synthetic flow generation
# ---------------------------------------------------------------------------

def _random_ip() -> str:
    """
    Generate a simple random IPv4 address.

    In plain English:
    - This is just for synthetic training data, not for real networking.
    """
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def _make_behavior_flows(label: str, n: int) -> pd.DataFrame:
    """
    Create synthetic flows for a specific behavior.

    Behaviors:
        - "benign"        : normal web/DNS traffic
        - "port_scan"     : many short-lived flows to many ports
        - "bruteforce"    : intense traffic to admin ports (22, 3389, 445)
        - "dns_tunnel"    : heavy DNS (port 53) flows

    In plain English:
    - We don't need perfect realism; we just need patterns that are
      different enough for the model to learn from.
    """

    rows: List[Dict[str, Any]] = []

    for _ in range(n):
        src_ip = _random_ip()
        dst_ip = _random_ip()

        if label == "benign":
            # Web / DNS-like traffic.
            dst_port = random.choice([80, 443, 8080, 53])
            protocol = random.choice(["TCP", "UDP"])
            packet_count = random.randint(5, 50)
            total_bytes = random.randint(1_000, 50_000)
            duration = random.uniform(0.5, 10.0)

        elif label == "port_scan":
            # Very short flows to lots of different destination ports.
            dst_port = random.randint(1, 1024)
            protocol = "TCP"
            packet_count = random.randint(1, 3)
            total_bytes = random.randint(60, 600)
            duration = random.uniform(0.01, 0.5)

        elif label == "bruteforce":
            # Lots of traffic to typical admin ports.
            dst_port = random.choice([22, 3389, 445])
            protocol = "TCP"
            packet_count = random.randint(20, 200)
            total_bytes = random.randint(10_000, 300_000)
            duration = random.uniform(2.0, 60.0)

        elif label == "dns_tunnel":
            # High-volume DNS-like traffic (covert channel).
            dst_port = 53
            protocol = "UDP"
            packet_count = random.randint(50, 800)
            total_bytes = random.randint(100_000, 2_000_000)
            duration = random.uniform(5.0, 120.0)

        else:
            # Fallback: treat as benign if unknown.
            dst_port = random.choice([80, 443, 8080])
            protocol = "TCP"
            packet_count = random.randint(5, 50)
            total_bytes = random.randint(1_000, 50_000)
            duration = random.uniform(0.5, 10.0)

        # Simple timestamps: pretend flows happen at random times.
        start_time = time.time() + random.uniform(-3600, 0)
        end_time = start_time + duration
        avg_pkt_size = total_bytes / packet_count if packet_count > 0 else 0.0

        row = {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": random.randint(1024, 65535),
            "dst_port": dst_port,
            "protocol": protocol,
            "packet_count": packet_count,
            "total_bytes": total_bytes,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "avg_packet_size": avg_pkt_size,
            "label": label,
        }
        rows.append(row)

    return pd.DataFrame(rows)


def generate_synthetic_dataset(
    n_benign: int = 2000,
    n_port_scan: int = 600,
    n_bruteforce: int = 400,
    n_dns_tunnel: int = 400,
) -> pd.DataFrame:
    """
    Generate a full synthetic dataset with multiple behaviors.

    In plain English:
    - We create several groups of flows with different statistical patterns.
    - We label each row with the behavior type.
    """

    benign_df = _make_behavior_flows("benign", n_benign)
    scan_df = _make_behavior_flows("port_scan", n_port_scan)
    brute_df = _make_behavior_flows("bruteforce", n_bruteforce)
    dns_df = _make_behavior_flows("dns_tunnel", n_dns_tunnel)

    all_flows = pd.concat([benign_df, scan_df, brute_df, dns_df], ignore_index=True)
    return all_flows


# ---------------------------------------------------------------------------
# Main training entrypoint
# ---------------------------------------------------------------------------

def run_training() -> None:
    """
    End-to-end training pipeline.

    Steps (plain English):
    1. Generate synthetic flow-level data for benign + attack behaviors.
    2. Build numeric features from those flows.
    3. Split into train/validation sets.
    4. Train a RandomForest classifier.
    5. Save the model, feature column list, and a training report.
    """

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Generate synthetic flows.
    flows = generate_synthetic_dataset()
    # Separate labels from raw flow columns.
    y = flows["label"]
    flows_no_label = flows.drop(columns=["label"])

    # 2) Build numeric features.
    X = build_features(flows_no_label)

    # Optionally save a copy of features to CSV for inspection.
    X_with_label = X.copy()
    X_with_label["label"] = y
    X_with_label.to_csv(FEATURES_CSV_PATH, index=False)

    # 3) Train/validation split.
    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    # 4) Train the model.
    model, metrics = train_packetvision_model(X_train, y_train, X_val, y_val)

    # 5) Save the model and feature column order.
    save_model(model, MODEL_PATH)
    save_feature_columns(list(X.columns), FEATURE_COLUMNS_PATH)

    # 6) Save a training report as JSON.
    report: Dict[str, Any] = {
        "metrics": metrics,
        "num_samples": int(X.shape[0]),
        "labels_distribution": y.value_counts().to_dict(),
    }

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(f"[PacketVision] Training complete.")
    print(f"  Saved model to:          {MODEL_PATH}")
    print(f"  Saved features to:       {FEATURES_CSV_PATH}")
    print(f"  Saved feature columns to:{FEATURE_COLUMNS_PATH}")
    print(f"  Saved report to:         {REPORT_PATH}")


if __name__ == "__main__":
    run_training()

