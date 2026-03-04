import asyncio
import socket
import logging

from fastapi import FastAPI

from app.core.broker import get_broker
from app.workers.consumer import IntelligenceConsumer
from shared.observability.logging import configure_logging

app = FastAPI(title="Intelligence Service")

configure_logging("intelligence-service")

broker = get_broker()

consumer_name = socket.gethostname()

consumer = IntelligenceConsumer(broker, consumer_name)

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consumer.start())


@app.get("/health")
async def health():
    return {"status": "intelligence-running"}