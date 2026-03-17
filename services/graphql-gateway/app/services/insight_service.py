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