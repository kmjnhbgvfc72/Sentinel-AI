import os

os.environ["DATABASE_URL"] = "sqlite:///./test_soar.db"
from fastapi.testclient import TestClient
from main import app
import pytest


@pytest.fixture
def client():
    with TestClient(app) as value:
        yield value
