"""Health endpoint tests."""

import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Health endpoint returns 200."""
    rv = client.get("/health")
    assert rv.status_code == 200
    assert b"healthy" in rv.data


def test_api_health_endpoint(client):
    """API health endpoint returns 200."""
    rv = client.get("/api/v1/health")
    assert rv.status_code == 200
