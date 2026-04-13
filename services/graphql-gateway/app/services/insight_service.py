from contextlib import contextmanager
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
import time

from app.core.database import SessionLocal
from app.models.insight import Insight


# -------------------------------
# CACHE (PER ACCOUNT)
# -------------------------------
_cache = {}
CACHE_TTL = 3600  # 🔥 1 hour


# -------------------------------
# DB SESSION MANAGER
# -------------------------------
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# HELPERS
# -------------------------------
def parse_uuid(value: str) -> UUID:
    try:
        return UUID(value)
    except Exception:
        raise ValueError("Invalid UUID format")


# -------------------------------
# CORE QUERY (SINGLE SOURCE OF TRUTH)
# -------------------------------
def get_filtered_insights(
    account_id: str,
    service: str = None,
    severity: str = None,
    limit: int = 100,
    offset: int = 0
):

    account_id = parse_uuid(account_id)

    now = time.time()
    cache_key = f"{account_id}_{service}_{severity}_{limit}_{offset}"

    # ✅ CACHE HIT
    if (
        cache_key in _cache
        and now - _cache[cache_key]["timestamp"] < CACHE_TTL
    ):
        return _cache[cache_key]["data"]

    with get_db() as db:

        query = db.query(Insight).filter(
            Insight.account_id == account_id
        )

        # 🔥 FILTERS
        if service:
            query = query.filter(Insight.service == service)

        if severity:
            query = query.filter(Insight.severity == severity)

        results = (
            query
            .order_by(Insight.generated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

    # ✅ STORE CACHE
    _cache[cache_key] = {
        "data": results,
        "timestamp": now
    }

    return results


# -------------------------------
# SUMMARY / ANALYTICS
# -------------------------------
def get_service_summary(account_id: str):

    account_id = parse_uuid(account_id)

    with get_db() as db:
        results = (
            db.query(
                Insight.service,
                func.count(Insight.id).label("count"),
            )
            .filter(Insight.account_id == account_id)
            .group_by(Insight.service)
            .order_by(func.count(Insight.id).desc())
            .all()
        )

    return [{"service": r[0], "count": r[1]} for r in results]


def get_severity_breakdown(account_id: str):

    account_id = parse_uuid(account_id)

    with get_db() as db:
        results = (
            db.query(
                Insight.severity,
                func.count(Insight.id).label("count"),
            )
            .filter(Insight.account_id == account_id)
            .group_by(Insight.severity)
            .all()
        )

    return [{"severity": r[0], "count": r[1]} for r in results]


def get_daily_insights(account_id: str):

    account_id = parse_uuid(account_id)

    with get_db() as db:
        results = (
            db.query(
                cast(Insight.generated_at, Date).label("date"),
                func.count(Insight.id).label("count"),
            )
            .filter(Insight.account_id == account_id)
            .group_by("date")
            .order_by("date")
            .all()
        )

    return [{"date": r[0], "count": r[1]} for r in results]