from typing import Any
from pydantic_settings import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    debug: bool = True
    title: str = "Recognizer Backend"
    version: str = "0.1.0"
    excluded_from_logging: list[str] = ["/healthcheck", "/"]

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {"debug": self.debug, "title": self.title, "version": self.version}



