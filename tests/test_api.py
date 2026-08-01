import os
import tempfile

# Use a temporary SQLite database for tests.
db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
db_file.close()
os.environ["DATABASE_URL"] = f"sqlite:///{db_file.name}"
os.environ["AWS_REGION"] = "test-region"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_and_list_user():
    email = "test-user@example.com"

    create_response = client.post(
        "/users",
        json={"name": "Test User", "email": email},
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == "Test User"

    list_response = client.get("/users")
    assert list_response.status_code == 200
    assert any(user["email"] == email for user in list_response.json())
