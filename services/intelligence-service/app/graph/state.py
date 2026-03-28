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