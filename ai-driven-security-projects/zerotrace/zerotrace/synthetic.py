"""
synthetic.py

Generate synthetic "memory snapshot" data for ZeroTrace.

Think of this as a fake export from Volatility / EDR:
each row ~= one process with attributes:
- process name, pid/ppid, path, modules, entropy, RWX regions, etc.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, asdict
from typing import List

import numpy as np
import pandas as pd

from .config import NUM_PROCESSES, SEED, SNAPSHOT_PATH, MODEL_CLASSES

from pathlib import Path

# Use a dataclass just to keep the fields tidy and explicit
@dataclass
class ProcessRecord:
    pid: int
    ppid: int
    name: str
    path: str
    user: str
    company: str
    signed: bool

    num_modules: int
    num_unsigned_modules: int
    num_rwx_regions: int
    avg_entropy: float
    has_network_connection: bool
    num_connections: int
    listening_ports: int
    high_entropy_strings: int
    cpu_usage: float
    memory_usage_mb: float

    label: str  # target for ML


# Some "normal" and "suspicious" process names / traits
BENIGN_PROCESSES = [
    ("explorer.exe", r"C:\Windows\explorer.exe", "NT AUTHORITY\\USER", "Microsoft", True),
    ("chrome.exe", r"C:\Program Files\Google\Chrome\Application\chrome.exe", "NT AUTHORITY\\USER", "Google LLC", True),
    ("Teams.exe", r"C:\Users\User\AppData\Local\Microsoft\Teams\current\Teams.exe", "NT AUTHORITY\\USER", "Microsoft", True),
    ("svchost.exe", r"C:\Windows\System32\svchost.exe", "NT AUTHORITY\\SYSTEM", "Microsoft", True),
    ("lsass.exe", r"C:\Windows\System32\lsass.exe", "NT AUTHORITY\\SYSTEM", "Microsoft", True),
]

SUSPICIOUS_PROCESSES = [
    ("svchost.exe", r"C:\Users\User\AppData\Roaming\svchost.exe", "NT AUTHORITY\\USER", "Unknown", False),
    ("chrome.exe", r"C:\Users\User\AppData\Local\Temp\chrome.exe", "NT AUTHORITY\\USER", "Unknown", False),
    ("update.exe", r"C:\Users\User\AppData\Roaming\Update\update.exe", "NT AUTHORITY\\USER", "Unknown", False),
    ("payload.exe", r"C:\ProgramData\payload.exe", "NT AUTHORITY\\USER", "Unknown", False),
]


def _seed_everything(seed: int) -> None:
    """Set Python & NumPy RNG seeds so runs are reproducible."""
    random.seed(seed)
    np.random.seed(seed)


def _make_benign_record(pid: int, ppid: int) -> ProcessRecord:
    """
    Create a "normal" looking process.

    In plain English:
    - signed binaries from Microsoft/Google
    - low number of unsigned modules
    - little to no RWX memory
    - moderate entropy (normal code/data)
    - some network usage, but not extreme
    """
    name, path, user, company, signed = random.choice(BENIGN_PROCESSES)

    num_modules = random.randint(10, 80)
    num_unsigned_modules = random.randint(0, 3)
    num_rwx_regions = random.randint(0, 1)
    avg_entropy = round(np.random.normal(5.5, 0.4), 2)  # typical code/data
    has_net = random.random() < 0.6
    num_conns = random.randint(0, 10) if has_net else 0
    listening_ports = random.randint(0, 2)
    high_entropy_strings = random.randint(0, 3)
    cpu_usage = round(abs(np.random.normal(4, 2)), 2)
    mem_mb = round(abs(np.random.normal(120, 40)), 1)

    return ProcessRecord(
        pid=pid,
        ppid=ppid,
        name=name,
        path=path,
        user=user,
        company=company,
        signed=signed,
        num_modules=num_modules,
        num_unsigned_modules=num_unsigned_modules,
        num_rwx_regions=num_rwx_regions,
        avg_entropy=max(0.0, min(avg_entropy, 8.0)),
        has_network_connection=has_net,
        num_connections=num_conns,
        listening_ports=listening_ports,
        high_entropy_strings=high_entropy_strings,
        cpu_usage=cpu_usage,
        memory_usage_mb=mem_mb,
        label="benign",
    )


def _make_infostealer_record(pid: int, ppid: int) -> ProcessRecord:
    """
    Simulate an info-stealer:

    - often lives under user profile / AppData
    - unsigned modules
    - some RWX memory for loaders/injection
    - lots of outbound connections
    - moderate to high entropy (packed/obfuscated code)
    """
    name, path, user, company, signed = random.choice(SUSPICIOUS_PROCESSES)

    num_modules = random.randint(5, 30)
    num_unsigned_modules = random.randint(3, 12)
    num_rwx_regions = random.randint(1, 4)
    avg_entropy = round(np.random.normal(6.8, 0.4), 2)
    has_net = True
    num_conns = random.randint(15, 60)
    listening_ports = random.randint(0, 1)
    high_entropy_strings = random.randint(10, 40)
    cpu_usage = round(abs(np.random.normal(8, 4)), 2)
    mem_mb = round(abs(np.random.normal(80, 30)), 1)

    return ProcessRecord(
        pid=pid,
        ppid=ppid,
        name=name,
        path=path,
        user=user,
        company=company,
        signed=False,
        num_modules=num_modules,
        num_unsigned_modules=num_unsigned_modules,
        num_rwx_regions=num_rwx_regions,
        avg_entropy=max(0.0, min(avg_entropy, 8.5)),
        has_network_connection=has_net,
        num_connections=num_conns,
        listening_ports=listening_ports,
        high_entropy_strings=high_entropy_strings,
        cpu_usage=cpu_usage,
        memory_usage_mb=mem_mb,
        label="infostealer_like",
    )


def _make_ransomware_record(pid: int, ppid: int) -> ProcessRecord:
    """
    Simulate ransomware:

    - high CPU and memory
    - many RWX regions (shellcode, encryptor)
    - very high entropy (encrypted data, packed code)
    - some network (C2, exfil)
    """
    name, path, user, company, signed = random.choice(SUSPICIOUS_PROCESSES)

    num_modules = random.randint(5, 25)
    num_unsigned_modules = random.randint(5, 15)
    num_rwx_regions = random.randint(3, 8)
    avg_entropy = round(np.random.normal(7.5, 0.3), 2)
    has_net = random.random() < 0.7
    num_conns = random.randint(5, 25) if has_net else 0
    listening_ports = random.randint(0, 2)
    high_entropy_strings = random.randint(30, 100)
    cpu_usage = round(abs(np.random.normal(40, 15)), 2)
    mem_mb = round(abs(np.random.normal(250, 80)), 1)

    return ProcessRecord(
        pid=pid,
        ppid=ppid,
        name=name,
        path=path,
        user=user,
        company=company,
        signed=False,
        num_modules=num_modules,
        num_unsigned_modules=num_unsigned_modules,
        num_rwx_regions=num_rwx_regions,
        avg_entropy=max(0.0, min(avg_entropy, 9.0)),
        has_network_connection=has_net,
        num_connections=num_conns,
        listening_ports=listening_ports,
        high_entropy_strings=high_entropy_strings,
        cpu_usage=cpu_usage,
        memory_usage_mb=mem_mb,
        label="ransomware_like",
    )


def _make_injected_loader_record(pid: int, ppid: int) -> ProcessRecord:
    """
    Simulate an injected loader / in-memory implant:

    - maybe looks like a legit process name
    - often has few modules but RWX memory
    - entropy moderate to high
    - may have a small number of steady C2 connections
    """
    name, path, user, company, signed = random.choice(SUSPICIOUS_PROCESSES)

    num_modules = random.randint(3, 20)
    num_unsigned_modules = random.randint(2, 10)
    num_rwx_regions = random.randint(2, 6)
    avg_entropy = round(np.random.normal(6.5, 0.5), 2)
    has_net = random.random() < 0.9
    num_conns = random.randint(3, 15) if has_net else 0
    listening_ports = random.randint(0, 1)
    high_entropy_strings = random.randint(15, 60)
    cpu_usage = round(abs(np.random.normal(12, 6)), 2)
    mem_mb = round(abs(np.random.normal(100, 50)), 1)

    return ProcessRecord(
        pid=pid,
        ppid=ppid,
        name=name,
        path=path,
        user=user,
        company=company,
        signed=False,
        num_modules=num_modules,
        num_unsigned_modules=num_unsigned_modules,
        num_rwx_regions=num_rwx_regions,
        avg_entropy=max(0.0, min(avg_entropy, 8.5)),
        has_network_connection=has_net,
        num_connections=num_conns,
        listening_ports=listening_ports,
        high_entropy_strings=high_entropy_strings,
        cpu_usage=cpu_usage,
        memory_usage_mb=mem_mb,
        label="injected_loader",
    )


def generate_synthetic_snapshot(n: int | None = None) -> pd.DataFrame:
    """
    Generate a synthetic "memory snapshot" as a pandas DataFrame.

    Each row ~= one process with attributes plus a ground-truth label.

    In plain English:
    - We randomly choose how many benign vs malicious processes to create.
    - We create slightly noisy but believable numbers for modules, entropy, etc.
    """
    _seed_everything(SEED)

    if n is None:
        n = NUM_PROCESSES

    records: List[ProcessRecord] = []

    # Decide how many of each class to make
    n_benign = int(n * 0.75)
    n_infostealer = int(n * 0.10)
    n_ransom = int(n * 0.08)
    n_injected = n - (n_benign + n_infostealer + n_ransom)

    pid_counter = 1000

    # Benign first
    for _ in range(n_benign):
        ppid = random.randint(200, 999)
        records.append(_make_benign_record(pid_counter, ppid))
        pid_counter += 1

    for _ in range(n_infostealer):
        ppid = random.randint(200, 999)
        records.append(_make_infostealer_record(pid_counter, ppid))
        pid_counter += 1

    for _ in range(n_ransom):
        ppid = random.randint(200, 999)
        records.append(_make_ransomware_record(pid_counter, ppid))
        pid_counter += 1

    for _ in range(n_injected):
        ppid = random.randint(200, 999)
        records.append(_make_injected_loader_record(pid_counter, ppid))
        pid_counter += 1

    # Convert dataclasses -> DataFrame
    df = pd.DataFrame([asdict(r) for r in records])

    # Shuffle rows so classes are mixed
    df = df.sample(frac=1.0, random_state=SEED).reset_index(drop=True)

    return df


from pathlib import Path

def save_snapshot_csv(path: str | None = None) -> str:
    """
    Generate a synthetic snapshot and save it to CSV.
    Ensures the output directory exists before writing.
    """
    # Default path
    if path is None:
        path = str(SNAPSHOT_PATH)

    out_path = Path(path)

    # 🔥 Make sure the folder exists (this prevents your error)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate data
    df = generate_synthetic_snapshot()

    # Write CSV safely
    df.to_csv(out_path, index=False)

    return str(out_path)


if __name__ == "__main__":
    # Manual quick test
    out_path = save_snapshot_csv()
    print(f"Saved synthetic snapshot to: {out_path}")

