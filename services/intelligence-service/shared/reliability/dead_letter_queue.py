from datetime import datetime, timezone
from typing import Any

from shared.events.base_event import BaseEvent
from shared.broker.interface import BrokerInterface
from shared.constants.streams import (
    COST_DATA_INGESTED_STREAM,
    COST_DATA_READY_FOR_ANALYSIS_STREAM,
    COST_ANOMALY_DETECTED_STREAM,
    DEAD_LETTER_STREAM,
)


DLQ_STREAM = DEAD_LETTER_STREAM


class DeadLetterQueue:

    def __init__(self, broker: BrokerInterface):
        self.broker = broker

    async def send(
        self,
        original_event: BaseEvent,
        failure_reason: str,
    ):
        """
        Send failed events to the dead letter stream.
        """

        dlq_payload = {
            "original_event": original_event.model_dump(mode="json"),
            "failure_reason": failure_reason,
            "retry_count": original_event.retry_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        await self.broker.publish(
            DLQ_STREAM,
            BaseEvent(
                source="dlq-handler",
                correlation_id=original_event.correlation_id,
                payload=dlq_payload,
            ),
        )