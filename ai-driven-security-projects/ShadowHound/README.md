# ShadowHound — Identity Attack Path Analysis (Active Directory)
**Tags:** TDNA, DNE, Identity Attack Paths, Active Directory, Graph Analysis, Machine Learning, Offensive Security

Target-centric analysis of identity relationships and privilege escalation paths in Active Directory environments to support Target Digital Network Analysis (TDNA) and Digital Network Exploitation (DNE).

---

## Overview

ShadowHound is an identity-focused analysis engine designed to identify high-risk identities, privilege relationships, and lateral movement paths within Active Directory environments. The project ingests BloodHound-style graph data, engineers graph-based features, applies machine learning to identify risky nodes and paths, and exposes predictions through an API.

ShadowHound supports TDNA and DNE workflows by treating identity infrastructure as a target surface and by enabling structured reasoning about how trust relationships and permissions can be chained into viable access paths.

This project is part of the TDNA & DNE portfolio of Jan Zabala.

---

## Why This Matters for TDNA & DNE

In many enterprise environments, identity is the primary control plane. Misconfigured permissions and trust relationships can:

- Enable privilege escalation without exploiting software vulnerabilities
- Provide lateral movement paths across domains and systems
- Collapse security boundaries through group membership abuse
- Create stealthy escalation chains that evade traditional detection

ShadowHound enables repeatable, lab-based analysis of these identity-driven attack paths.

---

## Key Capabilities

- Parsing and normalization of BloodHound-style Active Directory graphs
- Identification of high-risk privilege relationships and escalation paths
- Graph metric computation (degree, reachability, shortest paths)
- Supervised machine learning classification using RandomForest
- Persisted model artifacts and feature schemas
- FastAPI-based inference for real-time scoring
- End-to-end pipeline from synthetic data to prediction

---

## Technical Highlights

- Graph-based feature engineering using NetworkX
- Synthetic Active Directory graph generation for experimentation
- Modular Python architecture for extensibility
- Separation of data generation, feature engineering, modeling, and inference
- Designed for attack-path reasoning rather than tool-specific exploitation

---

## Project Structure

```
ai-driven-security-projects/shadowhound/
├── data/
│   ├── raw/                    # synthetic AD edges (BloodHound-like)
│   └── processed/              # engineered feature matrix
│
├── shadowhound/
│   ├── synthetic.py            # synthetic graph generation
│   ├── features.py             # graph metrics + feature engineering
│   ├── ml.py                   # model training pipeline
│   ├── api.py                  # FastAPI inference service
│   ├── graph.py                # graph loading & utilities
│   └── config.py               # file paths and constants
│
└── README.md
```

---

## Installation

```bash
git clone https://github.com/balajimz/tdna-dne-portfolio.git
cd tdna-dne-portfolio/ai-driven-security-projects/shadowhound

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### 1. Generate Synthetic Active Directory Graph

```bash
python -m shadowhound.synthetic
```

Output:

```
data/raw/ad_edges.json
```

---

### 2. Generate Feature Matrix

```bash
python -m shadowhound.features
```

Output:

```
data/processed/features.csv
```

---

### 3. Train the Machine Learning Model

```bash
python -m shadowhound.ml
```

Artifacts:

```
model.joblib
report.json
feature_columns.json
```

---

### 4. Start the Prediction API

```bash
uvicorn shadowhound.api:app --reload
```

Interactive API documentation:

http://127.0.0.1:8000/docs

---

## Example Prediction Request

POST /predict

Example request body:

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

Example response:

```json
{
  "prediction": {
    "class_label": "benign",
    "confidence": 1.0
  }
}
```

---

## TDNA / DNE Use Cases

- Identity attack-path analysis and privilege escalation reasoning
- Target characterization of Active Directory environments
- Support for lateral movement modeling and access validation
- Training and experimentation in lab or synthetic environments
- Evaluation of identity-focused detection assumptions

---

## Notes

- All graph data is synthetic or derived from publicly documented schemas
- No production or customer environments are used
- Project is OPSEC-safe and designed for reproducible experimentation

---

## License

MIT License.

---

## Author

Jan Zabala  
Target Digital Network Analysis & Digital Network Exploitation  
CEH | OSCP (in progress)
