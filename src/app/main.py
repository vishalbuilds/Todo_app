
from fastapi import FastAPI
from database.models import Base
from database.db_session import engine
from app.api.v1.api_router_v1 import router as router_api_v1

from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync((Base.metadata.create_all))
    yield 

app=FastAPI(lifespan=lifespan)


app.include_router(router_api_v1,prefix="/api/v1")
