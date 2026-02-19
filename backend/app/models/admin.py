# backend/app/models/admin.py

# Pydantic model (used by tests / validation / DTOs)
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime, timezone

class Admin(BaseModel):
    admin_id: Optional[int]
    firebase_uid: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    display_name: Optional[str] = Field(default=None, max_length=100)
    role: str = Field(default="admin", min_length=1, max_length=30)
    created_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None

    @validator("created_at", pre=True, always=True)
    def ensure_created_at(cls, v):
        if v is None:
            return datetime.now(timezone.utc)
        return v

# MongoEngine Document (used by repo layer / DB)
from mongoengine import (
    Document,
    StringField,
    IntField,
    EmailField,
    DateTimeField,
)

class AdminDocument(Document):
    meta = {
        "collection": "admins",
        "indexes": ["firebase_uid", "email", "username"]
    }

    admin_id = IntField(required=True, unique=True)
    firebase_uid = StringField(required=True, unique=True)
    username = StringField(required=True, unique=True, max_length=50)
    email = EmailField(required=True, unique=True)
    display_name = StringField()
    role = StringField(default="admin")
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    last_login_at = DateTimeField()
