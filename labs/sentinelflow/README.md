# SentinelFlow – AI-Powered Network Threat Detection

**Tech stack:** Python · scikit-learn · FastAPI · Docker  

SentinelFlow is an end-to-end, AI-driven security lab that simulates network
traffic, trains a machine learning model to spot suspicious behavior, and
exposes the model as a simple REST API.

The goal of this project is to demonstrate how offensive security and
machine learning can be combined into a realistic, reproducible pipeline
that would fit into a modern SOC stack.

---

## High-Level Architecture

1. **Synthetic Data Generator**
   - Creates realistic-looking network flow events:
     - `bytes_in`, `bytes_out`, `packet_count`, `protocol`, `dst_port`
   - Injects labeled behavior:
     - `normal` – everyday traffic
     - `scan` – high packet counts
     - `dos` – huge inbound byte volumes

2. **Feature Engineering**
   - Builds model-ready features:
     - Numeric features (bytes, packet_count)
     - `byte_ratio` = (bytes_in + 1) / (bytes_out + 1)
     - One-hot encoded protocol and destination port

3. **Model Training**
   - Baseline algorithm: **RandomForestClassifier**
   - Train/test split with stratified labels
   - Metrics saved as JSON (`precision`, `recall`, `f1-score`, etc.)

4. **Inference API**
   - **FastAPI** service:
     - `GET /health` – sanity check
     - `POST /predict` – classify a single network event
   - Returns:
     - `prediction` – `normal` / `scan` / `dos`
     - `confidence` – model probability for that class

5. **Containerization**
   - **Dockerfile** builds a self-contained image:
     - Installs dependencies
     - Runs the training pipeline at build time
     - Starts the FastAPI app with Uvicorn

---

## Project Layout

```text
labs/sentinelflow/
├── data/
│   ├── raw/               # Synthetic CSV generated here
│   └── processed/         # Trained model + metrics are stored here
├── notebooks/             # Optional Jupyter exploration
├── sentinelflow/          # Python package with core logic
│   ├── __init__.py
│   ├── api.py             # FastAPI inference server
│   ├── config.py          # Paths and simple configuration
│   ├── features.py        # Feature engineering utilities
│   ├── models.py          # Model training helpers
│   └── pipeline.py        # End-to-end training pipeline
├── tests/
│   └── tests_pipeline.py  # Simple pytest to verify training works
├── Dockerfile             # Containerized version of the service
├── README.md              # This file
└── requirements.txt       # Python dependencies

