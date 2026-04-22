from datetime import datetime, timezone
from uuid import uuid4
from pydantic import BaseModel

from .base_event import BaseEvent


class CostInsightGeneratedPayload(BaseModel):

    insight_id: str
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
        account_id: str,
        service: str,
        severity: str,
        message: str,
        recommendation: str,
    ):

        now = datetime.now(timezone.utc)

        payload = CostInsightGeneratedPayload(
            insight_id=str(uuid4()),
            account_id=account_id,
            service=service,
            severity=severity,
            message=message,
            recommendation=recommendation,
            generated_at=now,
        )

        return cls(
            source=source,
            correlation_id=correlation_id,
            payload=payload,
            timestamp=now,
        )