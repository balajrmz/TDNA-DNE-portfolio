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
    RANDOM_SEED,
)

# -------------------------------------------------------------------
# Load feature matrix
# -------------------------------------------------------------------


def load_features(path: str | bytes | "os.PathLike") -> pd.DataFrame:
    print(f"[RedRiver][ML] Loading feature matrix from: {path}")
    return pd.read_csv(path)


# -------------------------------------------------------------------
# Encode labels → integers
# -------------------------------------------------------------------


def encode_labels(df: pd.DataFrame):
    """
    Take the label column (e.g., 'benign', 'port_scan', 'brute_force', 'c2_beacon')
    and map it to integer classes 0..N-1.

    Returns:
      - df with an extra column 'label_encoded'
      - label_to_int:  {label_str -> int}
      - int_to_label:  {int -> label_str}
    """
    labels = sorted(df[LABEL_COLUMN].unique())
    print(f"[RedRiver][ML] Found labels: {labels}")

    label_to_int = {label: i for i, label in enumerate(labels)}
    int_to_label = {i: label for label, i in label_to_int.items()}

    df["label_encoded"] = df[LABEL_COLUMN].map(label_to_int)

    return df, label_to_int, int_to_label


# -------------------------------------------------------------------
# Train model
# -------------------------------------------------------------------


def train_model(X, y):
    """
    Train a RandomForest classifier on the provided features/labels.
    """
    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=14,
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )

    print("[RedRiver][ML] Training RandomForest classifier...")
    clf.fit(X, y)
    return clf


# -------------------------------------------------------------------
# Save artifacts
# -------------------------------------------------------------------


def save_artifacts(model, metrics, feature_cols, label_decoder):
    """
    Persist the trained model and metadata to disk so the API can reload
    everything consistently.
    """
    # 1) Model
    joblib.dump(model, MODEL_PATH)
    print(f"[RedRiver][ML] Saved model → {MODEL_PATH}")

    # 2) Metrics report
    with open(REPORT_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[RedRiver][ML] Saved metrics report → {REPORT_PATH}")

    # 3) Feature columns + label decoder
    payload = {
        "feature_columns": list(feature_cols),
        # keys must be JSON-serializable, so ensure ints become strings
        "label_decoder": {str(k): v for k, v in label_decoder.items()},
    }
    with open(FEATURE_COLUMNS_PATH, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"[RedRiver][ML] Saved feature metadata → {FEATURE_COLUMNS_PATH}")


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

    # Build feature matrix X, label vector y
    # Exclude the raw label column and the encoded one from X
    feature_cols = [c for c in df.columns if c not in [LABEL_COLUMN, "label_encoded"]]
    X = df[feature_cols]
    y = df["label_encoded"]

    print(f"[RedRiver][ML] Using {len(feature_cols)} feature columns.")

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_SEED, stratify=y
    )

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds, output_dict=True)

    print(f"[RedRiver][ML] Accuracy: {acc:.4f}")

    metrics = {
        "accuracy": acc,
        "classification_report": report,
        "label_mapping": {str(k): v for k, v in int_to_label.items()},
    }

    # Save everything
    save_artifacts(model, metrics, feature_cols, int_to_label)

    print("[RedRiver][ML] ===== Training Complete =====\n")


if __name__ == "__main__":
    run_training_pipeline()
