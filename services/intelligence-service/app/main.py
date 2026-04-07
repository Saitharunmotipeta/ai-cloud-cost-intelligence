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
from app.domain.embedding import get_embedding
from app.domain.rag_store import vector_store
from app.domain.rag_formatter import format_insight

app = FastAPI(title="Intelligence Service")

configure_logging("intelligence-service")

broker = get_broker()

consumer_name = socket.gethostname()

consumer = IntelligenceConsumer(broker, consumer_name)

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    load_mock_data()
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

def load_mock_data():
    mock_insights = [
        {
            "service": "EC2",
            "anomaly_type": "spike",
            "severity": "high",
            "root_cause": "Auto-scaling misconfiguration",
            "explanation": "Instances scaled aggressively due to low threshold"
        },
        {
            "service": "Lambda",
            "anomaly_type": "cost_increase",
            "severity": "medium",
            "root_cause": "High invocation rate",
            "explanation": "Unexpected surge in function calls"
        }
    ]

    for insight in mock_insights:
        text = format_insight(insight)
        emb = get_embedding(text)
        vector_store.add(emb, insight)