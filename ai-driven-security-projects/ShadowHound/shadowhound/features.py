# features.py — ShadowHound (fixed for categorical encoding)

import pandas as pd
import joblib
from pathlib import Path

from shadowhound.config import (
    RAW_GRAPH_PATH,
    FEATURES_PATH,
    FEATURE_COLS_PATH,
    LABEL_COLUMN
)

ENCODERS_PATH = Path(FEATURES_PATH).parent / "encoders.joblib"


def load_edges(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def build_graph(edges: pd.DataFrame):
    import networkx as nx
    G = nx.DiGraph()
    for _, r in edges.iterrows():
        G.add_edge(r["src"], r["dst"], edge_type=r["edge_type"])
    return G


def add_risk_labels(df: pd.DataFrame) -> pd.DataFrame:
    df[LABEL_COLUMN] = (df["num_admin_edges"] > 0).astype(int)
    return df


def encode_categoricals(df: pd.DataFrame):
    """
    Convert any non-numeric feature columns into numeric encodings.
    Saves encoders so inference stays consistent.
    """
    from sklearn.preprocessing import LabelEncoder

    encoders = {}

    for col in df.columns:
        if col == LABEL_COLUMN:
            continue

        if df[col].dtype == object:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le

    # Save all encoders for later inference
    joblib.dump(encoders, ENCODERS_PATH)

    return df


def extract_features(df_edges: pd.DataFrame) -> pd.DataFrame:
    import networkx as nx
    G = build_graph(df_edges)

    rows = []
    for node in G.nodes():
        degree = G.degree(node)
        admin_edges = sum(1 for _, _, d in G.out_edges(node, data=True)
                          if d.get("edge_type") == "admin")
        group_edges = sum(1 for _, _, d in G.out_edges(node, data=True)
                          if d.get("edge_type") == "member_of")

        rows.append({
            "node": node,
            "degree": degree,
            "num_admin_edges": admin_edges,
            "num_group_edges": group_edges,
        })

    df = pd.DataFrame(rows)
    df = add_risk_labels(df)
    df = encode_categoricals(df)

    return df


def save_features(df: pd.DataFrame, path: str) -> str:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return str(out)


def run_feature_pipeline():
    print("[ShadowHound] Loading raw AD edges...")
    edges = load_edges(RAW_GRAPH_PATH)

    print("[ShadowHound] Extracting features...")
    feats = extract_features(edges)
    print(f"[ShadowHound] Final feature matrix: {feats.shape}")

    print(f"[ShadowHound] Saving features to {FEATURES_PATH}")
    save_features(feats, FEATURES_PATH)

    # Save feature columns for ML
    feature_cols = [c for c in feats.columns if c != LABEL_COLUMN]
    joblib.dump(feature_cols, FEATURE_COLS_PATH)

    print("[ShadowHound] Feature pipeline complete.")
    return str(FEATURES_PATH)


if __name__ == "__main__":
    run_feature_pipeline()
