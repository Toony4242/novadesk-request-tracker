def test_requests_list_requires_login(client):
    response = client.get("/requests")
    assert response.status_code in (302, 401)


def test_requests_list_after_login(client, login_as):
    login_as()
    response = client.get("/requests")
    assert response.status_code == 200
    assert b"Exact Search Title" in response.data


def test_detail_page_for_normal_request(client, login_as):
    login_as()
    response = client.get("/requests/1")
    assert response.status_code == 200
    assert b"Exact Search Title" in response.data


def test_create_valid_request(client, login_as):
    login_as()
    response = client.post("/requests/new", data={
        "title": "New valid request",
        "description": "A clear description.",
        "customer_name": "New Customer",
        "customer_email": "new@example.test",
        "category": "general",
        "priority": "medium",
        "assigned_to_id": "",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"New valid request" in response.data


def test_search_exact_title(client, login_as):
    login_as()
    response = client.get("/requests/search?q=Exact")
    assert response.status_code == 200
    assert b"Exact Search Title" in response.data


def test_unsupported_status_is_rejected_and_logged(client, login_as, caplog):
    login_as()

    with caplog.at_level("WARNING"):
        response = client.post("/requests/1/edit", data={
            "status": "resolved",
            "priority": "medium",
            "assigned_to_id": "3",
        }, follow_redirects=True)

    assert response.status_code == 200
    assert b"status-new" in response.data
    assert "Request 1: status change to 'resolved' rejected because the status is not supported." in caplog.text

    valid_response = client.post("/requests/1/edit", data={
        "status": "closed",
        "priority": "medium",
        "assigned_to_id": "3",
    }, follow_redirects=True)

    assert valid_response.status_code == 200
    assert b"status-closed" in valid_response.data
