from pydantic import BaseModel
from backend.app.models.enums import Status
from typing import Optional
from datetime import datetime

class StatusUpdateRequest(BaseModel):
    status: Status

class StatusUpdateResponse(BaseModel):
    status: str
    applicant_id: int
    new_status: Status
    updated_at: datetime
