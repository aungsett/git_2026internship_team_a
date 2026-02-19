import pytest
from backend.app.schemas.apply import ApplyRequest
from backend.app.utils.constants import MAX_UPLOAD_SIZE

def test_apply_valid():
    req = ApplyRequest(
        full_name="Amit Sharma",
        dob="1990-01-01",
        email="amit@example.com",
        degree="B.Tech",
        experience_years=2,
        preferred_course="JLPT N4",
        cv_filename="resume.pdf",
        cv_size=1024
    )
    assert req.email == "amit@example.com"

@pytest.mark.parametrize("dob", ["1990-13-01", "01-01-1990", "19900202"])
def test_apply_invalid_dob(dob):
    with pytest.raises(ValueError):
        ApplyRequest(
            full_name="A",
            dob=dob,
            email="a@b.com",
            degree="X",
            experience_years=1,
            preferred_course="P",
            cv_filename="r.pdf",
            cv_size=100
        )

def test_apply_negative_experience():
    with pytest.raises(ValueError):
        ApplyRequest(
            full_name="A",
            dob="1990-01-01",
            email="a@b.com",
            degree="X",
            experience_years=-1,
            preferred_course="P",
            cv_filename="r.pdf",
            cv_size=100
        )

def test_apply_invalid_extension():
    with pytest.raises(ValueError):
        ApplyRequest(
            full_name="A",
            dob="1990-01-01",
            email="a@b.com",
            degree="X",
            experience_years=1,
            preferred_course="P",
            cv_filename="resume.exe",
            cv_size=100
        )

def test_apply_oversize():
    with pytest.raises(ValueError):
        ApplyRequest(
            full_name="A",
            dob="1990-01-01",
            email="a@b.com",
            degree="X",
            experience_years=1,
            preferred_course="P",
            cv_filename="r.pdf",
            cv_size=MAX_UPLOAD_SIZE + 1
        )
