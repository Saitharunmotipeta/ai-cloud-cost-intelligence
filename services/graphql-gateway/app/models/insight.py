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
    message = Column(String, nullable=False)
    recommendation = Column(String, nullable=False)
    generated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

Index(
    "idx_account_service",
    Insight.account_id,
    Insight.service,
)