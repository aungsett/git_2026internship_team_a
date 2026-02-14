from config.database import *  
from models.applicant import Applicant
from utils.id_generator import generate_applicant_id

def test_create_and_fetch_applicant():
    applicant = Applicant(
        applicant_id=generate_applicant_id(),
        full_name="Unit Test User",
        dob="1999-12-31",
        email="unittest@example.com",
        degree="BCA",
        experience_years=0,
        preferred_course="JLPT N4",
        cv_filename="unit.pdf",
        cv_url="http://example.com/unit.pdf"
    )

    applicant.save()

    fetched = Applicant.objects(email="unittest@example.com").first()

    assert fetched is not None
    assert fetched.full_name == "Unit Test User"

    # cleanup
    fetched.delete()

def setup_function():
    Applicant.objects(email="unittest@example.com").delete()

def teardown_function():
    Applicant.objects(email="unittest@example.com").delete()
