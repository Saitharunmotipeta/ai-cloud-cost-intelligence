import asyncio
import logging

logger = logging.getLogger(__name__)


class RetryHandler:

    MAX_RETRIES = 3

    BACKOFF = [2, 5, 10]

    @classmethod
    async def handle_retry(cls, event):

        event.increment_retry()

        retry = event.retry_count

        if retry > cls.MAX_RETRIES:
            return False

        delay = cls.BACKOFF[min(retry - 1, len(cls.BACKOFF) - 1)]

        logger.warning(
            f"Retrying event {event.event_id} attempt {retry} after {delay}s"
        )

        await asyncio.sleep(delay)

        return True