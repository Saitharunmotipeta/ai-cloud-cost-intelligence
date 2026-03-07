import os
from shared.broker.redis_streams_broker import RedisStreamsBroker


def get_broker():

    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = os.getenv("REDIS_PORT", "6379")

    redis_url = f"redis://{redis_host}:{redis_port}"

    return RedisStreamsBroker(redis_url=redis_url)