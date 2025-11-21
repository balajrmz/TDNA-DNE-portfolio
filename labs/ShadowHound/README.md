# 🐺 ShadowHound — AI-Assisted Active Directory Attack Path Analysis

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Machine Learning](https://img.shields.io/badge/ML-RandomForest-orange)
![Graph Analysis](https://img.shields.io/badge/Graph-NetworkX-lightgrey)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green)
![Offensive Security](https://img.shields.io/badge/OffSec-Red_Team-red)

**Status:** Completed
**Category:** Active Directory | Attack Path Analysis | AI-Driven Offensive Security

ShadowHound is an AI-assisted engine designed to identify high-risk identities, privilege relationships, and lateral movement paths inside Active Directory environments. It analyzes BloodHound-like graph data, extracts structural and behavioral features, trains an ML model, and serves real-time predictions through an API.

This project demonstrates:

* Offensive data engineering
* Graph theory for red-team operations
* Machine learning applied to domain privilege relationships
* Automated reasoning around escalation paths
* API-based inference for attacker simulation and detection

---

## 🚀 Key Capabilities

* Parses and normalizes BloodHound-style AD graphs
* Detects suspicious edges and privilege relationships
* Computes graph metrics: degree, reachability, admin edges, shortest-path
* Trains a RandomForest ML model for classification
* Exposes predictions via FastAPI microservice
* Full CLI pipeline: synthetic → features → ML → inference

---

## 🧠 Technical Highlights

* **Graph-based feature engineering** using NetworkX
* **RandomForest classifier** with persisted artifacts (model + schema)
* **Synthetic graph generator** for red-team simulation
* **FastAPI microservice** for real-time privilege-path scoring
* Modular Python package with clean, extensible architecture

---

## 📁 Repository Structure

```
shadowhound/
│
├── data/
│   ├── raw/                # synthetic AD edges (BloodHound-like)
│   └── processed/          # engineered feature matrix
│
├── shadowhound/
│   ├── synthetic.py        # synthetic graph generation
│   ├── features.py         # graph metrics + feature engineering
│   ├── ml.py               # model training pipeline
│   ├── api.py              # FastAPI inference service
│   ├── graph.py            # graph loading & utilities
│   └── config.py           # file paths and constants
│
└── README.md
```

---

## ⚙️ Installation

```
pip install -r requirements.txt
```

**Dependencies:**

* pandas
* networkx
* scikit-learn
* joblib
* fastapi
* uvicorn

---

## 🧪 How to Use

### **1. Generate Synthetic AD Graph**

```
python -m shadowhound.synthetic
```

Output:

```
data/raw/ad_edges.json
```

### **2. Generate Feature Matrix**

```
python -m shadowhound.features
```

Output:

```
data/processed/features.csv
```

### **3. Train the ML Model**

```
python -m shadowhound.ml
```

Artifacts:

```
model.joblib
report.json
feature_columns.json
```

### **4. Start the Prediction API**

```
uvicorn shadowhound.api:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🔮 Example API Request (POST /predict)

**Input**

```json
{
  "degree": 12,
  "num_admin_edges": 3,
  "num_group_edges": 5,
  "shortest_path_to_target": 2,
  "can_reach_target_steps": 2,
  "is_target_group_member": 0,
  "is_user": 1,
  "is_group": 0,
  "is_computer": 0
}
```

**Response**

```json
{
  "prediction": {
    "class_label": "benign",
    "confidence": 1.0
  },
  "model_info": {
    "feature_columns_used": [
      "degree",
      "num_admin_edges",
      "num_group_edges"
    ]
  }
}
```

---

## 🗺️ Architecture Overview

* **Synthetic Graph → Feature Extraction → ML Model → API Inference**
* Identifies abnormal privilege paths or identity misconfigurations
* Supports attacker-simulation and detection engineering

---

## 👤 Author

**Jan Zabala**
AI-Driven Offensive Security Engineer
Offensive Security Engineering Portfolio (2025)
