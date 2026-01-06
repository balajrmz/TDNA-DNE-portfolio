# TDNA – Active Directory Kerberos Assessment

This repository contains a two-part Active Directory assessment conducted using a **Trust-Driven Network Analysis (TDNA)** methodology.  
The purpose of this work is to demonstrate how Kerberos attack feasibility changes based on **service account design and configuration**.

This repository is intentionally structured to show **cause-and-effect**, not just exploitation.

---

## What This Repository Demonstrates

- A **hardened Active Directory baseline** where Kerberoasting is not possible
- A **deliberately misconfigured Active Directory environment** where Kerberoasting becomes viable
- A controlled, evidence-backed comparison using identical attacker positioning
- Windows-native attacker workflows aligned with real enterprise environments
- Clear documentation of both **offensive impact** and **defensive visibility**

---

## Repository Structure

```
tdna-active-directory/
│
├── reports/
│   ├── report-01-hardened-ad/
│   │   └── TDNA_Report_1_Hardened_AD_Final.docx
│   │
│   └── report-02-vulnerable-ad/
│       └── TDNA_Report_2_Vulnerable_AD_Final_Formatted.docx
│
├── methodology/
│   ├── tdna-phases.md
│   └── kerberos-attack-model.md
│
└── lab-environment/
    ├── ad-architecture.md
    └── assumptions.md
```

---

## Report Overview

### Report 1 – Hardened Active Directory (Baseline / Control)
This report documents a secure Active Directory configuration where:
- No user-based service accounts with SPNs exist
- Kerberos service tickets are issued only to machine principals
- Kerberoasting is **not applicable**

This report serves as the **control baseline** for comparison.

---

### Report 2 – Vulnerable Active Directory (Intentional Misconfiguration)
This report demonstrates Kerberoasting feasibility after a **controlled security regression**, including:
- Introduction of a user-managed service account
- Registration of a Service Principal Name (SPN)
- Use of non-expiring credentials and legacy encryption

The report documents:
- Attacker-side enumeration
- Kerberos ticket issuance
- Event log correlation
- Risk validation

---

## Methodology

Assessments follow TDNA-aligned phases:

1. Environment & Trust Validation  
2. Authentication & Kerberos Analysis  
3. Controlled Configuration Change  
4. Exploitation & Impact Validation  
5. Defensive Signal Mapping  

This approach mirrors how enterprise security teams evaluate identity-based risk.

---

## Disclaimer

All vulnerabilities demonstrated in this repository were **introduced intentionally** for training, research, and portfolio purposes.  
This repository does **not** represent a production environment.

---

## Author

Jan Zabala  
TDNA / Active Directory Security Research  
