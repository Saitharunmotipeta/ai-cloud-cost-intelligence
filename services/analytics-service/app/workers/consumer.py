import asyncio
import logging
import boto3
import json
import os
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
    def __init__(self, broker, consumer_name: str):
        self.consumer_name = consumer_name

        self.sqs = boto3.client(
            "sqs",
            region_name=os.getenv("AWS_DEFAULT_REGION")
        )

        # Input queue (from ingestion)
        self.queue_url = os.getenv("INGESTION_QUEUE_URL")

        # Output queue (to next stage)
        self.analytics_queue_url = os.getenv("ANALYTICS_QUEUE_URL")

    async def start(self):
        print(f"🚀 Analytics consumer started: {self.consumer_name}")

        while True:
            try:
                response = self.sqs.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=5,
                    WaitTimeSeconds=10
                )

                messages = response.get("Messages", [])

                for msg in messages:
                    body = json.loads(msg["Body"])

                    print("📩 Received event:", body)

                    payload = body["payload"]
                    cost = payload["cost"]

                    # 🔥 Simple anomaly detection
                    if cost > 200:
                        anomaly = True
                        severity = "HIGH"
                    else:
                        anomaly = False
                        severity = "LOW"

                    print(f"⚠️ Anomaly: {anomaly}, Severity: {severity}")

                    # 🔥 Create new event for next stage
                    new_event = {
                        "event_type": "cost_analyzed_v1",
                        "original_event": body,
                        "anomaly_detected": anomaly,
                        "severity": severity
                    }

                    # 🔥 Send to analytics queue
                    self.sqs.send_message(
                        QueueUrl=self.analytics_queue_url,
                        MessageBody=json.dumps(new_event)
                    )

                    # ✅ Delete message after processing
                    self.sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=msg["ReceiptHandle"]
                    )

            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")

            await asyncio.sleep(2)

    async def handle_message(self, message_id: str, base_event: BaseEvent):

        # Idempotency check
        if base_event.event_id in self.processed_events:
            await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)
            return

        try:

            # 🔹 Parse incoming event
            event = CostDataIngestedEvent.model_validate(base_event.model_dump(mode="json"))

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