# Lame — Target Walkthrough (Linux)

## Overview

This walkthrough analyzes a legacy Linux target exposing multiple network services with known, high-impact vulnerabilities. It demonstrates how disciplined service enumeration can quickly identify **catastrophic, unauthenticated access paths** resulting from outdated software.

The focus of this walkthrough is **attack-path reasoning** — recognizing when a target fails at the perimeter and prioritizing the most reliable access vector rather than chaining lower-confidence techniques.

---

## 🧭 Methodology Focus

This walkthrough emphasizes:

- Broad service enumeration and version identification
- Rapid prioritization of high-confidence vulnerabilities
- Assessing when exploitation results in immediate root access
- Understanding the operational risk of unpatched legacy services
- Avoiding unnecessary exploitation complexity

The focus is on **decision-making and access-path analysis**, not exploit novelty.

---

## 🔍 Enumeration

Enumeration focused on identifying exposed services and their versions.

```bash
nmap -sC -sV -p- <target_ip>
```

Key observations:

- FTP service exposed (vsftpd 2.3.4)
- SSH service available but not required for access
- Samba service running a legacy version
- Additional services indicating poor patch hygiene

Service version analysis revealed **Samba 3.0.20**, a version associated with a well-known remote code execution vulnerability.

---

## 🎯 Initial Access

The Samba service was vulnerable to **CVE-2007-2447**, allowing unauthenticated remote command execution.

Key access characteristics:

- Network-based exploitation
- No authentication required
- Immediate execution with root privileges

This represented a **single-step compromise** with no requirement for lateral movement or local privilege escalation.

---

## 🔼 Privilege Context

No additional privilege escalation was required.

Key implications:

- The vulnerability provided direct root access
- Demonstrates total failure of perimeter defense
- Highlights the risk of running end-of-life services in exposed environments

---

## ✅ Lessons Learned

- Version awareness during enumeration is critical
- Some targets fail entirely at the service exposure layer
- High-confidence exploits should be prioritized over complex chains
- Legacy services dramatically increase attack surface and risk

---

## 🔐 OPSEC Note

This walkthrough is based on a publicly available training environment.  
No production systems, credentials, or customer data are referenced.
