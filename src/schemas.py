from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict
    
class DocumentResponse(BaseModel):
    id: int
    filename: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)