from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_task():
    response = client.post("/tasks", params={"title": "Write CI tests"})
    assert response.status_code == 200
    assert response.json()["title"] == "Write CI tests"

    response = client.get("/tasks")
    assert response.status_code == 200

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "1.0.0"}

