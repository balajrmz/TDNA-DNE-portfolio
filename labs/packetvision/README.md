# PacketVision  
### AI-Powered PCAP Traffic Classifier, Threat Detector, and Rule Engine  
**Version:** 1.0.0  

PacketVision is a hybrid AI + signature-based network traffic analysis engine.  
It ingests PCAP files, extracts flow-level features, applies machine-learning classification, and layers rule-based detections on top for transparent, explainable threat analysis.

This project demonstrates modern security engineering patterns used at FAANG-scale companies:
- Behavioral ML detection
- Rule-driven risk scoring
- Feature engineering pipelines
- REST APIs for automated analysis
- Synthetic PCAP generation for reproducible testing

---

## 🚀 Features

### **1. PCAP Upload & Automated Analysis**
Upload a `.pcap` file through the FastAPI UI. PacketVision will:
- Convert packets into flows  
- Extract ML-ready feature vectors  
- Run both **ML classifier** and **rule engine**  
- Produce a full detection report  

---

### **2. Machine-Learning Detection**
PacketVision uses a trained Random Forest model to classify each flow as:
- `port_scan`
- `benign`

The model outputs:
- Predicted label  
- Confidence probabilities  
- Flow-level summaries  

This demonstrates applied ML workflow:  
feature extraction → model training → model evaluation → serving a live model via API.

---

### **3. Rule-Based Threat Engine**
Custom detection rules identify activity patterns difficult for ML models to detect alone.

Current rules include:

#### **WR01_EXCESSIVE_FANOUT**  
Detects high-fanout scanning behavior.  
Triggers when a single source IP targets > 50 distinct destination ports.

#### **WR02_BRUTEFORCE_LIKE**  
Detects brute-force or authentication-spray signaling by monitoring access to admin ports:
`22, 3389, 445, 139`

#### **WR03_INTERNAL_RESOURCES**  
Flags traffic destined for internal/private IP ranges.

Rule outputs include:
- Rule ID  
- Severity  
- Human-readable explanation  
- Affected flows  

---

### **4. Synthetic PCAP Generation**
PacketVision includes a built-in traffic generator that produces realistic PCAPs for testing:
- Randomized scanning  
- Benign browsing burst patterns  
- Admin/privileged port access  
- Mixed hybrid traffic  
- Replayable with deterministic seeds

All synthetic traffic is exported as a real `.pcap` file using Scapy.

---

### **5. FastAPI Web Interface**
Once PacketVision is running, documentation and testing UI appear automatically:

👉 **http://127.0.0.1:8000/docs**

Endpoints:
- `GET /health` — Healthcheck  
- `POST /analyze-pcap` — Upload & analyze a pcap file  

---

## 📁 Project Structure

```
packetvision/
│
├── api.py                  # FastAPI app & endpoints
├── analyzer.py             # PCAP parser, flow builder, feature extractor
├── features.py             # Feature engineering (packets, timing, fanout, burstiness)
├── ml.py                   # ML training & inference logic
├── rules.py                # Rule definitions & evaluation engine
├── pipeline.py             # End-to-end ML training pipeline
│
├── data/
│   ├── raw/                # Raw PCAP files
│   └── processed/          # Feature CSVs & processed flows
│
├── feature_columns.json    # Saved model feature order
├── model.joblib            # Trained ML model
├── report.json             # Training report
│
└── tests/
    └── test_parser.py      # Test for packet -> flow parsing
```

---

## ⚙️ Installation

### **1. Clone the Repository**
```bash
git clone https://github.com//pentest-portfolio.git
cd pentest-portfolio/labs/packetvision
```

### **2. Create a Virtual Environment**
```bash
python -m venv .venv
.\venv\Scripts\activate
```

### **3. Install Requirements**
```bash
pip install -r requirements.txt
```

---

## 🧠 Training a New ML Model (Optional)

Run the training pipeline:

```bash
python -m packetvision.pipeline
```

This will:
- Generate synthetic training data  
- Build flow-level feature vectors  
- Train the Random Forest model  
- Save:
  - `model.joblib`
  - `feature_columns.json`
  - `report.json`

---

## 🖥️ Running the API Server

Start FastAPI + Uvicorn:

```bash
uvicorn packetvision.api:app --reload
```

Open the interactive docs:

👉 **http://127.0.0.1:8000/docs**

---

## 🧪 Example Analysis Output

### **Bruteforce-Like Activity Detected**
```json
{
  "rule_based": {
    "risk_level": "high",
    "findings": [
      {
        "rule_id": "WR02_BRUTEFORCE_LIKE",
        "severity": "high",
        "message": "Observed 41 flow(s) targeting admin ports [22, 3389, 445, 139]. Possible brute-force/spray.",
        "flows_affected": 41
      }
    ]
  }
}
```

### **ML Port Scan Detection**
```json
{
  "ml_based": {
    "label_counts": {
      "port_scan": 200
    },
    "per_flow": [
      {
        "predicted_label": "port_scan",
        "probabilities": {
          "port_scan": 0.79,
          "benign": 0.21
        }
      }
    ]
  }
}
```

---

## 🎯 Talking Points for Interviews

You can describe PacketVision as:

> “A full-stack AI-driven network traffic analysis system. It includes PCAP parsing, feature extraction, ML classification, a rule engine, synthetic data generation, and a FastAPI inference service. I built the entire detection pipeline end-to-end.”

Or:

> “This project demonstrates both my offensive security knowledge and my machine-learning engineering background. It shows that I can design behavioral detections, engineer features, train models, and deploy them behind a modern API.”

Or:

> “The project uses principles used at FAANG-scale security teams: hybrid ML + rules, reproducible pipelines, deterministic synthetic datasets, and clean REST interfaces.”

---

## 📌 Future Enhancements (Planned)

- Flow visualization dashboard (heatmaps, timelines)
- Additional ML classes (DoS, SSH brute-force, beaconing)
- Packet-level LLM embeddings (advanced option)
- Multi-PCAP batch analysis
- Exportable PDF security reports

---

## 📜 License
MIT License. Free to use, modify, and showcase in your portfolio.

---

## 👤 Author
**Jan**  
Offensive Security + AI/ML Security Engineer  
This project is part of the larger **Pentest Portfolio** initiative.

