from datetime import datetime
from backend.app.services.storage_service import StorageService

class ApplicantService:
    def __init__(self):
        self.storage = StorageService()

    def create_application(self, data, file, applicant_id):
        cv_url = self.storage.upload_cv(file, applicant_id)

        return {
            "applicant_id": applicant_id,
            "full_name": data["full_name"],
            "dob": data["dob"],
            "email": data["email"],
            "degree": data["degree"],
            "experience_years": data["experience_years"],
            "preferred_course": data["preferred_course"],
            "location_country": data["location_country"],
            "location_state": data["location_state"],
            "comments": data["comments"],
            "status": "Pending",
            "duplicate_flag": False,
            "cv_filename": file.filename,
            "cv_url": cv_url,
            "submitted_at": datetime.utcnow(),
        }
