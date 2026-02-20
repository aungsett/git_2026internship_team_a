# backend/app/models/enums.py
from enum import Enum

class ApplicantStatus(Enum):
    Pending = "Pending"
    Reviewed = "Reviewed"
    Shortlisted = "Shortlisted"
    Accepted = "Accepted"
    Rejected = "Rejected"

# compatibility alias cuz some files may import `Status` instead of `ApplicantStatus`
Status = ApplicantStatus
