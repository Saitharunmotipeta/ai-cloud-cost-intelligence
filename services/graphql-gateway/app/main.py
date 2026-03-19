from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.schema import schema

app = FastAPI(title="GraphQL Gateway")

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "graphql-running"}


@app.get("/metrics")
async def metrics():
    return {
        "service": "graphql-gateway",
        "status": "running"
    }