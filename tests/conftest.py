import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_database

# Fake DB (no Postgres)
class FakeDB:
    def __init__(self):
        self.items = []
    
    def add(self, item):
        item.id = len(self.items) + 1
        self.items.append(item)
        return item

    async def commit(self):
        pass
    
    async def refresh(self, item):
        return item

@pytest.fixture
def client():
    """Create test client."""
    from app.main import app
    app.dependency_overrides[get_database] = lambda: FakeDB()

    with TestClient(app) as client:
        yield client

    app.dependency_overrides = {}


@pytest.fixture
def sample_item():
    """Sample item for testing."""
    return {"name": "Test Item", "description": "Test Description", "price": 100}
