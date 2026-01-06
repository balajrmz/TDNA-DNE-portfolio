# TDNA – Active Directory Kerberos Assessment

This repository contains a **two-part Active Directory Kerberos assessment** conducted using a **Trust-Driven Network Analysis (TDNA)** methodology.

The purpose of this work is to demonstrate **how Kerberos attack feasibility changes based on service account design and configuration**, not just how to execute an attack.

This repository is intentionally structured to show **cause-and-effect**, rather than exploitation in isolation.

---

## What This Repository Demonstrates

- A **hardened Active Directory baseline** where Kerberoasting is not possible  
- A **deliberately misconfigured Active Directory environment** where Kerberoasting becomes viable  
- A controlled comparison using **identical attacker positioning**  
- Windows-native attacker workflows aligned with real enterprise environments  
- Clear defensive visibility through Kerberos and security event logging  

---

## Repository Structure

```
tdna-active-directory/
├── reports/
│   ├── report-01-hardened-ad/
│   │   └── Report_01_Hardened_AD.pdf
│   └── report-02-vulnerable-ad/
│       └── Report_02_Vulnerable_AD.pdf
│
├── methodology/
│   ├── tdna-phases.md
│   └── kerberos-attack-model.md
│
├── lab-environment/
│   └── .gitkeep
│
└── README.md
```

---

## Reports

### Report 01 – Hardened Active Directory  
**Kerberoasting Not Possible**

📄 **PDF:**  
[Report_01_Hardened_AD.pdf](reports/report-01-hardened-ad/Report_01_Hardened_AD.pdf)

---

### Report 02 – Vulnerable Active Directory  
**Kerberoasting Enabled by Design**

📄 **PDF:**  
[Report_02_Vulnerable_AD.pdf](reports/report-02-vulnerable-ad/Report_02_Vulnerable_AD.pdf)

---

## Methodology

This assessment follows a **Trust-Driven Network Analysis (TDNA)** approach:
1. Establish trust boundaries  
2. Validate default behavior  
3. Introduce controlled misconfiguration  
4. Observe attacker feasibility  
5. Correlate attacker actions with defender telemetry  

---

## Disclaimer

This repository is for **educational and defensive research purposes only**.  
All environments are **isolated lab systems** with no production data.

---

## Author

**Jan Zabala**  

