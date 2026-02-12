from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.app.models.enums import Status

class ApplicantDTO(BaseModel):
    applicant_id: Optional[int]
    full_name: str
    dob: str
    email: str
    degree: str
    experience_years: int
    preferred_course: str
    location_country: Optional[str]
    location_state: Optional[str]
    comments: Optional[str]
    status: Status
    duplicate_flag: bool
    cv_filename: Optional[str]
    cv_url: Optional[str]
    submitted_at: Optional[datetime]
