import pytest_asyncio
from httpx import AsyncClient

from core.config import get_settings
from core.settings import TestSettings
from driver.main import app


@pytest_asyncio.fixture(scope="session")
async def async_client():
    settings = TestSettings()
    app.dependency_overrides[get_settings] = lambda: settings
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
