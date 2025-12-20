# 🤖 AI-Driven Security Projects
### Target Digital Network Analysis (TDNA) & Digital Network Exploitation (DNE)

This directory contains AI/ML-assisted projects focused on **offensive security, target analysis, and adversary-centric reasoning**.

---

## ⭐ Flagship Project: ShadowHound

**ShadowHound** is an identity attack-path analysis engine for **Active Directory**, designed to support **Target Digital Network Analysis (TDNA)** and **Digital Network Exploitation (DNE)** missions.

It applies graph analysis and ML-assisted risk scoring to reason about **privilege escalation paths, lateral movement, and exploitation feasibility**, treating identity infrastructure as a primary target surface.

📂 **Start here:** `shadowhound/`  
➡️ If you only review one AI-driven project, this is the recommended entry point.

---

## Professional Focus

This project suite reflects my work as a:

**Target Digital Network Analyst & Digital Network Exploitation Practitioner**

With emphasis on:
- Attack-path reasoning across identity, applications, and networks
- Adversary behavior modeling using ML and analytics
- Exploitation validation and telemetry analysis
- Automation that accelerates target understanding, not just detection

---

## Project Suite Overview

### 🔵 ShadowHound — Identity Attack Path Analysis (Active Directory)
Analyzes identity relationships and privilege escalation paths using graph-based analytics.

**Focus areas:**
- BloodHound-style graph ingestion
- Privilege escalation path discovery
- Graph feature engineering
- ML-assisted risk scoring

Supports TDNA/DNE by treating identity as a primary access surface.

---

### 🔴 RedRiver — AI-Assisted Network Flow Analysis
Models adversary-relevant network behaviors to support access-path reasoning and detection analysis.

**Focus areas:**
- Synthetic flow generation
- Behavioral feature engineering
- ML-based traffic classification
- FastAPI-based inference

Supports TDNA by characterizing network exposure and attacker tradecraft at the flow level.

---

### ☁️ CloudSentinel — Cloud Identity & IAM Misconfiguration Analysis
Target-centric analysis of cloud IAM policies and trust relationships.

**Focus areas:**
- IAM policy normalization
- Privilege escalation via misconfiguration
- Hybrid identity access paths
- Risk scoring and rule-based analysis

Supports DNE by identifying access paths without exploiting software vulnerabilities.

---

### 🟣 PacketVision — Network Visibility & Packet Analysis
Explores packet-level visibility to understand attacker tradecraft and telemetry limitations.

**Focus areas:**
- PCAP parsing and inspection
- Flow and protocol metadata extraction
- Visibility gap identification
- ML pipeline integration

Supports TDNA by characterizing network surfaces at the packet level.

---

### 🟢 SentinelFlow — Network Behavior Classification
End-to-end ML pipeline for classifying network activity based on adversary behaviors.

**Focus areas:**
- Flow-level behavioral analytics
- Reconnaissance and scanning detection
- Model robustness and interpretability
- Real-time inference

Supports access-path analysis and detection assumption testing.

---

### 🟠 ZeroTrace — Stealth & Telemetry Gap Analysis
Analyzes logging and telemetry blind spots that enable low-noise attacker activity.

**Focus areas:**
- Telemetry gap identification
- Stealth and persistence modeling
- Detection boundary mapping
- Feature extraction for future ML models

Supports DNE by informing stealthy access validation and persistence planning.

---

## Technical Foundations Across Projects

Across this collection, each project emphasizes:

- Reproducible data generation (synthetic or public)
- Feature engineering aligned to adversary tradecraft
- End-to-end pipelines (data → model → inference)
- Automation designed for analyst and operator workflows
- OPSEC-safe design suitable for public demonstration

These projects demonstrate not just ML proficiency, but **how AI integrates into real-world offensive analysis and target development workflows**.

---

## How to Use This Folder

Each project directory includes:
- A dedicated `README.md`
- Source code and pipelines
- Clear installation and usage instructions
- Structured outputs and artifacts

Projects can be explored independently or as a cohesive TDNA/DNE research portfolio.

---

## Future Enhancements

Planned additions include:
- Automated access-path ranking engines
- ML-assisted exploit chain prioritization
- Graph neural network (GNN) identity analysis
- Adversary behavior simulation frameworks
- Advanced telemetry gap classification models

---

## Author

Jan Zabala  
Target Digital Network Analysis & Digital Network Exploitation  
CEH | OSCP (in progress)
