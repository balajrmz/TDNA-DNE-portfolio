# PacketVision — Network Visibility & Packet Analysis Lab
**Tags:** TDNA, DNE, Network Visibility, Packet Analysis, PCAP, Flow Analysis, Offensive Security, AI Security

Target-centric exploration of packet-level visibility to support Target Digital Network Analysis (TDNA) and Digital Network Exploitation (DNE) workflows.

---

## Overview

PacketVision is a network visibility and packet analysis lab designed to explore how packet-level data can be leveraged for adversary-centric analysis. The project focuses on parsing packet captures (PCAPs), extracting protocol and flow-level metadata, and identifying patterns that are useful for understanding attacker tradecraft and network exposure.

PacketVision supports TDNA and DNE workflows by treating network traffic as a target surface, enabling structured analysis of how communications appear on the wire and where visibility gaps may exist.

This project is part of the TDNA & DNE portfolio of Jan Zabala.

---

## Why This Matters for TDNA & DNE

Packet-level visibility is foundational for:

- Characterizing network exposure and protocol usage
- Understanding how attacker behaviors manifest in raw traffic
- Identifying reconnaissance, scanning, and beaconing patterns
- Supporting access-path reasoning through traffic analysis
- Informing evasion and detection considerations

PacketVision enables hands-on experimentation with these concepts in a controlled, lab-based environment.

---

## Key Capabilities

- Parsing and inspection of PCAP files
- Extraction of protocol metadata and flow summaries
- Identification of anomalous or suspicious traffic patterns
- Generation of structured CSV and JSON output for analysis or ML ingestion
- Modular architecture for adding protocol- or behavior-specific parsers
- Automation-friendly workflows for repeatable analysis

---

## Technical Highlights

- Python-based packet inspection using common PCAP libraries
- Normalized feature extraction from packets to flows
- Clear separation of parsing, feature engineering, and reporting
- Designed to integrate with ML-based network analysis pipelines

---

## Project Structure

```
ai-driven-security-projects/packetvision/
├── data/
│   ├── pcaps/           # sample PCAP files for testing
│   └── output/          # extracted features & flow metadata
│
├── packetvision/
│   ├── parser.py        # core PCAP parsing logic
│   ├── features.py      # feature extraction utilities
│   ├── utils.py         # helpers, loaders, and filters
│   ├── pipeline.py      # end-to-end parsing → feature workflow
│   └── config.py        # file paths & constants
│
└── README.md
```

---

## Installation

```bash
git clone https://github.com/balajimz/tdna-dne-portfolio.git
cd tdna-dne-portfolio/ai-driven-security-projects/packetvision

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Parse a PCAP File

```bash
python -m packetvision.parser ./data/pcaps/sample.pcap
```

Output:

```
data/output/parsed_sample.json
```

---

### Extract Flow Features

```bash
python -m packetvision.features ./data/output/parsed_sample.json
```

Output:

```
data/output/flows.csv
```

---

### Run the Full Pipeline

```bash
python -m packetvision.pipeline ./data/pcaps/sample.pcap
```

This produces structured flow summaries suitable for manual analysis or ML-based modeling.

---

## Example Output Summary

```json
{
  "flow_id": "192.168.1.10-443-192.168.1.50-51523",
  "protocol": "TLS",
  "packet_count": 32,
  "byte_count": 40241,
  "duration_ms": 812,
  "suspicious_flags": []
}
```

---

## TDNA / DNE Use Cases

- Network exposure and protocol analysis
- Support for reconnaissance and access-path reasoning
- Validation of attacker tradecraft at the packet level
- Pre-processing layer for ML-based traffic analysis (e.g., SentinelFlow)
- Training and experimentation in lab environments

---

## Notes

- All PCAPs are synthetic or publicly available examples
- No production or customer traffic is used
- Project is OPSEC-safe and designed for reproducible experimentation

---

## License

MIT License.

---

## Author

Jan Zabala  
Target Digital Network Analysis & Digital Network Exploitation  
CEH | OSCP (in progress)
