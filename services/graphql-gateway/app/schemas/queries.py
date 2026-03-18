import strawberry
from typing import List

from app.services.insight_service import get_insights_by_account, get_recent_insights, get_insights_paginated, get_insights_by_severity, get_service_summary, get_severity_breakdown, get_daily_insights
from app.schemas.types import InsightType, ServiceSummaryType, SeverityBreakdownType, DailyInsightType


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
    
    @strawberry.field
    def recent_insights(self, limit: int = 10) -> List[InsightType]:
        insights = get_recent_insights(limit)

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
            for i in insights
        ]
    
    @strawberry.field
    def insights_paginated(
        self, account_id: str, limit: int = 10, offset: int = 0
    ) -> List[InsightType]:

        insights = get_insights_paginated(account_id, limit, offset)

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
            for i in insights
        ]
    
    @strawberry.field
    def insights_by_severity(
        self, severity: str
    ) -> List[InsightType]:

        insights = get_insights_by_severity(severity)

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
            for i in insights
        ]


    @strawberry.field
    def service_summary(self, account_id: str) -> List[ServiceSummaryType]:

        results = get_service_summary(account_id)

        return [
            ServiceSummaryType(
                service=r["service"],
                total_count=r["count"]
            )
            for r in results
        ]


    @strawberry.field
    def severity_breakdown(self) -> List[SeverityBreakdownType]:

        results = get_severity_breakdown()

        return [
            SeverityBreakdownType(
                severity=r["severity"],
                count=r["count"]
            )
            for r in results
        ]
    

    @strawberry.field
    def daily_insights(self) -> List[DailyInsightType]:

        results = get_daily_insights()

        return [
            DailyInsightType(
                date=str(r["date"]),
                count=r["count"]
            )
            for r in results
        ]
    