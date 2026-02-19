from pydantic import BaseModel
from typing import Any, Optional, Dict

class ErrorBody(BaseModel):
    code: int
    message: str
    details: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    error: ErrorBody
