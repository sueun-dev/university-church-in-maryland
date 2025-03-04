# tests/test_exceptions.py

from app.exceptions import InvalidUsage


def test_invalid_usage_exception_to_dict():
    exc = InvalidUsage("Test error", status_code=418, payload={"foo": "bar"})
    error_dict = exc.to_dict()
    assert error_dict["error"] == "Test error"
    assert error_dict["foo"] == "bar"
    assert exc.status_code == 418


def test_invalid_usage_error_handler(client):
    # Dynamically add a route that raises an InvalidUsage exception.
    @client.application.route("/raise")
    def raise_error():
        from app.exceptions import InvalidUsage

        raise InvalidUsage("Simulated error", status_code=418)

    response = client.get("/raise")
    assert response.status_code == 418
    # If the error is returned as JSON, check the content.
    data = response.get_json()
    assert data["error"] == "Simulated error"
