# ZeroTrace — AI-Powered Process Behavior Classifier

ZeroTrace is a lightweight, end-to-end behavioral malware detection engine. It extracts behavioral features from process telemetry, trains an ML classifier, and exposes real-time predictions through a FastAPI inference server.

This project demonstrates real Threat Detection Engineering capabilities used across TDNA teams, Red Teams, EDR development, and Security Data Science functions.

---

## 🚀 Features
• Synthetic process telemetry generation  
• Feature extraction pipeline (entropy, memory, networking, CPU, module metadata)  
• RandomForest multi-class behavioral classifier  
• Complete offline training pipeline with saved artifacts  
• FastAPI real-time scoring endpoint  
• JSON prediction output with class probabilities  
• Fully modular ML + rules architecture  

---

## 📁 Project Structure
zerotrace/  
├── api.py  
├── synthetic.py  
├── features.py  
├── ml.py  
├── rules.py  
├── config.py  
│  
├── data/  
│   ├── raw/  
│   └── processed/  
│  
├── model.joblib  
├── feature_columns.json  
└── report.json  

---

## 🧠 How ZeroTrace Works

### 1. Generate Synthetic Telemetry
Creates thousands of labeled process snapshots with behavioral attributes.

Run:
```
python -m zerotrace.synthetic
```
Outputs: data/raw/memory_snapshots.csv

---

### 2. Extract ML Features
Converts raw process telemetry into numerical ML-ready features.

Run:
```
python -m zerotrace.features
```
Outputs: data/processed/features.csv  
Also saves: feature_columns.json

---

### 3. Train the Behavioral ML Model
Trains a RandomForest classifier across four behavioral classes:

- benign  
- infostealer_like  
- ransomware_like  
- injected_loader  

Run:
```
python -m zerotrace.ml
```
Artifacts produced:  
• model.joblib  
• feature_columns.json  
• report.json  

---

### 4. Run the ZeroTrace API (FastAPI)
Start real-time behavioral detection service:

uvicorn zerotrace.api:app --reload

Interactive docs:
http://127.0.0.1:8000/docs

---

## 🔍 Example Prediction Request
```
POST /predict
{
  "pid": 1234,
  "ppid": 421,
  "num_modules": 150,
  "num_unsigned_modules": 3,
  "num_rx_regions": 2,
  "num_tx_regions": 6,
  "avg_entropy": 5.7,
  "has_network_connection": 1,
  "num_connections": 5,
  "listening_ports": 1,
  "high_entropy_strings": 40,
  "cpu_usage_pct": 12.5,
  "memory_usage_mb": 220
}

### Example Response
{
  "prediction": {
    "class_label": "benign",
    "confidence": 0.50,
    "probs": {
      "benign": 0.50,
      "infostealer_like": 0.18,
      "ransomware_like": 0.13,
      "injected_loader": 0.07
    }
  }
}
```
---

## 📦 Install & Run
```
pip install -r requirements.txt
```
Pipeline:
```
python -m zerotrace.synthetic
python -m zerotrace.features
python -m zerotrace.ml
uvicorn zerotrace.api:app --reload
```

---

## 🔮 Future Enhancements
• SHAP explainability  
• Model comparison (RF, XGBoost, LightGBM)  
• Per-process anomaly detection baseline  
• Streamlit detection dashboard  
• Docker + Kubernetes deployment  
• Rule-based correlation engine  

---

## 📜 License
MIT License

---

## ✨ Author
**Jan Zabala**  
Offensive Security Engineer  
Project: **ZeroTrace**  
Part of the **Offensive Security Engineering Portfolio**
