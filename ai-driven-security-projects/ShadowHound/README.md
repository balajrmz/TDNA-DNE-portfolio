# ShadowHound — Identity Attack-Path Analysis for Active Directory (TDNA/DNE)

**ShadowHound** is a target-centric analysis engine for **Active Directory identity attack paths**.  
It ingests BloodHound-style graph data, computes graph-based features, applies ML-assisted risk scoring, and exposes results via an API.

**Tags:** TDNA, DNE, Active Directory, Identity Attack Paths, BloodHound, Graph Analysis, FastAPI, Machine Learning

---

## Why ShadowHound

In real environments, **identity is the control plane**. Misconfigured permissions and trust relationships can enable:

- Privilege escalation without software exploitation  
- Lateral movement across domains and systems  
- Stealthy escalation chains that bypass traditional defenses  

ShadowHound supports **Target Digital Network Analysis (TDNA)** and **Digital Network Exploitation (DNE)** by treating identity infrastructure as a target surface and enabling structured **attack-path reasoning**.

---

## What It Does

- Ingests BloodHound-style relationships (synthetic or exported schemas)
- Computes graph metrics and path features (reachability, degrees, shortest paths)
- Scores identities/nodes for risk using a supervised model (RandomForest)
- Persists a stable feature schema to prevent drift
- Serves predictions through a **FastAPI** inference endpoint

---

## Quick Demo (60 seconds)

```bash
git clone https://github.com/balajrmz/TDNA-DNE-portfolio.git
cd TDNA-DNE-portfolio/ai-driven-security-projects/shadowhound

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 1) Generate synthetic AD graph
python -m shadowhound.synthetic

# 2) Build graph features
python -m shadowhound.features

# 3) Train model + export artifacts
python -m shadowhound.ml

# 4) Run inference API
uvicorn shadowhound.api:app --reload
```

Open:
`http://127.0.0.1:8000/docs`

---

## Example Prediction

**POST** `/predict`

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

**Response:**
```json
{
  "prediction": {
    "class_label": "high_risk",
    "confidence": 0.93
  }
}
```

---

## Architecture

```text
Graph Data (Synthetic / BloodHound-like)
        |
        v
Graph Loader + Normalization
        |
        v
Feature Engineering (NetworkX metrics + path features)
        |
        v
Model Training (RandomForest) + Artifact Export
        |
        v
FastAPI Inference Service
```

---

## Project Structure

```text
ai-driven-security-projects/shadowhound/
├── data/
│   ├── raw/
│   └── processed/
├── shadowhound/
│   ├── synthetic.py
│   ├── features.py
│   ├── ml.py
│   ├── api.py
│   ├── graph.py
│   └── config.py
└── README.md
```

---

## TDNA/DNE Use Cases

- Identity attack-path analysis and privilege escalation reasoning
- Target characterization of AD environments
- Lateral movement modeling and access validation
- Analyst support tooling for path prioritization

---

## OPSEC Note

All data is **synthetic** or derived from **public schemas**.  
No production environments or sensitive customer details are used.

---

## Roadmap

- [ ] Add path-ranking output (top-N candidate escalation chains)
- [ ] Add report generator (JSON + Markdown)
- [ ] Add export format compatibility for BloodHound CSV/JSON
- [ ] Add model evaluation notebook + metrics visualization

---

## Author

Jan Zabala  
**Target Digital Network Analysis & Digital Network Exploitation**  
CEH | OSCP (in progress)
