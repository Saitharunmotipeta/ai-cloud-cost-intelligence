from app.core.database import SessionLocal
from app.models.insight import Insight
from uuid import UUID

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