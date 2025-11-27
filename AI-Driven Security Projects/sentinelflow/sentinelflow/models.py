"""
Model training logic.

This file focuses on:
- Splitting data into train/test sets
- Training a baseline RandomForest classifier
- Producing a simple classification report
"""

from typing import Tuple, Dict, Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import pandas as pd


def train_baseline(
    X: pd.DataFrame, y: pd.Series
) -> Tuple[RandomForestClassifier, Dict[str, Any]]:
    """
    Train a RandomForest baseline model.

    In plain English:
    - Split the data into training and testing chunks
    - Train a forest of decision trees (RandomForest) on the training part
    - Evaluate it on the testing part and collect metrics

    RandomForest is a strong default for tabular security data:
    - Handles mixed numeric/categorical features
    - Reasonably robust and interpretable
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,          # 20% of data used to check how well we learned
        stratify=y,             # keep label proportions balanced
        random_state=42,        # fixed seed for reproducible results
    )

    model = RandomForestClassifier(
        n_estimators=200,        # number of trees in the forest
        max_depth=None,         # let trees grow until needed
        n_jobs=-1,              # use all CPU cores for speed
        random_state=42,
    )

    model.fit(X_train, y_train)

    # Get a dictionary of precision/recall/F1 scores, etc.
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)

    return model, report

