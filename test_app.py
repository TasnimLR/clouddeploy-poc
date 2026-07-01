import pytest, json
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    r = client.get("/")
    assert json.loads(r.data)["status"] == "running"

def test_health(client):
    r = client.get("/health")
    assert json.loads(r.data)["status"] == "healthy"

def test_version(client):
    r = client.get("/version")
    assert "version" in json.loads(r.data)

def test_pipelines(client):
    r = client.get("/pipelines")
    data = json.loads(r.data)
    assert data["total"] >= 1
