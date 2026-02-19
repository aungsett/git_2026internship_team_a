import pytest
from backend.app.schemas.status import StatusUpdateRequest
from backend.app.models.enums import Status
from pydantic import ValidationError

def test_status_update_valid():
    req = StatusUpdateRequest(status=Status.Shortlisted)
    assert req.status == Status.Shortlisted

def test_status_update_invalid():
    with pytest.raises(ValidationError):
        StatusUpdateRequest(status="NotAStatus")
