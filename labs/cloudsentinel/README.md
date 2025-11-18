CloudSentinel — AI-Powered Cloud IAM & Policy Analyzer

CloudSentinel is a hybrid security analysis engine that inspects AWS IAM policies and cloud configuration JSON to detect:

Over-permissive access

Privilege escalation paths

Dangerous action combinations

Wildcard abuses

ML-predicted risk levels

It combines deterministic rule-based detection with a machine learning classifier, similar to real CSPM platforms like Wiz, Lacework, and Panther.

CloudSentinel is part of my Offensive Security Engineering Portfolio.

Project Structure
cloudsentinel/
│
├── cloudsentinel/
│   ├── api.py
│   ├── analyzer.py
│   ├── config.py
│   ├── ml.py
│   ├── pipeline.py
│   ├── rules.py
│   └── __init__.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── model.joblib
│
├── tests/
│   └── test_analyzer.py
│
├── README.md
└── requirements.txt

Installation
1. Clone the repository
git clone https://github.com/YOUR-USERNAME/pentest-portfolio.git
cd labs/cloudsentinel

2. Create a virtual environment
python -m venv .venv

3. Activate it

Windows PowerShell:

.venv\Scripts\Activate.ps1

4. Install dependencies
pip install -r requirements.txt

Training the ML Model (Optional)
python -m cloudsentinel.pipeline


This creates:

model.joblib

Processed feature data

Synthetic training report

Running the API
uvicorn cloudsentinel.api:app --reload


Open Swagger UI:

http://127.0.0.1:8000/docs

Endpoints
GET /health

Response:

{ "status": "ok" }

POST /analyze

Example input:

{
  "policy": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": ["iam:PassRole", "ec2:RunInstances"],
        "Resource": "*"
      }
    ]
  }
}


Example output:

{
  "rule_based": {
    "risk_level": "medium",
    "risk_score": 6,
    "num_statements": 1,
    "num_findings": 2,
    "findings": [
      {
        "rule_id": "R02_WILDCARD_RESOURCE",
        "severity": "high",
        "message": "Policy applies to all resources: \"*\""
      },
      {
        "rule_id": "R04_PRIV_ESC_PASSROLE_EC2",
        "severity": "high",
        "message": "iam:PassRole + ec2:RunInstances may enable privilege escalation."
      }
    ]
  },
  "ml_based": {
    "risk_level": "medium",
    "probabilities": {
      "critical": 0.0,
      "medium": 1.0,
      "none": 0.0
    }
  }
}

How CloudSentinel Works
Rule Engine

Detects:

Wildcard resources (*)

Dangerous action combinations

Privilege escalation paths

Known misconfigurations

ML Engine

Uses synthetic IAM datasets to train a RandomForest classifier that predicts:

critical

medium

none

It combines traditional rule analysis with data-driven ML predictions.

Why This Project Matters

Demonstrates skills in:

Python automation

FastAPI backend development

Cloud IAM security

ML model development

Rule-based detection logic

Testing (pytest style)

Real-world security tool design

Useful for:

Cloud Security

SecOps

Threat Detection

AppSec

Offensive Security Engineering

DevSecOps

Future Enhancements

Remediation recommendations

Multi-statement correlation

Extended ML features

Docker support

Threat heatmap dashboard
