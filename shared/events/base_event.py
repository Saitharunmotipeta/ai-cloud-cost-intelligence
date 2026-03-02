from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, ConfigDict


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> str:
    return str(uuid.uuid4())


class BaseEvent(BaseModel):
    """
    Standard event envelope used across all services.

    This model is broker-agnostic and defines the transport contract
    for every event flowing through the system.
    """

    model_config = ConfigDict(
        extra="forbid",              # Prevent silent schema drift
        validate_assignment=True,    # Validate on mutation
        frozen=False                 # Allow retry_count increment
    )

    # --- Core envelope fields ---
    event_id: str = Field(default_factory=_uuid)
    event_type: str
    version: int = 1
    timestamp: datetime = Field(default_factory=_utc_now)

    # --- Tracing & routing ---
    source: str
    correlation_id: str = Field(default_factory=_uuid)

    # --- Reliability ---
    retry_count: int = 0

    # --- Business payload (generic here, typed in domain events) ---
    payload: Dict[str, Any]

    # --- Optional extensibility ---
    metadata: Optional[Dict[str, Any]] = None

    # ------------------------------------------------------------------
    # Reliability helpers
    # ------------------------------------------------------------------

    def increment_retry(self) -> None:
        """
        Increment retry count.
        Used by consumers before re-publishing failed events.
        """
        self.retry_count += 1

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert event to dictionary (JSON-safe).
        """
        return self.model_dump(mode="json")

    def to_json(self) -> str:
        """
        Serialize event to JSON string.
        """
        return self.model_dump_json()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseEvent":
        """
        Deserialize dictionary into BaseEvent.
        """
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, data: str) -> "BaseEvent":
        """
        Deserialize JSON string into BaseEvent.
        """
        return cls.model_validate_json(data)