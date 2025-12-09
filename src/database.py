from sqlmodel import SQLModel
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import get_settings
from src.models import Document

setting = get_settings()

# The primary point of entry for the database.
# `future=True` enables SQLAlchemy 2.0 style usage.
engine = create_async_engine(
    setting.DATABASE_URL,
    echo=setting.DEBUG,
    future=True,
)

# Creates all tables defined by SQLModel models.
# This is called once on application startup.
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency for FastAPI endpoints to get a database session.
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        # `expire_on_commit=False` prevents attributes from being expired
        # after commit, which is useful in an async context.
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session