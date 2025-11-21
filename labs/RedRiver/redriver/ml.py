# redriver/ml.py

import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from redriver.config import (
    FEATURES_PATH,
    MODEL_PATH,
    REPORT_PATH,
    FEATURE_COLUMNS_PATH,
    LABEL_COLUMN,
    RANDOM_SEED
)

# -------------------------------------------------------------------
# Load feature matrix
# -------------------------------------------------------------------
def load_features(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

# -------------------------------------------------------------------
# Encode labels → integers
# -------------------------------------------------------------------
def encode_labels(df: pd.DataFrame):
    labels = sorted(df[LABEL_COLUMN].unique())

    label_to_int = {label: i for i, label in enumerate(labels)}
    int_to_label = {i: label for label, i in label_to_int.items()}

    df["label_encoded"] = df[LABEL_COLUMN].map(label_to_int)

    return df, label_to_int, int_to_label

# -------------------------------------------------------------------
# Train model
# -------------------------------------------------------------------
def train_model(X, y):
    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=14,
        random_state=RANDOM_SEED
    )

    clf.fit(X, y)
    return clf

# -------------------------------------------------------------------
# Save artifacts
# -------------------------------------------------------------------
def save_artifacts(model, metrics, feature_cols, label_decoder):
    joblib.dump(model, MODEL_PATH)

    with open(REPORT_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    with open(FEATURE_COLUMNS_PATH, "w") as f:
        json.dump({
            "feature_columns": feature_cols,
            "label_decoder": label_decoder
        }, f, indent=2)

# -------------------------------------------------------------------
# CLI: run the full training pipeline
# -------------------------------------------------------------------
def run_training_pipeline() -> None:
    print("\n[RedRiver][ML] ===== Starting Training Pipeline =====")

    # Load data
    df = load_features(FEATURES_PATH)
    print(f"[RedRiver][ML] Loaded feature matrix: {df.shape}")

    # Encode labels
    df, label_to_int, int_to_label = encode_labels(df)

    # Split features
    feature_cols = [c for c in df.columns if c not in [LABEL_COLUMN, "label_encoded"]]
    X = df[feature_cols]
    y = df["label_encoded"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_SEED
    )

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds, output_dict=True)

    print(f"[RedRiver][ML] Accuracy: {acc:.4f}")

    # Save everything
    save_artifacts(model, report, feature_cols, int_to_label)

    print(f"[RedRiver][ML] Saved model → {MODEL_PATH}")
    print(f"[RedRiver][ML] Saved report → {REPORT_PATH}")
    print(f"[RedRiver][ML] Saved feature metadata → {FEATURE_COLUMNS_PATH}")

    print("[RedRiver][ML] ===== Training Complete =====\n")


if __name__ == "__main__":
    run_training_pipeline()
