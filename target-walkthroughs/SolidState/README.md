# SolidState — Target Walkthrough (Linux)

## Overview

This walkthrough analyzes a Linux-based messaging system exposing multiple mail-related services, demonstrating how **weak administrative controls and credential exposure** can be chained into full system compromise.

The focus of this walkthrough is **attack-path reasoning** — identifying identity-centric access vectors, abusing service trust relationships, and escalating privileges through scheduled task abuse rather than exploit-heavy techniques.

---

## 🧭 Methodology Focus

This walkthrough emphasizes:

- Enumerating non-standard services and management interfaces
- Abusing weak or default administrative credentials
- Harvesting credentials through service-level access (mailboxes)
- Escaping restricted execution environments
- Leveraging scheduled task execution for privilege escalation

The focus is on **decision-making and access-path analysis**, not exploit novelty.

---

## 🔍 Enumeration

Enumeration identified multiple exposed services related to messaging and mail delivery.

```bash
nmap -sC -sV -p- <target_ip>
```

Key observations:

- SMTP, POP3, and NNTP services exposed
- Apache James mail server in use
- Administrative interface accessible on a non-standard port
- Presence of legacy or weakly protected management services

These findings indicated a **broad identity-focused attack surface**.

---

## 🎯 Initial Access (Service Abuse)

The Apache James administrative service allowed authentication using **default credentials**.

This access enabled:

- Management of existing mail users
- Resetting mailbox credentials
- Indirect access to user communications

Rather than executing code directly, access was achieved by **manipulating identity data** within the mail system.

---

## 🔑 Credential Access & Lateral Movement

Mailbox access via POP3 revealed plaintext credentials reused for SSH access.

Key implications:

- Credential reuse collapsed authentication boundaries
- Mail services functioned as a credential store
- SSH access was achieved without exploiting the operating system

This step provided authenticated shell access as a standard user.

---

## 🧩 Restricted Shell Escape

The user environment enforced a restricted shell.

Analysis revealed multiple methods to escape execution constraints, enabling full shell access and local enumeration.

This reinforced the importance of **environment validation after access**, even when credentials are valid.

---

## 🔼 Privilege Escalation

Local enumeration identified a **root-executed scheduled task** running a world-writable Python script.

Key escalation characteristics:

- Script executed with root privileges via cron
- Writable by non-privileged users
- No integrity or permission controls

By modifying the script contents, arbitrary commands were executed as root, resulting in full system compromise.

---

## ✅ Lessons Learned

- Administrative interfaces are high-risk identity targets
- Default credentials remain a critical failure point
- Mail systems frequently expose sensitive credentials
- Credential reuse eliminates the need for complex escalation
- World-writable scheduled tasks represent catastrophic misconfigurations

---

## 🔐 OPSEC Note

This walkthrough is based on a publicly available training environment.  
No production systems, credentials, or customer data are referenced.
