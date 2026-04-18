import asyncio
import logging
import boto3
import json
import os
from typing import Set

from shared.events.cost_insight_generated_v1 import CostInsightGeneratedEvent
from app.graph.graph_builder import build_graph

logger = logging.getLogger(__name__)


class IntelligenceConsumer:

    def __init__(self, consumer_name: str):

        self.consumer_name = consumer_name
        self.processed_events: Set[str] = set()

        self.graph = build_graph()

        self.sqs = boto3.client(
            "sqs",
            region_name=os.getenv("AWS_DEFAULT_REGION")
        )

        # 🔥 Input queue (from analytics)
        self.queue_url = os.getenv("ANALYTICS_QUEUE_URL")

        # 🔥 Output queue (next stage)
        self.output_queue_url = os.getenv("INTELLIGENCE_QUEUE_URL")

    async def start(self):

        logger.info(f"🧠 Intelligence consumer started: {self.consumer_name}")

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

                    print("📩 Received analyzed event:", body)

                    await self.handle_message(body)

                    # ✅ delete message after processing
                    self.sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=msg["ReceiptHandle"]
                    )

            except Exception as e:
                logger.exception(f"Error consuming messages: {str(e)}")

            await asyncio.sleep(2)

    async def handle_message(self, body: dict):

        try:
            # 🔥 Extract original ingestion event
            original_event = body["original_event"]
            payload = original_event["payload"]

            account_id = payload["account_id"]
            service = payload["service"]
            cost = payload["cost"]

            # 🔥 TEMP LOGIC (Option A)
            expected_cost = cost * 0.7
            deviation = cost - expected_cost

            print(f"📊 Derived → expected: {expected_cost}, deviation: {deviation}")

            # 🔥 Invoke LangGraph
            result = await self.graph.ainvoke({
                "event": {
                    "account_id": account_id,
                    "service": service,
                    "cost": cost,
                    "expected_cost": expected_cost,
                    "deviation": deviation,
                },
                "anomaly_type": "basic",
            })

            explanation = result.get("explanation", "No explanation generated")
            root_cause = result.get("root_cause", "Unknown")
            confidence = result.get("confidence", "low")
            severity = result.get("severity", "low")

            # 🔥 Build insight event
            insight_event = CostInsightGeneratedEvent.create(
                source="intelligence-service",
                correlation_id=original_event["correlation_id"],
                account_id=account_id,
                service=service,
                severity=severity,
                message=explanation,
                recommendation=root_cause,
            )

            print("🧠 Insight Generated:", explanation)

            # 🔥 Send to next queue
            self.sqs.send_message(
                QueueUrl=self.output_queue_url,
                MessageBody=json.dumps(insight_event.model_dump(mode="json"))
            )

            logger.info(
                "Insight generated",
                extra={
                    "event_id": insight_event.event_id,
                    "correlation_id": insight_event.correlation_id,
                    "account_id": account_id,
                    "service": service,
                    "confidence": confidence,
                },
            )

        except Exception as e:
            logger.exception(f"Insight generation failed: {str(e)}")