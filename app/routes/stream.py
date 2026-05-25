from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.middleware.auth import verify_api_key
from app.services.ytdlp_service import extract_stream

router = APIRouter()

limiter = Limiter(
    key_func=get_remote_address
)


@router.get("/stream/{youtube_id}")
@limiter.limit("20/minute")
async def get_stream(
    request: Request,
    youtube_id: str,
    _: bool = Depends(
        verify_api_key
    )
):

    return extract_stream(
        youtube_id
    )
