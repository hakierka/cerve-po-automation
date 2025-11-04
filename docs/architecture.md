```mermaid
flowchart LR
    subgraph Internal_Systems[🏠 FreshConnect Internal Systems]
        SF[Salesforce CRM\nCustomer Orders]
        SAP[SAP / Warehouse\nStock Levels]
        HIST[Historical Demand DB]
    end

    subgraph PO_Engine[⚙️ PO Engine / Orchestrator]
        FORECAST[Demand Forecasting\n+ Reorder Logic]
        PRICECHECK[Supplier Price Comparison]
        DRAFTPO[Draft PO Generator]
    end

    subgraph Procurement_UI[🖥️ Procurement Interface]
        REVIEW[Review & Approve Draft Orders]
    end

    subgraph Cerve_API[🌐 Cerve API Platform]
        PRODUCTS[/Products Endpoint/]
        PRICE[/Price Endpoint/]
        STOCK[/Stock Endpoint/]
        ORDERS[/Create Order Endpoint/]
    end

    subgraph Supplier_Systems[🚚 Supplier Systems]
        SUP1[Supplier 1]
        SUP2[Supplier 2]
        SUP3[Supplier 3]
    end

    SF --> FORECAST
    SAP --> FORECAST
    HIST --> FORECAST
    FORECAST --> PRICECHECK
    PRICECHECK --> DRAFTPO
    DRAFTPO --> REVIEW
    REVIEW --> ORDERS
    ORDERS --> SUP1 & SUP2 & SUP3

    PRICECHECK --> PRODUCTS
    PRICECHECK --> PRICE
    FORECAST --> STOCK
