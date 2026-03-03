import asyncio
import socket
import logging

from fastapi import FastAPI

from app.core.broker import get_broker
from app.workers.consumer import AnalyticsConsumer
from shared.observability.logging import configure_logging

logger = configure_logging("analytics-service")

app = FastAPI(title="Analytics Service")

broker = get_broker()
consumer_name = f"{socket.gethostname()}"

consumer = AnalyticsConsumer(broker, consumer_name)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting analytics consumer")
    asyncio.create_task(consumer.start())


@app.get("/health")
async def health():
    return {"status": "analytics-running"}