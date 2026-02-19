from mongoengine import Document, StringField, IntField, EmailField, DateTimeField
from datetime import datetime, timezone

class Admin(Document):
    meta = {
        "collection": "admins",
        "indexes": [
            "firebase_uid",
            "email",
            "username"
        ]
    }

    admin_id = IntField(required=True, unique=True)
    firebase_uid = StringField(required=True, unique=True)
    username = StringField(required=True, unique=True, max_length=50)
    email = EmailField(required=True, unique=True)
    role = StringField(default="admin")
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    last_login_at = DateTimeField()
