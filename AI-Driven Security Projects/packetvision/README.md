# 📡 PacketVision — Network Packet Analysis & Offensive Visibility Lab

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Packet Analysis](https://img.shields.io/badge/Network-PCAP_Analysis-lightgrey)
![Data Engineering](https://img.shields.io/badge/Data-Engineering-orange)
![Offensive Security](https://img.shields.io/badge/OffSec-Red_Team-red)
![Automation](https://img.shields.io/badge/Automation-Scripting-green)

**Status:** Completed
**Category:** Network Visibility | Packet Analysis | Offensive Security Engineering

PacketVision is a focused research lab for exploring offensive use cases in packet capture analysis. It serves as a foundation for understanding how attackers observe, classify, and exploit network behavior. This lab is designed to help model visibility gaps, extract actionable packet insights, and prototype AI-assisted packet classification workflows.

This project demonstrates:

* Foundational offensive packet inspection
* Data extraction and transformation from PCAPs
* Structured feature engineering for network flows
* Early concepts for ML-driven packet anomaly detection
* Automation-driven parsing and reporting

---

## 🚀 Key Capabilities

* Parses packet captures (PCAP files)
* Extracts protocol metadata and flow summaries
* Identifies suspicious or abnormal traffic patterns
* Generates structured CSV/JSON output for analysis or ML ingestion
* Supports plugin-style packet feature modules
* Serves as a visibility lab for future AI enhancements

---

## 🧠 Technical Highlights

* Uses Python packet libraries for low-level inspection
* Normalized feature extraction for packet → flow summarization
* Modular architecture for adding protocol-specific detectors
* Ideal pre-processing layer for future ML models

---

## 📁 Repository Structure

```
packetvision/
│
├── data/
│   ├── pcaps/           # sample PCAP files for testing
│   ├── output/          # extracted features & flow metadata
│
├── packetvision/
│   ├── parser.py        # core PCAP parsing logic
│   ├── features.py      # feature extraction utilities
│   ├── utils.py         # helpers, loaders, and filters
│   ├── pipeline.py      # run-all workflow for parsing → features
│   └── config.py        # file paths & constants
│
└── README.md
```

---

## ⚙️ Installation

```
pip install -r requirements.txt
```

**Dependencies:**

* scapy or pyshark (depending on your implementation)
* pandas
* numpy
* json

---

## 🧪 How to Use

### **1. Parse a PCAP File**

```
python -m packetvision.parser ./data/pcaps/sample.pcap
```

Output:

```
data/output/parsed_sample.json
```

### **2. Extract Features**

```
python -m packetvision.features ./data/output/parsed_sample.json
```

Output:

```
data/output/flows.csv
```

### **3. Run the Full Pipeline**

```
python -m packetvision.pipeline ./data/pcaps/sample.pcap
```

This produces structured flow summaries ready for manual or ML analysis.

---

## 🔮 Example Output Summary

```json
{
  "flow_id": "192.168.1.10-443-192.168.1.50-51523",
  "protocol": "TLS",
  "packet_count": 32,
  "byte_count": 40241,
  "duration_ms": 812,
  "suspicious_flags": []
}
```

---

## 🗺️ Architecture Overview

* PCAP → Raw Packet Metadata → Features/Flows → CSV/JSON Output
* Supports reconnaissance training, traffic validation, and future ML modeling
* Forms a foundation for AI-assisted network anomaly detection (e.g., SentinelFlow)

---

## 👤 Author

**Jan Zabala**
AI-Driven Offensive Security Engineer
Offensive Security Engineering Portfolio (2025)
