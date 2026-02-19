from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CV(BaseModel):
    filename: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., min_length=1)
    uploaded_at: Optional[datetime] = None
    content_type: Optional[str] = Field(default=None, max_length=100)
    size_bytes: Optional[int] = Field(default=None, ge=0)
