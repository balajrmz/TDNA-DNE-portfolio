# JWT Auth Bypass → Privilege Escalation → Admin Takeover

## Overview

This project demonstrates a real-world attack chain against a JSON Web Token (JWT)-based authentication system.  
By abusing weak JWT validation and insecure role handling, an attacker can escalate from a normal user to an administrator and gain full control over protected application functionality.

## Goals

- Identify JWT implementation weaknesses
- Craft modified tokens to escalate privileges
- Demonstrate end-to-end account takeover
- Provide secure implementation and mitigation guidance

## Environment (Planned)

- Vulnerable web app (JWT-based auth)
- Backend: Node/Express or Python/Flask
- Database: SQLite/Postgres (lab)
- Tools: Burp Suite, jwt.io, curl, custom Python exploit

## Contents

- `report.md` – FAANG-style pentest report
- `exploit.py` – PoC exploit for JWT tampering / privilege escalation
- `screenshots/` – Evidence of exploitation
- `notes.md` – Extra lab notes, commands, and references

## Status

