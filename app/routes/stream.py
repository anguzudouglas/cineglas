from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx

from app.core.signer import verify, sign
from app.services.ytdlp_service import get_stream_url

router = APIRouter()


# STEP 1: generate shareable link
@router.get("/watch/{youtube_id}")
def create_watch_link(youtube_id: str):

    token = sign(youtube_id)

    return {
        "url": f"/api/watch/{youtube_id}?token={token}"
    }


# STEP 2: real streaming endpoint
@router.get("/watch/{youtube_id}")
async def watch(youtube_id: str, token: str):

    valid_id = verify(token)

    if valid_id != youtube_id:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    data = get_stream_url(youtube_id)

    stream_url = data["url"]

    async def proxy():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("GET", stream_url) as r:
                async for chunk in r.aiter_bytes(1024 * 512):
                    yield chunk

    return StreamingResponse(
        proxy(),
        media_type="video/mp4",
        headers={
            "Accept-Ranges": "bytes"
        }
    )
