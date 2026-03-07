import asyncio
import logging
from sqlalchemy import text

from shared.events.base_event import BaseEvent
from shared.events.cost_insight_generated_v1 import CostInsightGeneratedEvent

from app.core.database import SessionLocal
from shared.broker.interface import BrokerInterface

STREAM_NAME = "cost_insight_generated_v1"
GROUP_NAME = "storage-group-v1"

logger = logging.getLogger(__name__)


class StorageConsumer:

    def __init__(self, broker: BrokerInterface, consumer_name: str):
        self.broker = broker
        self.consumer_name = consumer_name

    async def start(self):

        await self.broker.create_consumer_group(STREAM_NAME, GROUP_NAME)

        logger.info("Starting storage consumer")

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

        try:

            event = CostInsightGeneratedEvent.model_validate(
                base_event.model_dump()
            )

            payload = event.payload

            db = SessionLocal()

            db.execute(
                text(
                    """
                    INSERT INTO insights (
                        id,
                        account_id,
                        service,
                        severity,
                        message,
                        recommendation,
                        correlation_id,
                        generated_at
                    )
                    VALUES (
                        :id,
                        :account_id,
                        :service,
                        :severity,
                        :message,
                        :recommendation,
                        :correlation_id,
                        :generated_at
                    )
                    """
                ),
                {
                    "id": event.event_id,
                    "account_id": payload.account_id,
                    "service": payload.service,
                    "severity": payload.severity,
                    "message": payload.message,
                    "recommendation": payload.recommendation,
                    "correlation_id": event.correlation_id,
                    "generated_at": payload.generated_at,
                },
            )

            db.commit()
            db.close()

            await self.broker.acknowledge(STREAM_NAME, GROUP_NAME, message_id)

            logger.info("Insight stored successfully")

        except Exception as e:

            logger.error(f"Failed to store insight: {str(e)}")