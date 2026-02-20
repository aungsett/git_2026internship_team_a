# backend/app/services/auth_service.py
from typing import Optional, Dict, Any
import importlib
from backend.app.config.settings import settings
from backend.app.repositories.admin_repository import AdminRepository
from backend.app.models.admin import AdminDocument
from datetime import datetime, timezone

# Helper: ensure admin record exists (no-op if AdminDocument missing)
def _ensure_admin_exists(uid: str, email: Optional[str], display_name: Optional[str]) -> None:
    if AdminDocument is None:
        return
    existing = AdminRepository.get_by_firebase_uid(uid)
    if existing:
        AdminRepository.update_last_login(uid)
        return
    admin_doc = AdminDocument(
        admin_id=1,  # replace with atomic counter if available
        firebase_uid=uid,
        username=(display_name or (email or uid).split("@")[0])[:50],
        email=email or "",
        display_name=display_name,
        role="admin",
        created_at=datetime.now(timezone.utc),
        last_login_at=datetime.now(timezone.utc),
    )
    AdminRepository.create(admin_doc)


class AuthService:
    """
    verify_admin(token)  -> verify raw token string (used by unit tests)
    verify_bearer_token(header) -> verify Authorization header (used by routes)
    """

    def _resolve_firebase_module(self):
        # prefer 'app.config.firebase_auth' so unit tests that monkeypatch that path are honored.
        try:
            return importlib.import_module("app.config.firebase_auth")
        except Exception:
            from backend.app.config import firebase_auth as fb_mod  # type: ignore
            return fb_mod

    def verify_admin(self, token: str) -> Dict[str, Any]:
        if getattr(settings, "DISABLE_AUTH", False):
            fake = {"uid": "dev", "email": "dev@example.com", "name": "dev"}
            try:
                _ensure_admin_exists(fake["uid"], fake["email"], fake["name"])
            except Exception:
                pass
            return fake

        if not token:
            raise ValueError("Missing token")

        firebase_auth_module = self._resolve_firebase_module()

        try:
            decoded = firebase_auth_module.verify_token(token)
        except Exception as e:
            raise ValueError(f"Invalid token: {e}")

        if not decoded:
            raise ValueError("Invalid token")

        try:
            uid = decoded.get("uid") or decoded.get("user_id")
            email = decoded.get("email")
            name = decoded.get("name") or decoded.get("displayName")
            if uid:
                _ensure_admin_exists(uid, email, name)
        except Exception:
            pass

        return decoded

    def verify_bearer_token(self, authorization_header: Optional[str]) -> Dict[str, Any]:
        if not authorization_header:
            raise ValueError("Missing Authorization header")
        parts = authorization_header.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            raise ValueError("Invalid Authorization header format")
        token = parts[1].strip()
        return self.verify_admin(token)
