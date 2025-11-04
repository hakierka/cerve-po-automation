"""
cerve_po_integration.py
Author: Amy Waliszewska (hakierka)
Role: Developer Relations candidate — demo script for Cerve integration.

What this script demonstrates (educational):
- Load local environment variables (client id/secret, supplier/customer ids)
- Authenticate with the Cerve OAuth2 token endpoint (client credentials)
- Call the price endpoint for a product (example)
- Create a draft order (draft=true) to simulate totals and availability
- Save the draft response to docs/samples/draft_order_example.json for demoing

Notes:
- This is a demo script. Keep secrets out of the repo: use code/samples/sample_env.example as a template.
- The script uses draft mode so no real orders are submitted during testing.
"""

import os
import time
import json
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load environment variables from .env in the repo root (for local testing only)
# Copy code/samples/sample_env.example -> .env and fill test credentials before running.
load_dotenv()

# Config (allow overriding CERVE_BASE_URL to point at a sandbox)
CERVE_BASE_URL = os.getenv("CERVE_BASE_URL", "").rstrip("/")  # e.g. https://api.sandbox.cerve.com or blank
if not CERVE_BASE_URL:
    # default production-ish endpoints (kept separate so callers can override)
    AUTH_HOST = "https://auth.cerve.com"
    API_HOST = "https://api.cerve.com"
else:
    AUTH_HOST = CERVE_BASE_URL.replace("/v2", "")  # allow passing full base if desired
    API_HOST = CERVE_BASE_URL.replace("/v2", "")

CERVE_AUTH_URL = f"{AUTH_HOST}/v2/token"
CERVE_API_BASE = f"{API_HOST}/v2"

# Credentials and identifiers (from .env or CI secrets)
CLIENT_ID = os.getenv("CERVE_CLIENT_ID")
CLIENT_SECRET = os.getenv("CERVE_CLIENT_SECRET")
SUPPLIER_ID = os.getenv("SUPPLIER_ID")
CUSTOMER_ID = os.getenv("CUSTOMER_ID")

# Basic timeout config for network calls
TIMEOUT = 15

# ---- Simple in-memory token cache ----
_TOKEN = None
_TOKEN_EXPIRES_AT = 0

def get_token():
    """
    Obtain an OAuth2 client_credentials token from Cerve.
    For demos we do a blocking call and cache the token in memory.
    """
    global _TOKEN, _TOKEN_EXPIRES_AT

    # Return cached token if still valid
    if _TOKEN and time.time() < (_TOKEN_EXPIRES_AT - 30):
        return _TOKEN

    if not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError("CERVE_CLIENT_ID and CERVE_CLIENT_SECRET must be set in your environment (.env)")

    resp = requests.post(
        CERVE_AUTH_URL,
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=TIMEOUT,
    )
    # raise_for_status will show a helpful HTTP error if auth fails
    resp.raise_for_status()
    body = resp.json()

    _TOKEN = body.get("access_token")
    expires_in = body.get("expires_in", 3600)
    _TOKEN_EXPIRES_AT = time.time() + int(expires_in)

    if not _TOKEN:
        raise RuntimeError("Authentication succeeded but no access_token returned")

    return _TOKEN

def auth_headers():
    """Return Authorization header dict for API requests."""
    token = get_token()
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# ---- API helpers ----
def get_price(product_id, quantity=1):
    """
    Call the Cerve price endpoint for a specific supplier/customer/product.
    Returns JSON price object or None if product not offered (404).
    """
    url = f"{CERVE_API_BASE}/suppliers/{SUPPLIER_ID}/customers/{CUSTOMER_ID}/products/{product_id}/price"
    params = {"quantity": quantity}
    r = requests.get(url, headers=auth_headers(), params=params, timeout=TIMEOUT)

    if r.status_code == 404:
        # Product not offered by this supplier/customer pair
        return None

    r.raise_for_status()
    return r.json()

