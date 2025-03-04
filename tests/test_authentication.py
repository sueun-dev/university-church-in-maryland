# tests/test_authentication.py

import base64
from app.config import Config


def get_basic_auth_header(username, password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode("utf-8")
    return {"Authorization": f"Basic {encoded_credentials}"}


def test_upload_requires_auth(client):
    response = client.post("/upload", data={})
    # Without auth, expect a 401 Unauthorized response.
    assert response.status_code == 401
    assert b"Authentication Required" in response.data


def test_upload_with_auth(client):
    # Provide correct credentials (adjust password if necessary)
    headers = get_basic_auth_header(Config.USERNAME, "password")
    # Simulate file upload (using dummy content)
    data = {"file_input": (b"dummy file content", "test.pdf")}
    response = client.post(
        "/upload", data=data, headers=headers, content_type="multipart/form-data"
    )
    # The response may be a 200 (or a redirect) depending on your route logic.
    assert response.status_code in (200, 302)


def test_blocked_ip(client):
    # Simulate several failed attempts to trigger the IP block.
    headers = {}  # No Authorization header.
    for _ in range(Config.MAX_ATTEMPTS):
        client.post("/upload", data={}, headers=headers)
    response = client.post("/upload", data={}, headers=headers)
    # After exceeding MAX_ATTEMPTS, expect a 403 Forbidden response.
    assert response.status_code == 403
    assert b"Your IP is blocked" in response.data
