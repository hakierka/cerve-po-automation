"""
Cerve Developer Experience Assessment — Automated Purchase Order Generation
Author: Amy Waliszewska
Date: November 2025
Purpose: Demonstrates integration with Cerve API for automated PO creation.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

CERVE_BASE_URL = os.getenv("CERVE_BASE_URL", "https://api.sandbox.cerve.com")
CERVE_AUTH_URL = f"{CERVE_BASE_URL.replace('api.', 'auth.')}/oauth/token"
CLIENT_ID = os.getenv("CERVE_CLIENT_ID")
CLIENT_SECRET = os.getenv("CERVE_CLIENT_SECRET")

def get_access_token() -> str:
    """Authenticate via OAuth2 and return bearer token."""
    res = requests.post(
        CERVE_AUTH_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        timeout=10,
    )
    res.raise_for_status()
    return res.json().get("access_token")

def get_products(access_token: str, category: str = "fresh-produce") -> list:
    """Fetch available products from Cerve API."""
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(
        f"{CERVE_BASE_URL}/v1/products",
        headers=headers,
        params={"category": category},
        timeout=10,
    )
    res.raise_for_status()
    return res.json().get("data", [])

def create_purchase_order(access_token: str, items: list) -> dict:
    """Create a draft Purchase Order in Cerve."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "supplier_id": "SUP1234",
        "status": "draft",
        "currency": "GBP",
        "items": items,
        "notes": "Auto-generated PO from FreshConnect integration demo",
    }
    res = requests.post(
        f"{CERVE_BASE_URL}/v1/purchase-orders",
        headers=headers,
        json=payload,
        timeout=10,
    )
    res.raise_for_status()
    return res.json()

def main():
    print("🚀 Starting Cerve Automated PO Example...")
    token = get_access_token()
    print("✅ Authenticated with Cerve API.")

    products = get_products(token)
    if not products:
        print("❌ No products found — aborting.")
        return

    po_items = [
        {
            "product_id": products[0]["id"],
            "quantity": 100,
            "unit_price": products[0]["price"],
        }
    ]
    po = create_purchase_order(token, po_items)
    print("✅ Draft PO Created:")
    print(po)

if __name__ == "__main__":
    main()
import os
import requests
from dotenv import load_dotenv

load_dotenv()
CERVE_AUTH_URL = f"{os.getenv('CERVE_BASE_URL', 'https://api.sandbox.cerve.com').replace('api.', 'auth.')}/oauth/token"

def test_auth():
    res = requests.post(
        CERVE_AUTH_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": os.getenv("CERVE_CLIENT_ID"),
            "client_secret": os.getenv("CERVE_CLIENT_SECRET"),
        },
        timeout=10,
    )
    if res.status_code == 200:
        print("✅ Authentication successful.")
    else:
        print(f"❌ Auth failed: {res.status_code} - {res.text}")

if __name__ == "__main__":
    test_auth()
