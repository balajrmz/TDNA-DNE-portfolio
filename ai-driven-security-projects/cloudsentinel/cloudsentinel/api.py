"""
CloudSentinel FastAPI service.

In plain English:
- This file exposes CloudSentinel as an HTTP API.
- Clients send an IAM policy in JSON format.
- The service runs the rule engine + analyzer to get findings and features.
- It then runs the ML model on those features to predict a risk level.
- The response contains both the rule-based analysis and the ML perspective.
"""

from __future__ import annotations

from typing import Any, Dict, List

import json

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .config import MODEL_PATH, FEATURES_PATH
from .analyzer import analyze_policy
from .ml import predict_risk


app = FastAPI(
    title="CloudSentinel API",
    description="Analyze AWS IAM policies for misconfigurations and risk.",
    version="0.1.0",
)


class PolicyInput(BaseModel):
    """
    Simple request body schema.

    In plain English:
    - The client POSTs a JSON body with a single field: 'policy'.
    - 'policy' is an AWS-style IAM policy document (Version + Statement).
    """
    policy: Dict[str, Any]


def _load_model(path: str | None = None):
    """
    Load the trained ML model from disk.

    We call this once at startup so the model stays in memory.
    """
    model_path = MODEL_PATH if path is None else path
    try:
        return joblib.load(model_path)
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"Model file not found at {model_path}. "
            "Run 'python -m cloudsentinel.pipeline' first to train the model."
        ) from exc


def _load_feature_columns(path: str | None = None) -> List[str]:
    """
    Load the list of feature column names used during training.

    In plain English:
    - When we trained the model, we saved the column order into
      FEATURES_PATH as JSON.
    - At inference time we reindex incoming features to match this order.
    """
    features_path = FEATURES_PATH if path is None else path
    try:
        with open(features_path, "r", encoding="utf-8") as f:
            cols = json.load(f)
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"Feature column file not found at {features_path}. "
            "Run 'python -m cloudsentinel.pipeline' first."
        ) from exc
    return cols


# Load model + feature schema once when the API starts.
MODEL = _load_model()
FEATURE_COLUMNS = _load_feature_columns()


@app.get("/health")
def healthcheck():
    """
    Basic health endpoint.

    Lets callers verify that the service is alive.
    """
    return {"status": "ok"}


@app.post("/analyze")
def analyze(input_data: PolicyInput):
    """
    Analyze an IAM policy with both rule-based logic and ML risk scoring.

    Steps in plain English:
    1. Take the incoming policy JSON from the request body.
    2. Run analyze_policy() to get:
        - findings
        - rule-based risk_level and risk_score
        - numeric 'features' describing the policy's risk shape
    3. Turn features into a one-row pandas DataFrame.
    4. Align DataFrame columns with the training-time feature order.
    5. Pass the aligned features to the ML model to get:
        - predicted risk level
        - class probabilities
    6. Return a combined JSON response.
    """
    policy = input_data.policy

    try:
        # 1–2. Run rule-based analysis and feature extraction.
        analysis = analyze_policy(policy, include_features=True)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=400, detail=f"Error analyzing policy: {exc}")

    if "features" not in analysis:
        # This should not happen if include_features=True, but we guard anyway.
        raise HTTPException(
            status_code=500,
            detail="Analyzer did not return features. Check pipeline configuration.",
        )

    features_dict = analysis["features"]

    # 3. Build a single-row DataFrame.
    X = pd.DataFrame([features_dict])

    # 4. Align features to the training-time schema.
    #    - Add missing columns with value 0.
    #    - Drop extra columns the model has never seen.
    missing_cols = [c for c in FEATURE_COLUMNS if c not in X.columns]
    for col in missing_cols:
        X[col] = 0

    extra_cols = [c for c in X.columns if c not in FEATURE_COLUMNS]
    if extra_cols:
        X = X.drop(columns=extra_cols)

    # Reorder to match training.
    X = X[FEATURE_COLUMNS]

    # 5. Run ML prediction.
    try:
        ml_result = predict_risk(MODEL, X)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"Error during ML prediction: {exc}")

    # We only sent one policy, so grab the first prediction.
    ml_level = ml_result["predicted_levels"][0]
    ml_probs = ml_result["probabilities"][0]

    # 6. Build combined response.
    response = {
        "rule_based": {
            "risk_level": analysis["risk_level"],
            "risk_score": analysis["risk_score"],
            "num_statements": analysis["num_statements"],
            "num_findings": analysis["num_findings"],
            "findings": analysis["findings"],
        },
        "ml_based": {
            "risk_level": ml_level,
            "probabilities": ml_probs,
        },
    }

    return response
