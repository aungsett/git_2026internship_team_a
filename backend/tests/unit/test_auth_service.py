import pytest
from app.services.auth_service import AuthService


def test_valid_token(monkeypatch):

    monkeypatch.setattr(
        "app.config.firebase_auth.verify_token",
        lambda token: {"uid": "123"}
    )

    service = AuthService()
    result = service.verify_admin("valid_token")

    assert result["uid"] == "123"


def test_invalid_token(monkeypatch):

    monkeypatch.setattr(
        "app.config.firebase_auth.verify_token",
        lambda token: None
    )

    service = AuthService()

    with pytest.raises(ValueError):
        service.verify_admin("invalid_token")
