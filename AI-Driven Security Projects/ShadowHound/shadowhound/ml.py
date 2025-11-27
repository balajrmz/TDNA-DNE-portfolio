# shadowhound/ml.py
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from shadowhound.config import (
    FEATURES_PATH,
    MODEL_PATH,
    REPORT_PATH,
    FEATURE_COLS_PATH,
    LABEL_COLUMN,
    RANDOM_SEED,
)

# -------------------------------------------------------------
# Load dataset
# -------------------------------------------------------------
def load_dataset(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

# -------------------------------------------------------------
# Split into X (features) and y (labels)
# -------------------------------------------------------------
def split_features_labels(df: pd.DataFrame):
    X = df.drop(columns=[LABEL_COLUMN])
    y = df[LABEL_COLUMN]
    return X, y

# -------------------------------------------------------------
# Train a RandomForest model
# -------------------------------------------------------------
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED
    )

    clf = RandomForestClassifier(
        n_estimators=160,
        max_depth=12,
        random_state=RANDOM_SEED,
    )

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    return clf, {"accuracy": acc, "classification_report": report}

# -------------------------------------------------------------
# Save model + metrics + feature columns
# -------------------------------------------------------------
def save_artifacts(model, metrics, feature_cols):
    joblib.dump(model, MODEL_PATH)

    with open(REPORT_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    with open(FEATURE_COLS_PATH, "w") as f:
        json.dump(feature_cols, f, indent=2)

    print(f"[ShadowHound][ML] Saved model to: {MODEL_PATH}")
    print(f"[ShadowHound][ML] Saved report to: {REPORT_PATH}")
    print(f"[ShadowHound][ML] Saved feature columns to: {FEATURE_COLS_PATH}")

# -------------------------------------------------------------
# Top-level training function (CLI entrypoint)
# -------------------------------------------------------------
def run_training_pipeline() -> None:
    print("[ShadowHound][ML] Starting training pipeline…")

    df = load_dataset(FEATURES_PATH)
    print(f"[ShadowHound][ML] Loaded dataset with shape: {df.shape}")

    X, y = split_features_labels(df)
    feature_cols = list(X.columns)

    print("[ShadowHound][ML] Training RandomForest classifier...")
    model, metrics = train_model(X, y)

    print("[ShadowHound][ML] Saving artifacts...")
    save_artifacts(model, metrics, feature_cols)

    print("[ShadowHound][ML] Training pipeline complete.")

# Allows running via: python -m shadowhound.ml
if __name__ == "__main__":
    run_training_pipeline()
