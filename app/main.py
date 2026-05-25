from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler

from fastapi.middleware.cors import CORSMiddleware

from app.core.limiter import limiter
from app.config import FRONTEND_URL

from app.routes.health import router as health_router
from app.routes.stream import router as stream_router

app = FastAPI(
    title="CineGlas API",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allows <video> tags from any origin
    allow_credentials=False,    # must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(stream_router, prefix="/api")
