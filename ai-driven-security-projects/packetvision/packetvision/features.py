"""
Feature engineering for PacketVision.

- This file takes flow-level statistics (one row per flow) and turns them into
  numeric features that a machine learning model can understand.
- We start from the DataFrame returned by parser.parse_pcap_to_flows().
- We add things like:
    * packets per second
    * bytes per second
    * flags for common destination ports (web / DNS / SSH / SMB / RDP)
    * one-hot encoding for protocol (is_tcp / is_udp)
"""

from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd


def _safe_divide(numerator: pd.Series, denominator: pd.Series, eps: float = 1e-6) -> pd.Series:
    """
    Helper for safe division.

    - Avoids division-by-zero.
    - If duration is 0, we divide by a tiny number instead of crashing.
    """
    return numerator / (denominator.replace(0, eps))


def build_features(flows: pd.DataFrame) -> pd.DataFrame:
    """
    Given a DataFrame of flows, compute model-ready features.

    Expected input columns (from parser.parse_pcap_to_flows):
        - src_ip
        - dst_ip
        - src_port
        - dst_port
        - protocol        (values like 'TCP' or 'UDP')
        - packet_count
        - total_bytes
        - start_time
        - end_time
        - duration
        - avg_packet_size

    Returns
    -------
    pd.DataFrame
        A new DataFrame where each row is a flow and each column is a numeric
        feature our model can learn from.

    - We take flow-level stats and derive extra signals (rates, flags, etc.).
    - We drop raw IP strings because they don't generalize for ML.
    - We keep ports and protocol info as numeric flags.
    """

    if flows.empty:
        # Nothing to do; return an empty DataFrame with no columns.
        return pd.DataFrame()

    df = flows.copy()

    # --- Basic rate features -------------------------------------------------
    # packets per second (how "chatty" the flow is)
    df["pkts_per_sec"] = _safe_divide(df["packet_count"], df["duration"])

    # bytes per second (throughput for the flow)
    df["bytes_per_sec"] = _safe_divide(df["total_bytes"], df["duration"])

    # We already have avg_packet_size, but ensure it's numeric.
    df["avg_packet_size"] = df["avg_packet_size"].astype(float)

    # --- Protocol one-hot ----------------------------------------------------
    # Instead of models learning from the string "TCP" or "UDP", we give them
    # explicit numeric columns.
    df["is_tcp"] = (df["protocol"] == "TCP").astype(int)
    df["is_udp"] = (df["protocol"] == "UDP").astype(int)

    # --- Destination port flags ----------------------------------------------
    # Simple flags for common service types.
    dst_port = df["dst_port"].astype(int)

    df["dst_is_web"] = dst_port.isin([80, 443, 8080]).astype(int)
    df["dst_is_dns"] = (dst_port == 53).astype(int)
    df["dst_is_ssh"] = (dst_port == 22).astype(int)
    df["dst_is_smb"] = dst_port.isin([139, 445]).astype(int)
    df["dst_is_rdp"] = (dst_port == 3389).astype(int)

    # Flag for "high" ephemeral ports (could be C2, scanning, or exfil).
    df["dst_high_port"] = (dst_port >= 1024).astype(int)

    # --- Source port flags (optional, but can be useful) ---------------------
    src_port = df["src_port"].astype(int)
    df["src_high_port"] = (src_port >= 1024).astype(int)

    # --- Flow duration buckets (very short vs long-lived) --------------------
    # These are rough buckets that might help distinguish scans vs beacons.
    df["is_short_flow"] = (df["duration"] < 1.0).astype(int)
    df["is_long_flow"] = (df["duration"] > 60.0).astype(int)

    # --- Drop non-ML-friendly columns ---------------------------------------
    # IPs are high-cardinality identifiers; for this portfolio ML model we drop
    # them to avoid overfitting on specific addresses.
    cols_to_drop: List[str] = [
        "src_ip",
        "dst_ip",
        "protocol",
        "start_time",
        "end_time",
    ]
    for col in cols_to_drop:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Ensure consistent column order (sorted by name for reproducibility).
    df = df.reindex(sorted(df.columns), axis=1)

    return df

