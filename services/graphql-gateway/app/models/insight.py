from sqlalchemy import Column, String, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Insight(Base):
    __tablename__ = "insights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    account_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    service = Column(String(100), nullable=False, index=True)

    severity = Column(String(20), nullable=False, index=True)

    # 🔥 NEW STRUCTURED FIELDS
    anomaly_type = Column(String(50), nullable=False, default="unknown")
    impact = Column(String(20), nullable=False, default="medium")

    explanation = Column(String, nullable=True)
    root_cause = Column(String, nullable=True)
    action = Column(String, nullable=True)
    confidence = Column(String(20), nullable=False, default="low")

    # 🔁 BACKWARD COMPATIBILITY (optional but smart)
    message = Column(String, nullable=True)
    recommendation = Column(String, nullable=True)

    generated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )


# 🔥 COMPOSITE INDEX (query optimization)
Index(
    "idx_account_service",
    Insight.account_id,
    Insight.service,
)