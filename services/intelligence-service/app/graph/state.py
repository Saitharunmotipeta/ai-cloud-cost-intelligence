from typing import TypedDict


class IntelligenceState(TypedDict):
    event: dict

    # existing
    recommendation: str
    message: str
    severity: str

    service: str
    cost: float
    expected_cost: float
    deviation: float

    # 🆕 context fields
    ratio: float
    spike: bool
    trend: str

    # 🆕 classification
    anomaly_type: str
    context: list[dict]

    # 🆕 structured output
    explanation: str
    root_cause: str
    action: str
    confidence: str
    impact: str

    # 🆕 historical context
    past_avg_cost: float
    historical_trend: str
    repeat_anomaly: bool