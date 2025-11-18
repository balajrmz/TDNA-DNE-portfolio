"""
CloudSentinel rule engine.

In plain English:
- This file contains the "if this, then that" logic for risky IAM policies.
- It does NOT do machine learning – it just applies security best-practice checks.
- The analyzer and API will call these functions to get a list of issues.

We treat each check as a "rule" that can produce one or more findings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Iterable, Set


# -----------------------------
# Data structures
# -----------------------------


@dataclass
class Finding:
    """
    Simple container for a single rule result.

    In plain English:
    - rule_id: short code so we know which rule fired (e.g., R01_WILDCARD_ACTION)
    - severity: how bad this is from a risk perspective (low / medium / high / critical)
    - message: explanation a human can read
    - location: where we saw the problem (e.g., "Statement[0]" or "Resource: *")
    """

    rule_id: str
    severity: str
    message: str
    location: str | None = None


# Some services are more sensitive than others. Wildcards here are especially scary.
HIGH_RISK_SERVICES: Set[str] = {"iam", "kms", "sts", "organizations"}

# Small set of actions used in common privilege escalation paths.
PASSROLE_ACTION = "iam:PassRole"
ASSUME_ROLE_ACTION = "sts:AssumeRole"
EC2_RUN_INSTANCES = "ec2:RunInstances"
LAMBDA_CREATE_FUNCTION = "lambda:CreateFunction"
LAMBDA_UPDATE_FUNCTION = "lambda:UpdateFunctionCode"


# -----------------------------
# Helper functions
# -----------------------------


def _to_list(value: Any) -> List[Any]:
    """
    Normalize IAM JSON fields to a list.

    AWS allows "Action" and "Resource" to be either:
    - a single string, or
    - a list of strings

    This helper makes life easier by always returning a list.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _extract_actions(statement: Dict[str, Any]) -> List[str]:
    """Return a list of actions from a single policy statement."""
    return [str(a) for a in _to_list(statement.get("Action"))]


def _extract_resources(statement: Dict[str, Any]) -> List[str]:
    """Return a list of resources from a single policy statement."""
    return [str(r) for r in _to_list(statement.get("Resource"))]


def _service_prefix(action: str) -> str:
    """
    Return the service part of an action, e.g.:

        "iam:PassRole" -> "iam"
        "s3:PutObject" -> "s3"

    If the action is just "*" we return "*" to indicate "all services".
    """
    if ":" not in action:
        return action
    return action.split(":", 1)[0]


# -----------------------------
# Rule implementations
# -----------------------------


def rule_wildcard_action(actions: Iterable[str], location: str) -> List[Finding]:
    """
    R01: Flag wildcard actions.

    In plain English:
    - If an IAM policy says "Action": "*" or "iam:*", it means "do anything".
    - That's usually NOT what you want and is almost always over-privileged.
    """
    findings: List[Finding] = []

    for action in actions:
        # Exact wildcard: "*"
        if action == "*":
            findings.append(
                Finding(
                    rule_id="R01_WILDCARD_ACTION",
                    severity="critical",
                    message='Policy allows all actions: "Action": "*"',
                    location=location,
                )
            )
            continue

        # Service-wide wildcard: "iam:*", "s3:*", etc.
        if action.endswith(":*"):
            service = _service_prefix(action)
            severity = "high" if service in HIGH_RISK_SERVICES else "medium"
            findings.append(
                Finding(
                    rule_id="R01_WILDCARD_ACTION",
                    severity=severity,
                    message=f'Policy allows all actions for service "{service}:*"',
                    location=location,
                )
            )

    return findings


def rule_wildcard_resource(resources: Iterable[str], location: str) -> List[Finding]:
    """
    R02: Flag wildcard resources.

    In plain English:
    - "Resource": "*" means "this permission applies to every resource".
    - That can be okay for some read-only policies, but in general it's risky,
      especially when combined with write or admin actions.
    """
    findings: List[Finding] = []

    for res in resources:
        if res == "*" or res.strip() == "*":
            findings.append(
                Finding(
                    rule_id="R02_WILDCARD_RESOURCE",
                    severity="high",
                    message='Policy applies to all resources: "Resource": "*"',
                    location=location,
                )
            )

    return findings


def rule_high_risk_service_wildcard(actions: Iterable[str], location: str) -> List[Finding]:
    """
    R03: High-risk service wildcards.

    In plain English:
    - This is a more focused version of the wildcard rule.
    - If we see "iam:*", "kms:*", "sts:*", etc., we call that out separately because
      those services control identity, keys, or cross-account access.
    """
    findings: List[Finding] = []

    for action in actions:
        if not action.endswith(":*"):
            continue
        service = _service_prefix(action)
        if service in HIGH_RISK_SERVICES:
            findings.append(
                Finding(
                    rule_id="R03_HIGH_RISK_WILDCARD",
                    severity="critical",
                    message=f'High-risk wildcard detected: "{action}"',
                    location=location,
                )
            )

    return findings


