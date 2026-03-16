from typing import Dict, Any, Tuple
from io import StringIO
import csv

from backend.app.repositories.applicant_repository import ApplicantRepository
from backend.app.models.enums import ApplicantStatus


class AdminService:
    def list_applicants(
        self,
        filters: Dict[str, Any],
        page: int = 1,
        limit: int = 25,
    ) -> Tuple[list, int]:

        query_filters = {}

        if "status" in filters and filters["status"]:
            query_filters["status"] = filters["status"]

        if "degree" in filters and filters["degree"]:
            query_filters["degree"] = filters["degree"]

        if "preferred_course" in filters and filters["preferred_course"]:
            query_filters["preferred_course"] = filters["preferred_course"]

        if "experience_years" in filters and filters["experience_years"] is not None:
            query_filters["experience_years"] = filters["experience_years"]

        total = ApplicantRepository.count(query_filters)
        applicants = ApplicantRepository.list(query_filters, page, limit)

        return applicants, total

    def get_applicant_detail(self, applicant_id: int):
        applicant = ApplicantRepository.get_by_applicant_id(applicant_id)
        if not applicant:
            raise ValueError("Applicant not found")

        return applicant

    def update_status(self, applicant_id: int, new_status: str, admin_comment: str | None = None) -> bool:

        valid_statuses = [s.value for s in ApplicantStatus]

        if new_status not in valid_statuses:
            raise ValueError("Invalid status value")

        updated = ApplicantRepository.update_status(applicant_id, new_status, admin_comment)

        if not updated:
            raise ValueError("Applicant not found")

        return True

    def delete_applicant(self, applicant_id: int) -> bool:
        deleted = ApplicantRepository.delete(applicant_id)
        if not deleted:
            raise ValueError("Applicant not found")
        return True

    def export_csv(self, filters: Dict[str, Any]) -> str:

        applicants, _ = self.list_applicants(filters, page=1, limit=100000)

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "Applicant ID",
            "Full Name",
            "Email",
            "Degree",
            "Experience Years",
            "Preferred Course",
            "Status",
            "Submitted At",
        ])

        for a in applicants:
            writer.writerow([
                a.applicant_id,
                a.full_name,
                a.email,
                a.degree,
                a.experience_years,
                a.preferred_course,
                a.status,
                a.submitted_at,
            ])

        return output.getvalue()
