from api_client import NewWorldAPIClient
from watchlist import WATCHLIST

def check_watchlist(client: NewWorldAPIClient) -> list[dict]:
    """
    Check all products in the WATCHLIST against target prices and discounts.
    Returns a list of products that triggered an alert.
    """
    alerts = []

    for product_id, watch_info in WATCHLIST.items():
        friendly_name = watch_info["friendly_name"]
        target_price = watch_info.get("target_price")
        min_discount_percent = watch_info.get("min_discount_percent")

        try:
            product = client.get_product_by_id(product_id)
        except Exception as e:
            print(f"Error fetching product {friendly_name}: {e}")
            continue

        reg_price_cents = product.get("singlePrice", {}).get("price")
        promo_info = product.get("promotions", [])

        if not reg_price_cents:
            print(f"Product {friendly_name} missing regular price.")
            continue

        regular_price = reg_price_cents / 100

        if not promo_info:
            print(f"No active promotion for {friendly_name}.")
            continue

        promo_price_cents = promo_info[0].get("rewardValue")
        if promo_price_cents is None:
            print(f"No promo reward value for {friendly_name}.")
            continue

        promo_price = promo_price_cents / 100

        # Check conditions
        price_triggered = target_price is not None and promo_price <= target_price
        discount_percent = ((regular_price - promo_price) / regular_price) * 100
        discount_triggered = min_discount_percent is not None and discount_percent >= min_discount_percent

        if price_triggered or discount_triggered:
            alerts.append({
                "friendly_name": friendly_name,
                "regular_price": regular_price,
                "promo_price": promo_price,
                "discount_percent": discount_percent,
                "price_triggered": price_triggered,
                "discount_triggered": discount_triggered
            })

    return alerts
