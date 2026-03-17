import strawberry
from typing import List

from app.services.insight_service import get_insights_by_account
from app.schemas.types import InsightType


@strawberry.type
class Query:

    @strawberry.field
    def insights(self, account_id: str) -> List[InsightType]:

        results = get_insights_by_account(account_id)

        return [
            InsightType(
                id=str(i.id),
                account_id=str(i.account_id),
                service=i.service,
                severity=i.severity,
                message=i.message,
                recommendation=i.recommendation,
                generated_at=i.generated_at,
            )
            for i in results
        ]