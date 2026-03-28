import asyncio
import socket
import logging

from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../infrastructure/docker/.env")
    )
)

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


@app.get("/metrics")
async def metrics():
    return {
        "service": "intelligence-service",
        "status": "running"
    }