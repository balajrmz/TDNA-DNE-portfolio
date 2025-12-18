"""
CloudSentinel analyzer.

In plain English:
- This file glues everything together for a single IAM policy.
- It runs the rule engine, summarizes the findings, calculates a simple
  risk score, and builds numeric "features" that a machine learning model
  can use later.

The API layer will call analyze_policy() and return that result as JSON.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Tuple

from .rules import Finding, evaluate_policy


# -----------------------------
# Risk scoring helpers
# -----------------------------

# Basic numeric weights for each severity level.
# These are intentionally simple and easy to explain in an interview.
SEVERITY_WEIGHTS: Dict[str, int] = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def _score_findings(findings: List[Finding]) -> Tuple[int, str]:
    """
    Convert a list of findings into:
    - an integer "risk score"
    - a human-friendly risk level (none / low / medium / high / critical)

    In plain English:
    - Each finding adds points based on severity.
    - We sum those points and map them into a simple risk bucket.
    """
    score = 0
    for f in findings:
        score += SEVERITY_WEIGHTS.get(f.severity.lower(), 1)

    # Map the numeric score into a risk level.
    if score == 0:
        level = "none"
    elif score <= 3:
        level = "low"
    elif score <= 7:
        level = "medium"
    elif score <= 12:
        level = "high"
    else:
        level = "critical"

    return score, level


# -----------------------------
# Feature extraction
# -----------------------------


def _build_features(findings: List[Finding], num_statements: int) -> Dict[str, Any]:
    """
    Build a small numeric feature vector from the findings.

    In plain English:
    - We count how many findings we have at each severity.
    - We set flags for specific rule types (wildcards, priv-esc, etc.).
    - This can be used later by a machine learning model or for reporting.
    """
    features: Dict[str, Any] = {
        "num_statements": num_statements,
        "num_findings": len(findings),
        "num_low": 0,
        "num_medium": 0,
        "num_high": 0,
        "num_critical": 0,
        # Flags for specific categories of rules.
        "has_wildcard_action": 0,
        "has_wildcard_resource": 0,
        "has_high_risk_wildcard": 0,
        "has_priv_esc_pattern": 0,
        "has_admin_like_action": 0,
    }

    for f in findings:
        sev = f.severity.lower()
        if sev in ("low", "medium", "high", "critical"):
            key = f"num_{sev}"
            features[key] += 1

        # Use rule_id prefixes to set category flags.
        if f.rule_id.startswith("R01_WILDCARD_ACTION"):
            features["has_wildcard_action"] = 1
        elif f.rule_id.startswith("R02_WILDCARD_RESOURCE"):
            features["has_wildcard_resource"] = 1
        elif f.rule_id.startswith("R03_HIGH_RISK_WILDCARD"):
            features["has_high_risk_wildcard"] = 1
        elif f.rule_id.startswith("R04_PRIV_ESC_") or f.rule_id.startswith("R04_ASSUME_ROLE"):
            features["has_priv_esc_pattern"] = 1
        elif f.rule_id.startswith("R05_ADMIN_LIKE_ACTION"):
            features["has_admin_like_action"] = 1

    return features


# -----------------------------
# Public analyzer API
# -----------------------------


def analyze_policy(policy: Dict[str, Any], include_features: bool = True) -> Dict[str, Any]:
    """
    Analyze a single IAM policy document.

    Steps in plain English:
    1. Run the rule engine against the policy.
    2. Calculate a numeric risk score and risk level.
    3. Build a simplified list of findings that can be returned as JSON.
    4. Optionally build a features dict for ML or further analysis.

    Returns a JSON-serializable dict, for example:

    {
        "risk_level": "high",
        "risk_score": 11,
        "num_statements": 2,
        "findings": [
            {
                "rule_id": "R01_WILDCARD_ACTION",
                "severity": "critical",
                "message": "Policy allows all actions: \"Action\": \"*\"",
                "location": "Statement[0]"
            },
            ...
        ],
        "features": {
            "num_statements": 2,
            "num_findings": 4,
            "num_low": 0,
            "num_medium": 1,
            "num_high": 1,
            "num_critical": 2,
            "has_wildcard_action": 1,
            ...
        }
    }
    """
    # Run the rules over the policy and collect all findings.
    findings: List[Finding] = evaluate_policy(policy)

    # Count how many statements we have for context.
    raw_statements = policy.get("Statement", [])
    if isinstance(raw_statements, dict):
        num_statements = 1
    else:
        num_statements = len(raw_statements)

    # Score findings and get overall risk level.
    risk_score, risk_level = _score_findings(findings)

    # Convert Finding dataclasses to plain dicts so they can be serialized to JSON.
    findings_payload = [asdict(f) for f in findings]

    result: Dict[str, Any] = {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "num_statements": num_statements,
        "num_findings": len(findings),
        "findings": findings_payload,
    }

    if include_features:
        result["features"] = _build_features(findings, num_statements)

    return result
