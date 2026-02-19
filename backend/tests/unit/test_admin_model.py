import pytest
from pydantic import ValidationError
from backend.app.models.admin import Admin

def test_admin_valid():
    a = Admin(
        firebase_uid="abc123",
        username="admin1",
        email="admin@example.com",
        role="admin",
    )
    assert a.username == "admin1"

def test_admin_invalid_email():
    with pytest.raises(ValidationError):
        Admin(
            firebase_uid="abc123",
            username="admin1",
            email="not-an-email",
            role="admin",
        )
