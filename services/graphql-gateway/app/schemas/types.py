import strawberry
from datetime import datetime

@strawberry.type
class InsightType:
    id: str
    account_id: str
    service: str
    severity: str
    message: str
    recommendation: str
    generated_at: datetime

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

