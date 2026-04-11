import asyncio
import logging
from datetime import datetime, timezone
from typing import Set

from shared.events.cost_data_ingested_v1 import CostDataIngestedEvent
from shared.events.cost_data_ready_for_analysis_v1 import (
    CostDataReadyForAnalysisEvent,
    CostDataReadyForAnalysisPayload,
)
from shared.events.cost_anomaly_detected_v1 import (
    CostAnomalyDetectedEvent,
    CostAnomalyDetectedPayload,
)
from shared.events.base_event import BaseEvent
from shared.broker.interface import BrokerInterface
from shared.constants.streams import (
    COST_DATA_INGESTED_STREAM,
    COST_DATA_READY_FOR_ANALYSIS_STREAM,
    COST_ANOMALY_DETECTED_STREAM,
    DEAD_LETTER_STREAM,
)

from app.domain.anomaly_detector import AnomalyDetector


STREAM_NAME = COST_DATA_INGESTED_STREAM
OUTPUT_STREAM = COST_DATA_READY_FOR_ANALYSIS_STREAM
ANOMALY_STREAM = COST_ANOMALY_DETECTED_STREAM
DLQ_STREAM = DEAD_LETTER_STREAM
GROUP_NAME = "analytics-group-v1"

logger = logging.getLogger(__name__)


class AnalyticsConsumer:

    def __init__(self, broker: BrokerInterface, consumer_name: str):
        self.broker = broker
        self.consumer_name = consumer_name
        self.processed_events: Set[str] = set()
        self.detector = AnomalyDetector()

    async def start(self):

        await self.broker.create_consumer_group(STREAM_NAME, GROUP_NAME)

        logger.info(
            "Starting analytics consumer",
            extra={"consumer": self.consumer_name},
        )

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

            # 🔹 Parse incoming event
            event = CostDataIngestedEvent.model_validate(base_event.model_dump())

            # 🔹 Emit "ready for analysis" event
            ready_payload = CostDataReadyForAnalysisPayload(
                account_id=event.payload.account_id,
                service=event.payload.service,
                cost=event.payload.cost,
                usage_timestamp=event.payload.usage_timestamp,
                processed_at=datetime.now(timezone.utc),
            )

            ready_event = CostDataReadyForAnalysisEvent(
                source="analytics-service",
                correlation_id=event.correlation_id,
                payload=ready_payload,
            )

            await self.broker.publish(OUTPUT_STREAM, ready_event)

            # ---------- 🔥 Anomaly Detection ----------

            result = self.detector.check_anomaly(
                event.payload.account_id,
                event.payload.service,
                event.payload.cost,
            )

            if result:

                anomaly_payload = CostAnomalyDetectedPayload(
                    account_id=event.payload.account_id,
                    service=event.payload.service,
                    cost=event.payload.cost,
                    expected_cost=result["expected_cost"],
                    deviation=result["deviation"],
                    anomaly_type=result["anomaly_type"],   # 🔥 NEW
                    confidence=result["confidence"],       # 🔥 NEW
                    detected_at=datetime.now(timezone.utc),
                )

                anomaly_event = CostAnomalyDetectedEvent(
                    source="analytics-service",
                    correlation_id=event.correlation_id,
                    payload=anomaly_payload,
                )

                await self.broker.publish(ANOMALY_STREAM, anomaly_event)

                logger.warning(
                    "Cost anomaly detected",
                    extra={
                        "event_id": anomaly_event.event_id,
                        "correlation_id": anomaly_event.correlation_id,
                        "account_id": event.payload.account_id,
                        "service": event.payload.service,
                        "anomaly_type": result["anomaly_type"],
                        "confidence": result["confidence"],
                    },
                )

            # ---------- ✅ Success ----------

            logger.info(
                "Processed cost_data_ingested_v1",
                extra={
                    "event_id": base_event.event_id,
                    "correlation_id": base_event.correlation_id,
                    "account_id": event.payload.account_id,
                    "service": event.payload.service,
                },
            )

            self.processed_events.add(base_event.event_id)

            await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)

        except Exception as e:

            logger.error(
                f"Processing failed: {str(e)}",
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
                    },
                )

                await self.broker.publish(DLQ_STREAM, base_event)

                await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)