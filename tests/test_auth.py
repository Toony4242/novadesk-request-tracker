def test_login_page_is_reachable(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_valid_login_works(client):
    response = client.post("/login", data={"email": "admin@test.local", "password": "Password123"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_invalid_login_fails(client):
    response = client.post("/login", data={"email": "admin@test.local", "password": "wrong"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Login failed" in response.data


def test_logout(client, login_as):
    login_as()
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
