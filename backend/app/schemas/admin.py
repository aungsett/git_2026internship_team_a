from pydantic import BaseModel, Field
from typing import List, Optional
from backend.app.dtos.applicant_dto import ApplicantDTO

class AdminListResponse(BaseModel):
    page: int = Field(..., ge=1)
    limit: int = Field(..., ge=1)
    total: int = Field(..., ge=0)
    data: List[ApplicantDTO]

class AdminDetailResponse(BaseModel):
    applicant: ApplicantDTO
