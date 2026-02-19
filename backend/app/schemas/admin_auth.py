from pydantic import BaseModel
from typing import Optional

class AdminIdentity(BaseModel):
    firebase_uid: str
    email: str
    display_name: Optional[str] = None
