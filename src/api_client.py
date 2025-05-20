# src/api_client.py

import asyncio
import json
import time
import jwt
from typing import Optional

from src.token_extractor import get_bearer_token
from src.token_cache import load_cached_token, save_token

class NewWorldAPIClient:
    def __init__(self, store_id: str):
        self.store_id = store_id
        self.base_url = "https://api-prod.newworld.co.nz/v1/edge"
        self.token = self.get_token()

    def get_token(self) -> str:
        cached_token = load_cached_token()
        if cached_token:
            print("🔄 Using cached token...")
            return cached_token

        print("🔄 No valid cached token found, fetching a new one...")
        fresh_token = asyncio.run(get_bearer_token())
        expiry = self._decode_expiry(fresh_token)
        save_token(fresh_token, expiry)
        return fresh_token

    def _decode_expiry(self, token: str) -> int:
        try:
            payload = jwt.decode(token.split()[1], options={"verify_signature": False})
            return payload.get("exp", int(time.time()) + 600)
        except Exception:
            return int(time.time()) + 600

    def search_products(self, query: str, page: int = 0, hits: int = 50) -> dict:
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
        }
        body = {
            "algoliaQuery": {
                "attributesToHighlight": [],
                "attributesToRetrieve": [
                    "productID", "Type", "sponsored", "category0SI", "category1SI", "category2SI"
                ],
                "facets": ["brand", "category1SI", "onPromotion", "productFacets", "tobacco"],
                "filters": f"stores:{self.store_id}",
                "highlightPostTag": "__/ais-highlight__",
                "highlightPreTag": "__ais-highlight__",
                "hitsPerPage": hits,
                "maxValuesPerFacet": 100,
                "page": page,
                "query": query,
                "analyticsTags": ["fs#WEB:desktop"]
            },
            "algoliaFacetQueries": [],
            "storeId": self.store_id,
            "hitsPerPage": hits,
            "page": page,
            "sortOrder": "SI_POPULARITY_ASC",
            "tobaccoQuery": True,
            "precisionMedia": {
                "adDomain": "SEARCH_PAGE",
                "adPositions": [4, 8, 12, 16],
                "publishImpressionEvent": False,
                "disableAds": False
            }
        }

        import requests
        url = f"{self.base_url}/search/paginated/products"
        response = requests.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch products: {response.status_code}, {response.text}")

        return response.json()

    def get_product_by_id(self, product_id: str) -> Optional[dict]:
        results = self.search_products(product_id)
        for product in results.get("products", []):
            if product.get("productId") == product_id:
                return product
        return None
