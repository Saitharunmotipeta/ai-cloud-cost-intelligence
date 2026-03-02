from shared.broker.redis_streams_broker import RedisStreamsBroker


def get_broker() -> RedisStreamsBroker:
    redis_url = "redis://redis:6379/0"
    return RedisStreamsBroker(redis_url=redis_url)