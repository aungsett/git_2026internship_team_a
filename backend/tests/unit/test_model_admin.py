import pytest
from mongoengine import connect, disconnect
from mongoengine.errors import NotUniqueError, ValidationError
from app.models.admin import Admin

# Setup test DB
connect("mongoenginetest", host="mongodb://localhost/mongoenginetest")

def teardown_module(module):
    Admin.drop_collection()
    disconnect()

def test_create_admin():
    admin = Admin(
        full_name="Test Admin",
        email="admin@test.com",
        password_hash="hashed123",
        role="superadmin"
    )
    admin.save()

    assert admin.email == "admin@test.com"
    assert admin.role == "superadmin"

def test_duplicate_email():
    Admin(
        full_name="Admin1",
        email="dup@test.com",
        password_hash="hash",
        role="reviewer"
    ).save()

    with pytest.raises(NotUniqueError):
        Admin(
            full_name="Admin2",
            email="dup@test.com",
            password_hash="hash",
            role="reviewer"
        ).save()

def test_invalid_role():
    with pytest.raises(ValidationError):
        Admin(
            full_name="Invalid Role",
            email="role@test.com",
            password_hash="hash",
            role="manager"  # not allowed
        ).save()
