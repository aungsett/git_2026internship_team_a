import pytest
from pydantic import ValidationError
from backend.app.models.cv import CV

def test_cv_valid():
    cv = CV(filename="resume.pdf", url="https://example.com/resume.pdf")
    assert cv.filename.endswith(".pdf")

def test_cv_invalid_empty_filename():
    with pytest.raises(ValidationError):
        CV(filename="", url="x")
