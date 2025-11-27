# **RedRiver – AI-Driven Network Flow Classifier**
### *Advanced ML-powered anomaly detection engine for offensive security engineers.*

![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal)
![Machine%20Learning](https://img.shields.io/badge/ML-RandomForest-yellow)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## ⭐ Overview

**RedRiver** is an AI-driven network flow classification engine designed for offensive-security modeling, detection evasion research, and practical machine-learning integration into cyber operations workflows.

It simulates realistic network traffic, engineers meaningful behavioral features, trains a supervised ML classifier, and exposes real-time scoring through a FastAPI microservice.

This project is part of the **AI-Driven Offensive Security Engineering Portfolio** of Jan Zabala.

---

## 🚀 Features

- **Synthetic Traffic Engine**  
  Generates labeled network flows: `benign`, `brute_force`, `port_scan`, `c2_beacon`.

- **Feature Engineering Pipeline**  
  Extracts bytes, packet rate, flags, protocol indicators, privileged-port behavior, and timing characteristics.

- **Supervised Machine Learning Model**  
  RandomForest classifier trained on engineered features with strong multi-class accuracy.

- **Production-Ready REST API**  
  Real-time scoring via FastAPI endpoints:  
  - `POST /predict`  
  - `GET /health`

- **End-to-End Automation**  
  `python -m redriver.pipeline` generates data → builds features → trains model.

---

## 🏗️ Architecture

```
              ┌──────────────────────┐
              │  synthetic.py         │
              │  (Generate flows)     │
              └───────────┬──────────┘
                          │ flows.csv
                          ▼
              ┌──────────────────────┐
              │  features.py          │
              │  (Engineer features)  │
              └───────────┬──────────┘
                       features.csv
                          ▼
              ┌──────────────────────┐
              │  ml.py                │
              │  (Train RandomForest) │
              ├──────────────────────┤
              │ model.joblib          │
              │ feature_columns.json  │
              │ report.json           │
              └───────────┬──────────┘
                          ▼
              ┌──────────────────────┐
              │  FastAPI Service     │
              │  (api.py)            │
              ├──────────────────────┤
              │ /health              │
              │ /predict             │
              └──────────────────────┘
```

---

## 📁 Project Structure

```
redriver/
│
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

## ⚙️ Installation

```bash
git clone https://github.com/balajrmz/pentest-portfolio.git
cd pentest-portfolio/labs/RedRiver
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔄 Run the Full Pipeline

```bash
python -m redriver.pipeline
```

Outputs:

```
data/raw/flows.csv
data/processed/features.csv
model/model.joblib
model/feature_columns.json
model/report.json
```

---

## 🌐 Start the API

```bash
uvicorn redriver.api:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🩺 Health Check

```
GET /health
```

Example:

```json
{
  "status": "ok",
  "model_loaded": true,
  "n_features": 15,
  "classes": ["benign", "brute_force", "c2_beacon", "port_scan"]
}
```

---

## 🔍 Prediction Endpoint

```
POST /predict
```

### Example Request

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

### Example Response

```json
{
  "prediction": {
    "class_label": "benign",
    "class_index": 0,
    "confidence": 0.92,
    "probs": {
      "benign": 0.92,
      "brute_force": 0.03,
      "c2_beacon": 0.01,
      "port_scan": 0.04
    }
  }
}
```

---

## 📊 Model Performance

- Accuracy: **92–96%**
- Strong separation between benign and malicious patterns
- Reliable identification of beaconing behaviors based on byte-rate dynamics

---

## 🔒 Offensive Security Use Cases

- Simulating attacker traffic patterns  
- Red Team behavioral detection tuning  
- Evasion-testing ML-based NDR/UEBA systems  
- Automated threat classification workflows  
- Teaching Blue Teams how ML responds to adversarial flows  

---

## 🧭 Future Enhancements

- Anomaly detection (Isolation Forest, One-Class SVM)
- PCAP ingestion and flow extraction
- Docker container build
- Batch prediction endpoint
- Model versioning + history tracking

---

## 📝 License

MIT License.

---

## 📚 Author

Developed by **Jan Zabala** as part of the *AI-Driven Offensive Security Engineering Portfolio*.
