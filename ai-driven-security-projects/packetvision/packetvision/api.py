"""
FastAPI service for PacketVision.

In plain English:
- This file exposes PacketVision as a simple web API.
- You can:
    * GET /health          → check the service is alive
    * POST /analyze-pcap   → upload a PCAP and get back a JSON report

Under the hood, /analyze-pcap:
    1. Saves the uploaded PCAP into data/raw/
    2. Calls analyzer.analyze_pcap() on it
    3. Returns the combined rule + ML detection result
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import shutil
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import RAW_PCAP_DIR
from .analyzer import analyze_pcap


app = FastAPI(
    title="PacketVision API",
    description="AI-powered PCAP traffic classifier and threat detector.",
    version="0.1.0",
)

# Optional CORS config so tools/frontends can call this API easily.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production you'd restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def healthcheck() -> Dict[str, str]:
    """
    Basic health endpoint.

    In plain English:
    - Lets callers verify that the service is up.
    """
    return {"status": "ok"}


@app.post("/analyze-pcap")
async def analyze_pcap_endpoint(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload a PCAP file and run PacketVision analysis.

    Usage:
    - In Swagger UI (http://127.0.0.1:8000/docs), choose a .pcap file and click "Execute".
    - The server will:
        1. Save the file under data/raw/
        2. Parse it into flows
        3. Run rule-based and ML-based analysis
        4. Return a JSON report

    Notes:
    - This is intentionally simple; in a real system you'd want auth, size limits, etc.
    """

    if file.content_type not in ("application/vnd.tcpdump.pcap", "application/octet-stream"):
        # We allow generic octet-stream because many clients send that for PCAPs.
        # This is just a light sanity check.
        pass

    RAW_PCAP_DIR.mkdir(parents=True, exist_ok=True)

    # Create a unique filename so multiple uploads don't collide.
    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    dest_path = RAW_PCAP_DIR / unique_name

    try:
        with dest_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {exc}")
    finally:
        file.file.close()

    try:
        report = analyze_pcap(dest_path)
    except Exception as exc:
        # In plain English:
        # - If anything goes wrong during analysis, we surface a 500 error with the message.
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}")

    return report

