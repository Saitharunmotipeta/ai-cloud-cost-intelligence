from app.core.database import SessionLocal
from app.models.insight import Insight
from uuid import UUID
from sqlalchemy import func

def get_insights_by_account(account_id: str):
    db = SessionLocal()

    results = (
        db.query(Insight)
        .filter(Insight.account_id == UUID(account_id))
        .all()
    )

    db.close()
    return results

def get_recent_insights(limit: int):
    db = SessionLocal()

    results = (
        db.query(Insight)
        .order_by(Insight.generated_at.desc())
        .limit(limit)
        .all()
    )

    db.close()
    return results

def get_insights_paginated(account_id: str, limit: int, offset: int):
    db = SessionLocal()

    results = (
        db.query(Insight)
        .filter(Insight.account_id == UUID(account_id))
        .order_by(Insight.generated_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    db.close()
    return results

def get_insights_by_severity(severity: str):
    db = SessionLocal()

    results = (
        db.query(Insight)
        .filter(Insight.severity == severity)
        .order_by(Insight.generated_at.desc())
        .all()
    )

    db.close()
    return results

def get_service_summary(account_id: str):
    db = SessionLocal()

    results = (
        db.query(
            Insight.service,
            func.count(Insight.id).label("count")
        )
        .filter(Insight.account_id == UUID(account_id))
        .group_by(Insight.service)
        .order_by(func.count(Insight.id).desc())
        .all()
    )

    db.close()

    return [
        {"service": r[0], "count": r[1]}
        for r in results
    ]

def get_severity_breakdown():
    db = SessionLocal()

    results = (
        db.query(
            Insight.severity,
            func.count(Insight.id).label("count")
        )
        .group_by(Insight.severity)
        .all()
    )

    db.close()

    return [
        {"severity": r[0], "count": r[1]}
        for r in results
    ]

from sqlalchemy import cast, Date

def get_daily_insights():
    db = SessionLocal()

    results = (
        db.query(
            cast(Insight.generated_at, Date).label("date"),
            func.count(Insight.id).label("count")
        )
        .group_by("date")
        .order_by("date")
        .all()
    )

    db.close()

    return [
        {"date": r[0], "count": r[1]}
        for r in results
    ]