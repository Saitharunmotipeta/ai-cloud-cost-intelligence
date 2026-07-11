import asyncio
import logging
import boto3
import json
import os
import time
from typing import Set

from shared.events.cost_insight_generated_v1 import CostInsightGeneratedEvent
from shared.observability.metrics import (start_timer,stop_timer,)
from app.graph.graph_builder import build_graph

logger = logging.getLogger(__name__)


def format_insight_for_embedding(explanation: dict, service: str) -> str:
    """
    Convert structured LLM output into human-readable message
    """
    try:
        deviation = explanation.get("deviation_significance", {})
        implication = explanation.get("deviation_implication", {})
        cause = explanation.get("specific_cause", {})

        percentage = (
            deviation.get("percentage")
            or deviation.get("percentage_deviation")
            or deviation.get("deviation_percentage")
            or 0
        )

        trend = (
            implication.get("trend")
            or implication.get("description")
            or "cost change"
        )

        if isinstance(trend, str):
            trend = trend.replace("This deviation implies", "").strip()

        root = (
            cause.get("specific_cause") 
            or cause.get("cause")
            or cause.get("description")
            or "unknown factors"
        )

        return (
            f"{service.upper()} cost increased by {round(percentage, 2)}%. "
            f"This indicates a {trend}. Likely due to {root}."
        )

    except Exception:
        return f"{service.upper()} cost anomaly detected. Further analysis required."


class IntelligenceConsumer:

    def __init__(self, consumer_name: str):

        self.consumer_name = consumer_name
        self.processed_events: Set[str] = set()

        self.graph = build_graph()

        self.sqs = boto3.client(
            "sqs",
            region_name=os.getenv("AWS_DEFAULT_REGION")
        )

        self.queue_url = os.getenv("ANALYTICS_QUEUE_URL")
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

                    self.sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=msg["ReceiptHandle"]
                    )

            except Exception as e:
                logger.exception(f"Error consuming messages: {str(e)}")

            await asyncio.sleep(2)

    async def handle_message(self, body: dict):

        try:
            pipeline_timer = start_timer()
            original_event = body["original_event"]
            payload = original_event["payload"]

            account_id = payload["account_id"]
            service = payload["service"]
            cost = payload["cost"]

            expected_cost = cost * 0.7
            deviation = cost - expected_cost

            print(f"📊 Derived → expected: {expected_cost}, deviation: {deviation}")

            # 🔥 Pattern classification (can remove later)
            if deviation > 200:
                anomaly_type = "cost_spike"
            elif deviation > 50:
                anomaly_type = "gradual_increase"
            else:
                anomaly_type = "low_usage"

            print(f"🧠 Classified Pattern → {anomaly_type}")
            graph_timer = start_timer()

            result = await self.graph.ainvoke({
                "account_id": account_id,
                "service": service,
                "cost": cost,
                "expected_cost": expected_cost,
                "deviation": deviation,
                "anomaly_type": anomaly_type,
                "severity": body.get("severity", "LOW"),
            })

            graph_ms = stop_timer(
                graph_timer
            )

            explanation = result.get("explanation")
            root_cause = result.get("root_cause")
            confidence = result.get("confidence", "low")

            incoming_severity = body.get("severity", "LOW")
            severity = incoming_severity

            # 🔥 FORMAT MESSAGE (MAIN UPGRADE)
            if isinstance(explanation, dict):
                message = format_insight_for_embedding(explanation, service)
                details = json.dumps(explanation, indent=2)
            else:
                message = explanation or "AI explanation unavailable"
                details = None

            # 🔥 CLEAN ROOT CAUSE
            if isinstance(root_cause, dict):
                root_cause = root_cause.get("specific_cause") or json.dumps(root_cause)

            if not root_cause:
                root_cause = "Requires further investigation"

            insight_event = CostInsightGeneratedEvent.create(
                source="intelligence-service",
                correlation_id=original_event["correlation_id"],
                account_id=account_id,
                service=service,
                severity=severity,
                message=message,              # 👈 HUMAN READABLE
                recommendation=root_cause,    # 👈 CLEAN STRING
            )

            print("🧠 Insight Generated:", message)

            self.sqs.send_message(
                QueueUrl=self.output_queue_url,
                MessageBody=json.dumps(insight_event.model_dump(mode="json"))
            )
            

            pipeline_ms = stop_timer(pipeline_timer)
            
            print("\n📈 Intelligence Metrics")
            print(f"🧠 Graph Execution : {graph_ms:.2f} ms")
            print(f"⚡ Total Intelligence Pipeline : {pipeline_ms:.2f} ms")
            print(f"📚 Context Retrieval : {result.get('context_retrieval_ms')} ms")
            print(f"🤖 LLM Reasoning : {result.get('llm_reasoning_ms')} ms")

        except Exception as e:
            logger.exception(f"Insight generation failed: {str(e)}")