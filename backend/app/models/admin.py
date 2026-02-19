from mongoengine import (
    Document,
    StringField,
    EmailField,
    DateTimeField,
    BooleanField
)
from datetime import datetime, timezone

class Admin(Document):
    meta = {
        "collection": "admins",
        "indexes": [
            "email",
            "role",
            "is_active"
        ]
    }

    full_name = StringField(required=True, max_length=100)

    email = EmailField(required=True, unique=True)

    password_hash = StringField(required=True)

    role = StringField(
        required=True,
        choices=["superadmin", "reviewer"],
        default="reviewer"
    )

    is_active = BooleanField(default=True)

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    last_login = DateTimeField()
