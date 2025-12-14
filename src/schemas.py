from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict
    
class DocumentResponse(BaseModel):
    id: int
    filename: str
    content: str
    created_at: datetime

    # Allows Pydantic to create this schema from an ORM model instance (e.g., Document).
    model_config = ConfigDict(from_attributes=True)

class SearchResponse(DocumentResponse):
    # The response for a search result is currently identical to a document response.
    # Defined as a separate class for future extension, e.g., to include a similarity score.
    pass