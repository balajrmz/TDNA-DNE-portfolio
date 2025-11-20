"""
ShadowHound API

FastAPI service that exposes the trained ShadowHound model over HTTP.

High-level idea in plain English:
- We load the trained RandomForest model from disk.
- We load the list of feature columns the model expects.
- We accept a JSON body that describes a single AD node (user / computer / group).
- We turn that JSON into a one-row pandas DataFrame.
- We make sure the columns line up with what the model saw during training.
- We ask the model to predict a risk label + probabilities.
- We return a friendly JSON response for dashboards or other tools.
"""

from pathlib import Path
from typing import Dict, List

import json
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Import paths from the ShadowHound config so everything stays in one place.
from .config import MODEL_PATH, FEATURE_COLS_PATH

# ---------------------------------------------------------------------------
# FastAPI app metadata
# ---------------------------------------------------------------------------

app = FastAPI(
    title="ShadowHound API",
    version="1.0.0",
    description=(
        "Graph-based Active Directory attack path risk scorer.\n\n"
        "This service takes features about a single AD node (user / computer / group) "
        "and uses a trained RandomForest model to predict whether that node looks "
        "low-risk or high-risk in the attack graph."
    ),
)


# ---------------------------------------------------------------------------
# Pydantic model: what a single prediction request looks like
# ---------------------------------------------------------------------------

class NodeFeatures(BaseModel):
    """
    This describes the shape of the JSON payload a client must send.

    All fields here are numeric or 0/1 flags so they're easy to plug into
    a machine-learning model.
    """

    # Basic graph structure
    degree: float = Field(
        ...,
        description="Total number of edges connected to this node (its graph degree).",
        example=12,
    )

    num_admin_edges: float = Field(
        ...,
        description="How many edges represent admin-like control (e.g., admin/owner).",
        example=3,
    )

    num_group_edges: float = Field(
        ...,
        description="How many edges come from group membership relationships.",
        example=5,
    )

    shortest_path_to_target: float = Field(
        ...,
        description="Length of the shortest path from this node to a crown-jewel target.",
        example=2,
    )

    can_reach_target_steps: float = Field(
        ...,
        description=(
            "Small integer that captures 'steps to reach a target' via attack paths. "
            "Often the same as shortest_path_to_target for this demo."
        ),
        example=2,
    )

    is_target_group_member: int = Field(
        ...,
        description="1 if this node is directly in a high-value / target group, else 0.",
        example=0,
    )

    # One-hot encoded node type flags
    is_user: int = Field(
        ...,
        description="1 if this node represents a user account, else 0.",
        example=1,
    )

    is_group: int = Field(
        ...,
        description="1 if this node represents a group object, else 0.",
        example=0,
    )

    is_computer: int = Field(
        ...,
        description="1 if this node represents a computer object, else 0.",
        example=0,
    )


# ---------------------------------------------------------------------------
# Model + feature metadata loading
# ---------------------------------------------------------------------------

def _load_artifacts():
    """
    Load the trained model and the list of feature columns from disk.

    In plain English:
    - model.joblib: the RandomForest we trained.
    - feature_columns.json: the exact column order the model saw during training.
    """
    model = joblib.load(MODEL_PATH)

    with open(FEATURE_COLS_PATH, "r", encoding="utf-8") as f:
        feature_cols: List[str] = json.load(f)

    return model, feature_cols


# Load artifacts once at import time so we don't reload on every request.
MODEL, FEATURE_COLUMNS = _load_artifacts()


# ---------------------------------------------------------------------------
# Helper: turn a NodeFeatures object into a model-ready DataFrame
# ---------------------------------------------------------------------------

def _build_feature_frame(sample: NodeFeatures) -> pd.DataFrame:
    """
    Convert the incoming JSON (NodeFeatures) into a 1-row DataFrame that matches
    the training-time feature layout.

    Steps:
    1. Convert Pydantic model -> Python dict.
    2. Build a one-row pandas DataFrame.
    3. Add any missing columns with default value 0 (safety).
    4. Drop any extra columns the model never saw.
    5. Reorder columns to exactly match FEATURE_COLUMNS.
    """

    # 1) Pydantic model -> plain dict
    data = sample.model_dump()

    # 2) One-row DataFrame
    X = pd.DataFrame([data])

    # 3) Add missing columns (if we ever extend the model, this keeps things robust)
    missing = [c for c in FEATURE_COLUMNS if c not in X.columns]
    for col in missing:
        X[col] = 0

    # 4) Drop any unexpected columns
    extra = [c for c in X.columns if c not in FEATURE_COLUMNS]
    if extra:
        X = X.drop(columns=extra)

    # 5) Reorder columns to training-time order
    X = X[FEATURE_COLUMNS]

    return X


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.get("/health", tags=["system"])
def healthcheck() -> Dict[str, str]:
    """
    Simple healthcheck endpoint.

    Lets callers (and your k8s/liveness probes) verify that:
    - The API is reachable.
    - The model successfully loaded.
    """
    return {"status": "ok"}


@app.post("/predict", tags=["inference"])
def predict_risk(sample: NodeFeatures):
    """
    Core prediction endpoint.

    Input:
      - JSON body describing a single AD node (see NodeFeatures).

    Output (high level):
      - Echo of the input features.
      - The predicted class label (e.g., 'low_risk' / 'high_risk').
      - The index of the chosen class.
      - A 'confidence' score (max probability).
      - A per-class probability dictionary.
    """

    # Turn the JSON payload into a model-ready DataFrame
    X = _build_feature_frame(sample)

    # Ask the RandomForest for class probabilities.
    # predict_proba returns: array([[p(class_0), p(class_1), ...]])
    proba = MODEL.predict_proba(X)[0]
    classes = list(MODEL.classes_)

    # Find the most likely class
    best_idx = int(proba.argmax())
    best_label = str(classes[best_idx])
    best_confidence = float(proba[best_idx])

    # Build a nicer dict of probabilities
    prob_dict = {str(cls): float(p) for cls, p in zip(classes, proba)}

    return {
        "input": sample.model_dump(),
        "prediction": {
            "class_label": best_label,
            "class_index": best_idx,
            "confidence": best_confidence,
            "probs": prob_dict,
        },
        "model_info": {
            "feature_columns_used": FEATURE_COLUMNS,
        },
    }
