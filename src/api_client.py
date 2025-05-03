# src/api_client.py
import asyncio
import jwt
import time
import requests
from src.token_extractor import get_bearer_token
from src.token_cache import load_cached_token, save_token, clear_token_cache


BASE_URL = "https://api-prod.newworld.co.nz/v1/edge/search/paginated/products"

class NewWorldAPIClient:

    def __init__(self, store_id: str):
        self.store_id = store_id
        self.session = requests.Session()
        self.token = self.get_token()
        self.session.headers.update({
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Authorization": f"{self.token}"
        })

    def _decode_token_expiry(self, token: str) -> int:
        try:
            payload = jwt.decode(token.split()[1], options={"verify_signature": False})
            return payload.get("exp", int(time.time()) + 600)
        except Exception:
            return int(time.time()) + 600
    
    def get_token(self) -> str:
        cached_token = load_cached_token()
        if cached_token:
            print("🔄 Using cached token...")
            return cached_token

        print("🔄 No valid cached token found, fetching a new one...")
        fresh_token = asyncio.run(get_bearer_token())
        expiry = self._decode_token_expiry(fresh_token)
        save_token(fresh_token, expiry)
        return fresh_token

    def _build_payload(self, query: str, filters: str = None, page: int = 0, hits_per_page: int = 50) -> dict:
        """
        Internal method to build the request payload.
        """
        algolia_query = {
            "attributesToHighlight": [],
            "attributesToRetrieve": [
                "productID",
                "Type",
                "sponsored",
                "category0SI",
                "category1SI",
                "category2SI"
            ],
            "facets": [
                "brand",
                "category1SI",
                "onPromotion",
                "productFacets",
                "tobacco"
            ],
            "highlightPostTag": "__/ais-highlight__",
            "highlightPreTag": "__ais-highlight__",
            "hitsPerPage": hits_per_page,
            "maxValuesPerFacet": 100,
            "page": page,
            "query": query,
            "analyticsTags": ["fs#WEB:desktop"]
        }

        if filters:
            algolia_query["filters"] = filters
        else:
            algolia_query["filters"] = f"stores:{self.store_id}"

        return {
            "algoliaQuery": algolia_query,
            "algoliaFacetQueries": [],
            "storeId": self.store_id,
            "hitsPerPage": hits_per_page,
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

    def search_products(self, search_query: str, page: int = 0, hits_per_page: int = 50) -> dict:
        # self.get_token()
        # self.session.headers["Authorization"] = self._cached_token
        payload = self._build_payload(query=search_query, page=page, hits_per_page=hits_per_page)
        response = self.session.post(BASE_URL, json=payload)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}, {response.text}")

        return response.json()

    def get_product_by_id(self, product_id: str) -> dict:
        # self.get_token()
        # self.session.headers["Authorization"] = self._cached_token
        payload = self._build_payload(query=product_id, filters=f"productID:{product_id}", page=0, hits_per_page=1)
        response = self.session.post(BASE_URL, json=payload)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}, {response.text}")

        response_json = response.json()
        products = response_json.get("products", [])

        if not products:
            raise ValueError(f"No product found with ID {product_id}")

        return products[0]