import asyncio
import logging
from typing import Set

from shared.events.base_event import BaseEvent
from shared.events.cost_anomaly_detected_v1 import CostAnomalyDetectedEvent
from shared.events.cost_insight_generated_v1 import (
    CostInsightGeneratedEvent,
)

from shared.broker.interface import BrokerInterface
from shared.constants.streams import (
    COST_ANOMALY_DETECTED_STREAM,
    DEAD_LETTER_STREAM,
    COST_INSIGHT_GENERATED_STREAM
)

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
        self.processed_events: Set[str] = set()

        self.graph = build_graph()

    async def start(self):

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
                logger.exception("Failed while consuming events")

            await asyncio.sleep(1)

    async def handle_message(self, message_id: str, base_event: BaseEvent):

        if base_event.event_id in self.processed_events:
            await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)
            return

        try:

            event = CostAnomalyDetectedEvent.model_validate(base_event.model_dump())
            payload = event.payload

            # 🔥 Invoke LangGraph (with full context)
            result = await self.graph.ainvoke({
                "event": {
                    "account_id": payload.account_id,
                    "service": payload.service,
                    "cost": payload.cost,
                    "expected_cost": payload.expected_cost,
                    "deviation": payload.deviation,
                },
                "anomaly_type": getattr(payload, "anomaly_type", "unknown"),
            })

            # 🔥 Use AI outputs properly
            explanation = result.get("explanation", "No explanation generated")
            root_cause = result.get("root_cause", "Unknown")
            confidence = result.get("confidence", "low")
            severity = result.get("severity", "low")

            # 🔥 Build insight event
            insight_event = CostInsightGeneratedEvent.create(
                source="intelligence-service",
                correlation_id=event.correlation_id,
                account_id=payload.account_id,
                service=payload.service,
                severity=severity,
                message=explanation,   # 🔥 AI explanation
                recommendation=root_cause,  # 🔥 mapped for now
            )

            await self.broker.publish(OUTPUT_STREAM, insight_event)

            logger.info(
                "Insight generated",
                extra={
                    "event_id": insight_event.event_id,
                    "correlation_id": insight_event.correlation_id,
                    "account_id": payload.account_id,
                    "service": payload.service,
                    "confidence": confidence,
                },
            )

            self.processed_events.add(base_event.event_id)

            await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)

        except Exception as e:

            logger.exception(f"Insight generation failed: {str(e)}")

            base_event.increment_retry()

            if base_event.retry_count >= 3:

                logger.error("Event moved to DLQ")

                await self.broker.publish(DLQ_STREAM, base_event)

                await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)
                return

            # retry
            await self.broker.publish(STREAM_NAME, base_event)

            await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)