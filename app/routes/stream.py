from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse

import httpx

from app.core.limiter import limiter
from app.middleware.auth import verify_api_key
from app.services.ytdlp_service import extract_stream

router = APIRouter()


@router.get("/stream/{youtube_id}")
@limiter.limit("20/minute")
async def get_stream(
    request: Request,
    youtube_id: str,
    _: bool = Depends(verify_api_key)
):

    data = extract_stream(youtube_id)
    stream_url = data.get("stream_url")

    if not stream_url:
        raise HTTPException(status_code=404, detail="Stream not found")

    async def proxy_stream():
        headers = {}

        if "range" in request.headers:
            headers["Range"] = request.headers["range"]

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("GET", stream_url, headers=headers) as r:
                async for chunk in r.aiter_bytes(1024 * 512):
                    yield chunk

    return StreamingResponse(
        proxy_stream(),
        media_type="video/mp4",
        headers={
            "Accept-Ranges": "bytes"
        }
    )
