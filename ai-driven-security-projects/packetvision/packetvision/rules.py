"""
Rule-based detection engine for PacketVision.

In plain English:
- This file contains "if this, then suspicious" style rules.
- We look at flow-level statistics and try to spot classic patterns:
    * port scans
    * brute-force-like activity
    * DNS tunneling-ish flows

The output is a list of findings plus an overall risk score/level.

This is NOT meant to be perfect detection, but it shows how you can
combine simple heuristics with machine learning in a realistic way.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List

import pandas as pd


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class RuleFinding:
    """
    A single rule-based finding.

    In plain English:
    - This is one "hit" from a rule, like:
        * "We think this looks like a port scan."
        * "This DNS flow is super chatty, maybe tunneling."
    """
    rule_id: str
    severity: str
    message: str
    flows_affected: int


# Map severity labels to numeric weights for scoring.
SEVERITY_WEIGHTS: Dict[str, int] = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


# ---------------------------------------------------------------------------
# Helper: overall risk level from score
# ---------------------------------------------------------------------------

def _score_to_level(score: int) -> str:
    """
    Convert a numeric risk score into a label.

    In plain English:
    - Tiny score → "none"
    - Small score → "low"
    - Medium score → "medium"
    - Big score → "high"
    """
    if score <= 0:
        return "none"
    if score <= 3:
        return "low"
    if score <= 7:
        return "medium"
    return "high"


# ---------------------------------------------------------------------------
# Individual rule implementations
# ---------------------------------------------------------------------------

def _rule_port_scan(flows: pd.DataFrame) -> RuleFinding | None:
    """
    Detect simple port-scan-like behavior.

    Heuristic (plain English):
    - Look for a single source IP talking to MANY different destination ports,
      usually with short flows and low packet counts.
    - Example: one host sending TCP SYNs to 100+ ports on the same target.

    Implementation details:
    - Group by src_ip and count distinct dst_port values.
    - If any src_ip hits more than a threshold, raise a finding.
    """
    if flows.empty:
        return None

    # Require the columns we actually use.
    required_cols = {"src_ip", "dst_port", "packet_count", "duration"}
    if not required_cols.issubset(flows.columns):
        return None

    # Group by source IP and count unique destination ports.
    port_counts = (
        flows.groupby("src_ip")["dst_port"]
        .nunique()
        .rename("unique_dst_ports")
        .reset_index()
    )

    # Threshold for "this looks like a port scan".
    SCAN_PORT_THRESHOLD = 50

    suspicious_sources = port_counts[port_counts["unique_dst_ports"] >= SCAN_PORT_THRESHOLD]
    if suspicious_sources.empty:
        return None

    total_sources = len(suspicious_sources)
    msg = (
        f"Detected {total_sources} source IP(s) hitting >= {SCAN_PORT_THRESHOLD} "
        "unique destination ports. This pattern is consistent with a port scan."
    )

    return RuleFinding(
        rule_id="PV01_PORT_SCAN",
        severity="high",
        message=msg,
        flows_affected=int(
            flows[flows["src_ip"].isin(suspicious_sources["src_ip"])].shape[0]
        ),
    )


def _rule_bruteforce_like(flows: pd.DataFrame) -> RuleFinding | None:
    """
    Detect brute-force-ish activity against SSH/RDP/SMB.

    Heuristic (plain English):
    - Lots of flows targeting typical admin ports:
        * SSH (22)
        * RDP (3389)
        * SMB (445, 139)
    - Many packets and/or longer durations.

    Implementation details:
    - Filter flows where dst_port is in a sensitive set.
    - If we see "enough" of these flows, we raise a medium/high severity finding.
    """
    if flows.empty:
        return None

    required_cols = {"dst_port", "packet_count"}
    if not required_cols.issubset(flows.columns):
        return None

    SENSITIVE_PORTS = [22, 3389, 445, 139]

    sensitive_flows = flows[flows["dst_port"].isin(SENSITIVE_PORTS)]
    if sensitive_flows.empty:
        return None

    # Simple thresholds; these can be tuned.
    BRUTE_FLOW_COUNT_THRESHOLD = 30
    BRUTE_PACKET_THRESHOLD = 1000

    total_flows = sensitive_flows.shape[0]
    total_packets = sensitive_flows["packet_count"].sum()

    if total_flows < BRUTE_FLOW_COUNT_THRESHOLD and total_packets < BRUTE_PACKET_THRESHOLD:
        # Below both thresholds → don't alert.
        return None

    severity = "medium"
    if total_flows >= BRUTE_FLOW_COUNT_THRESHOLD or total_packets >= BRUTE_PACKET_THRESHOLD:
        severity = "high"

    msg = (
        f"Observed {total_flows} flow(s) and {total_packets} packets targeting "
        f"admin ports {SENSITIVE_PORTS}. This may represent brute-force or "
        "authentication-spray activity."
    )

    return RuleFinding(
        rule_id="PV02_BRUTEFORCE_LIKE",
        severity=severity,
        message=msg,
        flows_affected=int(total_flows),
    )


def _rule_dns_tunnel_like(flows: pd.DataFrame) -> RuleFinding | None:
    """
    Detect DNS tunneling-ish behavior.

    Heuristic (plain English):
    - DNS (port 53) is normally small, bursty traffic.
    - If we see large amounts of data or many packets over DNS, it might be
      someone using DNS as a covert channel (DNS tunneling / exfil).

    Implementation details:
    - Filter flows where dst_port == 53.
    - Sum packet_count and total_bytes; compare to thresholds.
    """
    if flows.empty:
        return None

    required_cols = {"dst_port", "packet_count", "total_bytes"}
    if not required_cols.issubset(flows.columns):
        return None

    dns_flows = flows[flows["dst_port"] == 53]
    if dns_flows.empty:
        return None

    total_dns_pkts = int(dns_flows["packet_count"].sum())
    total_dns_bytes = int(dns_flows["total_bytes"].sum())

    # Simple thresholds for "this is a LOT of DNS traffic".
    DNS_PKT_THRESHOLD = 500
    DNS_BYTES_THRESHOLD = 500_000  # ~500 KB

    if total_dns_pkts < DNS_PKT_THRESHOLD and total_dns_bytes < DNS_BYTES_THRESHOLD:
        return None

    msg = (
        f"Observed high-volume DNS traffic: {total_dns_pkts} packets and "
        f"{total_dns_bytes} bytes to port 53. This may be consistent with "
        "DNS tunneling or data exfiltration over DNS."
    )

    severity = "medium"
    if total_dns_pkts >= DNS_PKT_THRESHOLD * 2 or total_dns_bytes >= DNS_BYTES_THRESHOLD * 2:
        severity = "high"

    return RuleFinding(
        rule_id="PV03_DNS_TUNNEL_LIKE",
        severity=severity,
        message=msg,
        flows_affected=int(dns_flows.shape[0]),
    )


# ---------------------------------------------------------------------------
# Public API: analyze_flows_with_rules
# ---------------------------------------------------------------------------

def analyze_flows_with_rules(flows: pd.DataFrame) -> Dict[str, object]:
    """
    Run all rule-based detectors on a flow DataFrame.

    Parameters
    ----------
    flows : pd.DataFrame
        Flow-level stats from parser.parse_pcap_to_flows().

    Returns
    -------
    dict
        {
          "risk_level": <str>,      # none/low/medium/high
          "risk_score": <int>,
          "num_findings": <int>,
          "findings": [ { ... }, ... ]
        }

    In plain English:
    - We run each rule.
    - For each rule that "hits", we add a finding.
    - We add up the severities into a risk_score.
    - We convert the risk_score into a simple label.
    """

    findings: List[RuleFinding] = []

    for rule_func in (
        _rule_port_scan,
        _rule_bruteforce_like,
        _rule_dns_tunnel_like,
    ):
        finding = rule_func(flows)
        if finding is not None:
            findings.append(finding)

    # Compute numeric risk score based on severity weights.
    score = 0
    for f in findings:
        weight = SEVERITY_WEIGHTS.get(f.severity, 1)
        score += weight

    risk_level = _score_to_level(score)

    return {
        "risk_level": risk_level,
        "risk_score": int(score),
        "num_findings": len(findings),
        "findings": [asdict(f) for f in findings],
    }

