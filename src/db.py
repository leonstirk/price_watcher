import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Initialize the DynamoDB resource
dynamodb = boto3.resource("dynamodb")

# Tables
tbl_users = dynamodb.Table("users")
tbl_products = dynamodb.Table("products")
tbl_watchlist = dynamodb.Table("watchlist")


def create_user(user_id: str, email: str, stores: list[str]) -> None:
    tbl_users.put_item(
        Item={
            "user_id": user_id,
            "email": email,
            "stores": stores,
        }
    )


def get_user(user_id: str) -> dict:
    response = tbl_users.get_item(Key={"user_id": user_id})
    return response.get("Item")


def add_product(product_id: str, metadata: dict) -> None:
    tbl_products.put_item(
        Item={
            "product_id": product_id,
            **metadata,
        }
    )


def get_product(product_id: str) -> dict:
    response = tbl_products.get_item(Key={"product_id": product_id})
    return response.get("Item")


def add_product_to_watchlist(user_id: str, product_id: str, target_price: float = None, min_discount_percent: float = None) -> None:
    item = {
        "user_id": user_id,
        "product_id": product_id,
    }
    if target_price is not None:
        item["target_price"] = Decimal(str(target_price))
    if min_discount_percent is not None:
        item["min_discount_percent"] = Decimal(str(min_discount_percent))

    tbl_watchlist.put_item(Item=item)


def get_user_watchlist(user_id: str) -> list[dict]:
    response = tbl_watchlist.query(
        KeyConditionExpression=Key("user_id").eq(user_id)
    )
    return response.get("Items", [])
