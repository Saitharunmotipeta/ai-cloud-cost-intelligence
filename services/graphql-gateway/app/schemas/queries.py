import strawberry
from typing import List

from app.services.insight_service import (
    get_insights_by_account,
    get_recent_insights,
    get_insights_paginated,
    get_insights_by_severity,
    get_service_summary,
    get_severity_breakdown,
    get_daily_insights,
)
from app.schemas.types import (
    InsightType,
    ServiceSummaryType,
    SeverityBreakdownType,
    DailyInsightType,
)

# -------------------------------
# CONFIG (production safety)
# -------------------------------
MAX_LIMIT = 50
DEFAULT_LIMIT = 10


# -------------------------------
# VALIDATION HELPERS
# -------------------------------
def validate_limit(limit: int) -> int:
    if limit <= 0:
        raise ValueError("limit must be greater than 0")
    return min(limit, MAX_LIMIT)


def validate_offset(offset: int) -> int:
    if offset < 0:
        raise ValueError("offset must be >= 0")
    return offset


def validate_severity(severity: str) -> str:
    allowed = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    severity = severity.upper()

    if severity not in allowed:
        raise ValueError(f"Invalid severity. Allowed: {allowed}")

    return severity


# -------------------------------
# MAPPER (DRY principle)
# -------------------------------
def map_to_type(i) -> InsightType:
    return InsightType(
        id=str(i.id),
        account_id=str(i.account_id),
        service=i.service,
        severity=i.severity,
        message=i.message,
        recommendation=i.recommendation,
        generated_at=i.generated_at,
    )


# -------------------------------
# GRAPHQL QUERY ROOT
# -------------------------------
@strawberry.type
class Query:

    # ---------------------------
    # BASIC QUERY
    # ---------------------------
    @strawberry.field
    def insights(self, account_id: str) -> List[InsightType]:

        results = get_insights_by_account(account_id)

        return [map_to_type(i) for i in results]

    # ---------------------------
    # RECENT (with safety)
    # ---------------------------
    @strawberry.field
    def recent_insights(self, limit: int = DEFAULT_LIMIT) -> List[InsightType]:

        limit = validate_limit(limit)

        insights = get_recent_insights(limit)

        return [map_to_type(i) for i in insights]

    # ---------------------------
    # PAGINATION
    # ---------------------------
    @strawberry.field
    def insights_paginated(
        self,
        account_id: str,
        limit: int = DEFAULT_LIMIT,
        offset: int = 0,
    ) -> List[InsightType]:

        limit = validate_limit(limit)
        offset = validate_offset(offset)

        insights = get_insights_paginated(account_id, limit, offset)

        return [map_to_type(i) for i in insights]

    # ---------------------------
    # FILTER BY SEVERITY
    # ---------------------------
    @strawberry.field
    def insights_by_severity(
        self,
        severity: str,
        limit: int = DEFAULT_LIMIT,
    ) -> List[InsightType]:

        severity = validate_severity(severity)
        limit = validate_limit(limit)

        insights = get_insights_by_severity(severity)

        return [map_to_type(i) for i in insights[:limit]]

    # ---------------------------
    # AGGREGATION: SERVICE
    # ---------------------------
    @strawberry.field
    def service_summary(self, account_id: str) -> List[ServiceSummaryType]:

        results = get_service_summary(account_id)

        return [
            ServiceSummaryType(
                service=r["service"],
                total_count=r["count"],
            )
            for r in results
        ]

    # ---------------------------
    # AGGREGATION: SEVERITY
    # ---------------------------
    @strawberry.field
    def severity_breakdown(self) -> List[SeverityBreakdownType]:

        results = get_severity_breakdown()

        return [
            SeverityBreakdownType(
                severity=r["severity"],
                count=r["count"],
            )
            for r in results
        ]

    # ---------------------------
    # AGGREGATION: TIME SERIES
    # ---------------------------
    @strawberry.field
    def daily_insights(self) -> List[DailyInsightType]:

        results = get_daily_insights()

        return [
            DailyInsightType(
                date=str(r["date"]),
                count=r["count"],
            )
            for r in results
        ]