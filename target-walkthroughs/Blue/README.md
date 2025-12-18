# Blue — Target Walkthrough (Windows)

## Overview

This walkthrough analyzes a legacy Windows target vulnerable to **MS17-010 (EternalBlue)**, demonstrating how an exposed and unpatched network service can provide immediate, unauthenticated system-level access.

The focus of this walkthrough is **attack-path reasoning** — identifying high-confidence exploitation opportunities during enumeration and understanding the operational impact of missing patch management on enterprise systems.

---

## 🧭 Methodology Focus

This walkthrough emphasizes:

- Identifying high-impact vulnerabilities during network enumeration
- Assessing exploit reliability versus alternative access paths
- Understanding the operational risk of unpatched legacy systems
- Evaluating how single-vulnerability failures collapse security boundaries

The focus is on **decision-making and access-path analysis**, not exploit novelty.

---

## 🔍 Enumeration

Enumeration focused on identifying exposed services and protocol versions.

```bash
nmap -sC -sV -p- <target_ip>
```

Key observations:

- SMB service exposed over TCP/445
- SMBv1 enabled
- Target identified as legacy Windows system
- Strong indicators of vulnerability to MS17-010

Based on these findings, MS17-010 represented a **high-confidence access vector**.

---

## 🎯 Initial Access

The MS17-010 vulnerability allows unauthenticated remote code execution via the SMB protocol.

Exploitation characteristics:

- No credentials required
- Network-based exploitation
- Immediate high-privilege execution context

This vulnerability provided direct SYSTEM-level access without the need for lateral movement or local privilege escalation.

---

## 🔼 Privilege Context

Unlike many targets, this system required **no additional privilege escalation**.

Key implications:

- Exploitation directly resulted in SYSTEM access
- Demonstrates catastrophic impact of missing critical patches
- Highlights why legacy SMB configurations are high-risk

---

## ✅ Lessons Learned

- Patch management failures can enable total compromise
- High-confidence exploits should be prioritized during access-path analysis
- Legacy protocol support (SMBv1) dramatically increases risk
- Some environments fail at the perimeter, not during escalation

---

## 🔐 OPSEC Note

This walkthrough is based on a publicly available training environment.  
No production systems, credentials, or customer data are referenced.
