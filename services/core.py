import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


def _find_field(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else default


def _parse_items(text: str) -> list[dict]:
    items: list[dict] = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # Format supported: item | qty | unit_price
    for line in lines:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        name = parts[0]
        qty_match = re.search(r"\d+(?:\.\d+)?", parts[1])
        price_match = re.search(r"\d+(?:\.\d+)?", parts[2])
        if not qty_match or not price_match:
            continue
        quantity = float(qty_match.group(0))
        unit_price = float(price_match.group(0))
        amount = round(quantity * unit_price, 2)
        items.append(
            {
                "item": name,
                "quantity": quantity,
                "unit_price": unit_price,
                "amount": amount,
            }
        )

    return items


def run_invoice_pipeline(user_input: str) -> dict:
    logger.info("Processing request in run_invoice_pipeline (chars=%d)", len(user_input))
    if not user_input.strip():
        logger.warning("Empty input received")
        return {"error": "Please provide invoice text input to continue."}

    vendor = _find_field(r"vendor\s*:\s*(.+)", user_input, "Unknown Vendor")
    invoice_number = _find_field(r"invoice\s*(?:no|number)?\s*:\s*(.+)", user_input, "N/A")
    date_raw = _find_field(r"date\s*:\s*(.+)", user_input, "")

    parsed_date = date_raw
    if date_raw:
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                parsed_date = datetime.strptime(date_raw, fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                continue

    items = _parse_items(user_input)

    if not items:
        # Fallback: detect standalone total amount
        amount_match = re.search(r"total\s*[:=]?\s*\$?\s*(\d+(?:\.\d+)?)", user_input, re.IGNORECASE)
        total_amount = float(amount_match.group(1)) if amount_match else 0.0
        return {
            "invoice": {
                "vendor": vendor,
                "invoice_number": invoice_number,
                "date": parsed_date or "N/A",
            },
            "items": [],
            "analytics": {
                "line_items": 0,
                "total_amount": round(total_amount, 2),
                "average_line_amount": 0.0,
                "highest_line_amount": round(total_amount, 2),
            },
            "warnings": [
                "No line-item table detected. Use 'item | qty | unit_price' format for full extraction.",
            ],
        }

    total = round(sum(item["amount"] for item in items), 2)
    avg = round(total / len(items), 2)
    high = round(max(item["amount"] for item in items), 2)

    logger.info("Parsed invoice vendor=%s invoice_number=%s items=%d total=%.2f", vendor, invoice_number, len(items), total)

    return {
        "invoice": {
            "vendor": vendor,
            "invoice_number": invoice_number,
            "date": parsed_date or "N/A",
        },
        "items": items,
        "analytics": {
            "line_items": len(items),
            "total_amount": total,
            "average_line_amount": avg,
            "highest_line_amount": high,
        },
        "warnings": [],
    }
