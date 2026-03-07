from sqlalchemy.orm import Session

from app.models.insight import Insight


class InsightRepository:

    def __init__(self, db: Session):
        self.db = db

    def save_insight(
        self,
        insight_id,
        account_id,
        service,
        severity,
        message,
        recommendation,
        generated_at,
    ):

        insight = Insight(
            id=insight_id,
            account_id=account_id,
            service=service,
            severity=severity,
            message=message,
            recommendation=recommendation,
            generated_at=generated_at,
        )

        self.db.add(insight)
        self.db.commit()
        self.db.refresh(insight)

        return insight