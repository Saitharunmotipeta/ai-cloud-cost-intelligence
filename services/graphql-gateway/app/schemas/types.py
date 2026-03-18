import strawberry
from datetime import datetime


# -------------------------------
# CORE TYPES
# -------------------------------
@strawberry.type
class InsightType:
    id: strawberry.ID  # better than raw str
    account_id: strawberry.ID
    service: str
    severity: str
    message: str
    recommendation: str
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
    date: str  # keep string for frontend compatibility
    count: int