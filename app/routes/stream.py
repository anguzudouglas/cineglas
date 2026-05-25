from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx

from app.core.signer import verify, sign
from app.services.ytdlp_service import get_stream_url
from app.middleware.auth import verify_api_key

router = APIRouter()


# STEP 1: client hits this with x-api-key header
# returns a fully signed, ready-to-use stream_url — drop it straight into <video src>
@router.get("/watch/{youtube_id}")
def create_watch_link(
    youtube_id: str,
    request: Request,
    _=Depends(verify_api_key)
):
    token = sign(youtube_id)
    base = str(request.base_url).rstrip("/")

    return {
        "stream_url": f"{base}/api/stream/{youtube_id}?token={token}"
    }


# STEP 2: browser hits this directly via <video src="...">
# no API key needed — the signed token is the auth
@router.get("/stream/{youtube_id}")
async def stream(youtube_id: str, token: str, request: Request):

    valid_id = verify(token)

    if valid_id != youtube_id:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    data = get_stream_url(youtube_id)
    stream_url = data["url"]
    mime_type  = data.get("mime", "video/mp4")

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
        headers={"Accept-Ranges": "bytes"}
    )
