from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

class Document(SQLModel, table=True):

    __tablename__ = "documents"

    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    content: str
    # Use a factory for the default to ensure a new UTC timestamp is generated for each record.
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))