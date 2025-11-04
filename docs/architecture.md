# Architecture (copy this to draw.io or Canva)

Mermaid diagram (use mermaid.live or draw.io with mermaid support):

```mermaid
flowchart LR
  SF[Salesforce Orders] -->|Order events| ETL[Event bus / ETL]
  SAP[WMS / SAP] -->|Inventory sync| ETL
  ETL --> InventoryMS[Inventory microservice]
  InventoryMS --> POEngine[PO Engine / Orchestrator]
  HistoricalDB[Historical demand DB] --> POEngine
  POEngine --> UI[Procurement UI (drafts & approve)]
  POEngine -->|API calls| CerveAPI[(Cerve API)]
  CerveAPI -->|forwards| SupplierSys[Supplier Systems]
