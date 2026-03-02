from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime
from backend.app.models.enums import Status
from backend.app.models.cv import CV


class Applicant(BaseModel):
    applicant_id: Optional[int] = None
    full_name: str = Field(..., max_length=100)
    dob: str
    email: EmailStr
    degree: str
    experience_years: int = Field(..., ge=0)
    preferred_course: str
    location_country: Optional[str] = None
    location_state: Optional[str] = None
    comments: Optional[str] = None
    status: Status = Status.Pending
    duplicate_flag: bool = False
    cv: Optional[CV] = None
    cv_filename: Optional[str] = None
    cv_url: Optional[str] = None
    submitted_at: Optional[datetime] = None

    @validator("dob")
    def _validate_dob(cls, v: str) -> str:
        datetime.strptime(v, "%Y-%m-%d")
        return v
