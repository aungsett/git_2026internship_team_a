from backend.app.config.settings import settings
import firebase_admin
from firebase_admin import credentials, auth

_initialized = False

def init_firebase():
    global _initialized
    if _initialized:
        return

    if not settings.FIREBASE_CREDENTIALS_JSON:
        raise RuntimeError("FIREBASE_CREDENTIALS_JSON not set")

    cred_path = settings.FIREBASE_CREDENTIALS_JSON
    cred = credentials.Certificate(cred_path)

    # In dev it’s common to switch Firebase projects; if an app is already
    # initialized, re-initialize only when the project_id differs.
    try:
        app = firebase_admin.get_app()
        try:
            current_project_id = app.credential.project_id  # type: ignore[attr-defined]
        except Exception:
            current_project_id = None

        try:
            desired_project_id = cred.project_id  # type: ignore[attr-defined]
        except Exception:
            desired_project_id = None

        if current_project_id and desired_project_id and current_project_id != desired_project_id:
            firebase_admin.delete_app(app)
            firebase_admin.initialize_app(cred)
    except ValueError:
        # No default app exists yet
        firebase_admin.initialize_app(cred)
    _initialized = True


def verify_token(id_token: str) -> dict:
    init_firebase()
    return auth.verify_id_token(id_token)
