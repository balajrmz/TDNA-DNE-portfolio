# TDNA – Active Directory Kerberos Assessment

This repository contains a **two-part Active Directory Kerberos assessment** conducted using a **Trust-Driven Network Analysis (TDNA)** methodology.

To maintain professional clarity, **internal lab hostnames have been abstracted** in documentation to reflect enterprise-typical naming conventions. The technical findings and workflows remain unchanged.

---

## Naming Abstraction

| Lab Hostname | Documented Name |
|-------------|-----------------|
| CaramelDC   | DC-PRIMARY      |
| OnlyFanDC  | DC-SECONDARY    |
| SRV-RTR    | SQL-SRV-01      |
| ATTACKER   | WKSTN-ATTACK-01 |

All reports and documentation below use the **Documented Name** column.

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
Senior Cybersecurity Analyst  
Identity, Active Directory, and Kerberos Security
