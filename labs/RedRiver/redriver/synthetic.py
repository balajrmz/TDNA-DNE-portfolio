"""
redriver.synthetic

Generate a synthetic network flow dataset for RedRiver.

In plain English:
- We pretend we have NetFlow / Zeek / firewall logs at the "flow" level.
- Each row is a flow between src_ip:src_port and dst_ip:dst_port.
- We include simple features like:
    - duration
    - bytes_sent / bytes_received
    - packets
    - protocol
- We assign each flow a label like:
    - benign
    - port_scan
    - brute_force
    - c2_beacon

so the ML model has something to learn from.
"""

from __future__ import annotations

import ipaddress
import random
from typing import List

import pandas as pd

from .config import FLOWS_PATH, RANDOM_SEED, RAW_DIR

# -------------------------------------------------------------
# Helpers
# -------------------------------------------------------------


def random_private_ip(rng: random.Random) -> str:
    """
    Generate a random private IPv4 address, e.g., 10.x.x.x or 192.168.x.x.
    """
    private_ranges = [
        ipaddress.IPv4Network("10.0.0.0/8"),
        ipaddress.IPv4Network("172.16.0.0/12"),
        ipaddress.IPv4Network("192.168.0.0/16"),
    ]
    net = rng.choice(private_ranges)
    host = rng.randint(0, net.num_addresses - 2)  # avoid broadcast
    return str(net.network_address + host)


def random_public_ip(rng: random.Random) -> str:
    """
    Generate a fake 'public' IPv4 by choosing outside private ranges.
    This is just for realism in logs.
    """
    while True:
        addr_int = rng.randint(1, 0xFFFFFFFF - 1)
        addr = ipaddress.IPv4Address(addr_int)
        if not addr.is_private and not addr.is_multicast and not addr.is_reserved:
            return str(addr)


# -------------------------------------------------------------
# Synthetic flow generation per behavior
# -------------------------------------------------------------


def generate_benign_flows(rng: random.Random, n: int) -> pd.DataFrame:
    """
    Simulate benign user traffic, e.g., web browsing, DNS, etc.
    """
    records = []
    for _ in range(n):
        src_ip = random_private_ip(rng)
        dst_ip = random_public_ip(rng)
        src_port = rng.randint(1024, 65535)
        dst_port = rng.choice([80, 443, 53, 123])  # HTTP/HTTPS/DNS/NTP-ish
        protocol = rng.choice(["tcp", "udp"])

        duration = abs(rng.gauss(3.0, 1.0))  # ~3 seconds
        bytes_sent = max(200, int(abs(rng.gauss(5000, 3000))))
        bytes_received = max(500, int(abs(rng.gauss(10000, 5000))))
        packets = max(3, int(bytes_sent / 500) + int(bytes_received / 800))

        records.append(
            {
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "protocol": protocol,
                "duration": duration,
                "bytes_sent": bytes_sent,
                "bytes_received": bytes_received,
                "packets": packets,
                "label": "benign",
            }
        )

    return pd.DataFrame(records)


def generate_port_scans(rng: random.Random, n: int) -> pd.DataFrame:
    """
    Simulate port-scanning behavior:
    - Many dst_ports from the same src_ip to the same dst_ip.
    - Short duration, low bytes per flow.
    """
    records = []
    for _ in range(n):
        src_ip = random_private_ip(rng)
        dst_ip = random_public_ip(rng)

        # Choose a port range to scan
        base_port = rng.randint(1, 60000)
        for offset in range(rng.randint(5, 25)):  # small multi-port scan
            dst_port = base_port + offset
            src_port = rng.randint(1024, 65535)

            duration = abs(rng.gauss(0.2, 0.1))
            bytes_sent = rng.randint(40, 300)
            bytes_received = rng.randint(0, 400)
            packets = rng.randint(1, 5)

            records.append(
                {
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "src_port": src_port,
                    "dst_port": dst_port,
                    "protocol": "tcp",
                    "duration": duration,
                    "bytes_sent": bytes_sent,
                    "bytes_received": bytes_received,
                    "packets": packets,
                    "label": "port_scan",
                }
            )
    return pd.DataFrame(records)


