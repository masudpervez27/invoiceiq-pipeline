import logging
import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from services.core import run_invoice_pipeline

load_dotenv()


def configure_logging() -> logging.Logger:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    root_logger = logging.getLogger()

    if not root_logger.handlers:
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        )
    else:
        root_logger.setLevel(level)

    return logging.getLogger("invoiceiq-pipeline.app")


logger = configure_logging()

st.set_page_config(page_title="InvoiceIQ Pipeline", page_icon="🚀", layout="wide")
st.title("InvoiceIQ Pipeline")
st.caption("Extract invoice fields, line items, and spending analytics from raw invoice text.")

st.markdown("Paste invoice text using this optional line-item format:")
st.code(
    """Vendor: Acme Supplies
Invoice No: INV-1022
Date: 2026-05-20

Laptop Stand | 2 | 49.99
USB-C Dock    | 1 | 129.50
Cloud Credits | 3 | 80
"""
)

user_input = st.text_area("Invoice Text", height=220)

if st.button("Extract Invoice Data", type="primary"):
    logger.info("Button clicked for InvoiceIQ Pipeline")
    output = run_invoice_pipeline(user_input)

    if output.get("error"):
        st.error(output["error"])
        st.stop()

    st.success("Extraction completed")

    invoice = output.get("invoice", {})
    analytics = output.get("analytics", {})
    items = output.get("items", [])

    col1, col2, col3 = st.columns(3)
    col1.metric("Vendor", invoice.get("vendor", "N/A"))
    col2.metric("Invoice", invoice.get("invoice_number", "N/A"))
    col3.metric("Date", invoice.get("date", "N/A"))

    m1, m2, m3 = st.columns(3)
    m1.metric("Line Items", analytics.get("line_items", 0))
    m2.metric("Total Amount", f"${analytics.get('total_amount', 0):,.2f}")
    m3.metric("Average Line Amount", f"${analytics.get('average_line_amount', 0):,.2f}")

    if items:
        df = pd.DataFrame(items)
        st.subheader("Extracted Line Items")
        st.dataframe(df, use_container_width=True)

        chart = px.bar(df, x="item", y="amount", title="Invoice Spend by Line Item")
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.info("No line-item table parsed. Fallback total extraction was used.")

    for warning in output.get("warnings", []):
        st.warning(warning)
