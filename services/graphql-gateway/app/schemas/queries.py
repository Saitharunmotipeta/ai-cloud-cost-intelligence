import strawberry
import time
from typing import List, Optional

from app.services.insight_service import (
    get_filtered_insights,
    get_service_summary,
    get_severity_breakdown,
    get_daily_insights,
)
from app.schemas.types import (
    InsightType,
    ServiceSummaryType,
    SeverityBreakdownType,
    DailyInsightType,
    AnomalyType,
)

# -------------------------------
# CONFIG
# -------------------------------
MAX_LIMIT = 50
DEFAULT_LIMIT = 10


# -------------------------------
# VALIDATION
# -------------------------------
def validate_limit(limit: int) -> int:
    if limit <= 0:
        raise ValueError("limit must be greater than 0")
    return min(limit, MAX_LIMIT)


def validate_offset(offset: int) -> int:
    if offset < 0:
        raise ValueError("offset must be >= 0")
    return offset


# -------------------------------
# MAPPER
# -------------------------------
def map_to_type(i) -> InsightType:
    return InsightType(
        id=str(i.id),
        account_id=str(i.account_id),
        service=i.service,

        anomaly_type=i.anomaly_type or "unknown",
        severity=i.severity,
        impact=i.impact or "medium",

        explanation=i.explanation or i.message or "No explanation available",
        root_cause=i.root_cause or "Not identified",
        action=i.action or i.recommendation or "No action provided",
        confidence=i.confidence or "low",

        generated_at=i.generated_at,
    )


# -------------------------------
# GRAPHQL QUERY ROOT
# -------------------------------
@strawberry.type
class Query:

    # 🔥 MAIN QUERY (FIXED)
    @strawberry.field
    def insights(
        self,
        account_id: str,
        service: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = DEFAULT_LIMIT,
        offset: int = 0,
    ) -> List[InsightType]:
        
        query_start = time.perf_counter()

        limit = validate_limit(limit)
        offset = validate_offset(offset)

        results = get_filtered_insights(
            account_id=account_id,
            service=service,
            severity=severity,
            limit=limit,
            offset=offset,
        )

        query_ms = (
        time.perf_counter() - query_start
        ) * 1000

        print(
            f"📊 GraphQL Insights Query : {query_ms:.2f} ms"
        )

        return [map_to_type(i) for i in results]


    # 🔥 SERVICE SUMMARY (ACCOUNT SAFE)
    @strawberry.field
    def service_summary(self, account_id: str) -> List[ServiceSummaryType]:

        query_start = time.perf_counter()

        results = get_service_summary(account_id)

        query_ms = (
            time.perf_counter() - query_start
        ) * 1000

        print(
            f"📊 GraphQL Service Summary : {query_ms:.2f} ms"
        )

        return [
            ServiceSummaryType(
                service=r["service"],
                total_count=r["count"],
            )
            for r in results
        ]


    # 🔥 SEVERITY BREAKDOWN (ACCOUNT SAFE)
    @strawberry.field
    def severity_breakdown(self, account_id: str) -> List[SeverityBreakdownType]:

        query_start = time.perf_counter()

        results = get_severity_breakdown(account_id)

        query_ms = (
            time.perf_counter() - query_start
        ) * 1000

        print(
            f"📊 GraphQL Severity Breakdown : {query_ms:.2f} ms"
        )

        return [
            SeverityBreakdownType(
                severity=r["severity"],
                count=r["count"],
            )
            for r in results
        ]


    # 🔥 DAILY INSIGHTS (ACCOUNT SAFE)
    @strawberry.field
    def daily_insights(self, account_id: str) -> List[DailyInsightType]:

        query_start = time.perf_counter()

        results = get_daily_insights(account_id)

        query_ms = (
            time.perf_counter() - query_start
        ) * 1000

        print(
            f"📊 GraphQL Daily Insights : {query_ms:.2f} ms"
        )

        return [
            DailyInsightType(
                date=str(r["date"]),
                count=r["count"],
            )
            for r in results
        ]


    @strawberry.field
    def anomalies(self, account_id: str) -> List[AnomalyType]:

        query_start = time.perf_counter()

        insights = get_filtered_insights(
            account_id=account_id,
            limit=100
        )

        query_ms = (
            time.perf_counter() - query_start
        ) * 1000

        print(
            f"📊 GraphQL Anomalies Query : {query_ms:.2f} ms"
        )

        return [
            AnomalyType(
                id=str(i.id),
                service=i.service,
                severity=i.severity,
                explanation=i.explanation or i.message or "No explanation",
                timestamp=str(i.generated_at),
            )
            for i in insights
            if i.severity in ["CRITICAL", "HIGH", "MEDIUM"]
        ]