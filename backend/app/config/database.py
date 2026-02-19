# backend/app/config/database.py
from mongoengine import connect, disconnect
from typing import Optional
from backend.app.config.settings import settings

_mongo_conn = None

def init_db(alias: str = "default", **connect_kwargs) -> None:
    """
    Initialize MongoEngine connection using MONGODB_URI from settings.
    Call this once at app startup.
    """
    global _mongo_conn
    if _mongo_conn:
        return

    uri = settings.MONGODB_URI
    # Allow callers to override connect kwargs (e.g., connect(host=uri, alias=alias))
    _mongo_conn = connect(host=uri, alias=alias, **connect_kwargs)

def close_db() -> None:
    """Disconnect mongoengine (useful for tests/shutdown)."""
    disconnect()
