from contextlib import contextmanager
from uuid import UUID

from sqlalchemy import func, cast, Date

from app.core.database import SessionLocal
from app.models.insight import Insight

import time

_cache = {
    "data": None,
    "timestamp": 0
}

CACHE_TTL = 10  # seconds


# -------------------------------
# DB SESSION MANAGER (CRITICAL)
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
# BASIC QUERIES
# -------------------------------
def get_insights_by_account(account_id: str):
    account_id = parse_uuid(account_id)

    with get_db() as db:
        return (
            db.query(Insight)
            .filter(Insight.account_id == account_id)
            .all()
        )


def get_recent_insights(limit: int):
    with get_db() as db:
        return (
            db.query(Insight)
            .order_by(Insight.generated_at.desc())
            .limit(limit)
            .all()
        )


def get_insights_paginated(account_id: str, limit: int, offset: int):
    account_id = parse_uuid(account_id)

    with get_db() as db:
        return (
            db.query(Insight)
            .filter(Insight.account_id == account_id)
            .order_by(Insight.generated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )


def get_insights_by_severity(severity: str):
    with get_db() as db:
        return (
            db.query(Insight)
            .filter(Insight.severity == severity)
            .order_by(Insight.generated_at.desc())
            .all()
        )


# -------------------------------
# AGGREGATIONS
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


def get_severity_breakdown():
    with get_db() as db:
        results = (
            db.query(
                Insight.severity,
                func.count(Insight.id).label("count"),
            )
            .group_by(Insight.severity)
            .all()
        )

    return [{"severity": r[0], "count": r[1]} for r in results]


def get_daily_insights():
    with get_db() as db:
        results = (
            db.query(
                cast(Insight.generated_at, Date).label("date"),
                func.count(Insight.id).label("count"),
            )
            .group_by("date")
            .order_by("date")
            .all()
        )

    return [{"date": r[0], "count": r[1]} for r in results]

def get_insights_from_db(limit: int = 100):
    with get_db() as db:
        return (
            db.query(Insight)
            .order_by(Insight.generated_at.desc())
            .limit(limit)
            .all()
        )
        
def get_all_insights():

    now = time.time()

    # ✅ return cached
    if _cache["data"] and now - _cache["timestamp"] < CACHE_TTL:
        return _cache["data"]

    db = SessionLocal()
    insights = db.query(Insight).all()

    result = insights

    db.close()

    # ✅ store cache
    _cache["data"] = result
    _cache["timestamp"] = now

    return result