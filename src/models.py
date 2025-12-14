from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime
from pgvector.sqlalchemy import Vector

class Document(SQLModel, table=True):

    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True)
    filename: str
    content: str
    # Use a factory for the default to ensure a new UTC timestamp is generated for each record.
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(timezone.utc),    
    )
    # Stores the 384-dimensional vector embedding from the 'all-MiniLM-L6-v2' model.
    # The `Vector` type is provided by the pgvector extension.
    embedding: list[float] | None = Field(default=None, sa_column=Column(Vector(384)))