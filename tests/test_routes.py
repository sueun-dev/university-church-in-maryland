# tests/test_routes.py


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    # Check for some known content from index.html (adjust text as needed)
    assert b"Return Home" in response.data


def test_404_route(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    # Verify that the custom 404 page content is rendered.
    assert b"404 - Not Found" in response.data
