# tests/test_routes.py


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_404_route(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    # Verify that the custom 404 page content is rendered.
    assert "홈으로 돌아가기".encode("utf-8") in response.data


def test_robots_txt(client):
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert b"User-agent: *" in response.data


def test_about_route(client):
    response = client.get("/about")
    assert response.status_code == 200


def test_api_returns_json(client):
    response = client.get("/api")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == []
