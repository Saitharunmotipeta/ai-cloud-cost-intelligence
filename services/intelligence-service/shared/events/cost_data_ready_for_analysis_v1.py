from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field
from .base_event import BaseEvent


class CostDataReadyForAnalysisPayload(BaseModel):
    account_id: str
    service: str
    cost: float
    usage_timestamp: datetime
    processed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CostDataReadyForAnalysisEvent(BaseEvent):
    event_type: Literal["cost_data_ready_for_analysis_v1"] = "cost_data_ready_for_analysis_v1"
    version: int = 1
    payload: CostDataReadyForAnalysisPayload