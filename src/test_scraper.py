import json
from config import STORE_IDS
from api_client import NewWorldAPIClient
from watcher import check_watchlist

# src/test_scraper.py

from api_client import NewWorldAPIClient
from config import STORE_IDS

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
## Friendly text product search

# if __name__ == "__main__":
#     store_name = "Dunedin"
#     store_id = STORE_IDS[store_name]

#     client = NewWorldAPIClient(store_id=store_id)

#     query = "aveeno conditioner"
#     response_json = client.search_products(search_query=query)

#     # with open("products_dump.json", "w", encoding="utf-8") as f:
#     #     json.dump(response_json, f, indent=2, ensure_ascii=False)

#     products = parse_product_results(response_json)

#     display_products(products)

################################################################################################################################
################################################################################################################################
## Individual product search

# if __name__ == "__main__":
#     store_name = "Chaffers"
#     store_id = STORE_IDS[store_name]

#     client = NewWorldAPIClient(store_id=store_id)

#     product_id = "5283196-EA-000"  # Example Aveeno product

#     product = client.get_product_by_id(product_id)
#     print(product)


################################################################################################################################
################################################################################################################################
## Check conditions for all products in watchlist

# if __name__ == "__main__":
#     store_name = "Dunedin"
#     store_id = STORE_IDS[store_name]

#     client = NewWorldAPIClient(store_id=store_id)

#     alerts = check_watchlist(client)

#     if alerts:
#         for alert in alerts:
#             print(f"🚨 {alert['friendly_name']}: Now ${alert['promo_price']:.2f} ({alert['discount_percent']:.1f}% off)")
#     else:
#         print("No promotions meeting alert conditions today.")

################################################################################################################################
################################################################################################################################
## Check conditions for all products in watchlist and send email

from emailer import send_alert_email

if __name__ == "__main__":
    store_name = "Dunedin"
    store_id = STORE_IDS[store_name]
    client = NewWorldAPIClient(store_id=store_id)

    alerts = check_watchlist(client)

    send_alert_email(alerts)
