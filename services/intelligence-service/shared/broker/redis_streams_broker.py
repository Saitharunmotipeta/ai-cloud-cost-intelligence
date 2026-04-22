from __future__ import annotations

import json
from typing import List, Tuple

import redis.asyncio as redis
from redis.exceptions import ResponseError

from shared.broker.interface import BrokerInterface
from shared.events.base_event import BaseEvent


class RedisStreamsBroker(BrokerInterface):
    """
    Redis Streams implementation of BrokerInterface.

    Uses:
    - XADD for publishing
    - XGROUP for consumer groups
    - XREADGROUP for consuming
    - XACK for acknowledgement
    """

    def __init__(self, redis_url: str) -> None:
        self._client = redis.from_url(
            redis_url,
            decode_responses=True,
        )

    # ---------------------------------------------------------
    # Publishing
    # ---------------------------------------------------------

    async def publish(self, stream: str, event: BaseEvent) -> None:
        try:
            await self._client.xadd(
                name=stream,
                fields={"data": event.to_json()},
                maxlen=1000,
                approximate=True,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to publish event to {stream}") from e

    # ---------------------------------------------------------
    # Consumer Group Management
    # ---------------------------------------------------------

    async def create_consumer_group(
        self,
        stream: str,
        group_name: str,
    ) -> None:
        try:
            await self._client.xgroup_create(
                name=stream,
                groupname=group_name,
                id="0",
                mkstream=True,
            )
        except ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise

    # ---------------------------------------------------------
    # Consuming
    # ---------------------------------------------------------

    async def consume(
        self,
        stream: str,
        group_name: str,
        consumer_name: str,
        count: int = 10,
        block: int = 5000,
    ) -> List[Tuple[str, BaseEvent]]:
        """
        Read new messages using XREADGROUP.

        Returns:
            List[(message_id, BaseEvent)]
        """

        try:
            response = await self._client.xreadgroup(
                groupname=group_name,
                consumername=consumer_name,
                streams={stream: ">"},
                count=count,
                block=block,
            )

        except ResponseError as e:

            # Stream or group may have been deleted (FLUSHALL, etc.)
            if "NOGROUP" in str(e) or "no such key" in str(e):

                # Recreate stream + group automatically
                try:
                    await self._client.xgroup_create(
                        name=stream,
                        groupname=group_name,
                        id="0",
                        mkstream=True,
                    )
                except ResponseError:
                    pass

                return []

            raise RuntimeError("Failed while consuming events") from e

        except Exception as e:
            raise RuntimeError("Failed while consuming events") from e

        if not response:
            return []

        messages: List[Tuple[str, BaseEvent]] = []

        for _, stream_messages in response:
            for message_id, fields in stream_messages:

                raw_event = fields.get("data")
                if raw_event is None:
                    continue

                event = BaseEvent.from_json(raw_event)
                messages.append((message_id, event))

        return messages

    # ---------------------------------------------------------
    # Acknowledgement
    # ---------------------------------------------------------

    async def acknowledge(
        self,
        stream: str,
        group_name: str,
        message_id: str,
    ) -> None:
        try:
            await self._client.xack(stream, group_name, message_id)
        except Exception as e:
            raise RuntimeError(
                f"Failed to acknowledge message {message_id}"
            ) from e