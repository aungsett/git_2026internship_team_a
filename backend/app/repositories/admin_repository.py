from typing import Optional
from datetime import datetime, timezone
from backend.app.models.admin import Admin

class AdminRepository:
    @staticmethod
    def get_by_firebase_uid(firebase_uid: str) -> Optional[Admin]:
        return Admin.objects(firebase_uid=firebase_uid).first()

    @staticmethod
    def create(admin: Admin) -> Admin:
        admin.save()
        return admin

    @staticmethod
    def update_last_login(firebase_uid: str) -> bool:
        updated = Admin.objects(firebase_uid=firebase_uid).update_one(
            set__last_login_at=datetime.now(timezone.utc)
        )
        return updated == 1
