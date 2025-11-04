# FreshConnect — Cerve PO Integration
> DevRel assignment — polished demo repo for Cerve integration (PO generation)

## Goal
Automatically suggest draft Purchase Orders using the Cerve API to cut manual PO time and stockouts.  
Target impact: reduce procurement admin from 15h/week → ~3h/week.

## What’s in this repo
- `/docs` — diagrams, API flow, sample outputs
- `/code/python` — working example integration
- `/code/samples` — env example and sample responses

## Quickstart (run locally)
1. Copy env:  
   ```bash
   cp code/samples/sample_env.example .env


2. Install deps:
```
python -m venv .venv
source .venv/bin/activate
pip install -r code/python/requirements.txt
```
3. Run example (creates a draft order JSON printed to console):
```
python code/python/cerve_po_example.py
```