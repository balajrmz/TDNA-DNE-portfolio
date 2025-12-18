# SentinelFlow — AI-Assisted Network Behavior Classification
**Tags:** TDNA, DNE, Network Behavior Analysis, Machine Learning, Flow Analysis, FastAPI, Offensive Security

Target-centric network behavior modeling to support Target Digital Network Analysis (TDNA) and Digital Network Exploitation (DNE) workflows.

---

## Overview

SentinelFlow is an end-to-end machine learning pipeline designed to classify network traffic based on adversary-relevant behaviors. The project generates synthetic network flows, engineers flow-level features, trains a supervised classification model, and exposes real-time predictions via a FastAPI microservice.

SentinelFlow supports TDNA and DNE workflows by enabling structured analysis of how reconnaissance, scanning, and denial-style behaviors manifest in network telemetry, and how these behaviors can be detected, modeled, or potentially evaded.

This project is part of the TDNA & DNE portfolio of Jan Zabala.

---

## Why This Matters for TDNA & DNE

Understanding network behavior at the flow level is critical when:

- Characterizing exposed services and network attack surfaces
- Identifying reconnaissance, scanning, and disruptive activity
- Reasoning about attacker timing, volume, and protocol usage
- Evaluating assumptions behind ML-based network detection systems

SentinelFlow enables hands-on validation of these behaviors in a controlled, lab-based environment.

---

## Key Capabilities

- Synthetic generation of labeled network traffic
- Flow-level feature engineering (volume, timing, rates, ports)
- Supervised machine learning using RandomForest
- Persisted feature schemas to prevent inference-time drift
- FastAPI-based real-time prediction service
- Automated pipeline from data generation through deployment

---

## Technical Highlights

- Modular Python architecture separating data, features, model, and service layers
- Reproducible synthetic data generator for controlled experiments
- Interpretable ML model focused on robustness over black-box accuracy
- Production-style API design suitable for integration or experimentation

---

## Project Structure

```
ai-driven-security-projects/sentinelflow/
├── data/
│   ├── raw/                # synthetic network traffic
│   └── processed/          # engineered feature matrices
│
├── sentinelflow/
│   ├── generate_data.py    # synthetic traffic generator
│   ├── features.py         # feature engineering logic
│   ├── ml.py               # model training & evaluation
│   ├── api.py              # FastAPI inference service
│   ├── schema.py           # feature column persistence
│   └── config.py           # paths & constants
│
└── README.md
```

---

## Installation

```bash
git clone https://github.com/balajimz/tdna-dne-portfolio.git
cd tdna-dne-portfolio/ai-driven-security-projects/sentinelflow

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### 1. Generate Synthetic Network Data

```bash
python -m sentinelflow.generate_data
```

Output:

```
data/raw/traffic.csv
```

---

### 2. Build Feature Matrix

```bash
python -m sentinelflow.features
```

Output:

```
data/processed/features.csv
```

---

### 3. Train the ML Model

```bash
python -m sentinelflow.ml
```

Artifacts:

```
model.joblib
metrics.json
feature_columns.json
```

---

### 4. Start the Prediction API

```bash
uvicorn sentinelflow.api:app --reload
```

Interactive API documentation:

http://127.0.0.1:8000/docs

---

## Example Prediction Request

POST /predict

Example request body:

```json
{
  "total_packets": 120,
  "total_bytes": 8042,
  "duration_ms": 450,
  "src_port": 51532,
  "dst_port": 80,
  "packet_rate": 0.27,
  "byte_rate": 17.87
}
```

Example response:

```json
{
  "prediction": {
    "class_label": "scan",
    "confidence": 0.91
  }
}
```

---

## TDNA / DNE Use Cases

- Network attack surface characterization
- Detection and modeling of reconnaissance activity
- Support for access-path reasoning through traffic analysis
- Evaluation of ML-based network detection assumptions
- Training and experimentation in lab environments

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
