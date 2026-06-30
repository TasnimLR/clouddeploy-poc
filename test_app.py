import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_contains_app_name(client):
    response = client.get("/")
    data = response.get_json()
    assert data["app"] == "CloudPilot AI"
    assert data["status"] == "running"


def test_health_returns_healthy(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_version_endpoint(client):
    response = client.get("/version")
    assert response.status_code == 200
    data = response.get_json()
    assert "version" in data
    assert "deployed_at" in data


def test_pipelines_returns_list(client):
    response = client.get("/pipelines")
    assert response.status_code == 200
    data = response.get_json()
    assert "pipelines" in data
    assert len(data["pipelines"]) > 0
    assert data["total"] == len(data["pipelines"])
