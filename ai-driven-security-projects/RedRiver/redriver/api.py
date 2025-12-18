# redriver/api.py

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import json
import numpy as np

from redriver.config import (
    MODEL_PATH,
    FEATURE_COLUMNS_PATH,
)

# ---------------------------------------------------------
# Load model + column order + label decoder
# ---------------------------------------------------------

MODEL = joblib.load(MODEL_PATH)

with open(FEATURE_COLUMNS_PATH, "r") as f:
    meta = json.load(f)

# Support both:
#  - {"feature_columns": [...], "label_decoder": {...}}
#  - or (older) ["col1", "col2", ...]
if isinstance(meta, dict) and "feature_columns" in meta:
    FEATURE_COLUMNS = meta["feature_columns"]
    LABEL_DECODER = meta.get("label_decoder", {})
else:
    FEATURE_COLUMNS = meta
    LABEL_DECODER = {}

# Normalize decoder so keys are strings
LABEL_DECODER = {str(k): v for k, v in LABEL_DECODER.items()}


def decode_label(idx: int) -> str:
    """Map model class index → human-readable label (e.g., 'benign')."""
    return LABEL_DECODER.get(str(idx), str(idx))


# Model classes (these are the integer codes we trained on)
CLASS_INDEXES = [int(i) for i in MODEL.classes_]
CLASS_NAMES = [decode_label(i) for i in CLASS_INDEXES]

# ---------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------

app = FastAPI(
    title="RedRiver Network Flow Classifier",
    description="AI-driven network flow scoring engine",
    version="1.0.0",
)


# ---------------------------------------------------------
# Request Schema
# ---------------------------------------------------------


class FlowInput(BaseModel):
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str  # "tcp" or "udp"
    duration: float
    bytes_sent: int
    bytes_received: int
    packets: int


# ---------------------------------------------------------
# Helper: convert raw flow → feature vector
# (MUST match redriver.features.compute_features)
# ---------------------------------------------------------


def build_features(flow: FlowInput) -> np.ndarray:
    """
    Re-implement the same feature engineering done in redriver.features.compute_features
    so online scoring uses the exact same columns and semantics as training.
    """

    proto = flow.protocol.lower()

    # Base numeric / derived fields
    bytes_total = flow.bytes_sent + flow.bytes_received

    base = {
        # raw fields (note: IPs were dropped during training, so they won't be used
        # unless FEATURE_COLUMNS explicitly contain them)
        "src_ip": flow.src_ip,
        "dst_ip": flow.dst_ip,
        "src_port": flow.src_port,
        "dst_port": flow.dst_port,
        "duration": flow.duration,
        "bytes_sent": flow.bytes_sent,
        "bytes_received": flow.bytes_received,
        "packets": flow.packets,
        # protocol one-hot
        "proto_tcp": 1 if proto == "tcp" else 0,
        "proto_udp": 1 if proto == "udp" else 0,
        # engineered features (must mirror redriver.features)
        "kb_sent": flow.bytes_sent / 1024.0,
        "kb_received": flow.bytes_received / 1024.0,
        "bytes_total": bytes_total,
        "rate_packets": flow.packets / (flow.duration + 0.1),
        "rate_bytes": bytes_total / (flow.duration + 0.1),
        "src_port_privileged": 1 if flow.src_port < 1024 else 0,
        "dst_port_privileged": 1 if flow.dst_port < 1024 else 0,
    }

    # Assemble vector in the exact column order the model expects
    vector = []
    for col in FEATURE_COLUMNS:
        value = base.get(col, 0.0)  # default 0.0 for any missing fields
        vector.append(value)

    return np.array(vector, dtype=float).reshape(1, -1)


# ---------------------------------------------------------
# Healthcheck Endpoint
# ---------------------------------------------------------


@app.get("/health")
async def health():
    """
    Lightweight health endpoint for uptime checks.
    """
    return {
        "status": "ok",
        "model_loaded": MODEL is not None,
        "n_features": int(len(FEATURE_COLUMNS)),
        "classes": CLASS_NAMES,
    }


# ---------------------------------------------------------
# Prediction Endpoint
# ---------------------------------------------------------


@app.post("/predict")
async def predict(flow: FlowInput):
    # Build vector in correct order
    X = build_features(flow)

    # Model prediction (integer class index)
    raw_pred = MODEL.predict(X)[0]
    pred_idx = int(raw_pred)
    pred_label = decode_label(pred_idx)

    # Probabilities over all known classes
    prob_arr = MODEL.predict_proba(X)[0]
    # prob_arr is a numpy array; convert to Python floats
    probs = {
        decode_label(int(cls_idx)): float(p)
        for cls_idx, p in zip(CLASS_INDEXES, prob_arr)
    }

    # Confidence for the predicted class
    pred_pos = CLASS_INDEXES.index(pred_idx)
    confidence = float(prob_arr[pred_pos])

    return {
        "input": flow.model_dump(),
        "prediction": {
            "class_label": pred_label,
            "class_index": int(pred_idx),
            "confidence": confidence,
            "probs": {k: float(v) for k, v in probs.items()},
        },
        "model_info": {
            "feature_columns_used": list(FEATURE_COLUMNS),
            "class_indexes": [int(x) for x in CLASS_INDEXES],
            "class_names": CLASS_NAMES,
        },
    }
