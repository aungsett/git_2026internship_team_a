import pytest
from backend.app.utils.validators import validate_cv_filename, validate_cv_size
from backend.app.utils.constants import MAX_UPLOAD_SIZE

def test_validate_cv_filename_ok():
    assert validate_cv_filename("resume.PDF") == "resume.PDF"
    assert validate_cv_filename("a.docx") == "a.docx"

@pytest.mark.parametrize("fname", ["noext", "file.exe", "badfile.bmp"])
def test_validate_cv_filename_bad(fname):
    with pytest.raises(ValueError):
        validate_cv_filename(fname)

def test_validate_cv_size_ok():
    assert validate_cv_size(0) == 0
    assert validate_cv_size(1024) == 1024

def test_validate_cv_size_negative():
    with pytest.raises(ValueError):
        validate_cv_size(-1)

def test_validate_cv_size_oversize():
    with pytest.raises(ValueError):
        validate_cv_size(MAX_UPLOAD_SIZE + 1)
