# FreshConnect — Cerve PO Integration

## Goal
Auto-generate draft purchase orders using the Cerve API to reduce manual PO time and cut stockouts.

## Repo structure
- /docs — diagrams and API flow
- /code/python — example integration scripts
- /code/samples — example env & test data

## Quickstart (dev)
1. Copy env: `cp code/samples/sample_env.example .env`
2. Install deps: `pip install -r code/python/requirements.txt` (create a small requirements file with `requests`)
3. Run example: `python code/python/cerve_po_example.py`

## How to present
- Use the Canva deck for slides (link to deck here).
- Demo: run `cerve_po_example.py` in draft mode then show the draft JSON in UI.

## Notes
- Uses OAuth2 client credentials (auth.cerve.com)
- Always use `draft=true` when testing
