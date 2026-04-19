import asyncio
import socket
import logging
import os

from fastapi import FastAPI
from dotenv import load_dotenv

# 🔥 Load env properly (keep this)
load_dotenv(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../infrastructure/docker/.env")
    )
)

from app.workers.consumer import IntelligenceConsumer
from shared.observability.logging import configure_logging
from app.domain.embedding import get_embedding
from app.domain.rag_store import vector_store
from app.domain.rag_formatter import format_insight_for_embedding

app = FastAPI(title="Intelligence Service")

configure_logging("intelligence-service")

logger = logging.getLogger(__name__)

# 🔥 NO broker anymore
consumer_name = socket.gethostname()
consumer = IntelligenceConsumer(consumer_name)


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
            "pattern": "cost_spike",
            "severity": "high",
            "root_cause": "Sudden increase in usage or misconfiguration",
            "explanation": "A sudden spike in usage can lead to unexpected cost increases across any service."
        },
        {
            "pattern": "gradual_increase",
            "severity": "medium",
            "root_cause": "Steady growth in workload or traffic",
            "explanation": "Costs increasing gradually may indicate scaling demand or inefficient resource usage."
        },
        {
            "pattern": "low_usage",
            "severity": "low",
            "root_cause": "Normal usage behavior",
            "explanation": "Cost levels are within expected range with no significant anomalies."
        }
    ]

    for insight in mock_insights:
        text = format_insight_for_embedding(insight)
        emb = get_embedding(text)
        vector_store.add(emb, insight)