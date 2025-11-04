# 🧭 Cerve API Flow (Reference Overview)

> This file summarizes the main endpoints used in the demo integration.  
> It is meant for developers reviewing the repo, not for production use.

---

### 🔐 Authentication

**POST** `https://auth.cerve.com/v2/token`  
→ OAuth2 client credentials flow  
Required headers: `Authorization: Basic {client_id:client_secret}`  
Returns: `access_token`, `expires_in`

---

### 📦 Product & Price Data

**GET** `/suppliers/{supplier_id}/customers/{customer_id}/products`  
→ Retrieve supplier catalog for this customer.

**GET** `/suppliers/{supplier_id}/customers/{customer_id}/products/{product_id}/price`  
→ Retrieve real-time price for a specific product.

**GET** `/suppliers/{supplier_id}/customers/{customer_id}/products/{product_id}/stock`  
→ Check stock availability.

---

### 🧾 Orders

**POST** `/suppliers/{supplier_id}/customers/{customer_id}/orders?draft=true`  
→ Generate a draft purchase order (simulation mode).  
Returns calculated totals, unavailable line items, and draft order ID.

**POST** `/suppliers/{supplier_id}/customers/{customer_id}/orders`  
→ Submit approved order (live mode).

---

### 📘 Notes

- All examples in this repo use `draft=true` to avoid live order creation.
- Real credentials are never included — see `code/samples/sample_env.example` for setup.
- This flow matches the endpoints defined in `Customers API.json`.

---

🧩 **See also:**
- [`code/python/cerve_po_integration.py`](../code/python/cerve_po_integration.py)
- [`docs/samples/draft_order_example.json`](./samples/draft_order_example.json)
