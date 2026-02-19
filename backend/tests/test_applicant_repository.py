import pytest
from repositories.applicant_repository import ApplicantRepository
from models.applicant import Applicant


@pytest.fixture
def repo():
    return ApplicantRepository()


@pytest.fixture
def sample_data():
    return {
        "full_name": "Repo Test User",
        "dob": "2000-01-01",
        "email": "repo_test@example.com",
        "degree": "B.Tech",
        "experience_years": 1,
        "preferred_course": "JLPT N5",
        "location_country": "India",
        "location_state": "UP",
        "comments": "Test comment",
        "cv_filename": "test.pdf",
        "cv_url": "http://example.com/test.pdf"
    }


def test_create_applicant(repo, sample_data):
    applicant = repo.create_applicant(sample_data)

    assert applicant is not None
    assert applicant.full_name == "Repo Test User"
    assert applicant.status == "Pending"

    # cleanup
    Applicant.objects(email=sample_data["email"]).delete()


def test_duplicate_email_flag(repo, sample_data):
    # First insert
    repo.create_applicant(sample_data)

    # Second insert with same email
    applicant2 = repo.create_applicant(sample_data)

    assert applicant2.duplicate_flag is True

    # cleanup
    Applicant.objects(email=sample_data["email"]).delete()


def test_find_by_id(repo, sample_data):
    applicant = repo.create_applicant(sample_data)

    fetched = repo.find_by_id(applicant.applicant_id)

    assert fetched is not None
    assert fetched.email == sample_data["email"]

    # cleanup
    Applicant.objects(email=sample_data["email"]).delete()


def test_update_status(repo, sample_data):
    applicant = repo.create_applicant(sample_data)

    updated = repo.update_status(applicant.applicant_id, "Shortlisted")

    assert updated is True

    updated_applicant = repo.find_by_id(applicant.applicant_id)
    assert updated_applicant.status == "Shortlisted"

    # cleanup
    Applicant.objects(email=sample_data["email"]).delete()


def test_list_applicants(repo, sample_data):
    repo.create_applicant(sample_data)

    results = repo.list_applicants(filters={}, page=1, limit=10)

    assert results["total"] >= 1
    assert isinstance(results["data"], list)

    # cleanup
    Applicant.objects(email=sample_data["email"]).delete()
