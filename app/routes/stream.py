from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx

from app.core.signer import verify, sign
from app.services.ytdlp_service import get_stream_url

router = APIRouter()


# STEP 1: generate shareable link
# renamed from /watch/{youtube_id} to /token/{youtube_id} — fixes duplicate route conflict
@router.get("/token/{youtube_id}")
def create_watch_link(youtube_id: str):

    token = sign(youtube_id)

    return {
        "url": f"/api/watch/{youtube_id}?token={token}"
    }


# STEP 2: real streaming endpoint
@router.get("/watch/{youtube_id}")
async def watch(youtube_id: str, token: str, request: Request):

    valid_id = verify(token)

    if valid_id != youtube_id:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    data = get_stream_url(youtube_id)

    stream_url = data["url"]
    mime_type  = data.get("mime", "video/mp4")

    # forward Range header so browsers can seek and buffer correctly
    upstream_headers = {}
    if "range" in request.headers:
        upstream_headers["Range"] = request.headers["range"]

    async def proxy():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("GET", stream_url, headers=upstream_headers) as r:
                async for chunk in r.aiter_bytes(1024 * 512):
                    yield chunk

    return StreamingResponse(
        proxy(),
        media_type=mime_type,
        headers={
            "Accept-Ranges": "bytes",
        }
    )
