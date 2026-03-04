from datetime import datetime, timezone
from pydantic import BaseModel

from .base_event import BaseEvent


class CostInsightGeneratedPayload(BaseModel):
    account_id: str
    service: str
    severity: str
    message: str
    recommendation: str
    generated_at: datetime


class CostInsightGeneratedEvent(BaseEvent):

    event_type: str = "cost_insight_generated_v1"
    version: int = 1

    payload: CostInsightGeneratedPayload

    @classmethod
    def create(
        cls,
        source: str,
        correlation_id: str,
        payload: CostInsightGeneratedPayload,
    ):
        return cls(
            source=source,
            correlation_id=correlation_id,
            payload=payload,
            timestamp=datetime.now(timezone.utc),
        )