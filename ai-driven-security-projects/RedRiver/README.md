# RedRiver — AI-Assisted Network Flow Analysis
**Tags:** TDNA, DNE, Network Behavior Analysis, Machine Learning, FastAPI, Offensive Security, AI Security

Target-centric network behavior modeling to support Target Digital Network Analysis (TDNA) and Digital Network Exploitation (DNE) workflows.

---

## Overview

RedRiver is an AI-assisted network flow analysis project designed to model adversary-relevant network behaviors in a controlled, lab-based environment. The project generates synthetic network traffic, engineers behavioral features, trains a supervised machine learning classifier, and exposes real-time scoring through a FastAPI service.

RedRiver supports TDNA and DNE workflows by enabling hands-on experimentation with network behaviors such as scanning, brute-force attempts, and command-and-control beaconing, and by demonstrating how these behaviors appear at the flow level.

This project is part of the TDNA & DNE portfolio of Jan Zabala.

---

## Why This Matters for TDNA & DNE

Understanding network behavior is critical when:

- Characterizing target networks and exposed services
- Identifying anomalous or attacker-like traffic patterns
- Reasoning about beaconing, scanning, and brute-force activity
- Evaluating how defensive analytics may respond to adversary actions

RedRiver enables practical validation of how offensive network behaviors manifest in telemetry and how they may be classified, detected, or potentially evaded.

---

## Features

- Synthetic traffic generation for multiple behavior classes
- Flow-level feature engineering focused on timing, byte rates, and protocol usage
- Supervised machine learning classification using RandomForest
- Persisted feature schemas to prevent training/inference drift
- Real-time prediction via a FastAPI REST service
- End-to-end automation from data generation through model deployment

---

## Architecture

Synthetic traffic is generated, transformed into engineered features, used to train a machine learning model, and then loaded into a FastAPI service for inference.

Key components include:
- synthetic.py – synthetic flow generation
- features.py – feature engineering pipeline
- ml.py – model training and evaluation
- pipeline.py – end-to-end execution
- api.py – FastAPI inference service

---

## Project Structure

```
ai-driven-security-projects/redriver/
├── synthetic.py
├── features.py
├── ml.py
├── pipeline.py
├── api.py
├── config.py
│
├── data/
│   ├── raw/flows.csv
│   └── processed/features.csv
│
└── model/
    ├── model.joblib
    ├── feature_columns.json
    └── report.json
```

---

## Installation

```bash
git clone https://github.com/balajimz/tdna-dne-portfolio.git
cd tdna-dne-portfolio/ai-driven-security-projects/redriver

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Run the Full Pipeline

```bash
python pipeline.py
```

This will generate synthetic data, engineer features, train the model, and produce trained artifacts in the model directory.

---

## Start the API

```bash
uvicorn api:app --reload
```

Interactive API documentation:
http://127.0.0.1:8000/docs

---

## Health Check

GET /health

Example response:

```json
{
  "status": "ok",
  "model_loaded": true,
  "n_features": 15,
  "classes": ["benign", "brute_force", "c2_beacon", "port_scan"]
}
```

---

## Prediction Endpoint

POST /predict

Example request body:

```json
{
  "src_ip": "10.0.0.10",
  "dst_ip": "8.8.8.8",
  "src_port": 54321,
  "dst_port": 443,
  "protocol": "tcp",
  "duration": 1.5,
  "bytes_sent": 1200,
  "bytes_received": 3500,
  "packets": 18
}
```

Example response:

```json
{
  "prediction": {
    "class_label": "benign",
    "confidence": 0.92
  }
}
```

---

## Model Performance

- Typical accuracy between 92% and 96%
- Strong separation between benign traffic and malicious behaviors
- Effective identification of beaconing patterns using timing-based features

---

## TDNA / DNE Use Cases

- Adversary network behavior modeling
- Support for attack-path reasoning and access validation
- Evaluation of ML-based network detection assumptions
- Training and experimentation in lab or synthetic environments

---

## Notes

- All data is synthetic
- No production or customer traffic is used
- Project is OPSEC-safe and designed for reproducible experimentation

---

## License

MIT License.

---

## Author

Jan Zabala  
Target Digital Network Analysis & Digital Network Exploitation  
CEH | OSCP (in progress)
