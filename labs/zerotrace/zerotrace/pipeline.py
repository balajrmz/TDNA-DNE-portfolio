"""
Runtime prediction pipeline for ZeroTrace.

In plain English:
- Load the trained model from disk.
- Take a single process snapshot (one row of features).
- Align it to the training feature order.
- Ask the model for a prediction + confidence.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

import joblib
import numpy as np
import pandas as pd

from .config import MODEL_PATH, FEATURE_COLUMNS, MODEL_CLASSES


# Global caches so we only load once
_MODEL = None
_FEATURE_ORDER = FEATURE_COLUMNS  # Same order we used when training.


def load_model() -> Any:
    """
    Load the trained model from disk (once) and cache it.

    In plain English:
    - If we've already loaded the model, reuse it.
    - Otherwise, read model.joblib from disk.
    """
    global _MODEL

    if _MODEL is not None:
        return _MODEL

    model_path = Path(MODEL_PATH)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at: {model_path}")

    _MODEL = joblib.load(model_path)
    return _MODEL


def build_feature_frame(sample: Dict[str, Any]) -> pd.DataFrame:
    """
    Turn a flat dict of process features into a pandas DataFrame
    that matches the training-time feature layout.

    Steps (plain English):
    - Wrap the dict in a one-row DataFrame.
    - Add any missing feature columns and fill them with 0.
    - Drop any extra keys we don't use for the model.
    - Force everything to numeric, replacing bad values with 0.
    """
    df = pd.DataFrame([sample])  # one row

    # Add missing columns
    for col in _FEATURE_ORDER:
        if col not in df.columns:
            df[col] = 0.0

    # Drop columns the model doesn't know about
    df = df[_FEATURE_ORDER]

    # Coerce to numeric, fill NaNs with zero
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    return df


def predict_sample(sample: Dict[str, Any]) -> Dict[str, Any]:
    """
    High-level helper: take a feature dict and return prediction details.

    Returns:
        {
          "class_index": 2,
          "class_label": "ransomware_like",
          "confidence": 0.91,
          "probs": {
             "benign": 0.02,
             "infostealer_like": 0.03,
             "ransomware_like": 0.91,
             "injected_loader": 0.04
          }
        }
    """
    model = load_model()
    X = build_feature_frame(sample)

    # Predict class and per-class probabilities
    proba = model.predict_proba(X)[0]  # one row => 1D array
    class_idx = int(np.argmax(proba))

    # Map numeric index back to friendly label
    class_label = MODEL_CLASSES[class_idx]

    # Build probability dict with friendly keys
    probs_by_name = {
        MODEL_CLASSES[i]: float(p) for i, p in enumerate(proba)
    }

    return {
        "class_index": class_idx,
        "class_label": class_label,
        "confidence": float(proba[class_idx]),
        "probs": probs_by_name,
    }
