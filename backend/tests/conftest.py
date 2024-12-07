import pytest
import pytest_asyncio
from mongomock_motor import AsyncMongoMockClient
from httpx import AsyncClient
from main import app
import services.sensors_service

@pytest_asyncio.fixture
async def mock_db():
    client = AsyncMongoMockClient()
    return client["test_database"]

@pytest_asyncio.fixture
async def client(mock_db):
    services.sensors_service.db = mock_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
