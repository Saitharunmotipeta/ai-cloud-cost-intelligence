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


def format_insight_for_embedding(explanation: dict, service: str) -> str:
    try:
        if not explanation or not isinstance(explanation, dict):
            return f"{service.upper()} cost anomaly detected. Further analysis required."

        deviation = explanation.get("deviation_significance", 0)
        implication = explanation.get("deviation_implication", "")
        cause = explanation.get("specific_cause") or explanation.get("root_cause")

        # ✅ FIXED percentage logic
        if isinstance(deviation, (int, float)):
            percentage = deviation * 100 if deviation <= 1 else deviation
        else:
            percentage = 0

        # ✅ Clean implication text
        implication_text = str(implication)\
            .replace("The deviation implies", "")\
            .replace("This deviation indicates", "")\
            .strip()

        # ✅ Clean cause
        cause_text = str(cause).strip() if cause else "unknown factors"

        return (
            f"{service.upper()} cost changed by {round(percentage, 2)}%. "
            f"{implication_text}. Likely due to {cause_text}."
        )

    except Exception as e:
        print("❌ FORMAT ERROR:", str(e))
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

            elif isinstance(explanation, str) and explanation.strip():
                message = explanation

            else:
                # 🔥 FALLBACK USING ROOT CAUSE
                fallback_cause = root_cause or "unknown factors"
                message = f"{service.upper()} cost anomaly detected. Likely due to {fallback_cause}."

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