from datetime import datetime, timezone
from uuid import UUID

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from shared.events.cost_data_ingested_v1 import (
    CostDataIngestedEvent,
    CostDataIngestedPayload,
)
from shared.observability.metrics import (
    start_timer,
    stop_timer,
    record_metric,
)
from .core.broker import get_broker
from shared.observability.logging import configure_logging
import logging

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
    processing_timer = start_timer()
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

   # --------------------------------------------------
    # Record ingestion processing time
    # --------------------------------------------------

    processing_ms = stop_timer(processing_timer)

    record_metric(
        event=event,
        service="ingestion",
        metric="request_processing_ms",
        value=processing_ms,
    )

    # --------------------------------------------------
    # Publish Event
    # --------------------------------------------------

    publish_timer = start_timer()

    await broker.publish(
        STREAM_NAME,
        event,
    )

    publish_ms = stop_timer(publish_timer)
    logger.info(
        "Published cost_data_ingested_v1",
        extra={
            "service_name": "ingestion-service",
            "event_id": event.event_id,
            "correlation_id": event.correlation_id,
            "account_id": account_id,   # 🔥 ADD THIS
            "stream": STREAM_NAME,
            "request_processing_ms": processing_ms,
            "broker_publish_ms": publish_ms,
        },
    )

    return {
        "status": "published",
        "event_id": event.event_id,
        "account_id": account_id,  
        "metrics": {
            "request_processing_ms": processing_ms,
            "broker_publish_ms": publish_ms,
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