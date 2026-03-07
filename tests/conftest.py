import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """
    Creates test client and ensures lifespan events run.
    """
    with TestClient(app) as c:
        yield c