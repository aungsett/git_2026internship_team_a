from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdminDTO(BaseModel):
    admin_id: Optional[int]
    firebase_uid: str
    username: str
    email: str
    display_name: Optional[str]
    role: str
    created_at: Optional[datetime]
    last_login_at: Optional[datetime]
