import asyncio
import base64
import json
import time
from playwright.async_api import async_playwright

def decode_jwt_expiry(token: str) -> int:
    """Decode the JWT and return the exp (expiry timestamp)."""
    payload_b64 = token.split(".")[1]
    padding = '=' * (-len(payload_b64) % 4)
    decoded = base64.urlsafe_b64decode(payload_b64 + padding)
    payload = json.loads(decoded)
    return payload.get("exp")

async def get_bearer_token():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        bearer_token = None

        # Listen for requests and extract Bearer token
        async def handle_request(request):
            nonlocal bearer_token
            headers = request.headers
            auth = headers.get("authorization")
            if auth and auth.startswith("Bearer "):
                bearer_token = auth
                # print(f"🛂 Found token: {auth}")

        page.on("request", handle_request)

        await page.goto("https://www.newworld.co.nz/shop/search?pg=1&q", wait_until="networkidle")

        # Wait a bit more for any JS to fire
        await asyncio.sleep(5)
        await browser.close()

        if not bearer_token:
            raise RuntimeError("Bearer token not found during page load.")

        return bearer_token

if __name__ == "__main__":
    token = asyncio.run(get_bearer_token())
    exp = decode_jwt_expiry(token.replace("Bearer ", ""))
    now = int(time.time())
    print("\n✅ Final Bearer Token:", token)
    print(f"⏳ Valid for: {exp - now} seconds")