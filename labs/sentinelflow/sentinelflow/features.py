"""
Feature engineering utilities.

This file is responsible for:
- Loading raw CSV network data
- Building numeric features the model can understand
- Handling basic encoding for categorical fields
"""

from typing import Tuple
import pandas as pd

# Columns that are useful as-is for numbers
NUMERIC_COLS = ["bytes_in", "bytes_out", "packet_count"]

# Columns that are text-like and need encoding
CATEGORICAL_COLS = ["protocol", "dst_port"]


def load_raw(path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    In plain English:
    - Take the path to a CSV file on disk
    - Read it into memory as a table we can work with
    """
    return pd.read_csv(path)


def build_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Turn raw network-event data into model-ready features.

    Steps in plain English:
    1. Start from the original columns.
    2. Create a 'byte_ratio' feature that compares inbound vs outbound bytes.
       This sometimes highlights DoS-style attacks (lots of inbound).
    3. One-hot encode categorical values (like protocol) so the model
       can understand them as numbers.
    4. Return:
       - X: table of numbers for the model
       - y: the labels (normal / scan / dos), if present
    """
    df = df.copy()

    # Simple defensive programming: if label doesn't exist, create a dummy one
    if "label" not in df.columns:
        df["label"] = "unknown"

    # New numeric feature comparing in vs out traffic.
    df["byte_ratio"] = (df["bytes_in"] + 1) / (df["bytes_out"] + 1)

    # Select columns we care about for the model.
    feature_cols = NUMERIC_COLS + ["byte_ratio"] + CATEGORICAL_COLS
    features = df[feature_cols].copy()

    # One-hot encode protocol and dst_port so the model gets 0/1 columns
    # instead of raw strings or integers treated like continuous values.
    features = pd.get_dummies(features, columns=CATEGORICAL_COLS, drop_first=True)

    # Target labels (normal / scan / dos)
    y = df["label"]

    return features, y

