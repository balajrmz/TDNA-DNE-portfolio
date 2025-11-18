"""
CloudSentinel machine learning helpers.

In plain English:
- This file does NOT parse IAM policies directly.
- It takes numeric "features" (already extracted by the analyzer) and
  trains a simple classifier that predicts risk level.
- The goal is to show how rule-based analysis and ML can work together.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def train_baseline(X: pd.DataFrame, y: pd.Series) -> Tuple[RandomForestClassifier, Dict[str, Any]]:
    """
    Train a baseline RandomForest classifier for risk levels.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix. Each row represents one IAM policy.
        Columns are numeric features such as:
            - num_findings
            - num_medium / num_high / num_critical
            - has_wildcard_action
            - has_priv_esc_pattern
            - ...
    y : pd.Series
        Target labels (e.g., "low", "medium", "high", "critical").

    Returns
    -------
    model : RandomForestClassifier
        Trained model.
    report : dict
        Simple metrics and information about the training run.

    In plain English:
    - We split the data into train / test sets.
    - We encode labels into numbers so scikit-learn can handle them.
    - We train a RandomForest classifier.
    - We measure accuracy and collect a small classification report.
    """

    # Make sure X and y have compatible lengths.
    if len(X) == 0:
        raise ValueError("Cannot train model: X is empty.")
    if len(X) != len(y):
        raise ValueError("X and y must have the same number of rows.")

    # Encode text labels (e.g., "low", "medium") into integers.
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Train/test split so we can measure how well the model generalizes.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.25,
        random_state=42,
        stratify=y_encoded,
    )

    # RandomForest is a good default: robust, handles nonlinearities, and
    # works well with small to medium-sized tabular datasets.
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        n_jobs=-1,
        random_state=42,
    )

    model.fit(X_train, y_train)

    # Evaluate on the held-out test set.
    y_pred = model.predict(X_test)

    acc = float(accuracy_score(y_test, y_pred))
    cls_report = classification_report(
        y_test,
        y_pred,
        target_names=list(label_encoder.classes_),
        output_dict=True,
        zero_division=0,
    )

    # Build a small JSON-friendly report.
    report: Dict[str, Any] = {
        "model": "RandomForestClassifier",
        "num_samples": int(len(X)),
        "num_features": int(X.shape[1]),
        "classes": list(label_encoder.classes_),
        "accuracy": acc,
        "classification_report": cls_report,
    }

    # Attach the label encoder to the model so we can recover text labels later
    # when making predictions.
    model.label_encoder_ = label_encoder  # type: ignore[attr-defined]

    return model, report


def predict_risk(model: RandomForestClassifier, features: pd.DataFrame) -> Dict[str, Any]:
    """
    Use a trained model to predict risk level for one or more feature rows.

    Parameters
    ----------
    model : RandomForestClassifier
        Trained model from train_baseline(). Must have a label_encoder_ attribute.
    features : pd.DataFrame
        Feature rows in the same format and order as used during training.

    Returns
    -------
    result : dict
        {
            "predicted_levels": [...],
            "probabilities": [...]
        }

    In plain English:
    - We run the model on the input feature rows.
    - We convert the numeric predictions back into text labels.
    - We also return class probabilities so we know how confident the model is.
    """

    if not hasattr(model, "label_encoder_"):
        raise AttributeError(
            "Model is missing 'label_encoder_'. "
            "Make sure you trained it with train_baseline()."
        )

    # Predict numeric classes and probabilities.
    probs = model.predict_proba(features)
    preds_numeric = np.argmax(probs, axis=1)

    # Convert numeric classes back to text labels (e.g., 0 -> "low").
    label_encoder = model.label_encoder_  # type: ignore[assignment]
    predicted_levels = label_encoder.inverse_transform(preds_numeric)

    # Turn probabilities into a list of dicts for easier JSON usage.
    class_names = list(label_encoder.classes_)
    prob_dicts = []
    for row in probs:
        prob_dict = {cls: float(p) for cls, p in zip(class_names, row)}
        prob_dicts.append(prob_dict)

    return {
        "predicted_levels": list(predicted_levels),
        "probabilities": prob_dicts,
    }

