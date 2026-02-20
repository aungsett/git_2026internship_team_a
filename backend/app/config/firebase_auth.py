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

    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_JSON)
    firebase_admin.initialize_app(cred)
    _initialized = True


def verify_token(id_token: str) -> dict:
    init_firebase()
    return auth.verify_id_token(id_token)
