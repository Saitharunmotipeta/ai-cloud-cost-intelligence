from datetime import datetime, timezone

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
    account_id: str
    service: str
    cost: float


@app.post("/ingest")
async def ingest_cost(data: IngestRequest):
    """
    Accept cost data and publish event to Redis Stream.
    """

    payload = CostDataIngestedPayload(
        account_id=data.account_id,
        service=data.service,
        cost=data.cost,
        usage_timestamp=datetime.now(timezone.utc),
    )

    event = CostDataIngestedEvent(
        source="ingestion-service",
        payload=payload,
    )

    logger.info(
        "Publishing cost_data_ingested_v1",
        extra={
            "service": "ingestion-service",
            "event_id": event.event_id,
            "correlation_id": event.correlation_id,
        },
    )
    await broker.publish(STREAM_NAME, event)

    return {
        "status": "published",
        "event_id": event.event_id,
    }