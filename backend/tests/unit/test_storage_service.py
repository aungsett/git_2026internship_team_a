import pytest
from app.services.storage_service import StorageService


class DummyFile:
    def __init__(self, filename):
        self.filename = filename


def test_upload_valid_pdf(monkeypatch):

    service = StorageService()
    file = DummyFile("resume.pdf")

    monkeypatch.setattr(
        "cloudinary.uploader.upload",
        lambda file, folder, resource_type: {"secure_url": "http://test.com/cv.pdf"}
    )

    url = service.upload_cv(file, 60001)

    assert "http://test.com" in url


def test_upload_invalid_file():

    service = StorageService()
    file = DummyFile("resume.exe")

    with pytest.raises(ValueError):
        service.upload_cv(file, 60001)
