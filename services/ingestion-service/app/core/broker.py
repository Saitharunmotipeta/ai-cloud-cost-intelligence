import os

from shared.broker.sqs_broker import SQSBroker
from shared.broker.redis_streams_broker import RedisStreamsBroker


def get_broker():

    """
    Broker factory.

    Local development:
        BROKER_TYPE=redis

    Production:
        BROKER_TYPE=sqs
    """

    broker_type = os.getenv("BROKER_TYPE", "redis")

    if broker_type == "redis":

        redis_host = os.getenv("REDIS_HOST", "redis")
        redis_port = os.getenv("REDIS_PORT", "6379")

        redis_url = f"redis://{redis_host}:{redis_port}"

        return RedisStreamsBroker(redis_url)

    if broker_type == "sqs":
        return SQSBroker()

    raise ValueError(f"Unsupported broker type: {broker_type}")