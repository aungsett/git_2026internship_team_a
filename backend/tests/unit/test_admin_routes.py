import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from routes.admin_routes import admin_bp


# --------------------------
# Test App Fixture
# --------------------------
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# --------------------------
# Test Create Admin
# --------------------------
@patch("routes.admin_routes.Admin")
def test_create_admin(mock_admin, client):
    mock_admin_instance = MagicMock()
    mock_admin.return_value = mock_admin_instance

    response = client.post(
        "/admin/create",
        json={
            "admin_id": 1,
            "name": "Harshit",
            "email": "harshit@test.com",
            "role": "SuperAdmin"
        }
    )

    assert response.status_code == 201
    mock_admin_instance.save.assert_called_once()


# --------------------------
# Test Get All Admins
# --------------------------
@patch("routes.admin_routes.Admin")
def test_get_all_admins(mock_admin, client):
    mock_admin.objects.return_value = [
        MagicMock(
            admin_id=1,
            name="Harshit",
            email="harshit@test.com",
            role="SuperAdmin"
        )
    ]

    response = client.get("/admin/all")

    assert response.status_code == 200
    assert isinstance(response.json, list)


# --------------------------
# Test Update Admin Status
# --------------------------
@patch("routes.admin_routes.Admin")
def test_update_admin_status(mock_admin, client):
    mock_admin_instance = MagicMock()
    mock_admin.objects.get.return_value = mock_admin_instance

    response = client.put(
        "/admin/1/status",
        json={"role": "Moderator"}
    )

    assert response.status_code == 200
    mock_admin_instance.save.assert_called_once()


# --------------------------
# Test Delete Admin
# --------------------------
@patch("routes.admin_routes.Admin")
def test_delete_admin(mock_admin, client):
    mock_admin_instance = MagicMock()
    mock_admin.objects.get.return_value = mock_admin_instance

    response = client.delete("/admin/1")

    assert response.status_code == 200
    mock_admin_instance.delete.assert_called_once()