def generate_bruteforce_flows(rng: random.Random, n: int) -> pd.DataFrame:
    """
    Simulate brute-force login attempts:
    - Many flows from same src_ip to the same dst_ip:22 or :3389 or :445.
    - Short duration, repetitive patterns.
    """
    records = []
    for _ in range(n):
        src_ip = random_private_ip(rng)
        dst_ip = random_public_ip(rng)
        dst_port = rng.choice([22, 3389, 445])

        for _ in range(rng.randint(10, 50)):  # repeated attempts
            src_port = rng.randint(1024, 65535)
            duration = abs(rng.gauss(1.0, 0.4))
            bytes_sent = rng.randint(200, 1000)
            bytes_received = rng.randint(50, 800)
            packets = rng.randint(2, 10)

            records.append(
                {
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "src_port": src_port,
                    "dst_port": dst_port,
                    "protocol": "tcp",
                    "duration": duration,
                    "bytes_sent": bytes_sent,
                    "bytes_received": bytes_received,
                    "packets": packets,
                    "label": "brute_force",
                }
            )

    return pd.DataFrame(records)


def generate_c2_beacons(rng: random.Random, n: int) -> pd.DataFrame:
    """
    Simulate beacon-like C2 flows:
    - Regular intervals (we just encode as similar durations).
    - Small, steady payload sizes.
    """
    records = []
    for _ in range(n):
        src_ip = random_private_ip(rng)
        dst_ip = random_public_ip(rng)
        dst_port = rng.choice([443, 8080, 8443])

        # multiple beacons along a "session"
        beacon_count = rng.randint(5, 30)
        for _ in range(beacon_count):
            src_port = rng.randint(1024, 65535)
            duration = abs(rng.gauss(0.5, 0.2))
            bytes_sent = rng.randint(80, 400)
            bytes_received = rng.randint(100, 800)
            packets = rng.randint(2, 8)

            records.append(
                {
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "src_port": src_port,
                    "dst_port": dst_port,
                    "protocol": "tcp",
                    "duration": duration,
                    "bytes_sent": bytes_sent,
                    "bytes_received": bytes_received,
                    "packets": packets,
                    "label": "c2_beacon",
                }
            )

    return pd.DataFrame(records)


# -------------------------------------------------------------
# Orchestration
# -------------------------------------------------------------


def generate_flows(
    num_benign: int = 2000,
    num_port_scans: int = 80,
    num_bruteforce: int = 80,
    num_c2: int = 80,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """
    Generate a combined synthetic dataset of flows.

    In plain English:
    - Build a big table of flows with mixed behaviors.
    - Shuffle the rows so attacks are mixed among benign.
    """
    rng = random.Random(seed)

    benign_df = generate_benign_flows(rng, num_benign)
    scan_df = generate_port_scans(rng, num_port_scans)
    brute_df = generate_bruteforce_flows(rng, num_bruteforce)
    c2_df = generate_c2_beacons(rng, num_c2)

    df = pd.concat([benign_df, scan_df, brute_df, c2_df], ignore_index=True)
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return df


def save_flows(df: pd.DataFrame, path=FLOWS_PATH) -> str:
    """
    Save the synthetic flows to CSV under data/raw/.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return str(path)


def run_synthetic_pipeline() -> str:
    """
    High-level entrypoint:
    - Generate synthetic flows
    - Save them to CSV
    - Print where they went
    """
    print("[RedRiver] Generating synthetic flows...")
    df = generate_flows()
    out_path = save_flows(df)
    print(f"[RedRiver] Wrote {len(df)} flows to: {out_path}")
    return out_path


if __name__ == "__main__":
    # Allow: python -m redriver.synthetic
    run_synthetic_pipeline()
