"""
PacketVision PCAP parser.

In plain English:
- This file knows how to read a .pcap file and turn it into a table of "flows".
- A flow is basically a conversation between two endpoints:
    (src_ip, dst_ip, src_port, dst_port, protocol)

For each flow we will compute:
- number of packets
- total bytes
- start time and end time
- duration
- average packet size

These flow-level features are much easier for machine learning to work with
than raw packets.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple
from collections import defaultdict

import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP  # type: ignore[import]


FlowKey = Tuple[str, str, int, int, str]


def parse_pcap_to_flows(pcap_path: str) -> pd.DataFrame:
    """
    Parse a PCAP file and aggregate packets into flows.

    Parameters
    ----------
    pcap_path : str
        Path to a .pcap file.

    Returns
    -------
    pd.DataFrame
        One row per flow with columns such as:
        - src_ip
        - dst_ip
        - src_port
        - dst_port
        - protocol
        - packet_count
        - total_bytes
        - start_time
        - end_time
        - duration
        - avg_packet_size

    In plain English:
    - We read all packets from the PCAP.
    - For each TCP/UDP packet with an IP header, we build a flow key.
    - We keep track of stats per flow (counts, bytes, timestamps).
    """

    packets = rdpcap(pcap_path)

    # We'll aggregate stats into these dicts keyed by flow.
    packet_counts: Dict[FlowKey, int] = defaultdict(int)
    total_bytes: Dict[FlowKey, int] = defaultdict(int)
    first_ts: Dict[FlowKey, float] = {}
    last_ts: Dict[FlowKey, float] = {}

    for pkt in packets:
        # We only care about IP packets with TCP or UDP.
        if IP not in pkt:
            continue

        ip_layer = pkt[IP]
        protocol: str

        if TCP in pkt:
            l4 = pkt[TCP]
            protocol = "TCP"
        elif UDP in pkt:
            l4 = pkt[UDP]
            protocol = "UDP"
        else:
            # Ignore non-TCP/UDP IP traffic for now.
            continue

        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        src_port = int(l4.sport)
        dst_port = int(l4.dport)
        key: FlowKey = (src_ip, dst_ip, src_port, dst_port, protocol)

        # Length in bytes. scapy's "len(pkt)" returns the serialized size.
        size_bytes = len(pkt)

        # Timestamp; scapy stores it on the packet object as "time".
        ts = float(pkt.time)

        packet_counts[key] += 1
        total_bytes[key] += size_bytes

        if key not in first_ts:
            first_ts[key] = ts
        # Always update last_ts so the final value is the last time we saw this flow.
        last_ts[key] = ts

    # Build rows for the DataFrame.
    rows = []
    for (src_ip, dst_ip, src_port, dst_port, protocol), count in packet_counts.items():
        bytes_total = total_bytes[(src_ip, dst_ip, src_port, dst_port, protocol)]
        start = first_ts[(src_ip, dst_ip, src_port, dst_port, protocol)]
        end = last_ts[(src_ip, dst_ip, src_port, dst_port, protocol)]
        duration = max(end - start, 0.0)
        avg_pkt_size = bytes_total / count if count > 0 else 0.0

        rows.append(
            {
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "protocol": protocol,
                "packet_count": count,
                "total_bytes": bytes_total,
                "start_time": start,
                "end_time": end,
                "duration": duration,
                "avg_packet_size": avg_pkt_size,
            }
        )

    if not rows:
        # Return an empty DataFrame with the expected columns if nothing was parsed.
        return pd.DataFrame(
            columns=[
                "src_ip",
                "dst_ip",
                "src_port",
                "dst_port",
                "protocol",
                "packet_count",
                "total_bytes",
                "start_time",
                "end_time",
                "duration",
                "avg_packet_size",
            ]
        )

    return pd.DataFrame(rows)

