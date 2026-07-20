import os

os.environ["DATABASE_URL"] = "sqlite:///./test_threat_intelligence.db"
os.environ["DEMO_DATA_ENABLED"] = "false"
os.environ["FEED_SCHEDULER_ENABLED"] = "false"

import pytest
from fastapi.testclient import TestClient

from database.connection import Base, engine
from main import app


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
