from pydantic import BaseModel
from typing import Any, Optional

class SuccessResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None

class MessageResponse(BaseModel):
    status: str
    message: str
