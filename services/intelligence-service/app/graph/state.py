from typing import TypedDict


class IntelligenceState(TypedDict):
    event: dict

    # intermediate
    recommendation: str
    message: str
    severity: str

    # raw values (for reuse)
    service: str
    cost: float
    expected_cost: float
    deviation: float