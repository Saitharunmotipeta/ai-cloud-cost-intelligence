import json
import boto3
import os
import logging

from shared.events.cost_insight_generated_v1 import CostInsightGeneratedEvent
from app.domain.mock_data import load_mock_data

# -------------------------
# Setup
# -------------------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_DEFAULT_REGION", "eu-north-1"),
)

OUTPUT_QUEUE = os.getenv("INTELLIGENCE_QUEUE_URL")

# 🔥 Lazy graph initialization
graph = None


def get_graph():
    global graph
    if graph is None:
        logger.info("⚙️ Initializing graph (cold start)")

        from app.graph.graph_builder import build_graph
        load_mock_data()  # 🔥 ensure context is loaded

        graph = build_graph()

    return graph


# -------------------------
# Formatter (FIXED)
# -------------------------
def format_insight_for_embedding(explanation: dict, service: str) -> str:
    try:
        deviation = explanation.get("deviation_significance", 0)

        # handle ratio vs percentage
        if isinstance(deviation, (int, float)):
            percentage = deviation * 100 if deviation <= 1 else deviation
        else:
            percentage = 0

        trend = explanation.get("deviation_implication", "cost change")

        if isinstance(trend, str):
            trend = trend.replace("The deviation implies", "").strip()

        # 🔥 FIX: support both keys
        root = (
            explanation.get("root_cause")
            or explanation.get("specific_cause")
            or "unknown factors"
        )

        return (
            f"{service.upper()} cost increased by {round(percentage, 2)}%. "
            f"This indicates {trend}. Likely due to {root}."
        )

    except Exception:
        return f"{service.upper()} cost anomaly detected. Further analysis required."

# -------------------------
# Lambda Handler
# -------------------------
def lambda_handler(event, context):

    logger.info(f"🚀 Lambda invoked with {len(event.get('Records', []))} records")

    graph_instance = get_graph()

    for record in event.get("Records", []):
        try:
            body = json.loads(record["body"])
            logger.info(f"📩 Received analyzed event: {body}")

            # 🔥 SAFE extraction
            original_event = body.get("original_event")
            if not original_event:
                logger.warning("⚠️ Missing original_event — skipping")
                continue

            payload = original_event.get("payload", {})

            account_id = payload.get("account_id", "unknown")
            service = payload.get("service", "unknown")
            cost = payload.get("cost", 0)

            expected_cost = cost * 0.7
            deviation = cost - expected_cost

            logger.info(f"📊 Derived → expected: {expected_cost}, deviation: {deviation}")

            # 🔥 Pattern classification
            if deviation > 200:
                anomaly_type = "cost_spike"
            elif deviation > 50:
                anomaly_type = "gradual_increase"
            else:
                anomaly_type = "low_usage"

            logger.info(f"🧠 Classified Pattern → {anomaly_type}")

            # 🔥 Invoke graph
            result = graph_instance.invoke({
                "account_id": account_id,
                "service": service,
                "cost": cost,
                "expected_cost": expected_cost,
                "deviation": deviation,
                "anomaly_type": anomaly_type,
                "severity": body.get("severity", "LOW"),
            })

            explanation = result.get("explanation")
            root_cause = result.get("root_cause")
            severity = body.get("severity", "LOW")

            # -------------------------
            # Format explanation
            # -------------------------
            if isinstance(explanation, dict):
                message = format_insight_for_embedding(explanation, service)
            else:
                message = explanation or "AI explanation unavailable"

            # -------------------------
            # Clean root cause
            # -------------------------
            if isinstance(root_cause, dict):
                root_cause = root_cause.get("specific_cause") or json.dumps(root_cause)

            if not root_cause:
                root_cause = "Requires further investigation"

            # -------------------------
            # Build event
            # -------------------------
            insight_event = CostInsightGeneratedEvent.create(
                source="intelligence-service",
                correlation_id=original_event.get("correlation_id", "unknown"),
                account_id=account_id,
                service=service,
                severity=severity,
                message=message,
                recommendation=root_cause,
            )

            logger.info(f"🧠 Insight Generated: {message}")

            # -------------------------
            # Send to next queue (SAFE LOCAL)
            # -------------------------
            if OUTPUT_QUEUE and OUTPUT_QUEUE != "dummy":
                sqs.send_message(
                    QueueUrl=OUTPUT_QUEUE,
                    MessageBody=json.dumps(insight_event.model_dump(mode="json"))
                )
            else:
                logger.info("🧪 Skipping SQS send (local mode)")

        except Exception as e:
            logger.exception(f"❌ Lambda processing failed: {str(e)}")

    return {"statusCode": 200}