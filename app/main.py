from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.stream import router as stream_router

app = FastAPI(
    title="CineGlas Stream API"
)

app.include_router(
    health_router,
    prefix="/api"
)

app.include_router(
    stream_router,
    prefix="/api"
)
