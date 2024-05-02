from functools import lru_cache
from core.settings import BaseSettings


@lru_cache
def get_settings() -> BaseSettings:
    return BaseSettings()


settings = get_settings()
