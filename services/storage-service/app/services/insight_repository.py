from sqlalchemy.orm import Session

from app.models.insight import Insight

import time 


class InsightRepository:

    def __init__(self, db: Session):
        self.db = db

    def save_insight(
        self,
        insight_id,
        account_id,
        service,
        severity,
        impact,
        anomaly_type,
        explanation,
        root_cause,
        action,
        confidence,
        message,
        recommendation,
        generated_at,
    ):

        # 🔥 NO account validation here
        # account_id is treated as external identity

        insight = Insight(
            id=insight_id,
            account_id=account_id,
            service=service,
            severity=severity,
            impact=impact,
            anomaly_type=anomaly_type,
            explanation=explanation,
            root_cause=root_cause,
            action=action,
            confidence=confidence,
            message=message,
            recommendation=recommendation,
            generated_at=generated_at,
        )

        db_start = time.perf_counter()

        self.db.add(insight)
        self.db.commit()
        self.db.refresh(insight)

        db_ms = (
            time.perf_counter() - db_start
        ) * 1000

        print(
            f"🗄 Database Insert Time : {db_ms:.2f} ms"
        )
        
        return insight