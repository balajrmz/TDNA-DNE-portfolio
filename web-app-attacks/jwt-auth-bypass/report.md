# Pentest Report – JWT Auth Bypass → Admin Takeover

## 1. Executive Summary

This assessment identified weaknesses in the application's JSON Web Token (JWT) implementation that allow a malicious user to modify tokens and escalate privileges from a standard user to an administrator. Successful exploitation leads to full control over protected admin functionality and potential exposure or modification of sensitive data.

---

## 2. Scope

- **Target:** JWT authentication & authorization flow
- **Environment:** Lab environment
- **Testing Focus:**
  - Token signing/verification
  - Role/permission handling
  - Session management security

---

## 3. Technical Findings

### 3.1 Weak JWT Signature Validation

**Severity:** High  
**Impact:** Privilege escalation & full account takeover  

**Description:**  
The JWT authentication mechanism accepts modified or unsigned tokens due to improper signature validation. Attackers can elevate permissions by tampering with the payload.

**Reproduction Steps:**
1. Log in as a normal user and capture the issued JWT.
2. Decode the token header and payload.
3. Modify the payload (e.g., `"role": "admin"`).
4. Re-sign the token with a weak secret or set `alg: none` if allowed.
5. Submit the modified token to the admin endpoint.

**PoC Token:**  
_(Add sample here once attack is executed)_

**Mitigation:**
- Enforce strict algorithm allowlisting.
- Use strong secrets or asymmetric signing (RS256).
- Validate user roles server-side, not from the JWT payload.
- Add token rotation and short TTL.

**Detection & Logging:**
- Alert on access attempts with invalid signatures.
- Monitor admin endpoint anomalies.
- Log JWT header anomalies (unexpected alg values).

---

## 4. Attack Chain Diagram

_Add diagram stored under `/assets/diagrams/`_

---

## 5. Recommendations

- Follow OWASP JWT security guidelines.
- Harden signature validation.
- Implement server-side authorization mapping.
- Add tests for token verification and role elevation scenarios.

---

## 6. Appendix

- Raw HTTP requests/responses
- Decoded JWTs (redacted)
- Burp Suite logs
- Exploit script output
