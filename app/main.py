from fastapi import FastAPI

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from fastapi.middleware.cors import CORSMiddleware

from app.config import FRONTEND_URL

from app.routes.health import router as health_router
from app.routes.stream import router as stream_router

app = FastAPI(
    title="CineGlas API",
    version="1.0.0"
)

limiter = Limiter(
    key_func=get_remote_address
)

app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    health_router,
    prefix="/api"
)

app.include_router(
    stream_router,
    prefix="/api"
)
