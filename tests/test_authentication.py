# tests/test_authentication.py

from app.config import Config


def test_upload_get_renders_page(client):
    response = client.get("/upload")
    assert response.status_code == 200


def test_upload_post_without_auth_redirects_to_login(client):
    response = client.post("/upload", data={})
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_with_valid_credentials(client):
    response = client.post(
        "/login",
        data={"username": Config.USERNAME, "password": "password"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert sess.get("is_pastor") is True


def test_login_with_invalid_credentials(client):
    response = client.post(
        "/login",
        data={"username": "wrong", "password": "wrong"},
        follow_redirects=False,
    )
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess.get("is_pastor") is None