def rule_privilege_escalation_patterns(actions: Iterable[str], location: str) -> List[Finding]:
    """
    R04: Look for simple privilege escalation patterns.

    In plain English:
    - Some combinations of actions are known to be dangerous together.
    - Example: if a user can both PassRole and RunInstances, they may be able
      to attach a more privileged role to a new instance and "become" admin.

    This is not a complete list, but it shows the idea.
    """
    actions_set = {a.lower() for a in actions}
    findings: List[Finding] = []

    has_passrole = PASSROLE_ACTION.lower() in actions_set
    has_assumerole = ASSUME_ROLE_ACTION.lower() in actions_set
    has_ec2_run = EC2_RUN_INSTANCES.lower() in actions_set
    has_lambda_create = LAMBDA_CREATE_FUNCTION.lower() in actions_set
    has_lambda_update = LAMBDA_UPDATE_FUNCTION.lower() in actions_set

    # PassRole + EC2:RunInstances
    if has_passrole and has_ec2_run:
        findings.append(
            Finding(
                rule_id="R04_PRIV_ESC_PASSROLE_EC2",
                severity="high",
                message=(
                    "Policy allows iam:PassRole and ec2:RunInstances. "
                    "This combination can enable privilege escalation by launching "
                    "instances with more privileged roles."
                ),
                location=location,
            )
        )

    # PassRole + Lambda function management
    if has_passrole and (has_lambda_create or has_lambda_update):
        findings.append(
            Finding(
                rule_id="R04_PRIV_ESC_PASSROLE_LAMBDA",
                severity="high",
                message=(
                    "Policy allows iam:PassRole and Lambda function management. "
                    "This combination can enable privilege escalation by attaching "
                    "privileged roles to Lambda functions."
                ),
                location=location,
            )
        )

    # sts:AssumeRole by itself is not automatically bad, but we mark it for review.
    if has_assumerole:
        findings.append(
            Finding(
                rule_id="R04_ASSUME_ROLE_REVIEW",
                severity="medium",
                message=(
                    "Policy allows sts:AssumeRole. Risk depends on which roles "
                    "are assumable and their privileges."
                ),
                location=location,
            )
        )

    return findings


def rule_admin_like_actions(actions: Iterable[str], location: str) -> List[Finding]:
    """
    R05: Generic "looks like admin" rule.

    In plain English:
    - We look for patterns that usually appear in Administrator-style policies,
      such as 'AdministratorAccess', 'PowerUser', or 'FullAccess' in action names.
    - This is a heuristic, not a perfect check.
    """
    findings: List[Finding] = []
    keywords = ("AdministratorAccess", "FullAccess", "PowerUser")

    for action in actions:
        if any(kw.lower() in action.lower() for kw in keywords):
            findings.append(
                Finding(
                    rule_id="R05_ADMIN_LIKE_ACTION",
                    severity="high",
                    message=f'Action "{action}" looks like an admin or full-access permission.',
                    location=location,
                )
            )

    return findings


# -----------------------------
# Top-level API
# -----------------------------


def evaluate_statement(statement: Dict[str, Any], index: int) -> List[Finding]:
    """
    Run all rules against a single IAM statement.

    In plain English:
    - Take one JSON statement from the policy.
    - Extract actions and resources.
    - Run each rule.
    - Return a list of findings for that statement.
    """
    location = f"Statement[{index}]"
    actions = _extract_actions(statement)
    resources = _extract_resources(statement)

    findings: List[Finding] = []
    findings.extend(rule_wildcard_action(actions, location))
    findings.extend(rule_wildcard_resource(resources, location))
    findings.extend(rule_high_risk_service_wildcard(actions, location))
    findings.extend(rule_privilege_escalation_patterns(actions, location))
    findings.extend(rule_admin_like_actions(actions, location))

    return findings


def evaluate_policy(policy: Dict[str, Any]) -> List[Finding]:
    """
    Run all rules against an entire IAM policy document.

    In plain English:
    - AWS policies have a top-level "Statement" key which can be:
        * a single object, or
        * a list of objects.
    - We normalize that to a list and run evaluate_statement() on each one.
    """
    raw_statements = policy.get("Statement", [])
    statements: List[Dict[str, Any]]

    if isinstance(raw_statements, dict):
        # Single statement case
        statements = [raw_statements]
    else:
        statements = list(raw_statements)

    all_findings: List[Finding] = []
    for idx, stmt in enumerate(statements):
        all_findings.extend(evaluate_statement(stmt, idx))

    return all_findings

