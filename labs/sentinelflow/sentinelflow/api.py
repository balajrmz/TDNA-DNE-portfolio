
"""
FastAPI service that exposes the trained model as a REST API.

This lets us send a single network event and get back:
- The predicted label (normal / scan / dos)
- The model's confidence in that prediction
"""

from typing import Optional

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from .config import MODEL_PATH
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


# Load the model once when the API starts.
model = _load_model()


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
    3. Ask the model for a predicted label and probability.
    4. Return those to the caller as JSON.
    """

    # Create a one-row table from the incoming JSON.
    df = pd.DataFrame([sample.dict()])

    # The build_features function expects a label column.
    # For inference we don't have one, so we add a dummy value.
    df["label"] = "unknown"

    X, _ = build_features(df)

    pred = model.predict(X)[0]
    # Some scikit-learn models provide predict_proba; RandomForest does.
    proba = float(max(model.predict_proba(X)[0]))

    return {
        "prediction": pred,
        "confidence": proba,
    }
