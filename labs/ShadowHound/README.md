# ShadowHound
ML-driven detection of high-risk identities and attack paths in Active Directory graphs.
Part of the Offensive Security Engineering Portfolio — Developed by Jan Zabala.

ShadowHound is an end-to-end machine learning pipeline that analyzes Active Directory graph data (BloodHound-style edges) and identifies high-risk identities, suspicious privilege relationships, and attacker-like behavior inside Windows domains.

It includes:
- Synthetic AD graph generator
- Feature extraction engine for graph metrics
- RandomForest classifier for behavior detection
- FastAPI prediction microservice
- CLI pipelines for synthetic → features → model → inference

The project demonstrates end-to-end offensive data engineering, threat analytics, and ML deployment.

---------------------------------------------------------------------

## Repository Structure
```
shadowhound/
  data/
    raw/               
    processed/         
  shadowhound/
    synthetic.py       
    features.py        
    ml.py              
    api.py             
    config.py          
    graph.py           
  README.md
```
---------------------------------------------------------------------

## Features

1. Synthetic AD Graph Generator
   - Generates user, group, and computer nodes
   - Adds edges such as member_of, admin_to, has_session, can_rdp
   - Supports risk-injection for malicious behavior patterns

2. Feature Extraction
   - Node degree
   - Number of admin edges
   - Number of group edges
   - Shortest-path to critical targets
   - Reachability metrics
   - Node-type one-hot encoding

3. Machine Learning Model
   - RandomForestClassifier
   - Output:
       model.joblib
       report.json
       feature_columns.json

4. Prediction API
   - FastAPI server
   - /predict route accepts a feature vector and returns:
       predicted class
       probability distribution
       metadata (feature list)

5. CLI Pipelines
   python -m shadowhound.synthetic
   python -m shadowhound.features
   python -m shadowhound.ml
   uvicorn shadowhound.api:app --reload

---------------------------------------------------------------------

## Installation
```
pip install -r requirements.txt
```
Dependencies:
pandas
networkx
joblib
scikit-learn
fastapi
uvicorn

---------------------------------------------------------------------

## Usage

### 1. Generate Synthetic AD Edges
```
python -m shadowhound.synthetic
```
Outputs:
```
data/raw/ad_edges.json
```
### 2. Generate Feature Matrix
```
python -m shadowhound.features
```
Outputs:
```
data/processed/features.csv
```
### 3. Train ML Model
```
python -m shadowhound.ml
```
Outputs:
```
model.joblib
report.json
feature_columns.json
```
### 4. Start the API
```
uvicorn shadowhound.api:app --reload
```
Open Swagger docs:
```
http://127.0.0.1:8000/docs
```
---------------------------------------------------------------------

## Example API Prediction Request (POST /predict)

Input example:
```
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
```
{
  "input": { ... },
  "prediction": {
    "class_label": "benign",
    "confidence": 1.0,
    "probs": {
      "benign": 1.0,
      "infostealer_like": 0.0,
      "ransomware_like": 0.0,
      "injected_loader": 0.0
    }
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
---------------------------------------------------------------------

## Author
Jan Zabala
Offensive Security Engineer
2025 PenTest & Threat Analytics Portfolio
