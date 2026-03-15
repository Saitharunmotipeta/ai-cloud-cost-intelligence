from datetime import datetime, timezone
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from shared.events.cost_data_ingested_v1 import (
    CostDataIngestedEvent,
    CostDataIngestedPayload,
)
from .core.broker import get_broker
from shared.observability.logging import configure_logging
import logging

app = FastAPI(title="Ingestion Service")

broker = get_broker()

logger = configure_logging("ingestion-service")

STREAM_NAME = "cost_data_ingested_v1"


class IngestRequest(BaseModel):
    account_id: UUID
    service: str
    cost: float


@app.post("/ingest")
async def ingest_cost(data: IngestRequest):
    """
    Accept cost data and publish event to Redis Stream.
    """

    payload = CostDataIngestedPayload(
        account_id=str(data.account_id),
        service=data.service,
        cost=data.cost,
        usage_timestamp=datetime.now(timezone.utc),
    )

    event = CostDataIngestedEvent(
        source="ingestion-service",
        payload=payload,
    )

    await broker.publish(STREAM_NAME, event)

    logger.info(
        "Published cost_data_ingested_v1",
        extra={
            "service_name": "ingestion-service",
            "event_id": event.event_id,
            "correlation_id": event.correlation_id,
            "stream": STREAM_NAME,
        },
    )

    return {
        "status": "published",
        "event_id": event.event_id,
    }