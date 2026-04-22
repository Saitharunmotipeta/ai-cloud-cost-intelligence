from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from .base_event import BaseEvent


class CostDataIngestedPayload(BaseModel):
    account_id: str
    service: str
    cost: float
    usage_timestamp: datetime


class CostDataIngestedEvent(BaseEvent):
    event_type: Literal["cost_data_ingested_v1"] = "cost_data_ingested_v1"
    version: int = 1
    payload: CostDataIngestedPayload