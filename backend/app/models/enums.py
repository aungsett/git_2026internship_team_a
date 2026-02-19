from enum import Enum

class Status(str, Enum):
    Pending = "Pending"
    Reviewed = "Reviewed"
    Shortlisted = "Shortlisted"
    Accepted = "Accepted"
    Rejected = "Rejected"
