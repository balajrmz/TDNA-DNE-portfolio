🛡️ Target Digital Network Analysis & Digital Network Exploitation Portfolio
By Jan Zabala — TDNA | DNE | AI-Assisted Target Analytics | Identity & Network Attack Paths

Welcome to my Target Digital Network Analysis (TDNA) and Digital Network Exploitation (DNE) portfolio.  
This repository showcases work focused on analyzing digital networks as adversary targets — identifying access vectors, attack paths, and exploitation opportunities across identity, applications, and infrastructure.

My work sits at the intersection of:

• Target Digital Network Analysis (TDNA)  
• Digital Network Exploitation (DNE)  
• Identity-centric attack path analysis (AD, Cloud IAM)  
• AI/ML-assisted target analytics  
• Automation, tooling, and exploitation validation  
• OSCP-style offensive tradecraft  

All content is developed in lab, synthetic, or public environments and is designed for clarity, reproducibility, and operational realism.

---

## 🧭 How I Approach TDNA & DNE

My work follows a **target-centric methodology**, rather than tool-driven exploitation:

1. **Target Characterization**
   - Network topology, identity boundaries, exposed services
   - Trust relationships (Active Directory, cloud identity, applications)

2. **Access Vector Identification**
   - Authentication paths
   - Misconfigurations
   - Protocol weaknesses
   - Application logic flaws

3. **Attack Path Analysis**
   - Chaining access across systems, identities, and services
   - Evaluating feasibility, impact, and persistence

4. **Exploitation Validation (Lab / Synthetic)**
   - Hands-on testing in controlled environments
   - OSCP-style validation of theoretical access paths

5. **Reporting & Translation**
   - Clear articulation of risk, assumptions, and operational relevance

---

## 🚀 Featured Projects

### 1. SentinelFlow — AI-Assisted Network Threat Classification
📁 labs/sentinelflow/ | 📌 Completed

An end-to-end ML pipeline designed to analyze network behavior from an attacker and defender perspective, featuring:

• Synthetic network traffic generation  
• Flow-level feature engineering  
• RandomForest threat classification  
• Schema persistence to prevent feature drift  
• Real-time inference via FastAPI  

**Tech:** Python, Pandas, Scikit-Learn, FastAPI, Uvicorn

---

### 2. ShadowHound — Identity Attack Path Analysis
📁 labs/shadowhound/ | 📌 Completed

An Active Directory attack-path analysis engine that:

• Parses and normalizes BloodHound data  
• Identifies high-risk privilege escalation paths  
• Applies reasoning logic to surface exploitable relationships  
• Outputs structured access path recommendations  

**Tech:** Python, Graph Analysis, JSON Processing

---

### 3. CloudSentinel — Cloud IAM Misconfiguration Lab
📁 labs/cloudsentinel/ | 📌 Completed

A lab focused on cloud identity targeting, including:

• IAM policy experimentation  
• Common misconfiguration patterns  
• Foundations for automated risk scoring and analysis APIs  

**Tech:** Python, AWS & Azure IAM Concepts, JSON Policy Analysis

---

### 4. PacketVision — Network Capture Analysis Lab
📁 labs/packetvision/ | 📌 Completed

A network-focused lab exploring offensive visibility and tradecraft:

• Parsing and inspecting packet captures  
• Identifying attacker-relevant visibility gaps  
• Prototyping concepts for AI-assisted recon and evasion  

**Tech:** Python, PCAP / Traffic Analysis

---

### 5. ZeroTrace — Stealth, Telemetry & Detection Gaps
📁 labs/zerotrace/ | 📌 Completed

An experimental space for:

• Studying logging and telemetry blind spots  
• Exploring stealth techniques and detection resistance  
• Informing how offensive tooling is designed and tested  

**Tech:** Python, Logging & Telemetry Concepts, Offensive R&D

---

## 🧪 Additional Projects (In Progress / Planned)

• **RedRiver** — AI-assisted network flow analysis & adversary behavior modeling  
• **AnomalyHunter** — Isolation Forest & One-Class SVM anomaly detection  
• **MalScanAI** — Byte-level malware classification  
• **WebGuard** — ML-based web exploit detection  
• **AttackGraph Generator** — Graph-based AD escalation mapping  
• **DockerSec Inspect** — Dockerfile vulnerability analysis  
• **Credential Auditor** — Entropy & breach correlation engine  

---

## 🖥️ Hack The Box Writeups (Sanitized)

Writeups focus on **methodology and transferable patterns**, not box-specific trivia:

• Active — AD Enumeration & Kerberos Abuse  
• Reel — Payload Delivery & Initial Access  
• Archetype — Azure Hybrid Attack Paths  
• Nineveh — Multi-Service Recon & Chaining  
• Celestial — Application Logic & Reverse Engineering  

---

## 🧭 Repository Structure

tdna-dne-portfolio/
│
├── labs/
│   ├── sentinelflow/
│   ├── shadowhound/
│   ├── cloudsentinel/
│   ├── packetvision/
│   ├── zerotrace/
│   └── ...
│
├── writeups/
│   ├── active.md
│   ├── reel.md
│   ├── archetype.md
│   ├── nineveh.md
│   └── celestial.md
│
├── dne-automation/
├── identity-attack-paths/
├── cloud-identity-and-access/
├── application-access-vectors/
├── offensive-tradecraft-workflows/
├── assets/
│
└── README.md

---

## 🔐 Core Competencies Demonstrated

### Target Digital Network Analysis & Exploitation
• Attack-path reasoning and access vector identification  
• Identity-centric targeting (AD, cloud IAM)  
• Enumeration, exploitation, and privilege escalation workflows  

### AI-Assisted Target Analytics
• Synthetic traffic generation  
• ML-based behavioral modeling  
• AI-assisted attack surface mapping  

### Cloud & Identity Security
• Azure & AWS IAM misconfiguration analysis  
• Hybrid AD / cloud attack paths  
• Detection and telemetry considerations  

### Engineering & Architecture
• Python-based tooling and automation  
• FastAPI microservices  
• Reproducible, GitHub-ready project structure  

---

## 🧭 Roadmap

• Expand to 12+ mature TDNA/DNE projects  
• Add Dockerized deployments for AI services  
• Publish an Offensive Network Targeting handbook  
• Launch a dedicated portfolio website  
• Expand AI-assisted target analytics and access-path modeling  

---

## 👤 About Me

**Jan Zabala**  
Target Digital Network Analysis & Digital Network Exploitation  
CEH | OSCP (in progress)  

Background in HUMINT & Special Operations–aligned intelligence  
Cybersecurity Bachelor’s student  
Focused on adversary-centric, AI-accelerated network targeting

---

## 📫 Contact

GitHub: https://github.com/balajrmz  
LinkedIn: https://www.linkedin.com/in/jan-zabala-5aaa59380  
Email: jzabala81@protonmail.com
