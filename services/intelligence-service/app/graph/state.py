from typing import TypedDict

class IntelligenceState(TypedDict):
    account_id: str
    service: str
    cost: float
    expected_cost: float
    deviation: float

    anomaly_type: str
    severity: str

    ratio: float
    spike: bool
    trend: str

    context: list[dict]

    historical_trend: str
    repeat_anomaly: bool

    explanation: str
    root_cause: str
    confidence: str