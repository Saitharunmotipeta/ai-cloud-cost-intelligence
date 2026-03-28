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
from shared.constants.streams import (
    COST_ANOMALY_DETECTED_STREAM,
    DEAD_LETTER_STREAM,
    COST_INSIGHT_GENERATED_STREAM
)

from app.domain.insight_engine import InsightEngine
from app.graph.graph_builder import build_graph


STREAM_NAME = COST_ANOMALY_DETECTED_STREAM
OUTPUT_STREAM = COST_INSIGHT_GENERATED_STREAM
DLQ_STREAM = DEAD_LETTER_STREAM
GROUP_NAME = "intelligence-group-v1"

logger = logging.getLogger(__name__)


class IntelligenceConsumer:

    def __init__(self, broker: BrokerInterface, consumer_name: str):

        self.broker = broker
        self.consumer_name = consumer_name

        # idempotency protection
        self.processed_events: Set[str] = set()

        self.graph = build_graph()

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
            event = CostAnomalyDetectedEvent.model_validate(base_event.model_dump())

            payload = event.payload

            if payload.service == "DLQ_TEST":
                raise Exception("Forced failure for DLQ testing")

            result = await self.graph.ainvoke({
                "event": {
                    "account_id": payload.account_id,
                    "service": payload.service,
                    "cost": payload.cost,
                    "expected_cost": payload.expected_cost,
                    "deviation": payload.deviation,
                }
            })

            insight = {
                "severity": result["severity"],
                "message": result.get(
                    "message",
                    "No detailed explanation generated for low severity anomaly."
                ),
                "recommendation": result["recommendation"],
            }

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

        except Exception as e:

            logger.exception(
                f"Insight generation failed: {str(e)}",
                extra={
                    "event_id": base_event.event_id,
                    "correlation_id": base_event.correlation_id,
                },
            )

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

            return

        # retry only if retry_count < 3
        await self.broker.publish(STREAM_NAME, base_event)

        await self.broker.acknowledge(
            STREAM_NAME,
            GROUP_NAME,
            message_id,
        )