## Representative Hybrid Risk Scenario (Conceptual)

### Scenario
An enterprise operates a hybrid identity model with on-prem Active Directory synchronized to a cloud identity provider. Administrative identities are reused across on-prem and cloud environments for convenience.

### Risk Pattern
- Standing on-prem administrative privilege
- Privileged identities synced to cloud identity
- Limited conditional access enforcement for admin actions
- Cloud roles that allow tenant-wide impact

### Why This Matters
A compromise of a high-privilege identity in this model can affect both on-prem and cloud control planes, increasing blast radius beyond traditional directory boundaries.

### Defensive Considerations
- Separation of admin and non-admin identities
- Just-in-time elevation for sensitive roles
- Conditional access enforcement for privileged actions
- Explicit Tier 0 definition spanning hybrid identity

### Prioritization Insight
Not all identity paths present equal risk. Paths that converge on identity-provider control and privileged role assignment represent higher-impact remediation opportunities.
