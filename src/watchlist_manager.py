import json
from pathlib import Path

WATCHLIST_PATH = Path("data/watchlist.json")

### Core I/O Functions ###

def load_watchlist() -> dict:
    if WATCHLIST_PATH.exists():
        with open(WATCHLIST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_watchlist(data: dict) -> None:
    with open(WATCHLIST_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


### CRUD Operations ###

def add_product(product_id: str, data: dict) -> None:
    watchlist = load_watchlist()
    if product_id in watchlist:
        raise ValueError(f"Product ID {product_id} already in watchlist.")
    watchlist[product_id] = data
    save_watchlist(watchlist)


def remove_product(product_id: str) -> bool:
    watchlist = load_watchlist()
    if product_id in watchlist:
        del watchlist[product_id]
        save_watchlist(watchlist)
        return True
    return False


def update_product(product_id: str, field: str, value) -> bool:
    watchlist = load_watchlist()
    if product_id in watchlist:
        watchlist[product_id][field] = value
        save_watchlist(watchlist)
        return True
    return False


def list_watchlist() -> list[dict]:
    watchlist = load_watchlist()
    return [
        {"product_id": pid, **details} for pid, details in watchlist.items()
    ]


def get_product(product_id: str) -> dict:
    watchlist = load_watchlist()
    return watchlist.get(product_id, {})
