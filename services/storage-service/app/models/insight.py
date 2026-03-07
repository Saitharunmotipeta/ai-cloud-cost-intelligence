from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Insight(Base):

    __tablename__ = "insights"

    id = Column(UUID(as_uuid=True), primary_key=True)
    account_id = Column(UUID(as_uuid=True), index=True)
    service = Column(String)
    severity = Column(String)
    message = Column(String)
    recommendation = Column(String)
    generated_at = Column(DateTime)