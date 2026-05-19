from __future__ import annotations

import json

from .config import REPORTS_DIR
from .data import build_order_line_items


def generate_summary() -> dict:
    line_items = build_order_line_items()
    summary = {
        "total_orders": int(line_items["order_id"].nunique()),
        "total_pizzas_sold": int(line_items["quantity"].sum()),
        "total_revenue": round(float(line_items["revenue"].sum()), 2),
        "top_pizza": line_items.groupby("name")["quantity"].sum().sort_values(ascending=False).index[0],
        "top_category": line_items.groupby("category")["revenue"].sum().sort_values(ascending=False).index[0],
        "peak_hour": int(line_items.groupby("hour")["order_id"].nunique().sort_values(ascending=False).index[0]),
    }
    return summary


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    summary = generate_summary()
    output_path = REPORTS_DIR / "eda_summary.json"
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
