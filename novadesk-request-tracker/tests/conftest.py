import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from app import create_app, db
from app.models import SupportRequest, User
from config import TestingConfig


@pytest.fixture()
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        admin = User(name="Test Admin", email="admin@test.local", role="admin", active=True)
        admin.set_password("Password123")
        viewer = User(name="Test Viewer", email="viewer@test.local", role="viewer", active=True)
        viewer.set_password("Password123")
        agent = User(name="Test Agent", email="agent@test.local", role="agent", active=True)
        agent.set_password("Password123")
        db.session.add_all([admin, viewer, agent])
        db.session.flush()
        db.session.add(SupportRequest(
            title="Exact Search Title",
            description="A normal test request.",
            customer_name="Example Customer",
            customer_email="customer@example.test",
            category="general",
            priority="medium",
            status="new",
            assigned_to_id=agent.id,
        ))
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def login_as(client):
    def _login(email="admin@test.local", password="Password123"):
        return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)
    return _login
