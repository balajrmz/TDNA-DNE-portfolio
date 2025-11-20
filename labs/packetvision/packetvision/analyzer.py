"""
High-level analyzer for PacketVision.

In plain English:
- This file connects all the building blocks:
    * parse PCAPs into flows
    * build numeric features
    * run rule-based detections
    * run the ML model (if available)
- It returns a single JSON-friendly dictionary that our API can send back.

Think of this as the "orchestrator" for PacketVision.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import os

import pandas as pd

from .config import RAW_PCAP_DIR, MODEL_PATH, FEATURE_COLUMNS_PATH
from .parser import parse_pcap_to_flows
from .features import build_features
from .rules import analyze_flows_with_rules
from .ml import (
    load_model,
    load_feature_columns,
    align_features_for_inference,
    predict_flows,
)


def _ml_available() -> bool:
    """
    Check if the ML artifacts exist on disk.

    In plain English:
    - Before we try to load a model, make sure the files are actually there.
    """
    return MODEL_PATH.exists() and FEATURE_COLUMNS_PATH.exists()


def _summarize_ml_predictions(flow_predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize ML predictions into simple counts per label.

    In plain English:
    - If we classified 100 flows, it's useful to see:
        * how many are benign
        * how many look like port scans
        * how many look like bruteforce, etc.
    """
    summary: Dict[str, int] = {}

    for pred in flow_predictions:
        label = pred.get("predicted_label", "unknown")
        summary[label] = summary.get(label, 0) + 1

    return {
        "num_flows_scored": len(flow_predictions),
        "label_counts": summary,
    }


def analyze_pcap(pcap_path: str | Path) -> Dict[str, Any]:
    """
    Full analysis pipeline for a single PCAP file.

    Steps (plain English):
    1. Parse the PCAP into flows.
    2. Run rule-based detections on the flows.
    3. Build numeric features from the flows.
    4. If an ML model is available, run it on the features.
    5. Return a combined report.

    Parameters
    ----------
    pcap_path : str or Path
        Path to a .pcap file on disk.

    Returns
    -------
    dict
        JSON-friendly structure with:
            - flows_count
            - rule_based (risk_level, findings, etc.)
            - ml_based (flow-level predictions + summary)
    """

    pcap_path = str(pcap_path)

    # 1) Parse PCAP into flow-level stats.
    flows_df: pd.DataFrame = parse_pcap_to_flows(pcap_path)
    num_flows = int(flows_df.shape[0])

    # 2) Run rule-based detections.
    rule_result = analyze_flows_with_rules(flows_df)

    # 3) Build numeric features from the flows.
    features_df = build_features(flows_df)

    ml_flow_predictions: List[Dict[str, Any]] = []
    ml_summary: Dict[str, Any] = {
        "num_flows_scored": 0,
        "label_counts": {},
    }

    # 4) Run the ML model if we have one and have features to score.
    if _ml_available() and not features_df.empty:
        model = load_model(MODEL_PATH)
        feature_columns = load_feature_columns(FEATURE_COLUMNS_PATH)
        X_aligned = align_features_for_inference(features_df, feature_columns)
        ml_flow_predictions = predict_flows(model, X_aligned)
        ml_summary = _summarize_ml_predictions(ml_flow_predictions)
    else:
        # ML model not found or no flows → we just skip ML.
        pass

    report: Dict[str, Any] = {
        "pcap_path": os.path.basename(pcap_path),
        "num_flows": num_flows,
        "rule_based": rule_result,
        "ml_based": {
            "summary": ml_summary,
            "per_flow": ml_flow_predictions,
        },
    }

    return report
