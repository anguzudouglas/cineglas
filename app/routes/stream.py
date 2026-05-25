from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse

import httpx

from app.middleware.auth import verify_api_key
from app.services.ytdlp_service import extract_stream
from app.main import limiter

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

        # IMPORTANT: enables seeking / scrubbing
        if "range" in request.headers:
            headers["Range"] = request.headers["range"]

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("GET", stream_url, headers=headers) as r:

                # pass through correct status (200 or 206 for partial content)
                status_code = r.status_code

                async def generate():
                    async for chunk in r.aiter_bytes(1024 * 512):
                        yield chunk

                return StreamingResponse(
                    generate(),
                    status_code=status_code,
                    headers={
                        "Content-Type": r.headers.get("content-type", "video/mp4"),
                        "Accept-Ranges": "bytes",
                        "Content-Disposition": f'inline; filename="{data.get("title","video")}.mp4"'
                    }
                )

    return await proxy_stream()
