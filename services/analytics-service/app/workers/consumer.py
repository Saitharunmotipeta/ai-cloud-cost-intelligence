import asyncio
from datetime import datetime, timezone
from typing import Set

from shared.events.cost_data_ingested_v1 import CostDataIngestedEvent
from shared.events.cost_data_ready_for_analysis_v1 import (
    CostDataReadyForAnalysisEvent,
    CostDataReadyForAnalysisPayload,
)
from shared.events.base_event import BaseEvent
from shared.broker.interface import BrokerInterface


STREAM_NAME = "cost_data_ingested_v1"
OUTPUT_STREAM = "cost_data_ready_for_analysis_v1"
GROUP_NAME = "analytics-group-v1"


class AnalyticsConsumer:
    def __init__(self, broker: BrokerInterface, consumer_name: str):
        self.broker = broker
        self.consumer_name = consumer_name
        self.processed_events: Set[str] = set()

    async def start(self):
        await self.broker.create_consumer_group(STREAM_NAME, GROUP_NAME)

        while True:
            messages = await self.broker.consume(
                stream=STREAM_NAME,
                group_name=GROUP_NAME,
                consumer_name=self.consumer_name,
            )

            for message_id, base_event in messages:
                await self.handle_message(message_id, base_event)

            await asyncio.sleep(0.1)

    async def handle_message(self, message_id: str, base_event: BaseEvent):
        # Idempotency check
        if base_event.event_id in self.processed_events:
            await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)
            return

        try:
            event = CostDataIngestedEvent.model_validate(base_event.model_dump())

            ready_payload = CostDataReadyForAnalysisPayload(
                account_id=event.payload.account_id,
                service=event.payload.service,
                cost=event.payload.cost,
                usage_timestamp=event.payload.usage_timestamp,
                processed_at=datetime.now(timezone.utc),
            )

            new_event = CostDataReadyForAnalysisEvent(
                source="analytics-service",
                correlation_id=event.correlation_id,
                payload=ready_payload,
            )

            await self.broker.publish(OUTPUT_STREAM, new_event)

            self.processed_events.add(base_event.event_id)

            await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)

        except Exception:
            base_event.increment_retry()

            if base_event.retry_count >= 3:
                # Future DLQ stream
                await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)