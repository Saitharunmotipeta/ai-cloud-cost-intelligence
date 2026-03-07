import asyncio
import logging
from typing import Set

from shared.events.base_event import BaseEvent
from shared.events.cost_anomaly_detected_v1 import CostAnomalyDetectedEvent
from shared.events.cost_insight_generated_v1 import (
    CostInsightGeneratedEvent,
    CostInsightGeneratedPayload,
)

from shared.broker.interface import BrokerInterface

from app.domain.insight_engine import InsightEngine


STREAM_NAME = "cost_anomaly_detected_v1"
OUTPUT_STREAM = "cost_insight_generated_v1"
DLQ_STREAM = "cost_data_dead_letter_v1"
GROUP_NAME = "intelligence-group-v1"

logger = logging.getLogger(__name__)


class IntelligenceConsumer:

    def __init__(self, broker: BrokerInterface, consumer_name: str):

        self.broker = broker
        self.consumer_name = consumer_name

        # idempotency protection
        self.processed_events: Set[str] = set()

        # insight engine (rule + Gemini)
        self.engine = InsightEngine()

    async def start(self):

        # ensure consumer group exists
        await self.broker.create_consumer_group(STREAM_NAME, GROUP_NAME)

        logger.info(
            "Starting intelligence consumer",
            extra={
                "consumer": self.consumer_name,
                "stream": STREAM_NAME,
                "group": GROUP_NAME,
            },
        )

        while True:

            try:

                messages = await self.broker.consume(
                    stream=STREAM_NAME,
                    group_name=GROUP_NAME,
                    consumer_name=self.consumer_name,
                )

                for message_id, base_event in messages:
                    await self.handle_message(message_id, base_event)

            except Exception:

                logger.exception(
                    "Failed while consuming events",
                    extra={
                        "consumer": self.consumer_name,
                        "stream": STREAM_NAME,
                        "group": GROUP_NAME,
                    },
                )

            # prevent hot retry loop
            await asyncio.sleep(1)

    async def handle_message(self, message_id: str, base_event: BaseEvent):

        # idempotency check
        if base_event.event_id in self.processed_events:
            await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)
            return

        try:

            # reconstruct anomaly event
            event = CostAnomalyDetectedEvent.model_validate(
                base_event.model_dump()
            )

            payload = event.payload

            # generate insight using rule engine + Gemini
            insight = self.engine.generate_insight(
                payload.account_id,
                payload.service,
                payload.cost,
                payload.expected_cost,
                payload.deviation,
            )

            insight_event = CostInsightGeneratedEvent.create(
                source="intelligence-service",
                correlation_id=event.correlation_id,
                account_id=payload.account_id,
                service=payload.service,
                severity=insight["severity"],
                message=insight["message"],
                recommendation=insight["recommendation"],
            )

            # publish insight event
            await self.broker.publish(OUTPUT_STREAM, insight_event)

            logger.info(
                "Insight generated",
                extra={
                    "event_id": insight_event.event_id,
                    "correlation_id": insight_event.correlation_id,
                    "stream": OUTPUT_STREAM,
                },
            )

            # mark processed
            self.processed_events.add(base_event.event_id)

            # acknowledge original message
            await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)

        except Exception:

            logger.exception(
                "Insight generation failed",
                extra={
                    "event_id": base_event.event_id,
                    "correlation_id": base_event.correlation_id,
                },
            )

            # retry logic
            base_event.increment_retry()

            if base_event.retry_count >= 3:

                logger.error(
                    "Event moved to DLQ",
                    extra={
                        "event_id": base_event.event_id,
                        "correlation_id": base_event.correlation_id,
                        "stream": DLQ_STREAM,
                    },
                )

                await self.broker.publish(DLQ_STREAM, base_event)

                await self.broker.acknowledge(
                    STREAM_NAME,
                    GROUP_NAME,
                    message_id,
                )