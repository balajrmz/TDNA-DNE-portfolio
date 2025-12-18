# CloudSentinel — Cloud Identity & IAM Misconfiguration Analysis
**Tags:** TDNA, DNE, Cloud Identity, IAM, Privilege Escalation, Offensive Security, Azure, AWS

Target-centric analysis of cloud identity boundaries and IAM misconfigurations to support Target Digital Network Analysis (TDNA) and Digital Network Exploitation (DNE).

---

## Overview

CloudSentinel is a cloud identity–focused research lab designed to analyze, model, and reason about real-world IAM misconfigurations in AWS and Azure environments. The project provides a controlled environment for identifying dangerous permission combinations, privilege escalation paths, and identity abuse patterns that can enable unauthorized access without traditional exploitation.

CloudSentinel supports TDNA and DNE workflows by treating cloud identity as a target surface, emphasizing how permissions, roles, and trust relationships can be chained into viable access paths.

This project is part of the TDNA & DNE portfolio of Jan Zabala.

---

## Why This Matters for TDNA & DNE

In cloud environments, identity is often the primary control plane. Misconfigured IAM policies can:

- Enable privilege escalation without exploiting software vulnerabilities
- Provide initial access through over-permissioned roles or users
- Bridge access between cloud services and hybrid identity environments
- Create stealthy persistence paths through role chaining

CloudSentinel enables structured analysis of these identity-driven access vectors.

---

## Key Capabilities

- Analysis of IAM JSON policies for high-risk permissions
- Identification of dangerous permission combinations (e.g., PassRole + RunInstances)
- Detection of wildcard actions and overly broad resource scopes
- Discovery of privilege escalation and abuse chains
- Support for AWS and Azure IAM policy structures
- Structured risk scoring output for analysis and comparison

---

## Technical Highlights

- Normalization of IAM policy documents into analyzable structures
- Rule-based detection engine for known escalation patterns
- Modular Python architecture for rapid expansion
- Designed to support future ML-driven risk scoring

---

## Project Structure

```
ai-driven-security-projects/cloudsentinel/
├── data/
│   ├── samples/          # example AWS / Azure IAM policies
│   └── output/           # generated analysis reports
│
├── cloudsentinel/
│   ├── analyzer.py       # core policy analysis engine
│   ├── rules.py          # dangerous permission rules
│   ├── utils.py          # loaders and normalizers
│   ├── api.py            # optional FastAPI service
│   └── config.py         # constants and paths
│
└── README.md
```

---

## Installation

```bash
git clone https://github.com/balajimz/tdna-dne-portfolio.git
cd tdna-dne-portfolio/ai-driven-security-projects/cloudsentinel

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Analyze a Single Policy

```bash
python -m cloudsentinel.analyzer ./data/samples/policy.json
```

Example output:

```json
{
  "policy_name": "policy.json",
  "wildcard_actions": ["*"],
  "dangerous_combinations": ["PassRole + RunInstances"],
  "risk_score": 72,
  "critical_findings": []
}
```

---

### Analyze a Directory of Policies

```bash
python -m cloudsentinel.analyzer ./data/samples/
```

---

### Optional API Mode

```bash
uvicorn cloudsentinel.api:app --reload
```

API documentation:
http://127.0.0.1:8000/docs

---

## Example Output Summary

```json
{
  "policy": "admin_escalation.json",
  "findings": {
    "wildcards": ["*"],
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

## TDNA / DNE Use Cases

- Cloud identity attack-path analysis
- Privilege escalation reasoning without exploits
- Hybrid identity targeting and access modeling
- Validation of cloud IAM detection assumptions
- Training and experimentation in lab environments

---

## Notes

- All policies are synthetic or publicly documented examples
- No production or customer environments are used
- Project is OPSEC-safe and designed for reproducible research

---

## License

MIT License.

---

## Author

Jan Zabala  
Target Digital Network Analysis & Digital Network Exploitation  
CEH | OSCP (in progress)
