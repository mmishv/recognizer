import pytest
import pytest_asyncio
from jose import jwt
from redis.asyncio import Redis

from adapters.repositories.cache_repository.redis_cache_repository import RedisCacheRepository

driver_token = "driver_token"


@pytest.fixture
def headers():
    payload = {"iss": driver_token, "roles": ["DRIVER"]}
    return {"Authorization": f"Bearer {jwt.encode(payload, 'super_secret', algorithm='HS256')}"}


@pytest.fixture
def admin_headers():
    payload = {"iss": driver_token, "roles": ["ADMIN"]}
    return {"Authorization": f"Bearer {jwt.encode(payload, 'super_secret', algorithm='HS256')}"}


@pytest_asyncio.fixture
async def cache_repository(redis_session: Redis):
    yield RedisCacheRepository(redis_session)
    await redis_session.flushdb()
