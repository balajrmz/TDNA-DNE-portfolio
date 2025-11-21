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
# Load model + column order
# ---------------------------------------------------------

MODEL = joblib.load(MODEL_PATH)

with open(FEATURE_COLUMNS_PATH, "r") as f:
    FEATURE_COLUMNS = json.load(f)

# Your class names (in the order the model was trained)
CLASS_NAMES = ["benign", "port_scan_like", "brute_force_like"]

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
    protocol: str
    duration: float
    bytes_sent: int
    bytes_received: int
    packets: int


# ---------------------------------------------------------
# Helper: convert raw flow → feature vector
# (MUST match training feature logic exactly)
# ---------------------------------------------------------

def build_features(flow: FlowInput):

    # Basic numerical features that existed in the CSV
    protocol_map = {"TCP": 6, "UDP": 17, "ICMP": 1}
    proto_numeric = protocol_map.get(flow.protocol.upper(), 0)

    feat = {
        "src_ip": int(flow.src_ip.split(".")[3]),       # last octet only
        "dst_ip": int(flow.dst_ip.split(".")[3]),
        "src_port": flow.src_port,
        "dst_port": flow.dst_port,
        "protocol": proto_numeric,
        "duration": flow.duration,
        "bytes_sent": flow.bytes_sent,
        "bytes_received": flow.bytes_received,
        "packets": flow.packets,
    }

    # Arrange in correct ML column order
    vector = [feat[col] for col in FEATURE_COLUMNS]

    return np.array(vector).reshape(1, -1)


# ---------------------------------------------------------
# Prediction Endpoint
# ---------------------------------------------------------

@app.post("/predict")
async def predict(flow: FlowInput):

    # Build vector in correct order
    X = build_features(flow)

    # Model prediction
    pred_idx = int(MODEL.predict(X)[0])
    pred_label = CLASS_NAMES[pred_idx]

    # Probabilities
    probs_arr = MODEL.predict_proba(X)[0]
    probs = {CLASS_NAMES[i]: float(probs_arr[i]) for i in range(len(CLASS_NAMES))}

    # Confidence = highest probability
    confidence = float(probs_arr[pred_idx])

    return {
        "input": flow.model_dump(),
        "prediction": {
            "class_label": pred_label,
            "class_index": pred_idx,
            "confidence": confidence,
            "probs": probs,
        },
        "model_info": {
            "feature_columns_used": FEATURE_COLUMNS,
            "num_classes": len(CLASS_NAMES)
        }
    }
