from fastapi import APIRouter
from fastapi import Depends

from app.middleware.auth import verify_api_key
from app.services.ytdlp_service import extract_stream

router = APIRouter()

@router.get("/stream/{youtube_id}")
def get_stream(
    youtube_id: str,
    _: str = Depends(verify_api_key)
):

    return extract_stream(youtube_id)
