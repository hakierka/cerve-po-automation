# API Flow — critical endpoints (summary)

## Product catalog
GET /suppliers/{supplier_id}/customers/{customer_id}/products
- purpose: build supplier catalog & product metadata

## Price calculation
GET /suppliers/{supplier_id}/customers/{customer_id}/products/{product_id}/price?quantity=...
- purpose: get total price, unit price, discounts for a given qty

## Stock/availability
GET /suppliers/{supplier_id}/customers/{customer_id}/products/{product_id}/stock
- purpose: live availability per supplier

## Create order (draft)
POST /suppliers/{supplier_id}/customers/{customer_id}/orders?draft=true
- purpose: compute totals & unavailable items without committing

## Create order (final)
POST /suppliers/{supplier_id}/customers/{customer_id}/orders
- purpose: submit the official order to supplier via Cerve
