from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.stream import router as stream_router
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vm-6xmqn0bzgaas1u3u1v8w1g49.vusercontent.net"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
