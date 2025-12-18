# Devel — Target Walkthrough (Windows)

## Overview

This walkthrough analyzes a Windows web server exposing a writable FTP service mapped directly to the IIS web root. It demonstrates how **misconfigured file transfer permissions** can provide immediate web-based code execution, which can then be chained into full system compromise through **token impersonation privileges**.

The focus of this walkthrough is **attack-path reasoning** — identifying weak trust boundaries between services, validating execution context, and assessing privilege escalation opportunities on Windows systems.

---

## 🧭 Methodology Focus

This walkthrough emphasizes:

- Identifying dangerous service-to-service trust relationships
- Validating write access as an execution vector
- Assessing Windows privilege tokens and impersonation rights
- Chaining initial access into SYSTEM-level compromise
- Prioritizing reliable escalation paths over exploit novelty

The focus is on **decision-making and access-path analysis**, not tool-specific exploitation.

---

## 🔍 Enumeration

Enumeration focused on exposed network services and permission boundaries.

```bash
nmap -sC -sV -p- <target_ip>
```

Key observations:

- FTP service allowed anonymous authentication
- FTP directory mapped directly to the IIS web root
- Web server accessible over HTTP
- Windows host with common IIS deployment patterns

These findings indicated a **high-confidence path to web-based code execution**.

---

## 🎯 Initial Access

Anonymous FTP access allowed file uploads to the web root.

By uploading a server-side script to the writable directory, arbitrary command execution was achieved through the web server context.

Key access characteristics:

- No authentication required beyond anonymous FTP
- Immediate execution via HTTP request
- Execution context limited to the IIS service account

This provided a stable initial access point for local enumeration.

---

## 🔼 Privilege Escalation

Local enumeration identified **SeImpersonatePrivilege**, a Windows privilege commonly abused for escalation.

Key considerations:

- IIS service accounts frequently possess impersonation rights
- Token impersonation enables privilege escalation without kernel exploits
- Escalation reliability is high when impersonation privileges are present

Abuse of impersonation privileges resulted in SYSTEM-level access.

---

## ✅ Lessons Learned

- Writable file transfer services mapped to web roots are critical misconfigurations
- Initial access does not require exploits when trust boundaries are weak
- Token impersonation remains a common and reliable Windows escalation vector
- Enumeration of privileges is as important as vulnerability discovery

---

## 🔐 OPSEC Note

This walkthrough is based on a publicly available training environment.  
No production systems, credentials, or customer data are referenced.
