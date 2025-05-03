# src/test_scraper.py
from src.config import STORE_IDS
from src.watcher import run_daily_check

def display_products(products: list[dict]):
    """
    Nicely print the parsed product list.
    """
    if not products:
        print("No products found.")
        return

    print(f"{'Brand':<15} {'Product Name':<50} {'Size':<10} {'Reg Price':<10} {'Promo Price':<10}")
    print("-" * 100)

    for p in products:
        brand = p.get("brand", "Unknown")
        name = p.get("name", "Unknown")
        size = p.get("size", "")
        reg_price = f"${p['regular_price']:.2f}" if p.get("regular_price") else "N/A"
        promo_price = f"${p['promo_price']:.2f}" if p.get("promo_price") else "-"
        print(f"{brand:<15} {name:<50} {size:<10} {reg_price:<10} {promo_price:<10}")


def parse_product_results(api_json: dict) -> list[dict]:
    """
    Parse the API JSON into a clean list of products.
    """
    raw_products = api_json.get("products", [])
    parsed = []

    for prod in raw_products:
        # Base price (always there)
        price_cents = prod.get("singlePrice", {}).get("price", None)
        price_dollars = price_cents / 100 if price_cents is not None else None

        # Check if there's a promotion (e.g., club deal price)
        promotions = prod.get("promotions", [])
        if promotions:
            promo_cents = promotions[0].get("rewardValue", None)
            promo_price_dollars = promo_cents / 100 if promo_cents is not None else None
        else:
            promo_price_dollars = None

        parsed.append({
            "brand": prod.get("brand", "Unknown"),
            "name": prod.get("name", "Unknown"),
            "size": prod.get("displayName", ""),
            "regular_price": price_dollars,
            "promo_price": promo_price_dollars,
            "onPromotion": bool(promotions)
        })

    return parsed

################################################################################################################################
################################################################################################################################
## Check conditions for all products in watchlist and send email

if __name__ == "__main__":
    alerts = run_daily_check()
