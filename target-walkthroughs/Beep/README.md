# Beep — Target Walkthrough (Linux)

## Overview

This walkthrough analyzes a legacy Linux-based communications appliance with an unusually large exposed attack surface. It demonstrates how careful enumeration and identification of a single web application weakness can be chained into full system compromise through **credential disclosure and reuse**, rather than local privilege escalation.

The focus of this walkthrough is **attack-path reasoning** — narrowing a noisy target, identifying the most promising access vector, and understanding how legacy systems collapse security boundaries through misconfiguration.

---

## 🧭 Methodology Focus

This walkthrough emphasizes:

- Reducing a broad attack surface through disciplined enumeration
- Identifying high-impact vulnerabilities within complex service stacks
- Leveraging configuration disclosure rather than exploit chaining
- Exploiting credential reuse to bypass traditional privilege escalation
- Accounting for legacy protocol constraints during access validation

The focus is on **decision-making and access-path analysis**, not exploit novelty.

---

## 🔍 Enumeration

Initial enumeration revealed a target exposing numerous services typical of a legacy VoIP and messaging appliance.

```bash
nmap -p- --min-rate 1000 -T4 <target_ip>
nmap -sC -sV -p22,80,443,10000 <target_ip>
```

Key observations:

- Large number of exposed services increased noise but not value
- Web services presented the most promising access vector
- Legacy software versions suggested configuration and input validation weaknesses

Web enumeration identified multiple application paths, including a legacy CRM component.

---

## 🎯 Initial Access

Further inspection revealed a **Local File Inclusion (LFI)** vulnerability in a web application component, allowing arbitrary file reads.

This vulnerability enabled retrieval of sensitive configuration files, including application credentials stored in plaintext.

Key access characteristics:

- No authentication required to exploit the LFI
- Direct disclosure of backend credentials
- No need for code execution at this stage

This access vector provided credentials with elevated privileges.

---

## 🔼 Privilege Escalation (Credential Reuse)

Rather than escalating privileges locally, this target relied on **credential reuse** across services.

Analysis of disclosed configuration files revealed credentials reused for administrative access, including SSH.

Important considerations:

- Password reuse eliminated the need for kernel or sudo exploitation
- Direct administrative access was possible immediately upon authentication
- Legacy SSH configurations required enabling deprecated key-exchange algorithms

This resulted in direct root-level access.

---

## ✅ Lessons Learned

- Broad attack surfaces often hide a single high-impact weakness
- Configuration disclosure can be more powerful than code execution
- Credential reuse collapses privilege boundaries entirely
- Legacy systems frequently require adapting tooling to older cryptographic standards
- Enumeration discipline is critical in noisy environments

---

## 🔐 OPSEC Note

This walkthrough is based on a publicly available training environment.  
No production systems, credentials, or customer data are referenced.
