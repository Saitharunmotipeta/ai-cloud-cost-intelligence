from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple

from shared.events.base_event import BaseEvent


class BrokerInterface(ABC):
    """
    Abstract broker interface.

    Services must depend on this interface,
    not on Redis or SQS implementations directly.
    """

    # ---------------------------------------------------------
    # Publishing
    # ---------------------------------------------------------

    @abstractmethod
    async def publish(self, stream: str, event: BaseEvent) -> None:
        """
        Publish an event to a stream.
        """
        pass

    # ---------------------------------------------------------
    # Consumer Group Management
    # ---------------------------------------------------------

    @abstractmethod
    async def create_consumer_group(
        self,
        stream: str,
        group_name: str,
    ) -> None:
        """
        Create a consumer group for a stream.
        Should be idempotent.
        """
        pass

    # ---------------------------------------------------------
    # Consuming
    # ---------------------------------------------------------

    @abstractmethod
    async def consume(
        self,
        stream: str,
        group_name: str,
        consumer_name: str,
        count: int = 10,
        block: int = 5000,
    ) -> List[Tuple[str, BaseEvent]]:
        """
        Consume events from a stream using consumer groups.

        Returns:
            List of tuples:
            (message_id, BaseEvent)
        """
        pass

    # ---------------------------------------------------------
    # Acknowledgement
    # ---------------------------------------------------------

    @abstractmethod
    async def acknowledge(
        self,
        stream: str,
        group_name: str,
        message_id: str,
    ) -> None:
        """
        Acknowledge a message after successful processing.
        """
        pass