import strawberry
from datetime import datetime


# -------------------------------
# CORE TYPES
# -------------------------------
@strawberry.type
class InsightType:
    id: strawberry.ID
    account_id: strawberry.ID
    service: str
    anomaly_type: str
    severity: str
    impact: str
    explanation: str
    root_cause: str
    action: str
    confidence: str
    generated_at: datetime

# -------------------------------
# AGGREGATION TYPES
# -------------------------------
@strawberry.type
class ServiceSummaryType:
    service: str
    total_count: int


@strawberry.type
class SeverityBreakdownType:
    severity: str
    count: int


@strawberry.type
class DailyInsightType:
    date: str  
    count: int

@strawberry.type
class AnomalyType:
    service: str
    expected_cost: float
    severity: str
    actual_cost: float
    deviation: float
    timestamp: str