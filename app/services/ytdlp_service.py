import yt_dlp
from app.services.cache import stream_cache

def extract_stream(youtube_id: str):

    # return cached result if available
    if youtube_id in stream_cache:
        return stream_cache[youtube_id]

    url = f"https://www.youtube.com/watch?v={youtube_id}"

    options = {
        "quiet": True,
        "noplaylist": True,
        "format": "best[height<=1080]"
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)

    result = {
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "stream_url": info.get("url")
    }

    stream_cache[youtube_id] = result

    return result
