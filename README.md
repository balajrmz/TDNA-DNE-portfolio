# TDNA–DNE Portfolio
**Adversary-Centric Offensive Security & Purple Team Research**

This repository contains hands-on offensive security research focused on adversary emulation,
attack-path reasoning, and threat-based testing designed to improve real-world detection and response.

The work emphasizes how attackers realistically move through environments, how defensive assumptions
are validated, and how offensive findings translate into detection and remediation outcomes.

---

## Methodology & Adversary Perspective

This portfolio shows how I analyze digital networks the way an attacker would —
not just looking for vulnerabilities, but understanding how systems, identities,
and trust relationships connect and can be abused together.

Instead of focusing on individual tools or exploits, the work here emphasizes
**attack-path reasoning**: how access is realistically gained, how it spreads,
and which paths are actually worth pursuing.

The projects combine offensive security techniques, intelligence-style analysis,
and automation to demonstrate how complex environments can be broken down,
understood, and targeted in a deliberate way.

---

## ⭐ Flagship Project: ShadowHound

**ShadowHound** is an identity attack-path analysis engine for **Active Directory**, designed to
support **Target Digital Network Analysis (TDNA)** and **Digital Network Exploitation (DNE)**
through threat-based testing and purple team use cases.

It treats identity infrastructure as a **target surface**, enabling analysts and security teams
to reason about privilege escalation paths, lateral movement, and exploitation feasibility
using graph analysis and ML-assisted risk scoring. The project is intended to help prioritize
high-impact identity attack paths and validate detection and remediation assumptions.

📂 **Start here:** `ai-driven-security-projects/shadowhound/`  
➡️ This is the best single project to review for understanding my approach to adversary-centric
network analysis and identity-focused offensive security.

---

Welcome to my **Target Digital Network Analysis (TDNA)** and
**Digital Network Exploitation (DNE)** portfolio.

This repository showcases work focused on analyzing digital networks as
**adversary targets** — identifying access vectors, attack paths, and exploitation
opportunities across **identity, applications, and infrastructure**.

All content is developed in **lab, synthetic, or public environments** and is designed
for clarity, reproducibility, and operational realism.

---

## 🔍 Areas of Focus

- Target Digital Network Analysis (TDNA)
- Digital Network Exploitation (DNE)
- Identity-centric attack path analysis (Active Directory & Cloud IAM)
- Threat-based offensive security testing
- Purple team detection validation
- AI / ML–assisted target analytics
- Automation and exploitation validation

---

## 🧭 How I Approach TDNA & DNE

My work follows a **target-centric methodology**, rather than tool-driven exploitation:

1. **Target Characterization**  
   Network topology, identity boundaries, exposed services, and trust relationships.

2. **Access Vector Identification**  
   Authentication paths, misconfigurations, protocol weaknesses, and application logic flaws.

3. **Attack Path Analysis**  
   Chaining access across identities, services, and systems to assess feasibility and impact.

4. **Exploitation Validation (Lab / Synthetic)**  
   Hands-on validation of theoretical access paths using controlled environments to test
   detection and prevention controls.

5. **Reporting & Translation**  
   Clear articulation of findings, assumptions, and security relevance for remediation.

---

## 🚀 Featured AI-Driven Security Projects

All projects below live under:

```
ai-driven-security-projects/
```

### 🔵 ShadowHound — Identity Attack Path Analysis (Active Directory)
Graph-based analysis of identity relationships and privilege escalation paths using ML-assisted
risk scoring to support threat-based testing and remediation prioritization.

### 🔴 RedRiver — AI-Assisted Network Flow Analysis
Models adversary-relevant network behaviors to support access-path reasoning,
detection validation, and purple team exercises.

### ☁️ CloudSentinel — Cloud Identity & IAM Misconfiguration Analysis
Target-centric analysis of cloud IAM policies and privilege escalation via misconfiguration.

### 🟣 PacketVision — Network Visibility & Packet Analysis
Packet-level visibility analysis to understand attacker tradecraft and telemetry gaps.

### 🟢 SentinelFlow — Network Behavior Classification
End-to-end ML pipeline for classifying reconnaissance, scanning, and disruptive behaviors.

### 🟠 ZeroTrace — Stealth & Telemetry Gap Analysis
Analysis of logging blind spots and detection boundaries that enable low-noise attacker activity.

---

## 🖥️ Target Walkthroughs (Sanitized)

This section contains **sanitized, methodology-focused walkthroughs** derived from publicly
available training environments. These are not step-by-step exploit guides; they are
**analyst-style breakdowns** emphasizing decision-making, attack-path reasoning,
and transferable patterns relevant to TDNA and DNE work.

All walkthroughs are OPSEC-safe and focus on *how to think*, not just *what to type*.

---

## 🧩 Identity as a Control Plane (On-Prem → Hybrid → Cloud)

This portfolio places particular emphasis on **identity as a control plane** across modern
enterprise environments.

Rather than treating Active Directory, hybrid identity, and cloud IAM as separate problems,
the work here models how **trust, privilege, and attack paths evolve** as organizations
transition from on-prem infrastructure to hybrid and cloud operating models.

---

## 🧭 Repository Structure

```
tdna-dne-portfolio/
│
├── ai-driven-security-projects/
│   ├── redriver/
│   ├── shadowhound/
│   ├── cloudsentinel/
│   ├── packetvision/
│   ├── sentinelflow/
│   └── zerotrace/
│
├── target-walkthroughs/
├── identity-attack-paths/
├── cloud-identity-and-access/
├── application-access-vectors/
├── offensive-tradecraft-workflows/
├── assets/
└── README.md
```

---

## 👤 About Me

**Jan Zabala**  
Offensive Security | Red & Purple Team | Adversary Emulation  
CEH | OSCP (in progress)

Background in HUMINT & Special Operations–aligned intelligence  
Focused on adversary-centric, threat-based offensive security and detection validation

---

> All work is for authorized testing, research, or educational purposes only.
