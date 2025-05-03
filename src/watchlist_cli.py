import sys
from src.api_client import NewWorldAPIClient
from src.config import STORE_IDS
from src.watchlist_manager import add_product


def select_store():
    print("Available stores:")
    for i, name in enumerate(STORE_IDS.keys(), start=1):
        print(f"{i}. {name}")
    choice = int(input("Select store by number: ")) - 1
    return list(STORE_IDS.keys())[choice]


def search_and_add():
    store_name = select_store()
    store_id = STORE_IDS[store_name]
    client = NewWorldAPIClient(store_id)

    query = input("Enter product search query: ").strip()
    response = client.search_products(query)
    products = response.get("products", [])

    if not products:
        print("No products found.")
        return

    print("\nSearch results:")
    for i, p in enumerate(products):
        print(f"{i+1}. {p.get('name')} ({p.get('displayName')}) - ${p.get('singlePrice', {}).get('price', 0)/100:.2f}")

    index = int(input("Enter number of product to add to watchlist: ")) - 1
    selected = products[index]

    product_id = selected.get("productId")
    friendly_name = selected.get("name") + " " + selected.get("displayName", "")
    store = store_name

    target_price = input("Target price (leave blank to skip): ").strip()
    discount = input("Minimum discount % (leave blank to skip): ").strip()

    data = {
        "friendly_name": friendly_name,
        "store": store
    }
    if target_price:
        data["target_price"] = float(target_price)
    if discount:
        data["min_discount_percent"] = float(discount)

    try:
        add_product(product_id, data)
        print(f"✅ Added {friendly_name} to watchlist.")
    except ValueError as e:
        print(f"❌ {e}")


if __name__ == "__main__":
    search_and_add()
