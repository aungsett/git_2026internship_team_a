# backend/app/services/applicant_service.py
from datetime import datetime, timezone
import importlib

from backend.app.repositories.applicant_repository import ApplicantRepository
from backend.app.models.counter import Counter

# IMPORTANT: resolve StorageService the same way tests monkeypatch it
try:
    storage_mod = importlib.import_module("app.services.storage_service")
except Exception:
    storage_mod = importlib.import_module("backend.app.services.storage_service")

StorageService = storage_mod.StorageService


class ApplicantService:
    def __init__(self) -> None:
        self.repo = ApplicantRepository
        self.storage = StorageService()

    def _next_applicant_id(self) -> int:
        """
        Atomically generate the next applicant_id using the 'counters' collection.
        Starts from 60000 (see Counter default) and increments by 1.
        """
        # Simple, non-conflicting strategy:
        # - If counter exists, just $inc it.
        # - If not, create it starting at 60000.
        existing = Counter.objects(name="applicant_id").first()
        if existing is None:
            created = Counter(name="applicant_id", value=60000)
            created.save()
            return int(created.value)

        updated = Counter.objects(id=existing.id).modify(new=True, inc__value=1)
        return int(updated.value)

    def create_applicant(self, data: dict, file_obj):
        """
        Create a new applicant application from parsed form data and an uploaded CV file.
        Persists applicant to MongoDB and uploads CV to Cloudinary.
        """
        applicant_id = self._next_applicant_id()
        return self.create_application(data, file_obj, applicant_id)

    def create_application(self, data: dict, file_obj, applicant_id: int):
        # duplicate email check
        existing = self.repo.get_by_email(data.get("email"))
        if existing:
            raise ValueError("Duplicate email")

        # this will now properly use monkeypatched version in tests
        cv_url = self.storage.upload_cv(file_obj, applicant_id)

        payload = {
            "applicant_id": applicant_id,
            "full_name": data.get("full_name"),
            "dob": data.get("dob"),
            "email": data.get("email"),
            "degree": data.get("degree"),
            "experience_years": int(data.get("experience_years") or 0),
            "preferred_course": data.get("preferred_course"),
            "location_country": data.get("location_country"),
            "location_state": data.get("location_state"),
            "comments": data.get("comments"),
            "status": "Pending",
            "duplicate_flag": False,
            "cv_filename": getattr(file_obj, "filename", ""),
            "cv_url": cv_url,
            "submitted_at": datetime.now(timezone.utc),
        }

        created = self.repo.create(payload)
        return created