"""
FastAPI service that exposes the trained model as a REST API.

This lets us send a single network event and get back:
- The predicted label (normal / scan / dos)
- The model's confidence in that prediction
"""

from typing import Optional, List
import json

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from .config import MODEL_PATH, FEATURES_PATH
from .features import build_features

app = FastAPI(
    title="SentinelFlow API",
    description="AI-powered demo service for classifying network flows.",
    version="0.1.0",
)


class FlowSample(BaseModel):
    """
    Schema for one network event coming into the API.

    In plain English:
    - These are the fields a caller must send in JSON.
    - They roughly match the columns in our training data.
    """

    bytes_in: int
    bytes_out: int
    packet_count: int
    protocol: str
    dst_port: int


def _load_model(path: Optional[str] = None):
    """
    Helper to load a trained model from disk.

    We keep it in a function so we can later add caching,
    better error handling, or support for multiple versions.
    """
    if path is None:
        path = str(MODEL_PATH)
    return joblib.load(path)


def _load_feature_columns(path: Optional[str] = None) -> List[str]:
    """
    Load the list of feature columns used during training.

    In plain English:
    - When we trained the model, we saved the list of columns
      (including one-hot encoded ones) to a JSON file.
    - Here we read that list so we can force incoming requests
      to match the same structure and order.
    """
    if path is None:
        path = str(FEATURES_PATH)
    with open(path, "r") as f:
        cols = json.load(f)
    return cols


# Load the model and feature column order once when the API starts.
model = _load_model()
FEATURE_COLUMNS = _load_feature_columns()


@app.get("/health")
def healthcheck():
    """
    Simple health endpoint.

    Returns a tiny JSON response so we know the service is alive.
    """
    return {"status": "ok"}


@app.post("/predict")
def predict(sample: FlowSample):
    """
    Predict the class of a single network event.

    Steps in plain English:
    1. Turn the incoming JSON into a pandas DataFrame.
    2. Run our feature builder so it matches training features.
    3. Align the DataFrame's columns to match the model's expectations.
    4. Ask the model for a predicted label and probability.
    5. Return those to the caller as JSON.
    """

    # Create a one-row table from the incoming JSON.
    df = pd.DataFrame([sample.dict()])

    # The build_features function expects a label column.
    # For inference we don't have one, so we add a dummy value.
    df["label"] = "unknown"

    X, _ = build_features(df)

    # --- NEW: Align with training feature columns ---

    # 1. Add any missing columns with value 0.
    missing_cols = [c for c in FEATURE_COLUMNS if c not in X.columns]
    for col in missing_cols:
        X[col] = 0

    # 2. Drop any extra columns that the model never saw.
    extra_cols = [c for c in X.columns if c not in FEATURE_COLUMNS]
    if extra_cols:
        X = X.drop(columns=extra_cols)

    # 3. Reorder columns to exactly match training time.
    X = X[FEATURE_COLUMNS]

    # --- Inference ---

    pred = model.predict(X)[0]
    # RandomForest provides prediction probabilities.
    proba = float(max(model.predict_proba(X)[0]))

    return {
        "prediction": pred,
        "confidence": proba,
    }
