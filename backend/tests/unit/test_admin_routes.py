import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from backend.app.routes.admin_routes import bp


# -----------------------------------
# Test App Fixture
# -----------------------------------
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# -----------------------------------
# Helper: Mock Auth Success
# -----------------------------------
def mock_auth_success(mock_auth):
    mock_auth.return_value.verify_bearer_token.return_value = {"admin_id": 1}


# -----------------------------------
# Test: Ping
# -----------------------------------
@patch("backend.app.routes.admin_routes.AuthService")
def test_ping(mock_auth, client):
    mock_auth_success(mock_auth)

    response = client.get(
        "/admin/ping",
        headers={"Authorization": "Bearer testtoken"},
    )

    assert response.status_code == 200
    assert response.json["status"] == "ok"


# -----------------------------------
# Test: List Applicants
# -----------------------------------
@patch("backend.app.routes.admin_routes.AdminService")
@patch("backend.app.routes.admin_routes.AuthService")
def test_list_applicants(mock_auth, mock_service, client):
    mock_auth_success(mock_auth)

    mock_service.return_value.list_applicants.return_value = ([], 0)

    response = client.get(
        "/admin/applicants",
        headers={"Authorization": "Bearer testtoken"},
    )

    assert response.status_code == 200
    assert response.json["data"] == []
    assert response.json["total"] == 0


# -----------------------------------
# Test: Get Single Applicant
# -----------------------------------
@patch("backend.app.routes.admin_routes.AdminService")
@patch("backend.app.routes.admin_routes.AuthService")
def test_get_applicant(mock_auth, mock_service, client):
    mock_auth_success(mock_auth)

    # Plain values only: unset MagicMock attributes are nested mocks and break jsonify().
    fake_applicant = MagicMock()
    fake_applicant.applicant_id = 1
    fake_applicant.full_name = "Harshit"
    fake_applicant.email = "harshit@test.com"
    fake_applicant.dob = None
    fake_applicant.degree = "B.Tech"
    fake_applicant.experience_years = 2
    fake_applicant.preferred_course = "Backend"
    fake_applicant.location_country = None
    fake_applicant.location_state = None
    fake_applicant.status = "Pending"
    fake_applicant.submitted_at = None
    fake_applicant.cv_filename = None
    fake_applicant.cv_url = "http://example.com/cv.pdf"
    fake_applicant.comments = None
    fake_applicant.review_comment = None

    mock_service.return_value.get_applicant_detail.return_value = fake_applicant

    response = client.get(
        "/admin/applicants/1",
        headers={"Authorization": "Bearer testtoken"},
    )

    assert response.status_code == 200
    assert response.json["applicant_id"] == 1


# -----------------------------------
# Test: Update Applicant Status
# -----------------------------------
@patch("backend.app.routes.admin_routes.AdminService")
@patch("backend.app.routes.admin_routes.AuthService")
def test_update_status(mock_auth, mock_service, client):
    mock_auth_success(mock_auth)

    response = client.put(
        "/admin/applicants/1/status",
        json={"status": "Approved"},
        headers={"Authorization": "Bearer testtoken"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Status updated successfully"


# -----------------------------------
# Test: Export CSV
# -----------------------------------
@patch("backend.app.routes.admin_routes.AdminService")
@patch("backend.app.routes.admin_routes.AuthService")
def test_export_csv(mock_auth, mock_service, client):
    mock_auth_success(mock_auth)

    mock_service.return_value.export_csv.return_value = "id,name\n1,Harshit"

    response = client.get(
        "/admin/export/csv",
        headers={"Authorization": "Bearer testtoken"},
    )

    assert response.status_code == 200
    assert response.mimetype == "text/csv"