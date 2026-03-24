import pytest

from backend.app.services.applicant_service import ApplicantService


class DummyFile:
    def __init__(self, filename):
        self.filename = filename


def test_create_application(monkeypatch):
    monkeypatch.setattr(
        "backend.app.services.applicant_service.StorageService.upload_cv",
        lambda self, file, applicant_id: "http://test.com/cv.pdf",
    )
    monkeypatch.setattr(
        "backend.app.services.applicant_service.ApplicantRepository.get_by_email",
        lambda email: None,
    )
    monkeypatch.setattr(
        "backend.app.services.applicant_service.ApplicantRepository.create",
        lambda payload: payload,
    )

    service = ApplicantService()

    data = {
        "full_name": "Test User",
        "dob": "2000-01-01",
        "email": "test@test.com",
        "degree": "B.Tech",
        "experience_years": 1,
        "preferred_course": "AI",
        "location_country": "India",
        "location_state": "Delhi",
        "comments": "test",
    }

    file = DummyFile("resume.pdf")

    result = service.create_application(data, file, 60001)

    assert result["status"] == "Pending"
    assert result["duplicate_flag"] is False
    assert result["cv_url"] == "http://test.com/cv.pdf"
    assert result["applicant_id"] == 60001
