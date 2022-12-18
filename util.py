import os
import json

CACHE_PATH = "cache/cache.json"

# Create cache directory if not exists
os.makedirs("cache", exist_ok=True)

def get_cache() -> dict:
    """
    Retrieve cache dict from file if exists.
    Otherwise return None.
    """
    try:
        f = open(CACHE_PATH, mode="r")
        cache = json.load(f)
        f.close()
    except FileNotFoundError:
        cache = None
    return cache

def set_cache(cache: dict):
    """
    Completely replace cache file with input dict.
    """
    f = open(CACHE_PATH, mode="w")
    json.dump(cache, f)
    f.close()
