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
    location_country: Optional[str] = None
    location_state: Optional[str] = None
    comments: Optional[str] = None
    status: Status = Status.Pending
    duplicate_flag: bool = False
    cv_filename: Optional[str] = None
    cv_url: Optional[str] = None
    submitted_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, d: dict):
        # accepts DB dicts (e.g., pymongo result) and normalizes keys
        if "submitted_at" in d and isinstance(d["submitted_at"], str):
            d["submitted_at"] = datetime.fromisoformat(d["submitted_at"])
        return cls(**d)

    def to_dict(self) -> dict:
        out = self.dict()
        if isinstance(out.get("submitted_at"), datetime):
            out["submitted_at"] = out["submitted_at"].isoformat()
        return out
