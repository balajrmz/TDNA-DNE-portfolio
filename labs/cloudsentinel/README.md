# ☁️ CloudSentinel — Cloud IAM Misconfiguration Analysis Lab

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Cloud Security](https://img.shields.io/badge/Cloud-AWS/Azure-orange)
![IAM](https://img.shields.io/badge/Identity-IAM-yellow)
![Offensive Security](https://img.shields.io/badge/OffSec-Red_Team-red)
![Automation](https://img.shields.io/badge/Automation-Security_Engineering-green)

**Status:** Completed
**Category:** Cloud Identity | IAM Misconfig Analysis | Offensive Security Engineering

CloudSentinel is a cloud identity and IAM-focused research lab designed to explore, analyze, and model real-world misconfigurations in AWS and Azure identity environments. It provides a controlled testing ground for dangerous permission combinations, escalation paths, wildcard policies, privilege amplification, and identity abuse patterns.

This project demonstrates:

* Cloud identity threat modeling
* Privilege escalation path discovery
* IAM risk pattern analysis (PassRole, AssumeRole, wildcard actions)
* Automated parsing and scoring of policy documents
* Offensive identity engineering techniques for red-team and cloud abuse research

---

## 🚀 Key Capabilities

* Analyzes IAM JSON policies for high-risk permissions
* Identifies dangerous combinations (e.g., PassRole + EC2)
* Flags wildcard permissions ("Action": "*" or overly broad resources)
* Detects privilege escalation chains
* Supports AWS and Azure policy styles
* Produces structured risk scoring output

---

## 🧠 Technical Highlights

* Normalization of IAM policy JSON into analyzable structures
* Rule-based detection of misconfigurations
* Early architecture designed for ML-driven scoring in future versions
* Modular Python design for rapid expansion

---

## 📁 Repository Structure

```
cloudsentinel/
│
├── data/
│   ├── samples/        # example AWS/Azure IAM policies
│   └── output/         # generated analysis reports
│
├── cloudsentinel/
│   ├── analyzer.py     # core policy analysis engine
│   ├── rules.py        # dangerous permission rules
│   ├── utils.py        # loaders, normalizers, helpers
│   ├── api.py          # FastAPI (optional future module)
│   └── config.py       # paths + constants
│
└── README.md
```

---

## ⚙️ Installation

```
pip install -r requirements.txt
```

**Dependencies:**

* Python 3.10+
* pandas
* fastapi (optional)
* uvicorn (optional)
* jsonschema (optional)

---

## 🧪 How to Use

### **1. Analyze a Policy**

```
python -m cloudsentinel.analyzer ./data/samples/policy.json
```

Output:

```
{
  "policy_name": "policy.json",
  "wildcard_actions": [...],
  "dangerous_combinations": [...],
  "risk_score": 72,
  "critical_findings": [...]
}
```

### **2. Analyze an Entire Directory**

```
python -m cloudsentinel.analyzer ./data/samples/
```

### **3. (Optional) Start the API**

```
uvicorn cloudsentinel.api:app --reload
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## 🔮 Example Output Summary

```json
{
  "policy": "admin_escalation.json",
  "findings": {
    "wildcards": ["*"] ,
    "dangerous_pairs": ["PassRole + RunInstances"],
    "excessive_privileges": 5,
    "recommendations": [
      "Limit PassRole to specific roles",
      "Restrict EC2 RunInstances to controlled resources"
    ]
  },
  "risk_score": 88
}
```

---

## 🗺️ Architecture Overview

* IAM Policy JSON → Normalization → Rule Engine → Risk Score
* Designed to extend into ML-driven IAM risk prediction
* Supports hybrid AWS/Azure identity research

---

## 👤 Author

**Jan Zabala**
AI-Driven Offensive Security Engineer
Offensive Security Engineering Portfolio (2025)
