from sqlmodel import SQLModel
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import get_settings
from sqlalchemy import text, create_engine

setting = get_settings()

# The primary point of entry for the database.
# `future=True` enables SQLAlchemy 2.0 style usage.
engine = create_async_engine(
    setting.DATABASE_URL,
    echo=setting.DEBUG,
    future=True,
)

# `expire_on_commit=False` prevents attributes from being expired
# after commit, which is useful in an async context.
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    # The original implementation runs CREATE EXTENSION and CREATE TABLE in the same transaction.
    # While this should work, separating them can be more robust, especially in async contexts
    # where DDL commands might have special transactional behavior.
    async with engine.connect() as conn:
        # Ensure the vector extension is created in a separate, committed transaction
        # before proceeding to create tables. This avoids race conditions.
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.commit()

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

def get_sync_engine():
    # Create a synchronous engine for use in Celery workers.
    # Replaces the async driver `asyncpg` with the sync driver `psycopg`.
    # Celery runs in a separate process and cannot share the main async event loop.
    sync_db_url = setting.DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg")
    return create_engine(sync_db_url, echo=setting.DEBUG, future=True)