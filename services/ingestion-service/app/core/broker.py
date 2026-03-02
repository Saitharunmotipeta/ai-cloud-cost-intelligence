from redis.asyncio import Redis

from shared.broker.redis_streams_broker import RedisStreamsBroker


def get_broker() -> RedisStreamsBroker:
    """
    Factory for RedisStreamsBroker.
    Keeps wiring separate from business logic.
    """
    redis_url = "redis://redis:6379/0"  # Docker service name
    return RedisStreamsBroker(redis_url=redis_url)