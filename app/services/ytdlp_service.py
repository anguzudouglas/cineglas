import yt_dlp
from app.services.cache import stream_cache

def get_stream_url(video_id: str):

    if video_id in stream_cache:
        return stream_cache[video_id]

    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "quiet": True,
        "format": "best[height<=1080]",
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    stream = {
        "url": info["url"],
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail")
    }

    stream_cache[video_id] = stream
    return stream
