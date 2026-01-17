# Hybrid Identity Attack Paths (Enterprise Identity Risk)

## Overview
This repository examines how identity risk and attack paths evolve as large enterprises transition from on‑prem Active Directory (AD) environments to hybrid and cloud identity models.

It is written from the perspective of regulated, security‑mature organizations where stability, auditability, and risk prioritization are critical. The focus is not exploitation, but understanding how identity trust and privilege decisions propagate across hybrid identity boundaries.

---

## Enterprise Context (Why This Matters for Financial Institutions)
In large financial institutions, identity is the foundation of access control, auditability, and operational trust. As organizations move toward cloud operating models, identity increasingly becomes the control plane that governs both infrastructure and data access.

Legacy AD design decisions — including standing privilege, broad delegation, and implicit trust — do not disappear during cloud adoption. Instead, they often extend into hybrid identity platforms, where their impact can scale rapidly.

Managing this transition safely requires:
- Clear Tier 0 definition across on‑prem and cloud
- Prioritization of identity risk, not just enumeration
- Guardrails that reduce risk without disrupting business operations

---

## Key Concepts
- **Identity is the control plane**
- **Tier 0 does not disappear in the cloud — it shifts**
- **Hybrid identity stretches trust boundaries rather than removing them**
- **Risk reduction must balance security, availability, and operational impact**

---

## Cloud Shift: Tier 0 Beyond the Domain Controller
In traditional on‑prem environments, Tier 0 typically includes:
- Domain Controllers
- Directory administration surfaces
- Highly privileged groups and delegated rights

In hybrid and cloud environments, Tier 0 expands to include:
- Identity provider configuration (e.g., Entra ID tenant control)
- Privileged cloud roles and role assignment mechanisms
- Token issuance and federation paths
- Control‑plane APIs and policy enforcement services

Understanding how privilege moves across these boundaries is essential to reducing blast radius during cloud adoption.

---

## Repository Structure
This repository separates analysis, remediation, and supporting visuals to reflect how identity risk should be approached in enterprise environments:

```
analysis/
  ├── on_prem_identity_risk.md
  ├── hybrid_identity_risk.md
  └── cloud-control-plane.md

remediation/
  ├── identity-guardrails.md
  └── phased-migration.md

visuals/
  ├── hybrid-trust-boundaries.png
  └── tier0-shift-onprem-to-cloud.png

notes/
  └── assumption-and-limits.md
```

---

## Visual Models
### Tier 0 Shift (On‑Prem → Hybrid → Cloud)
This diagram illustrates how Tier 0 authority transitions from directory‑centric control to identity‑provider and cloud control‑plane dominance.

![Tier 0 Shift](visuals/tier0-shift-onprem-to-cloud.png)

### Hybrid Trust Boundaries
This diagram highlights where trust crosses boundaries between users, administrators, on‑prem systems, and cloud identity services.

![Hybrid Trust Boundaries](visuals/hybrid-trust-boundaries.png)

---

## How BloodHound Fits In
BloodHound provides visibility into complex identity trust relationships that are difficult to reason about using traditional lists or spreadsheets.

In enterprise environments, its value is not in raw enumeration, but in:
- Visualizing privilege relationships and implicit trust
- Identifying paths that converge on Tier 0
- Supporting risk‑based discussions with defensive teams

However, large environments often generate hundreds or thousands of potential paths. Without prioritization, this can overwhelm remediation efforts.

---

## ShadowHound and Risk Prioritization
ShadowHound builds on attack‑path visibility by focusing on **prioritization and impact** rather than volume.

The intent is to:
- Rank identity paths by proximity to Tier 0
- Account for privilege strength and blast radius
- Help security teams focus on changes that materially reduce risk

In regulated enterprises, this approach aligns better with operational reality, audit constraints, and change‑management processes.

---

## What This Repository Covers
- On‑prem AD trust and privilege accumulation
- Hybrid AD ↔ Entra ID identity risk
- Cloud control‑plane privilege patterns (AWS, Azure, GCP – conceptual)
- Identity guardrails suitable for regulated environments
- A phased approach to reducing identity risk during cloud migration

---

## What This Repository Is Not
- An exploitation guide
- A step‑by‑step attack walkthrough
- Based on real organizational data
- A cloud engineering or deployment tutorial

---

## Intended Audience
- IAM / PAM engineers
- Identity governance teams
- Threat‑informed defense teams
- Security architects in regulated enterprises
- Leaders responsible for identity risk during cloud adoption

---

## Safety & Ethics
All content is conceptual and defensive in nature.  
No real environments, credentials, or organizational data are used.

The intent is to support responsible identity security decision‑making in large enterprise and financial‑services environments.

---

## Why This Matters
As enterprises modernize infrastructure, identity mistakes scale faster than traditional system failures.

Understanding how attack paths evolve — and how to prioritize their remediation safely — is essential to protecting modern enterprise control planes.
