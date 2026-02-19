from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime
from backend.app.utils.constants import ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE

class ApplyRequest(BaseModel):
    full_name: str = Field(..., max_length=100)
    dob: str
    email: EmailStr
    degree: str
    experience_years: int = Field(..., ge=0)
    preferred_course: str
    location_country: Optional[str] = None
    location_state: Optional[str] = None
    comments: Optional[str] = None
    cv_filename: str
    cv_size: int

    @validator("dob")
    def _dob_format(cls, v: str) -> str:
        datetime.strptime(v, "%Y-%m-%d")
        return v

    @validator("cv_filename")
    def _ext_allowed(cls, v: str) -> str:
        if "." not in v:
            raise ValueError("invalid file name")
        ext = v.rsplit(".", 1)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError("invalid file extension")
        return v

    @validator("cv_size")
    def _size_ok(cls, v: int) -> int:
        if v > MAX_UPLOAD_SIZE:
            raise ValueError("file too large")
        return v
