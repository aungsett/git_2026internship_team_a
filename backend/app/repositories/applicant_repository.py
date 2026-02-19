from typing import Optional, List, Dict, Any, Tuple
from backend.app.models.applicant import Applicant

class ApplicantRepository:
    @staticmethod
    def get_by_email(email: str) -> Optional[Applicant]:
        return Applicant.objects(email=email).first()

    @staticmethod
    def get_by_applicant_id(applicant_id: int) -> Optional[Applicant]:
        return Applicant.objects(applicant_id=applicant_id).first()

    @staticmethod
    def create(applicant: Applicant) -> Applicant:
        applicant.save()
        return applicant

    @staticmethod
    def count(filters: Dict[str, Any]) -> int:
        qs = Applicant.objects(**filters)
        return int(qs.count())

    @staticmethod
    def list(filters: Dict[str, Any], page: int, limit: int) -> List[Applicant]:
        skip = (page - 1) * limit
        qs = Applicant.objects(**filters).order_by("-submitted_at").skip(skip).limit(limit)
        return list(qs)

    @staticmethod
    def update_status(applicant_id: int, new_status: str) -> bool:
        updated = Applicant.objects(applicant_id=applicant_id).update_one(set__status=new_status)
        return updated == 1
