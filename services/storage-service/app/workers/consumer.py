import asyncio
import logging
from typing import Set

from sqlalchemy.orm import Session

from shared.events.base_event import BaseEvent
from shared.events.cost_insight_generated_v1 import CostInsightGeneratedEvent

from shared.broker.interface import BrokerInterface

from app.core.database import SessionLocal
from app.services.insight_repository import InsightRepository


STREAM_NAME = "cost_insight_generated_v1"
GROUP_NAME = "storage-group-v1"

logger = logging.getLogger(__name__)


class StorageConsumer:

    def __init__(self, broker: BrokerInterface, consumer_name: str):

        self.broker = broker
        self.consumer_name = consumer_name

        # protects against duplicate processing
        self.processed_events: Set[str] = set()

    async def start(self):

        await self.broker.create_consumer_group(
            STREAM_NAME,
            GROUP_NAME,
        )

        logger.info(
            "Starting storage consumer",
            extra={
                "consumer": self.consumer_name,
                "stream": STREAM_NAME,
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

                logger.exception("Storage consumer failure")

            await asyncio.sleep(1)

    async def handle_message(self, message_id: str, base_event: BaseEvent):

        if base_event.event_id in self.processed_events:

            await self.broker.acknowledge(
                STREAM_NAME,
                GROUP_NAME,
                message_id,
            )

            return

        try:

            event = CostInsightGeneratedEvent.model_validate(
                base_event.model_dump()
            )

            payload = event.payload

            db: Session = SessionLocal()

            repo = InsightRepository(db)

            repo.save_insight(
                insight_id=payload.insight_id,
                account_id=payload.account_id,
                service=payload.service,
                severity=payload.severity,
                message=payload.message,
                recommendation=payload.recommendation,
                generated_at=payload.generated_at,
            )

            db.close()

            logger.info(
                "Insight stored",
                extra={
                    "insight_id": payload.insight_id,
                    "account_id": payload.account_id,
                },
            )

            self.processed_events.add(base_event.event_id)

            await self.broker.acknowledge(
                STREAM_NAME,
                GROUP_NAME,
                message_id,
            )

        except Exception:

            logger.exception(
                "Failed storing insight",
                extra={
                    "event_id": base_event.event_id,
                },
            )