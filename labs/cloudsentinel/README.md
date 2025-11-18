# CloudSentinel — AI-Powered Cloud IAM & Policy Analyzer

CloudSentinel is a hybrid security analysis engine that inspects AWS IAM policies and cloud configuration JSON to detect over-permissive access, privilege escalation paths, wildcard abuses, and ML-predicted risk levels. It combines deterministic rule-based detection with a machine learning classifier, similar to real CSPM platforms like Wiz, Lacework, and Panther. CloudSentinel is part of my Offensive Security Engineering Portfolio.

## Project Structure
```
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
```
## Installation

1. Clone the repository:
git clone https://github.com/YOUR-USERNAME/pentest-portfolio.git
cd labs/cloudsentinel

2. Create a virtual environment:
python -m venv .venv

3. Activate it (Windows PowerShell):
.venv\Scripts\Activate.ps1

4. Install dependencies:
pip install -r requirements.txt

## Training the ML Model (Optional)
python -m cloudsentinel.pipeline
This creates:
- model.joblib
- processed feature data
- synthetic training report

## Running the API
uvicorn cloudsentinel.api:app --reload

Open Swagger UI:
http://127.0.0.1:8000/docs

## Endpoints

### GET /health
Response:
{ "status": "ok" }

### POST /analyze
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

## How CloudSentinel Works

Rule Engine:
- Detects wildcard resources (*)
- Detects dangerous action combinations
- Detects privilege escalation paths
- Detects known misconfigurations

ML Engine:
- Uses synthetic IAM datasets
- Trains a RandomForest classifier
- Predicts risk categories (critical / medium / none)

This combines rule-based and ML detection into one engine.

## Why This Project Matters

Demonstrates:
- Python automation
- FastAPI backend development
- Cloud IAM security
- ML pipeline development
- Real-world rule-based detection
- Testing (pytest-style)
- Practical security tool design

Useful for:
- Cloud Security
- SecOps
- Threat Detection
- AppSec
- DevSecOps
- Offensive Security Engineering

## Future Enhancements
- Auto-remediation suggestions
- Multi-statement correlation
- Expanded ML feature set
- Docker support
- Risk visualization dashboard

CloudSentinel is fully implemented and functional.
