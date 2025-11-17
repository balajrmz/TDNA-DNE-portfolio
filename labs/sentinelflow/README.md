# 🚀 SentinelFlow  
**AI-Driven Network Threat Detection Pipeline**  
*(Synthetic Network Traffic → Feature Engineering → ML Model → FastAPI Inference API)*

---

## 📌 Overview

**SentinelFlow** is an end-to-end, AI-powered cybersecurity lab project designed to simulate real SOC detection pipelines. It:

1. Generates synthetic network traffic  
2. Engineers ML features  
3. Trains a RandomForest threat-detection model  
4. Saves model + metrics for reproducibility  
5. Serves real-time predictions through FastAPI  

This mirrors how modern EDR/SIEM enrichment engines and ML-driven detections work inside enterprise environments.

---

## ✨ Key Features

### 🔹 Synthetic Network Traffic Generator
Creates realistic flow-style events including:

- Normal internal → external movement  
- Port scans  
- DoS-like “bursty” traffic  
- TCP / UDP / ICMP  
- Common port distribution: 22, 80, 443, 3306, 8080, etc.

Enables safe experimentation without exposing private logs.

---

### 🔹 Feature Engineering

SentinelFlow produces consistent, ML-ready feature vectors using:

- `bytes_in`, `bytes_out`, `packet_count`
- Derived metrics (`byte_ratio`, burst patterns)
- One-hot encoded:
  - Protocol  
  - Destination port

These engineered features match the type of numeric embeddings used in cloud security ML pipelines.

---

### 🔹 Model Training

Uses `RandomForestClassifier` for stable, interpretable multi-class classification.

Artifacts saved under `data/processed`:

- `model.joblib` – serialized trained model  
- `report.json` – metrics + diagnostics  
- `feature_columns.json` – **persisted feature ordering**  

Persisting the training-time feature order eliminates schema drift between training and inference.

---

### 🔹 FastAPI Inference Service

The API exposes:

#### `GET /health`
Simple health probe.

#### `POST /predict`
Example input:

```json
{
  "bytes_in": 10000,
  "bytes_out": 500,
  "packet_count": 80,
  "protocol": "TCP",
  "dst_port": 22
}
```

Example output:

```json
{
  "prediction": "scan",
  "confidence": 0.99
}
```

Ideal for integration into SIEM alert enrichment or lab simulations.

---

## 🏗️ Project Structure

```
sentinelflow/
│
├── api.py                  # FastAPI inference service
├── config.py               # Paths & configuration
├── features.py             # Feature engineering logic
├── models.py               # Model constructor / baseline
├── pipeline.py             # Training pipeline
│
├── data/
│   ├── raw/                # Synthetic generated CSVs
│   └── processed/
│       ├── model.joblib
│       ├── report.json
│       └── feature_columns.json
│
└── tests/
    └── test_pipeline.py    # Future test suite
```

---

## 🏃 How to Run

### 1️⃣ Create a virtual environment

```bash
python -m venv .venv
```

Activate:

**PowerShell**
```bash
. .venv\Scripts\Activate.ps1
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Train the model

```bash
python -m sentinelflow.pipeline
```

This generates:

```
data/processed/model.joblib
data/processed/report.json
data/processed/feature_columns.json
```

---

### 4️⃣ Start the API

```bash
uvicorn sentinelflow.api:app --reload
```

Then open:

```
http://127.0.0.1:8000/docs
```

Use the built-in Swagger UI to send predictions.

---

## 🧠 Engineering Decisions

- **Feature mismatch protection**  
  A common ML failure mode occurs when inference-time input columns don’t match training-time one-hot encodings.  
  SentinelFlow solves this by saving the training-time feature column list to:  

  ```
  data/processed/feature_columns.json
  ```

  The inference pipeline **reindexes** incoming data to match this schema.

- **Synthetic data for safe experimentation**  
  Avoids sensitive log exposure while enabling repeatable lab experiments.

- **Microservice architecture**  
  FastAPI mirrors modern SOC/EDR inference microservices and is easy to deploy via Docker/Kubernetes.

---

## 📈 Example `report.json`

```json
{
  "model": "RandomForestClassifier",
  "samples": 5000,
  "metrics": {
    "accuracy": 0.94,
    "precision": 0.93,
    "recall": 0.92
  }
}
```

---

## 🔮 Roadmap

- [ ] Add additional attack patterns (SSH brute force, DNS tunneling)  
- [ ] Add SHAP model explainability  
- [ ] Add retraining scheduler  
- [ ] Add Grafana dashboard for inference telemetry  
- [ ] Build Docker container + optional Kubernetes manifest  

---

## 👤 Author

**Jan Zabala**  
Offensive Security • Cloud Security • AI  
Part of the *pentest-portfolio* project.

