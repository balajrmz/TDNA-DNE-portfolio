# 🛡️ Offensive Security Engineering Portfolio  
**By Jan Zabala — Offensive Security | Cloud Security | AI Security**

Welcome to my curated portfolio of hands-on security engineering projects.  
This repository showcases practical, end-to-end work across:

- Penetration Testing  
- Cloud Security (AWS, Azure, Identity/IAM)  
- Machine Learning for Security Detection  
- Threat Hunting & SOC Engineering  
- Security Automation & Tool Development  
- Linux, Networking, and OSCP-level techniques  

Each project is built to demonstrate real-world, applied skills — not academic examples.  
Nearly every tool here is structured, documented, and designed like production code.

---

# 🚀 Featured Projects

## 1. **SentinelFlow — AI-Driven Network Threat Classifier**
📌 *Status: Complete*  
📁 `labs/sentinelflow/`

An end-to-end ML pipeline that:

- Generates synthetic network traffic  
- Builds engineered ML features  
- Trains a RandomForest classifier (normal vs scan vs DoS)  
- Saves model artifacts + feature schema  
- Serves real-time predictions via FastAPI  

**What it demonstrates:**

- Security ML engineering  
- Feature engineering for network flows  
- Preventing schema drift with persisted feature columns  
- Building inference microservices  

**Tech:** Python, Pandas, Scikit-Learn, FastAPI, Uvicorn  
➡️ Full details in: `labs/sentinelflow/README.md`

---

## 2. **CloudSentinel — AWS IAM Misconfiguration & Risk Analyzer**
📌 *Status: In Progress (Coming Next)*  
📁 `labs/cloudsentinel/`

A hybrid **rule-based + ML** engine that evaluates IAM policies for:

- Privilege escalation paths  
- Wildcards (`"Action": "*"` / `"Resource": "*"`)  
- Dangerous combinations (e.g., PassRole + EC2)  
- Overly broad role assumptions  
- High-risk admin patterns  

Outputs a structured risk score + explanations via a FastAPI API.

**Tech:** Python, IAM Analysis, ML, FastAPI  

---

# 🧪 Additional Labs (Coming Soon)

These will be added daily to build out a ~12-project portfolio:

- **RedTeamRecon** — Automated OSINT + Subdomain Hunter  
- **MalScanAI** — Static Malware Classifier (byte-level ML)  
- **LogShield** — SIEM Rule Generator & Log Parser  
- **WebGuard** — ML Classifier for SQLi/XSS/LFI Detection  
- **PKINIT Analyzer** — Detect AD PKINIT Misconfigurations  
- **DockerSec Inspect** — Dockerfile Security Scanner  
- **AnomalyHunter** — Isolation Forest & One-Class SVM  
- **AttackGraph Generator** — Graph-based Attack Paths  
- **Credential Auditor** — Password Entropy & Breach Checker  
- **Offensive Tools Collection** — Red Team Utilities  

Each will be fully documented with READMEs and clean code.

---

# 🧭 Repository Structure

```
pentest-portfolio/
│
├── labs/
│   ├── sentinelflow/           # AI network detection pipeline
│   ├── cloudsentinel/          # IAM risk analyzer (coming)
│   └── ...                     # additional labs as added
│
├── offensive-tools/            # custom red-team / pentest tools
├── web-app-attacks/            # web exploit and payload labs
└── README.md                   # <-- this file
```

---

# 🧰 Core Skills Demonstrated

### 🔐 **Offensive Security**
- Enumeration, exploitation, privilege escalation  
- Custom tooling development  
- Active Directory & Kerberos exploration  
- OSCP-style methodologies  

### ☁️ **Cloud Security (AWS/Azure)**
- IAM analysis & threat modeling  
- Cloud logging & detection engineering  
- Identity-based attack paths  

### 🤖 **Machine Learning for Security**
- Synthetic dataset generation  
- Feature engineering for detection  
- Supervised & unsupervised models  
- API-based inference services  

### 🛠️ **Engineering & Automation**
- Python package design  
- FastAPI microservices  
- Virtual environments, linting, structured code  
- Git/GitHub workflows  

---

# 🎯 Roadmap

- Add 12+ professional-grade labs  
- Create an “Offensive Security Engineering Handbook” PDF  
- Add Docker images for all major ML or API projects  
- Build a portfolio web page linking to each lab  

---

# 👤 About Me

**Jan Zabala**  
*Offensive Security Engineering | Cloud Security | AI/ML for Detection*  

- OSCP (in progress), CEH  
- Background in HUMINT / Special Operations  
- Cybersecurity Bachelor’s Student  
- Hands-on practitioner building real tools  
- Passion for automation, AI, cloud identity, and red-team methodology  

---

# 📫 Contact

- GitHub: https://github.com/balajimz  
- LinkedIn: www.linkedin.com/in/jan-zabala-5aaa59380 
- Email:   

---

If you'd like, I can also create:

- A visual **portfolio banner** for the top of this README  
- Badges (Python, FastAPI, ML, Cybersecurity)  
- Navigation buttons  
- A better ASCII or PNG architecture diagram  
- A pinned repositories section  

Just say:  
**“BackDoor, let’s polish the portfolio.”**
