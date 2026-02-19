from backend.app.schemas.common import SuccessResponse, MessageResponse

def test_success_response_minimal():
    r = SuccessResponse(status="success")
    assert r.status == "success"
    assert r.message is None

def test_success_response_with_data():
    r = SuccessResponse(status="ok", message="done", data={"a": 1})
    assert r.data["a"] == 1

def test_message_response():
    r = MessageResponse(status="error", message="something went wrong")
    assert r.message == "something went wrong"
