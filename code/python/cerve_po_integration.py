# cerve_po_example.py
# Simple example: authenticate, fetch price for a product, create a draft order.
import os
import time
import requests

CERVE_AUTH_URL = "https://auth.cerve.com/v2/token"
CERVE_API_BASE = "https://api.cerve.com/v2"
CLIENT_ID = os.getenv("CERVE_CLIENT_ID")
CLIENT_SECRET = os.getenv("CERVE_CLIENT_SECRET")
SUPPLIER_ID = os.getenv("CERVE_SUPPLIER_ID")      # e.g. 'supplier_abc'
CUSTOMER_ID = os.getenv("CERVE_CUSTOMER_ID")      # FreshConnect's customer id at supplier
TIMEOUT = 10

def get_token():
    """Client credentials flow. Cache token in-memory for demo."""
    resp = requests.post(
        CERVE_AUTH_URL,
        data={"grant_type":"client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=TIMEOUT
    )
    resp.raise_for_status()
    j = resp.json()
    return j["access_token"], time.time() + j.get("expires_in", 3000)

# simple token cache
_TOKEN = None
_TOKEN_EXP = 0
def auth_header():
    global _TOKEN, _TOKEN_EXP
    if not _TOKEN or time.time() > (_TOKEN_EXP - 30):
        _TOKEN, _TOKEN_EXP = get_token()
    return {"Authorization": f"Bearer {_TOKEN}", "Content-Type": "application/json"}

def get_price(product_id, quantity=1):
    """Calls: GET /suppliers/{supplier_id}/customers/{customer_id}/products/{product_id}/price"""
    url = f"{CERVE_API_BASE}/suppliers/{SUPPLIER_ID}/customers/{CUSTOMER_ID}/products/{product_id}/price"
    params = {"quantity": quantity}
    r = requests.get(url, headers=auth_header(), params=params, timeout=TIMEOUT)
    if r.status_code == 404:
        return None  # product not offered
    r.raise_for_status()
    return r.json()  # contains price, discount, vat_rate per spec. :contentReference[oaicite:26]{index=26}

def create_draft_order(line_items, shipping_method_id, customer_order_ref="auto-1"):
    """Calls POST /suppliers/{supplier_id}/customers/{customer_id}/orders?draft=true
       line_items: list of {supplier_product_id, unit_of_measure, quantity}
    """
    url = f"{CERVE_API_BASE}/suppliers/{SUPPLIER_ID}/customers/{CUSTOMER_ID}/orders"
    params = {"draft": "true"}
    payload = {
        "customer_order_id": customer_order_ref,
        "line_items": line_items,
        "shipments": [
            {"supplier_shipping_method_id": shipping_method_id, "time": "2025-11-05T08:00:00Z"}
        ]
    }
    r = requests.post(url, headers=auth_header(), params=params, json=payload, timeout=TIMEOUT)
    if r.status_code == 409:
        raise RuntimeError("Conflict while creating order - check duplicates")
    r.raise_for_status()
    return r.json()  # returns an Order object (draft totals, unavailable_line_items). :contentReference[oaicite:27]{index=27}

# ----- Example usage -----
if __name__ == "__main__":
    # example placeholders
    example_product_id = "00000000-0000-0000-0000-000000000001"
    supplier_product_id = "APLJ-1L"
    shipment_method = "ship_method_1"

    try:
        price_info = get_price(example_product_id, quantity=10)
        if not price_info:
            print("Product not available from this supplier.")
        else:
            print("Price info:", price_info)

        draft = create_draft_order(
            line_items=[{"supplier_product_id": supplier_product_id, "unit_of_measure": "each", "quantity": 10}],
            shipping_method_id=shipment_method,
            customer_order_ref="FC-PO-1234-DRAFT"
        )
        print("Draft order created:", draft.get("supplier_order_id") or draft.get("id"))
        # Show unavailable items or totals
        if draft.get("unavailable_line_items"):
            print("Unavailable items:", draft["unavailable_line_items"])
        else:
            print("Draft total:", draft.get("total"))
    except requests.HTTPError as e:
        print("API error:", e, e.response.text)
    except Exception as e:
        print("Error:", e)
