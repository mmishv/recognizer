from driver import healthcheck
from driver.error_handlers.handlers_list import app
from driver.v1.recognizer import router as recognizer


app.include_router(healthcheck.router, tags=["Healthcheck"])
app.include_router(recognizer, tags=["Recognizer"])
