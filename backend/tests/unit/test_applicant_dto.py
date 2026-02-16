from backend.app.dtos.applicant_dto import ApplicantDTO
from datetime import datetime

def test_dto_from_to_dict():
    d = {
        "applicant_id": 60001,
        "full_name": "A",
        "dob": "1990-01-01",
        "email": "a@b.com",
        "degree": "X",
        "experience_years": 1,
        "preferred_course": "P",
        "submitted_at": datetime.utcnow().isoformat()
    }
    dto = ApplicantDTO.from_dict(d)
    out = dto.to_dict()
    assert isinstance(out["submitted_at"], str)
    assert out["email"] == "a@b.com"
