from fastapi import FastAPI

from .api.v1.api import router as api_router
from .core.config import PROJECT_NAME, API_V1_STR
from .db.mongodb_utils import close_mongo_connection, connect_to_mongo

app = FastAPI(
    title=PROJECT_NAME,
    redoc_url="/redocs"
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(api_router, prefix=API_V1_STR)