# 🌐 SentinelFlow — AI-Driven Network Threat Classifier

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Machine Learning](https://img.shields.io/badge/ML-RandomForest-orange)
![Network Security](https://img.shields.io/badge/Security-Network_Threats-red)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green)
![Automation](https://img.shields.io/badge/Automation-Pipeline-lightgrey)

**Status:** Completed
**Category:** Network Security | Threat Classification | AI-Driven Detection

SentinelFlow is an end-to-end ML pipeline for classifying network traffic into behavioral categories such as **normal**, **port scan**, and **DoS-like** activity. It generates synthetic traffic, engineers robust flow-level features, trains a RandomForest classifier, and serves predictions via a FastAPI microservice.

This project demonstrates:

* Synthetic network traffic generation for security modeling
* Feature engineering for flow-based detection
* Supervised ML for network threat classification
* Schema-stable model deployment (persisted feature columns)
* API-based inference suitable for integration into larger monitoring stacks

---

## 🚀 Key Capabilities

* Generates labeled synthetic network traffic
* Builds flow-level features (e.g., packet counts, byte volumes, timing)
* Trains a RandomForest classifier on engineered features
* Persists feature column order to prevent schema drift at inference time
* Exposes a FastAPI endpoint for real-time predictions
* Provides a simple CLI pipeline from raw data → model → API

---

## 🧠 Technical Highlights

* Synthetic data generator for controlled threat scenarios
* Modular feature engineering layer with reproducible transforms
* RandomForest model optimized for interpretability and robustness
* FastAPI app wrapping model artifacts for production-style inference
* Separation of concerns between data, model, and service layers

---

## 📁 Repository Structure

```
sentinelflow/
│
├── data/
│   ├── raw/                # synthetic or captured traffic (CSV/PCAP-derived)
│   └── processed/          # feature matrices used for training
│
├── sentinelflow/
│   ├── generate_data.py    # synthetic traffic generator
│   ├── features.py         # feature engineering logic
│   ├── ml.py               # model training & evaluation pipeline
│   ├── api.py              # FastAPI inference service
│   ├── schema.py           # feature column persistence utilities
│   └── config.py           # paths, constants, and settings
│
└── README.md
```

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

**Dependencies:**

* Python 3.10+
* pandas
* numpy
* scikit-learn
* joblib
* fastapi
* uvicorn

---

## 🧪 How to Use

### **1. Generate Synthetic Network Data**

```bash
python -m sentinelflow.generate_data
```

Outputs (example):

```text
data/raw/traffic.csv
```

### **2. Build Feature Matrix**

```bash
python -m sentinelflow.features
```

Outputs:

```text
data/processed/features.csv
```

### **3. Train the ML Model**

```bash
python -m sentinelflow.ml
```

Artifacts:

```text
model.joblib
metrics.json
feature_columns.json
```

### **4. Start the Prediction API**

```bash
uvicorn sentinelflow.api:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## 🔮 Example API Request (POST /predict)

**Input**

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

**Response**

```json
{
  "prediction": {
    "class_label": "scan",
    "confidence": 0.91
  },
  "model_info": {
    "feature_columns_used": [
      "total_packets",
      "total_bytes",
      "duration_ms",
      "src_port",
      "dst_port",
      "packet_rate",
      "byte_rate"
    ]
  }
}
```

---

## 🗺️ Architecture Overview

* **Synthetic Traffic → Feature Engineering → ML Training → API Inference**
* Designed as a blueprint for network detection pipelines
* Easily extensible with new labels, models, and feature sets
* Provides a foundation for more advanced anomaly detection labs (e.g., AnomalyHunter)

---

## 👤 Author

**Jan Zabala**
AI-Driven Offensive Security Engineer
Offensive Security Engineering Portfolio (2025)
