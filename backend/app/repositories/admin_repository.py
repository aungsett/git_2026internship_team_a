from typing import Optional
from datetime import datetime, timezone
from backend.app.models.admin import AdminDocument

class AdminRepository:
    @staticmethod
    def get_by_firebase_uid(firebase_uid: str) -> Optional[AdminDocument]:
        return AdminDocument.objects(firebase_uid=firebase_uid).first()

    @staticmethod
    def create(admin: AdminDocument) -> AdminDocument:
        admin.save()
        return admin

    @staticmethod
    def update_last_login(firebase_uid: str) -> bool:
        updated = AdminDocument.objects(firebase_uid=firebase_uid).update_one(
            set__last_login_at=datetime.now(timezone.utc)
        )
        return updated == 1