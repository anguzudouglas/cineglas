from cachetools import TTLCache

stream_cache = TTLCache(
    maxsize=500,
    ttl=1800
)
