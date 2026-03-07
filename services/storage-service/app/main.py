import asyncio
import socket

from fastapi import FastAPI

from app.core.broker import get_broker
from app.core.database import Base, engine
from app.workers.consumer import StorageConsumer

app = FastAPI(title="Storage Service")

broker = get_broker()

consumer_name = socket.gethostname()

consumer = StorageConsumer(broker, consumer_name)

@app.on_event("startup")
async def startup_event():   
    Base.metadata.create_all(bind=engine)
    asyncio.create_task(consumer.start())

@app.get("/health")
async def health():
    return {"status": "storage-running"}