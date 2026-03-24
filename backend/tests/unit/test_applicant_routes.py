import pytest
from io import BytesIO
from flask import Flask
from unittest.mock import patch, MagicMock


# ---------------------------------------
# Test Client Fixture
# ---------------------------------------
@pytest.fixture
def client():
    from backend.app.routes.applicant_routes import applicant_bp

    app = Flask(__name__)
    app.register_blueprint(applicant_bp)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# ---------------------------------------
# Test Successful Submission
# ---------------------------------------
@patch("backend.app.routes.applicant_routes.ApplicantService")
def test_create_applicant_success(mock_service, client):
    mock_instance = MagicMock()
    mock_instance.create_applicant.return_value = MagicMock(applicant_id=1)
    mock_service.return_value = mock_instance

    # Route requires multipart + CV (JSON-only is rejected with 400).
    response = client.post(
        "/applicants",
        data={
            "full_name": "Harshit",
            "dob": "2000-01-01",
            "email": "harshit@test.com",
            "degree": "B.Tech",
            "experience_years": "2",
            "preferred_course": "AI",
            "cv": (BytesIO(b"%PDF-1.4 fake"), "resume.pdf"),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 201
    assert response.json["message"] == "Application submitted successfully"
    assert response.json["application_id"] == 1


# ---------------------------------------
# Test Missing Body
# ---------------------------------------
def test_create_applicant_no_body(client):
    response = client.post("/applicants")

    assert response.status_code == 400
    assert "error" in response.json


# ---------------------------------------
# Test Validation Error
# ---------------------------------------
@patch("backend.app.routes.applicant_routes.ApplicantService")
def test_create_applicant_validation_error(mock_service, client):
    response = client.post(
        "/applicants",
        json={
            "full_name": "Harshit",
            "dob": "invalid-date",
            "email": "wrong-email",
            "degree": "B.Tech",
            "experience_years": -1,
            "preferred_course": "AI"
        }
    )

    assert response.status_code == 400
    assert "error" in response.json


# ---------------------------------------
# Test Internal Server Error
# ---------------------------------------
@patch("backend.app.routes.applicant_routes.ApplicantService")
def test_create_applicant_internal_error(mock_service, client):
    mock_instance = MagicMock()
    mock_instance.create_applicant.side_effect = Exception("DB error")
    mock_service.return_value = mock_instance

    response = client.post(
        "/applicants",
        data={
            "full_name": "Harshit",
            "dob": "2000-01-01",
            "email": "harshit@test.com",
            "degree": "B.Tech",
            "experience_years": "2",
            "preferred_course": "AI",
            "cv": (BytesIO(b"%PDF-1.4 fake"), "resume.pdf"),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 500
    assert "error" in response.json