"""
Machine learning utilities for PacketVision.

In plain English:
- This file knows how to:
    * train a classifier,
    * save and load the model,
    * make predictions on new flow features.

We keep ML-specific logic here so that other parts of the project
(api, parser, rules) don't need to care about scikit-learn details.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from .config import MODEL_PATH, FEATURE_COLUMNS_PATH


# ---------------------------------------------------------------------------
# Training utilities
# ---------------------------------------------------------------------------

def train_packetvision_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_val: pd.DataFrame,
    y_val: pd.Series,
) -> Tuple[RandomForestClassifier, Dict[str, Any]]:
    """
    Train a RandomForest classifier on flow features.

    Parameters
    ----------
    X_train, y_train : training data
    X_val, y_val     : validation data

    Returns
    -------
    model : RandomForestClassifier
        Trained classifier.
    metrics : dict
        Simple metrics about how well the model did.

    In plain English:
    - We fit a RandomForest on the training set.
    - We check accuracy and a basic classification report on the validation set.
    - We return both the model and a dictionary of metrics to log/save.
    """

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    # Evaluate on validation data.
    y_pred = model.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    report = classification_report(y_val, y_pred, output_dict=True)

    metrics: Dict[str, Any] = {
        "accuracy": float(acc),
        "num_train_samples": int(X_train.shape[0]),
        "num_val_samples": int(X_val.shape[0]),
        "classes": list(model.classes_),
        "classification_report": report,
    }

    return model, metrics


# ---------------------------------------------------------------------------
# Model persistence
# ---------------------------------------------------------------------------

def save_model(model: RandomForestClassifier, path=MODEL_PATH) -> None:
    """
    Save the trained model to disk using joblib.

    In plain English:
    - We serialize the model object so we can load it later without retraining.
    """
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def load_model(path=MODEL_PATH) -> RandomForestClassifier:
    """
    Load a previously saved model from disk.

    In plain English:
    - This is used at inference time (e.g., in the API) to get a ready-to-use model.
    """
    model: RandomForestClassifier = joblib.load(path)
    return model


def save_feature_columns(columns: List[str], path=FEATURE_COLUMNS_PATH) -> None:
    """
    Save the list of feature column names to JSON.

    In plain English:
    - The model expects features in a specific column order.
    - We remember that order so we can re-create it when new data arrives.
    """
    import json

    FEATURE_COLUMNS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(columns, f, indent=2)


def load_feature_columns(path=FEATURE_COLUMNS_PATH) -> List[str]:
    """
    Load feature column names from disk.
    """
    import json

    with open(path, "r") as f:
        cols = json.load(f)
    return list(cols)


# ---------------------------------------------------------------------------
# Inference helpers
# ---------------------------------------------------------------------------

def align_features_for_inference(
    X_new: pd.DataFrame,
    feature_columns: List[str],
) -> pd.DataFrame:
    """
    Align new feature data with the columns used during training.

    In plain English:
    - When we trained the model, it saw a specific set of columns.
    - New data may have:
        * missing columns (we add them with 0),
        * extra columns (we drop them),
        * different column order.
    - This function fixes all of that.

    Parameters
    ----------
    X_new : pd.DataFrame
        New feature data.
    feature_columns : list of str
        The exact column names used during training.

    Returns
    -------
    pd.DataFrame
        A DataFrame matching the training-time feature layout.
    """

    X = X_new.copy()

    # 1) Add missing columns as zeros.
    for col in feature_columns:
        if col not in X.columns:
            X[col] = 0.0

    # 2) Drop any extra columns the model never saw.
    extra_cols = [c for c in X.columns if c not in feature_columns]
    if extra_cols:
        X = X.drop(columns=extra_cols)

    # 3) Reorder columns to match training-time order.
    X = X[feature_columns]

    return X


def predict_flows(
    model: RandomForestClassifier,
    X_aligned: pd.DataFrame,
) -> List[Dict[str, Any]]:
    """
    Run predictions on aligned feature data.

    Parameters
    ----------
    model : RandomForestClassifier
        Trained classifier.
    X_aligned : pd.DataFrame
        Feature matrix that already matches the expected columns.

    Returns
    -------
    List[dict]
        One dictionary per flow, including:
            - predicted_label
            - predicted_proba_per_class

    In plain English:
    - We call model.predict() and model.predict_proba().
    - We package the results into a list of dictionaries that our API/analyzer
      can turn into JSON later.
    """

    if X_aligned.empty:
        return []

    y_pred = model.predict(X_aligned)
    proba = model.predict_proba(X_aligned)
    classes = list(model.classes_)

    results: List[Dict[str, Any]] = []
    for idx in range(X_aligned.shape[0]):
        row_proba = proba[idx]
        proba_dict = {str(cls): float(p) for cls, p in zip(classes, row_proba)}

        results.append(
            {
                "predicted_label": str(y_pred[idx]),
                "probabilities": proba_dict,
            }
        )

    return results

