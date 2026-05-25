import yt_dlp

def extract_stream(youtube_id: str):

    url = f"https://www.youtube.com/watch?v={youtube_id}"

    options = {
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(options) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

        formats = info.get("formats", [])

        video_formats = []

        for fmt in formats:

            if (
                fmt.get("ext") == "mp4"
                and fmt.get("vcodec") != "none"
                and fmt.get("url")
            ):
                video_formats.append(
                    {
                        "quality": fmt.get("height"),
                        "url": fmt.get("url")
                    }
                )

        video_formats.sort(
            key=lambda x: x["quality"] or 0,
            reverse=True
        )

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "streams": video_formats[:5]
        }
