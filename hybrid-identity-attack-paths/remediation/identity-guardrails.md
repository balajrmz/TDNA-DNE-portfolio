# Hybrid Identity Risk (AD ↔ Entra ID)

## Key Shift
Hybrid identity extends trust from on-prem Active Directory into cloud identity platforms. This transition does not inherently reduce risk; instead, it relocates and often amplifies it.

As identity becomes the primary control plane, weaknesses in privilege design and governance can have cross-environment impact.

---

## Boundary Stretching
In hybrid environments:
- On-prem privilege can influence cloud identity posture
- Identity changes propagate more quickly and broadly
- Token-based access can increase blast radius compared to traditional credential abuse

Hybrid identity should be treated as a trust extension, not a clean break from on-prem risk.

---

## Cloud Tier 0 (Conceptual)
In cloud and hybrid environments, Tier 0 commonly includes:
- Identity provider configuration and tenant-wide administration
- Privileged cloud roles and role assignment mechanisms
- Token issuance, federation, and authentication policy
- Control-plane APIs and security policy enforcement

Control of these elements enables wide-reaching impact across environments.

---

## Common Enterprise Risk Patterns
- Reuse of administrative identities across on-prem and cloud
- Standing administrative privilege without time-bound controls
- Limited conditional access enforcement for privileged actions
- Weak separation between user, admin, and service identities

These patterns often emerge for operational convenience and persist without intentional remediation.

---

## Representative Hybrid Risk Scenario (Conceptual)

### Scenario
An enterprise operates a hybrid identity model with on-prem Active Directory synchronized to a cloud identity provider. For convenience, administrative identities are reused across both environments.

### Risk Pattern
- Standing on-prem administrative privilege
- Privileged identities synchronized into cloud identity
- Limited conditional access enforcement for administrative actions
- Cloud roles capable of tenant-wide impact

### Why This Matters
In this model, compromise of a single high-privilege identity can affect both on-prem and cloud control planes. The resulting blast radius exceeds traditional directory compromise and may include cloud-wide access, persistence, and policy manipulation.

### Defensive Considerations
- Separate administrative identities from daily-use accounts
- Enforce just-in-time elevation for sensitive roles
- Apply conditional access controls to privileged actions
- Explicitly define Tier 0 across hybrid identity boundaries

### Prioritization Insight
Not all identity paths present equal risk. Paths that converge on identity-provider control and privileged role assignment represent higher-impact remediation opportunities and should be addressed first.

---

## What Good Looks Like
- Clear Tier 0 definition spanning on-prem and cloud identity
- Strong separation of administrative and non-administrative identities
- Time-bound privilege elevation for sensitive roles
- Continuous monitoring of identity control-plane changes

Hybrid identity risk is best reduced through intentional design, phased controls, and risk-based prioritization rather than reactive enforcement.
