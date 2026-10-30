# InvoiceIQ Pipeline

Invoice extraction and analytics starter app with logging-enabled workflow.

## What It Does

- Extracts invoice header fields from raw text
- Parses line items from structured invoice-like rows
- Computes spend analytics (total, average, highest line amount)
- Visualizes extracted spending in Streamlit

## Implemented Feature Slice

- Invoice header extraction (vendor, invoice number, date)
- Line-item parsing from structured text rows (item | qty | unit_price)
- Total, average, and highest line amount analytics
- Table and bar-chart visualization in Streamlit
- Fallback total extraction when line items are not available

## Architecture

```mermaid
flowchart TD
    subgraph Extraction["📥 Extraction"]
        A[Invoice text input] --> B[Header field\nextraction]
        A --> C[Line-item parser]
        B --> F[Invoice metadata]
    end

    subgraph Analytics["📊 Analytics"]
        C --> D[Amount calculator]
        D --> E[Analytics aggregator]
    end

    subgraph UI["🖥️ Streamlit"]
        G[Structured\nextraction result] --> H[Table + metrics\n+ bar chart]
    end

    E --> G
    F --> G

    classDef source fill:#1e40af,stroke:#93c5fd,stroke-width:2px,color:#ffffff
    classDef process fill:#0f766e,stroke:#5eead4,stroke-width:2px,color:#ffffff
    classDef store fill:#7c2d12,stroke:#fdba74,stroke-width:2px,color:#ffffff
    classDef rank fill:#6d28d9,stroke:#c4b5fd,stroke-width:2px,color:#ffffff
    classDef ui fill:#15803d,stroke:#86efac,stroke-width:2px,color:#ffffff

    class A source
    class B,C process
    class F store
    class D,E rank
    class G,H ui

    style Extraction fill:#f1f5f9,stroke:#334155,stroke-width:2px,color:#0f172a
    style Analytics fill:#f1f5f9,stroke:#334155,stroke-width:2px,color:#0f172a
    style UI fill:#f1f5f9,stroke:#334155,stroke-width:2px,color:#0f172a

    linkStyle default stroke:#f59e0b,stroke-width:2px
```

## Outcome

- Converts unstructured invoice text into structured financial data
- Provides quick spending visibility without manual spreadsheets
- Creates a foundation for OCR and multimodal extraction extensions

## Quick Start

### Prerequisites

- [UV](https://docs.astral.sh/uv/) installed (`powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` on Windows)

### Run Locally

```bash
cd invoiceiq-pipeline
uv sync

uv run streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
invoiceiq-pipeline/
├── app.py                  # Streamlit entry point — sample text, metrics, table, bar chart
├── services/
│   ├── __init__.py
│   └── core.py             # _find_field, _parse_items, run_invoice_extraction
├── .streamlit/
│   └── config.toml         # App theme
├── pyproject.toml          # UV dependencies
└── README.md
```

---

## Logging

- Logging is configured on startup.
- Use LOG_LEVEL to adjust verbosity.
