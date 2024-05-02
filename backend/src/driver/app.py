import logging.config
from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from core.logging_filters import EndpointFilter

print(Path(__file__).parent.parent / "core/logging.conf")
logging.config.fileConfig(Path(__file__).parent.parent / "core/logging.conf", disable_existing_loggers=False)
logger = getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    user_agent_logger = logging.getLogger("uvicorn.access")
    user_agent_logger.setLevel(logging.INFO)
    console_handler = user_agent_logger.handlers[0]
    console_handler.addFilter(EndpointFilter(settings.excluded_from_logging))
    yield


app = FastAPI(**settings.fastapi_kwargs, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_methods=["*"], allow_headers=["*"], allow_origins=["*"]
)
