# InvoiceIQ Pipeline - YouTube Transcript Script

## Title
Build an Invoice Extraction and Analytics App with Streamlit (Project 09)

## Intro
This project implements InvoiceIQ from the portfolio plan.

We parse invoice text into:
- vendor,
- invoice number,
- date,
- line items,
- and spending analytics.

## Input format
For best extraction we support this line format:
item | qty | unit_price

Example:
Laptop Stand | 2 | 49.99

## Pipeline
1. Extract header fields with regex.
2. Parse line items from structured rows.
3. Calculate total, average, and max spend.
4. Render table + bar chart in Streamlit.
5. Fallback to total-only extraction if line table is missing.

## UI output
The app shows:
- invoice metadata cards,
- analytics metrics,
- extracted item dataframe,
- spend bar chart,
- warnings when parsing is partial.

## Logging
We log button events, parse completion, and extracted totals using LOG_LEVEL-driven logging.

## Outro
This is a functional invoice analytics slice and can be extended with OCR and multimodal extraction next.
