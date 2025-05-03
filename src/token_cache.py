import json
import time
from pathlib import Path

CACHE_FILE = Path(".cache/token_cache.json")
CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_cached_token() -> str | None:
    if not CACHE_FILE.exists():
        return None

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if time.time() < (data.get("expires_at", 0) - 60): # Refresh 1 minute before actual expiry
                return data.get("token")
    except Exception:
        pass  # Fail silently; fallback will trigger

    return None


def save_token(token: str, expires_at: int):
    data = {
        "token": token,
        "expires_at": expires_at
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def clear_token_cache():
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