def create_draft_order(line_items, shipping_method_id=None, customer_order_ref=None):
    """
    Create a draft order via Cerve (simulation mode).
    - line_items: list of dicts {supplier_product_id, unit_of_measure, quantity}
    - shipping_method_id: optional supplier shipping method id
    - customer_order_ref: optional reference id used by the customer system

    Returns the order JSON (draft) from Cerve.
    """
    url = f"{CERVE_API_BASE}/suppliers/{SUPPLIER_ID}/customers/{CUSTOMER_ID}/orders"
    params = {"draft": "true"}
    payload = {
        "customer_order_id": customer_order_ref or f"FC-DEMO-{int(time.time())}",
        "line_items": line_items,
    }
    if shipping_method_id:
        payload["shipments"] = [{"supplier_shipping_method_id": shipping_method_id}]

    r = requests.post(url, headers=auth_headers(), params=params, json=payload, timeout=TIMEOUT)

    # Handle common HTTP responses explicitly for clearer demo output
    if r.status_code == 401:
        raise RuntimeError("Unauthorized — check client credentials and token scopes")
    if r.status_code == 409:
        raise RuntimeError("Conflict creating draft order — possible duplicate or business rule")
    r.raise_for_status()

    return r.json()

def save_sample(obj, path="docs/samples/draft_order_example.json"):
    """
    Persist a pretty-printed JSON sample to docs/samples for demo and review.
    This makes it easy to open the sample in the browser during your interview.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2))
    print(f"Saved sample output to {p.resolve()}")

# ---- Demo main flow ----
def main():
    """
    Demo flow:
      1) Show how to get a price for a product
      2) Build a single-line draft order and post it in draft mode
      3) Save the returned draft JSON to docs/samples for the demo
    """
    # Simple validation to help new reviewers run this locally
    missing = [name for name in ("CLIENT_ID", "CLIENT_SECRET", "SUPPLIER_ID", "CUSTOMER_ID")
               if not os.getenv(name) and name in ("CLIENT_ID", "CLIENT_SECRET", "SUPPLIER_ID", "CUSTOMER_ID")]
    # This check is gentle: we recommend copying sample_env -> .env before running
    if not all([CLIENT_ID, CLIENT_SECRET, SUPPLIER_ID, CUSTOMER_ID]):
        print("Warning: one or more required env vars are missing (see code/samples/sample_env.example).")
        print("You can still run the script to exercise auth/errors if you want to demo failure handling.")
    try:
        # Example product and supplier product id - replace these with real IDs in staging
        example_product_id = os.getenv("EXAMPLE_PRODUCT_ID", "00000000-0000-0000-0000-000000000001")
        supplier_product_id = os.getenv("EXAMPLE_SUPPLIER_PRODUCT_ID", "APLJ-1L")
        shipment_method = os.getenv("EXAMPLE_SHIP_METHOD", None)

        print("→ Fetching price for product:", example_product_id)
        price_info = get_price(example_product_id, quantity=10)
        if price_info is None:
            print("Product not offered by this supplier/customer pair (404).")
        else:
            # Print only a small, helpful snippet to keep console clean
            snippet = {k: price_info.get(k) for k in ("unit_price", "total_price", "discount", "currency") if price_info.get(k) is not None}
            print("Price info (snippet):", snippet)

        # Build a simple line item for the draft order
        line_items = [
            {"supplier_product_id": supplier_product_id, "unit_of_measure": "each", "quantity": 10}
        ]

        print("→ Creating draft order (simulation mode)...")
        draft = create_draft_order(line_items, shipping_method_id=shipment_method, customer_order_ref="FC-PO-EXAMPLE-DRAFT")
        print("Draft order created. Order id (draft):", draft.get("id") or draft.get("supplier_order_id") or draft.get("order_id"))

        # Save the full draft JSON to docs/samples for you to open during the interview
        save_sample(draft)

    except requests.HTTPError as e:
        # Print helpful status and body for debugging during demo
        print("HTTP error during API call:", e)
        if e.response is not None:
            try:
                print("Response body:", e.response.json())
            except Exception:
                print("Response text:", e.response.text)
    except Exception as e:
        print("Unexpected error:", str(e))

if __name__ == "__main__":
    print("🚀 Running Cerve PO demo (draft mode).")
    main()
    print("✅ Demo finished.")
