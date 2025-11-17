🚀 SentinelFlow

AI-Driven Network Threat Detection Pipeline
(Synthetic Network Traffic → Feature Engineering → ML Model → FastAPI Inference API)

📌 Overview

SentinelFlow is an end-to-end, AI-powered cybersecurity lab project designed to simulate real SOC workflows:

Generate synthetic network flow logs

Engineer ML features

Train a baseline threat-detection model

Export the trained model + metrics

Serve real-time predictions via a FastAPI microservice

This design mirrors how modern cloud-native detection pipelines operate inside enterprise SOCs.

✨ Key Features
🔹 Synthetic Network Traffic Generator

Creates realistic flow-style events using randomized patterns:

Internal → External movement

Common ports (22, 80, 443, 3306, 8080…)

Protocols: TCP / UDP / ICMP

“Normal” vs. “Scan” vs. “DoS-like” patterns

This avoids the need for production logs while producing rich training data.

🔹 Feature Engineering

SentinelFlow builds ML-ready features using:

bytes_in, bytes_out, packet_count

Derived metrics like:

byte_ratio (bytes_in / bytes_out)

traffic_burst patterns

One-hot encodings for:

Protocol

Destination port

All preprocessing steps are consistent across training and inference.

🔹 Model Training

Uses RandomForestClassifier for interpretable, low-variance detection.

Outputs include:

model.joblib – serialized model

report.json – metrics & evaluation summary

feature_columns.json – persisted training-time feature ordering (critical for inference)

🔹 API Service (FastAPI + Uvicorn)

An inference microservice exposes:

GET /health

Quick health/status probe.

POST /predict

Accepts lightweight JSON network events:

{
  "bytes_in": 10000,
  "bytes_out": 500,
  "packet_count": 80,
  "protocol": "TCP",
  "dst_port": 22
}


Returns:

{
  "prediction": "scan",
  "confidence": 0.99
}

🧠 Architecture Diagram
Synthetic Data  →  Feature Engineering  →  RandomForest Model  →  FastAPI Service
    generator        (one-hot, ratios)         (trained)           (/predict)

🏗️ Project Structure
sentinelflow/
│
├── api.py                  # FastAPI inference service
├── config.py               # Paths & configuration
├── features.py             # Feature engineering logic
├── models.py               # Model constructor / baseline
├── pipeline.py             # Training pipeline
│
├── data/
│   ├── raw/                # Synthetic CSVs
│   └── processed/
│       ├── model.joblib
│       ├── report.json
│       └── feature_columns.json
│
└── tests/
    └── test_pipeline.py    # Basic tests (placeholder)

🏃 How to Run
1️⃣ Create a virtual environment
python -m venv .venv


Activate it:

PowerShell

. .venv\Scripts\Activate.ps1

2️⃣ Install requirements
pip install -r requirements.txt

3️⃣ Train the Model
python -m sentinelflow.pipeline


Outputs appear under:

data/processed/

4️⃣ Start the API
uvicorn sentinelflow.api:app --reload


Navigate to:

http://127.0.0.1:8000/docs


Use SwaggerUI to test predictions.

📝 Design Notes / Engineering Decisions

Feature mismatch prevention
Real ML systems often crash when inference-time features don’t match training.
SentinelFlow solves this by saving training column order to:

data/processed/feature_columns.json


Incoming requests are reindexed to this schema before prediction.

Synthetic data generation
Enables repeatable tests without exposing private logs.

Lightweight, SOC-style architecture
The project mimics real-world detection pipelines used in EDR/SIEM engines.

FastAPI for modern microservices
Production-ready async server, easily containerized.

📈 Example Output (report.json)
{
  "model": "RandomForestClassifier",
  "samples": 5000,
  "metrics": {
    "accuracy": 0.94,
    "precision": 0.93,
    "recall": 0.92
  }
}

🐳 Docker (Optional Future Addition)

I can generate a complete Dockerfile + docker-compose for this project on request.
This would allow:

Containerized training

Containerized inference

API deployment to cloud / Kubernetes

🔮 Roadmap

 Expand synthetic dataset (SSH brute force, DNS tunneling)

 Add SHAP explainability

 Add model retraining scheduler

 Build Grafana dashboard for prediction telemetry

 Containerize with Docker

👤 Author

Jan Zabala — Offensive Security Engineering • Cloud • AI
Part of the pentest-portfolio project.

If you want, I can also:
