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