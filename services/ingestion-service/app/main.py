from datetime import datetime, timezone
from uuid import UUID

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from shared.events.cost_data_ingested_v1 import (
    CostDataIngestedEvent,
    CostDataIngestedPayload,
)
from .core.broker import get_broker
from shared.observability.logging import configure_logging
import logging
import time

app = FastAPI(title="Ingestion Service")

broker = get_broker()

logger = configure_logging("ingestion-service")

STREAM_NAME = "cost_data_ingested_v1"


# 🔥 REMOVE account_id from body
class IngestRequest(BaseModel):
    service: str
    cost: float


@app.post("/ingest")
async def ingest_cost(
    data: IngestRequest,
    x_account_id: str = Header(...)
):
    """
    Accept cost data and publish event to Redis Stream.
    Account ID is passed via header (X-Account-ID).
    """

    # 🔥 Validate UUID
    total_start = time.perf_counter()
    try:
        account_id = str(UUID(x_account_id))
    except:
        raise HTTPException(status_code=400, detail="Invalid account_id")

    payload = CostDataIngestedPayload(
        account_id=account_id,
        service=data.service,
        cost=data.cost,
        usage_timestamp=datetime.now(timezone.utc),
    )

    event = CostDataIngestedEvent(
        source="ingestion-service",
        payload=payload,
    )

    publish_start = time.perf_counter()

    await broker.publish(STREAM_NAME, event)

    publish_ms = (
        time.perf_counter() - publish_start
    ) * 1000

    total_ms = (
        time.perf_counter() - total_start
    ) * 1000

    logger.info(
        "Published cost_data_ingested_v1",
        extra={
            "service_name": "ingestion-service",
            "event_id": event.event_id,
            "correlation_id": event.correlation_id,
            "account_id": account_id,   # 🔥 ADD THIS
            "stream": STREAM_NAME,
            "broker_publish_ms": round(publish_ms, 2),
            "ingestion_total_ms": round(total_ms, 2),
        },
    )

    return {
        "status": "published",
        "event_id": event.event_id,
        "account_id": account_id,  
        "metrics": {
            "broker_publish_ms": round(publish_ms, 2),
            "ingestion_total_ms": round(total_ms, 2)
        }
    }


@app.get("/health")
async def health():
    return {"status": "ingestion-running"}


@app.get("/metrics")
async def metrics():
    return {
        "service": "ingestion-service",
        "status": "running"
    }