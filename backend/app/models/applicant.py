from mongoengine import (
    Document,
    StringField,
    IntField,
    BooleanField,
    DateTimeField,
    EmailField,
    ReferenceField
)
from datetime import datetime, timezone

class Applicant(Document):
    meta = {
        "collection": "applicants",
        "indexes": [
            "email",
            "status",
            "submitted_at",
            "degree",
            "preferred_course",
            "experience_years"
        ]
    }

    applicant_id = IntField(required=True, unique=True)
    full_name = StringField(required=True, max_length=100)
    dob = StringField(required=True)
    email = EmailField(required=True)
    degree = StringField(required=True)
    experience_years = IntField(required=True, min_value=0)
    preferred_course = StringField(required=True)

    location_country = StringField()
    location_state = StringField()
    comments = StringField()

    status = StringField(
        default="Pending",
        choices=[
            "Pending",
            "Reviewed",
            "Shortlisted",
            "Accepted",
            "Rejected"
        ]
    )
    updated_by = ReferenceField("Admin", null=True)

    duplicate_flag = BooleanField(default=False)

    cv_filename = StringField(required=True)
    cv_url = StringField(required=True)

    submitted_at = DateTimeField(default=lambda: datetime.now(timezone.utc))