# Bashed — Target Walkthrough (Linux)

## Overview

This walkthrough analyzes a Linux target with exposed web-based command execution, demonstrating how limited web access can be chained into full system compromise through privilege escalation misconfigurations.

The focus of this walkthrough is **attack-path reasoning** — how enumeration reveals execution context, how access boundaries are evaluated, and how misconfigurations enable escalation.

---

## 🧭 Methodology Focus

This walkthrough emphasizes:

- Enumerating exposed web functionality
- Assessing execution context and privilege boundaries
- Chaining low-privilege access into root-level control
- Identifying misconfigurations that enable escalation

The focus is on **decision-making and access-path reasoning**, not exploit novelty.

---

## 🔍 Enumeration

Initial enumeration focused on identifying exposed services and application functionality.

```bash
nmap -sC -sV -p- <target_ip>
```

Results indicated an HTTP service hosting a web application with limited interactive functionality.

Further inspection revealed a web-based interface capable of executing system commands under a restricted user context.

---

## 🎯 Initial Access

The exposed web interface allowed limited command execution.

Key observations during this phase:

- Commands executed under a non-privileged user
- No direct file upload capability
- Restricted execution environment

This access provided an initial foothold suitable for local enumeration and privilege escalation assessment.

---

## 🔼 Privilege Escalation

Local enumeration focused on identifying misconfigurations that could allow escalation.

Key findings included:

- Sudo permissions allowing execution of scripts without password prompts
- Writable files executed in higher-privilege contexts

These misconfigurations allowed privilege escalation from the restricted user context to root.

---

## ✅ Lessons Learned

- Web-based command execution often provides sufficient access for escalation
- Enumeration of execution context is critical before attempting exploitation
- Sudo misconfigurations remain a common and reliable escalation vector
- Low-complexity misconfigurations can have high operational impact

---

## 🔐 OPSEC Note

This walkthrough is based on a publicly available training environment.  
No production systems, credentials, or customer data are referenced.
