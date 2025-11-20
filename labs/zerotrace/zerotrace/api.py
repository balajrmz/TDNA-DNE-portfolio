"""
ZeroTrace REST API.

In plain English:
- /health: quick "am I alive?" check.
- /predict: accept one process snapshot and return class + confidence.

We keep the request model simple and explicit so it's clear in Swagger
what features the model expects.
"""

from __future__ import annotations

from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .pipeline import predict_sample
from .config import FEATURE_COLUMNS, MODEL_CLASSES


app = FastAPI(
    title="ZeroTrace API",
    version="0.1.0",
    description="AI-powered in-memory process classifier for anomaly and malware detection.",
)


class ProcessSample(BaseModel):
    """
    One process snapshot's feature vector.

    NOTE: These field names must match the FEATURE_COLUMNS used in training.
    Adjust as needed to match your config.py.
    """

    pid: int = Field(..., description="Process ID")
    ppid: int = Field(..., description="Parent process ID")
    num_modules: int = Field(..., description="Total loaded modules (DLLs)")
    num_unsigned_modules: int = Field(..., description="Loaded modules without valid signatures")
    num_rx_regions: int = Field(..., description="RX memory regions (suspicious)")
    num_rwx_regions: int = Field(..., description="RWX memory regions (very suspicious)")
    avg_entropy: float = Field(..., description="Average section entropy across modules")
    has_network_connection: int = Field(..., description="1 if process owns any network socket, else 0")
    num_connections: int = Field(..., description="Number of active network connections")
    listening_ports: int = Field(..., description="Count of listening ports owned by the process")
    high_entropy_strings: int = Field(..., description="Count of high-entropy strings in memory")
    cpu_usage_pct: float = Field(..., description="CPU usage percentage at sampling time")
    memory_usage_mb: float = Field(..., description="Resident memory usage in MB")


@app.get("/health", summary="Healthcheck")
async def healthcheck() -> Dict[str, str]:
    """
    Simple "am I alive?" endpoint.

    Good for:
    - K8s liveness checks
    - Quick smoke tests in a lab
    """
    return {"status": "ok"}


@app.post("/predict", summary="Classify a single process snapshot")
async def predict_endpoint(sample: ProcessSample) -> Dict:
    """
    Take one process snapshot and return the ZeroTrace model's verdict.

    The incoming JSON body maps directly to the ProcessSample fields.
    """
    result = predict_sample(sample.dict())
    return {
        "input": sample.dict(),
        "model_classes": MODEL_CLASSES,
        "prediction": result,
    }
