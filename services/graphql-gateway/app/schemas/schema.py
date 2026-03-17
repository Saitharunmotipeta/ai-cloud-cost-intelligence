import strawberry
from app.schemas.queries import Query

schema = strawberry.Schema(query=Query)