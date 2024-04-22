def test_login_get(client):
    """Test that the login page is accessible via GET request."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"login" in response.data