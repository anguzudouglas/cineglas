import time
import hmac
import hashlib
import os

SECRET = os.getenv("SECRET_KEY", "dev_secret")

def sign(video_id: str, expires_in: int = 3600):
    exp = int(time.time()) + expires_in
    payload = f"{video_id}:{exp}"

    sig = hmac.new(
        SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return f"{payload}:{sig}"


def verify(token: str):
    try:
        video_id, exp, sig = token.split(":")
        exp = int(exp)

        if time.time() > exp:
            return None

        payload = f"{video_id}:{exp}"

        expected = hmac.new(
            SECRET.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected, sig):
            return None

        return video_id

    except:
        return None
