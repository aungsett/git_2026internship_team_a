from datetime import datetime, timezone
import time
from typing import Optional, Dict, Any

from backend.app.config.firebase_auth import verify_token
from backend.app.config.settings import settings
from backend.app.repositories.admin_repository import AdminRepository

# Import DB models (AdminDocument and optional Counter)
try:
    from backend.app.models.admin import AdminDocument
except Exception:
    AdminDocument = None

try:
    from backend.app.models.counter import CounterDocument
except Exception:
    CounterDocument = None


def _generate_admin_id() -> int:
    """
    Try to atomically increment a 'admin_id' counter using CounterDocument (if available).
    Fallback to timestamp-based id (ms) if CounterDocument is absent.
    """
    if CounterDocument is not None:
        # Use modify to atomically increment and return new seq
        counter = CounterDocument.objects(name="admin_id").modify(
            upsert=True, new=True, inc__seq=1
        )
        # CounterDocument expected to have .seq attribute
        seq = getattr(counter, "seq", None)
        if seq is not None:
            return int(seq)
    # fallback (not atomic)
    return int(time.time() * 1000)


def _ensure_admin_exists(uid: str, email: Optional[str], display_name: Optional[str]) -> None:
    """
    Ensure there is an AdminDocument for this firebase uid.
    Creates a minimal AdminDocument if missing.
    """
    if AdminDocument is None:
        # No AdminDocument available (maybe tests use Pydantic Admin). Nothing to persist.
        return

    existing = AdminRepository.get_by_firebase_uid(uid)
    if existing:
        # update last_login_at
        AdminRepository.update_last_login(uid)
        return

    # create an admin record
    username = (display_name or (email.split("@")[0] if email else uid))[:50]
    admin_id = _generate_admin_id()

    admin_doc = AdminDocument(
        admin_id=admin_id,
        firebase_uid=uid,
        username=username,
        email=email or "",
        display_name=display_name,
        role="admin",
        created_at=datetime.now(timezone.utc),
        last_login_at=datetime.now(timezone.utc),
    )
    AdminRepository.create(admin_doc)


class AuthService:
    def verify_bearer_token(self, authorization_header: Optional[str]) -> Dict[str, Any]:
        """
        Verifies the Authorization header and returns the decoded Firebase token payload.
        Side-effect: creates Admin record on-first-login and updates last_login_at.

        Raises:
            ValueError with a clear message for callers to convert into 401/400 responses.
        """
        # Dev bypass
        if getattr(settings, "DISABLE_AUTH", False):
            # return a fake decoded payload for local dev
            fake = {"uid": "dev", "email": "dev@example.com", "name": "dev"}
            # ensure admin exists (no-op if AdminDocument missing)
            try:
                _ensure_admin_exists(fake["uid"], fake["email"], fake["name"])
            except Exception:
                # swallow creation errors in dev mode
                pass
            return fake

        if not authorization_header:
            raise ValueError("Missing Authorization header")

        parts = authorization_header.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            raise ValueError("Invalid Authorization header format")

        token = parts[1].strip()
        if not token:
            raise ValueError("Empty token")

        # verify with Firebase Admin SDK (verify_token wraps firebase_admin.auth.verify_id_token)
        try:
            decoded = verify_token(token)
        except Exception as e:
            # firebase_admin throws different exceptions; expose a clear message
            raise ValueError(f"Invalid token: {e}")

        # ensure admin presence & update last_login
        try:
            uid = decoded.get("uid") or decoded.get("user_id")  # handle possible keys
            email = decoded.get("email")
            name = decoded.get("name") or decoded.get("displayName")
            if uid:
                _ensure_admin_exists(uid, email, name)
        except Exception:
            # don't fail verification just because admin creation failed;
            # surface a warning later via logs (not implemented here).
            pass

        return decoded
