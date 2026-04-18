import asyncio
import logging
import boto3
import json
import os
from typing import Set

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.insight_repository import InsightRepository

logger = logging.getLogger(__name__)

class StorageConsumer:

    def __init__(self, consumer_name: str):

        self.consumer_name = consumer_name
        self.processed_events: Set[str] = set()

        self.sqs = boto3.client(
            "sqs",
            region_name=os.getenv("AWS_DEFAULT_REGION")
        )

        # 🔥 Read from intelligence queue
        self.queue_url = os.getenv("INTELLIGENCE_QUEUE_URL")

    async def start(self):

        logger.info(f"💾 Storage consumer started: {self.consumer_name}")

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

                    print("📥 Received insight event:", body)

                    await self.handle_message(body)

                    # ✅ delete message after storing
                    self.sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=msg["ReceiptHandle"]
                    )

            except Exception as e:
                logger.exception(f"Storage consumer failure: {str(e)}")

            await asyncio.sleep(2)

    async def handle_message(self, data: dict):

        db: Session = SessionLocal()

        try:
            repo = InsightRepository(db)

            payload = data.get("payload", {})

            repo.save_insight(
                insight_id=payload.get("insight_id"),
                account_id=payload.get("account_id"),
                service=payload.get("service"),

                severity=payload.get("severity"),
                impact=payload.get("impact", "medium"),
                anomaly_type=payload.get("anomaly_type", "basic"),

                explanation=payload.get("message"),
                root_cause=payload.get("recommendation"),
                action=payload.get("recommendation"),
                confidence=payload.get("confidence", "low"),

                message=payload.get("message"),
                recommendation=payload.get("recommendation"),

                generated_at=payload.get("generated_at"),
            )

            logger.info(
                "✅ Insight stored in DB",
                extra={
                    "event_id": data.get("event_id"),
                    "account_id": payload.get("account_id"),  # 🔥 FIXED
                },
            )

        except Exception as e:
            logger.exception(f"❌ Failed storing insight: {str(e)}")

        finally:
            db.close()   # 🔥 ALWAYS closes