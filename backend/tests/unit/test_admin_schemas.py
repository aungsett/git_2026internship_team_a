from backend.app.schemas.admin import AdminListResponse, AdminDetailResponse
from backend.app.dtos.applicant_dto import ApplicantDTO
from datetime import datetime

def make_dto() -> ApplicantDTO:
    return ApplicantDTO(
        applicant_id=60001,
        full_name="Amit Sharma",
        dob="1990-01-01",
        email="amit@example.com",
        degree="B.Tech",
        experience_years=2,
        preferred_course="JLPT N4",
        location_country="IN",
        location_state="MH",
        comments=None,
        status="Pending",
        duplicate_flag=False,
        cv_filename="a.pdf",
        cv_url="https://example.com/a.pdf",
        submitted_at=datetime.utcnow(),
    )

def test_admin_list_response_valid():
    dto = make_dto()
    resp = AdminListResponse(page=1, limit=25, total=1, data=[dto])
    assert resp.data[0].email == "amit@example.com"

def test_admin_detail_response_valid():
    dto = make_dto()
    detail = AdminDetailResponse(applicant=dto)
    assert detail.applicant.applicant_id == 60001
