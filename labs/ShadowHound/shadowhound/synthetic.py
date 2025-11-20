"""
ShadowHound synthetic data generator.

This script builds a *fake* Active Directory-style graph so we can
practice attack path analysis without any real environment.

In plain English:
- We make up some users, groups, and computers.
- We connect them with relationships like "member_of", "admin_to", etc.
- We mark some "crown jewel" targets (like Domain Admins / Tier-0 servers).
- We label nodes as higher or lower risk depending on whether they can
  reach those targets through admin-like paths.

The output is a CSV saved to RAW_GRAPH_PATH with:
  src, dst, edge_type, src_type, dst_type
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

import networkx as nx
import pandas as pd

from .config import (
    RAW_DIR,
    RAW_GRAPH_PATH,
    RANDOM_SEED,
)


# ---------------------------
# Simple dataclass definitions
# ---------------------------

@dataclass
class Node:
    """Represents a single AD object (user, group, computer)."""
    name: str
    node_type: str  # "user", "group", "computer"


@dataclass
class Edge:
    """Represents a relationship between two objects."""
    src: str
    dst: str
    edge_type: str  # "member_of", "admin_to", "session_on", etc.


# ---------------------------
# Synthetic graph generator
# ---------------------------

def build_synthetic_ad(
    num_users: int = 60,
    num_groups: int = 10,
    num_computers: int = 25,
) -> tuple[List[Node], List[Edge]]:
    """
    Build a toy AD-style environment.

    In plain English:
    - Create some users, groups, and computers.
    - Make nested groups.
    - Add admin rights on some computers.
    - Add user sessions on computers (like they’re logged in).
    """
    random.seed(RANDOM_SEED)

    nodes: List[Node] = []
    edges: List[Edge] = []

    # --- Create users, groups, computers ---

    users = [Node(f"user_{i}", "user") for i in range(num_users)]
    groups = [Node(f"group_{i}", "group") for i in range(num_groups)]
    computers = [Node(f"comp_{i}", "computer") for i in range(num_computers)]

    nodes.extend(users)
    nodes.extend(groups)
    nodes.extend(computers)

    # Pick a few "crown jewel" targets:
    # - A high-priv group (like Domain Admins)
    # - A couple of Tier-0 servers
    da_group = groups[0]                 # pretend this is "Domain Admins"
    tier0_computers = computers[:3]      # pretend these are DCs / Tier-0

    # --- Group nesting (group -> group, member_of) ---

    for child_idx in range(1, len(groups)):
        # Point some groups to parent groups to create depth
        parent_idx = random.randint(0, child_idx - 1)
        edges.append(
            Edge(
                src=groups[child_idx].name,
                dst=groups[parent_idx].name,
                edge_type="member_of",
            )
        )

    # --- Users -> groups (member_of) ---

    for user in users:
        # Each user belongs to 1–3 groups
        group_memberships = random.sample(groups, k=random.randint(1, 3))
        for g in group_memberships:
            edges.append(
                Edge(
                    src=user.name,
                    dst=g.name,
                    edge_type="member_of",
                )
            )

    # --- Admin rights (principal -> computer, admin_to) ---

    # Some groups have local admin on many computers
    admin_groups = random.sample(groups, k=min(3, len(groups)))
    for g in admin_groups:
        for comp in random.sample(computers, k=random.randint(3, len(computers))):
            edges.append(
                Edge(
                    src=g.name,
                    dst=comp.name,
                    edge_type="admin_to",
                )
            )

    # Make DA group very powerful: admin on Tier-0 and many others
    for comp in tier0_computers + random.sample(computers, k=5):
        edges.append(
            Edge(
                src=da_group.name,
                dst=comp.name,
                edge_type="admin_to",
            )
        )

    # --- User sessions (user -> computer, session_on) ---

    # Pretend users are logged into random machines
    for user in users:
        for comp in random.sample(computers, k=random.randint(1, 4)):
            edges.append(
                Edge(
                    src=user.name,
                    dst=comp.name,
                    edge_type="session_on",
                )
            )

    return nodes, edges


# ---------------------------
# Helper: convert to DataFrame
# ---------------------------

def to_edge_dataframe(nodes: List[Node], edges: List[Edge]) -> pd.DataFrame:
    """
    Convert our Node/Edge lists into a CSV-friendly table.

    We include src_type/dst_type so we don't have to look this up later.
    """
    node_type_map = {n.name: n.node_type for n in nodes}

    records = []
    for e in edges:
        records.append(
            {
                "src": e.src,
                "dst": e.dst,
                "edge_type": e.edge_type,
                "src_type": node_type_map.get(e.src, "unknown"),
                "dst_type": node_type_map.get(e.dst, "unknown"),
            }
        )

    df = pd.DataFrame.from_records(records)
    return df


# ---------------------------
# Main entrypoint
# ---------------------------

def generate_and_save() -> None:
    """
    Generate the synthetic environment and save it to RAW_GRAPH_PATH.

    In plain English:
    - Build the fake environment.
    - Turn it into a table.
    - Make sure the raw directory exists.
    - Save it as a CSV so the rest of the pipeline can use it.
    """
    print("[ShadowHound] Building synthetic AD graph...")
    nodes, edges = build_synthetic_ad()

    df = to_edge_dataframe(nodes, edges)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_GRAPH_PATH, index=False)

    print(f"[ShadowHound] Wrote graph to {RAW_GRAPH_PATH}")
    print(f"[ShadowHound] Num edges: {len(df)}")


if __name__ == "__main__":
    generate_and_save()
