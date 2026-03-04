from datetime import datetime
from pydantic import BaseModel
from .base_event import BaseEvent


class CostAnomalyDetectedPayload(BaseModel):
    account_id: str
    service: str
    cost: float
    expected_cost: float
    deviation: float
    detected_at: datetime


class CostAnomalyDetectedEvent(BaseEvent):
    event_type: str = "cost_anomaly_detected_v1"
    payload: CostAnomalyDetectedPayload