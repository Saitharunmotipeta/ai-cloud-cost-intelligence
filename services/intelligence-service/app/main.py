from fastapi import FastAPI

app = FastAPI(title="Intelligence Service")


@app.get("/health")
async def health():
    return {"status": "intelligence-service-running"}