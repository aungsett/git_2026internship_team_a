from models.applicant import Applicant
from utils.id_generator import generate_applicant_id
from datetime import datetime


class ApplicantRepository:
    """
    Repository layer for Applicant collection.
    Handles all database operations using MongoEngine ODM.
    """

    def create_applicant(self, data: dict):
        """
        Create a new applicant record.
        Implements duplicate email flag policy.
        """

        existing = self.find_by_email(data["email"])
        duplicate_flag = True if existing else False

        applicant = Applicant(
            applicant_id=generate_applicant_id(),
            full_name=data["full_name"],
            dob=data["dob"],
            email=data["email"],
            degree=data["degree"],
            experience_years=data["experience_years"],
            preferred_course=data["preferred_course"],
            location_country=data.get("location_country"),
            location_state=data.get("location_state"),
            comments=data.get("comments"),
            cv_filename=data["cv_filename"],
            cv_url=data["cv_url"],
            duplicate_flag=duplicate_flag,
            status="Pending",
            submitted_at=datetime.utcnow()
        )

        applicant.save()
        return applicant

    def find_by_email(self, email: str):
        return Applicant.objects(email=email).first()

    def find_by_id(self, applicant_id: int):
        return Applicant.objects(applicant_id=applicant_id).first()

    def update_status(self, applicant_id: int, new_status: str) -> bool:
        """
        Update application status.
        Returns True if update was successful.
        """
        updated = Applicant.objects(
            applicant_id=applicant_id
        ).update_one(set__status=new_status)

        return updated > 0

    def list_applicants(
        self,
        filters: dict,
        page: int = 1,
        limit: int = 25
    ):
        """
        List applicants with filters and pagination.
        """

        query = Applicant.objects(**filters)

        total = query.count()
        skip = (page - 1) * limit

        results = query.skip(skip).limit(limit)

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "data": list(results)
        }
