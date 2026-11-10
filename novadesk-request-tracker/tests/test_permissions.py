def test_viewer_can_view_requests(client, login_as):
    login_as("viewer@test.local")
    response = client.get("/requests")
    assert response.status_code == 200
    assert b"Exact Search Title" in response.data


def test_viewer_cannot_post_edit(client, login_as):
    login_as("viewer@test.local")
    response = client.post("/requests/1/edit", data={"status": "closed", "priority": "low"})
    assert response.status_code == 403


def test_admin_can_open_edit_page(client, login_as):
    login_as("admin@test.local")
    response = client.get("/requests/1/edit")
    assert response.status_code == 200
    assert b"Edit request" in response.data
