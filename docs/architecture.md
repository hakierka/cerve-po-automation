```mermaid
fflowchart LR
 subgraph FreshConnect["FreshConnect"]
        SF["📦 Salesforce — Customer Orders"]
        SAP["🏭 SAP / WMS — Stock Levels"]
        HIST["📊 Historical Demand DB"]
  end
    SF -- order events --> ETL["🔁 Event Bus / ETL"]
    SAP -- stock sync --> ETL
    HIST -- demand data --> POEngine["⚙️ PO Engine / Orchestrator\n(forecast + price compare)"]
    ETL --> Inventory["🧮 Inventory Service\n(canonical stock + par levels)"]
    Inventory --> POEngine
    POEngine -- price/stock queries --> Cerve["🌐 Cerve API"]
    Cerve -- supplier responses --> Suppliers["🚚 Supplier Systems"]
    POEngine --> UI["🧾 Procurement UI\n(review & approve)"]
    UI -- approve --> POEngine
    POEngine -- POST order --> Cerve
    Cerve --> Suppliers
