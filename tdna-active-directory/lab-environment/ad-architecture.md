# Active Directory Architecture (Sanitized)

This document describes the Active Directory lab environment used for the TDNA Kerberos assessments.
All hostnames have been **sanitized** to reflect enterprise-typical naming conventions. The underlying
lab configuration and behavior remain unchanged.

---

## Naming Abstraction

| Lab Hostname | Documented Name |
|-------------|-----------------|
| CaramelDC   | DC-PRIMARY      |
| OnlyFanDC  | DC-SECONDARY    |
| SRV-RTR    | SQL-SRV-01      |
| ATTACKER   | WKSTN-ATTACK-01 |
| Client VM  | WKSTN-USER-01   |

All subsequent references use the **Documented Name** column.

---

## Forest & Domain

- Forest Name: `example.local`
- Single-domain forest
- Functional Level: Windows Server 2019

---

## Domain Controllers

### DC-PRIMARY
- Role: Primary Domain Controller
- Services:
  - Active Directory Domain Services (AD DS)
  - DNS
  - DHCP
- FSMO Roles:
  - Schema Master
  - Domain Naming Master
  - RID Master
  - PDC Emulator
  - Infrastructure Master
- Global Catalog: Enabled

### DC-SECONDARY
- Role: Secondary Domain Controller
- Services:
  - Active Directory Domain Services (AD DS)
  - DNS
- Global Catalog: Enabled
- Purpose:
  - Redundancy
  - Replication validation
  - Multi-DC attack surface analysis

---

## Member Servers

### SQL-SRV-01
- Role: Application / SQL Server
- Domain Joined
- Purpose:
  - Host service account workload
  - Provide Kerberos SPN target for assessment
- Service Accounts:
  - `svc_sql` (intentionally misconfigured in Report 2)

---

## Workstations

### WKSTN-USER-01
- Role: Standard domain user workstation
- Used to validate user-level access controls and GPO behavior

### WKSTN-ATTACK-01
- Role: Attacker workstation
- Domain joined
- Used to simulate internal attacker with valid low-privilege credentials

---

## Network Segmentation

- Domain Controllers reside on a protected server network
- Member servers reside on a server VLAN
- User workstations and attacker workstation reside on the same logical client network
- No external trusts or cross-forest relationships configured

---

## Security Posture (Baseline)

- Default Windows security auditing enabled
- No custom SIEM or correlation rules
- No endpoint detection interference
- No gMSA usage for legacy SQL service (intentional for Report 2)

---

## Notes

This architecture was designed to:
- Reflect realistic enterprise Active Directory deployments
- Support controlled comparison between hardened and vulnerable Kerberos configurations
- Enable both offensive validation and defensive telemetry analysis
