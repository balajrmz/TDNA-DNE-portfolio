# 🕶️ ZeroTrace — Offensive Stealth & Telemetry Evasion Lab

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Telemetry](https://img.shields.io/badge/Telemetry-Logging_Analysis-lightgrey)
![Detection Evasion](https://img.shields.io/badge/Evasion-Stealth-red)
![Offensive Security](https://img.shields.io/badge/OffSec-Red_Team-darkred)
![Automation](https://img.shields.io/badge/Automation-Workflows-green)

**Status:** Completed
**Category:** Detection Evasion | Logging Gaps | Offensive Security Engineering

ZeroTrace is an offensive research lab focused on **stealth**, **logging gaps**, and **telemetry evasion techniques**. It serves as a controlled environment for studying how adversaries bypass visibility, reduce their footprint, and operate in low-noise scenarios. This lab is a foundation for offensive R&D, detection bypass analysis, and future ML-based stealth pattern modeling.

This project demonstrates:

* Logging/telemetry gap identification
* Offensive visibility reduction techniques
* Event pipeline analysis and bypass scenarios
* Automated parsing of logs to detect blind spots
* Foundations for AI-assisted stealth classification models

---

## 🚀 Key Capabilities

* Analyzes log sources to identify missing or incomplete telemetry
* Maps attacker actions to detection opportunities and blind spots
* Simulates low-noise attacker behaviors
* Extracts structured features from logs for anomaly or stealth modeling
* Supports Python-based extensible plugin architecture

---

## 🧠 Technical Highlights

* Designed for future ML-driven stealth detection and evasion research
* Modular log-parsing utilities for structured extraction
* Detection gap taxonomy for red-team simulation workflows
* Enables rapid prototyping of stealth concepts

---

## 📁 Repository Structure

```
zerotrace/
│
├── data/
│   ├── logs/             # sample event logs, telemetry sources
│   ├── processed/        # extracted features, summaries
│
├── zerotrace/
│   ├── parser.py         # log parsing and normalization
│   ├── analyzer.py       # detection gap + stealth techniques analysis
│   ├── features.py       # structured feature extraction
│   ├── utils.py          # helpers + shared functions
│   └── config.py         # constants + paths
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
* numpy
* json
* datetime

---

## 🧪 How to Use

### **1. Parse Logs**

```
python -m zerotrace.parser ./data/logs/
```

Output:

```
data/processed/parsed_logs.json
```

### **2. Extract Features**

```
python -m zerotrace.features ./data/processed/parsed_logs.json
```

Output:

```
data/processed/features.csv
```

### **3. Analyze Telemetry Gaps**

```
python -m zerotrace.analyzer ./data/processed/features.csv
```

Example output:

```
{
  "missing_events": [...],
  "incomplete_coverage": [...],
  "stealth_opportunities": [...],
  "critical_blindspots": [...]
}
```

---

## 🔮 Example Output Summary

```json
{
  "log_source": "windows_event_log",
  "missing_events": ["4688", "4624"],
  "coverage": "partial",
  "stealth_findings": [
    "High stealth opportunity: no parent process auditing",
    "Blind spot detected: PowerShell script block logging disabled"
  ],
  "risk_score": 91
}
```

---

## 🗺️ Architecture Overview

* Raw Logs → Normalization → Feature Extraction → Stealth/Gaps Analysis
* Provides attacker-mapped visibility analysis for red teams
* Forms groundwork for ML-driven stealth classification

---

## 👤 Author

**Jan Zabala**
AI-Driven Offensive Security Engineer
Offensive Security Engineering Portfolio (2025)
