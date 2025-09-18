
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from .auth import auth_url
from typing import AsyncGenerator

# Create an engine object that manages the connection pool and SQL execution, echo=True enables SQL logging

engine = create_async_engine(auth_url, echo=True)
async_session_pool = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Dependency Injection for DB Session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_pool() as session:
        yield session




