from src.api_client import NewWorldAPIClient
from src.emailer import send_alert_email  # <- make sure this accepts list of alerts
from src.watchlist_manager import load_watchlist  # <- loads from JSON file
from src.config import STORE_IDS

def run_daily_check():
    watchlist = load_watchlist()
    alerts = []
    client = NewWorldAPIClient(store_id="default")  # or inject dynamically per entry

    for product_id, watch_info in watchlist.items():
        friendly_name = watch_info["friendly_name"]
        store_name = watch_info["store"]
        target_price = watch_info.get("target_price")
        min_discount_percent = watch_info.get("min_discount_percent")

        client.store_id = STORE_IDS[store_name]  # switch store dynamically if needed

        try:
            product = client.get_product_by_id(product_id)
        except Exception as e:
            print(f"❌ Error fetching product {friendly_name}: {e}")
            continue

        reg_cents = product.get("singlePrice", {}).get("price")
        promo_info = product.get("promotions", [])
        if not reg_cents or not promo_info:
            continue

        promo_cents = promo_info[0].get("rewardValue")
        if promo_cents is None:
            continue

        regular_price = reg_cents / 100
        promo_price = promo_cents / 100
        discount_pct = ((regular_price - promo_price) / regular_price) * 100

        price_triggered = target_price is not None and promo_price <= target_price
        discount_triggered = min_discount_percent is not None and discount_pct >= min_discount_percent

        if price_triggered or discount_triggered:
            alerts.append({
                "friendly_name": friendly_name,
                "store": store_name,
                "regular_price": regular_price,
                "promo_price": promo_price,
                "discount_percent": discount_pct,
                "price_triggered": price_triggered,
                "discount_triggered": discount_triggered
            })

    if alerts:
        send_alert_email(alerts, 'placeholder')  # format and bundle in one email
    else:
        print("✅ No alerts today.")
