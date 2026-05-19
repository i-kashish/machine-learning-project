from __future__ import annotations

import pandas as pd

from .config import DAILY_SALES_PATH, DATA_DIR


def load_raw_tables(data_dir=DATA_DIR) -> dict[str, pd.DataFrame]:
    """Load the four raw CSV tables from the Maven Pizza Place Sales dataset."""
    return {
        "orders": pd.read_csv(data_dir / "orders.csv"),
        "order_details": pd.read_csv(data_dir / "order_details.csv"),
        "pizzas": pd.read_csv(data_dir / "pizzas.csv"),
        "pizza_types": pd.read_csv(data_dir / "pizza_types.csv", encoding="latin1"),
    }


def build_order_line_items(tables: dict[str, pd.DataFrame] | None = None) -> pd.DataFrame:
    """Merge orders, order details, pizza prices, and pizza metadata into one table."""
    tables = tables or load_raw_tables()
    orders = tables["orders"].copy()
    order_details = tables["order_details"].copy()
    pizzas = tables["pizzas"].copy()
    pizza_types = tables["pizza_types"].copy()

    orders["date"] = pd.to_datetime(orders["date"])
    orders["datetime"] = pd.to_datetime(orders["date"].astype(str) + " " + orders["time"].astype(str))

    line_items = (
        order_details.merge(orders, on="order_id", how="left")
        .merge(pizzas, on="pizza_id", how="left")
        .merge(pizza_types, on="pizza_type_id", how="left")
    )
    line_items["revenue"] = line_items["quantity"] * line_items["price"]
    line_items["hour"] = line_items["datetime"].dt.hour
    line_items["day_of_week"] = line_items["date"].dt.dayofweek
    line_items["month"] = line_items["date"].dt.month
    line_items["is_weekend"] = line_items["day_of_week"].isin([5, 6]).astype(int)
    return line_items


def build_daily_sales_features(line_items: pd.DataFrame | None = None) -> pd.DataFrame:
    """Aggregate transaction data into daily ML features for revenue forecasting."""
    line_items = line_items if line_items is not None else build_order_line_items()

    daily = (
        line_items.groupby("date")
        .agg(
            revenue=("revenue", "sum"),
            pizzas_sold=("quantity", "sum"),
            orders=("order_id", "nunique"),
            avg_pizza_price=("price", "mean"),
            unique_pizza_types=("pizza_type_id", "nunique"),
            lunch_orders=("hour", lambda values: ((values >= 11) & (values <= 14)).sum()),
            dinner_orders=("hour", lambda values: ((values >= 17) & (values <= 21)).sum()),
        )
        .reset_index()
        .sort_values("date")
    )

    daily["day_of_week"] = daily["date"].dt.dayofweek
    daily["month"] = daily["date"].dt.month
    daily["day_of_month"] = daily["date"].dt.day
    daily["is_weekend"] = daily["day_of_week"].isin([5, 6]).astype(int)
    daily["avg_order_value"] = daily["revenue"] / daily["orders"]

    for lag in [1, 7, 14]:
        daily[f"revenue_lag_{lag}"] = daily["revenue"].shift(lag)
        daily[f"orders_lag_{lag}"] = daily["orders"].shift(lag)

    daily["revenue_7d_avg"] = daily["revenue"].shift(1).rolling(7).mean()
    daily["orders_7d_avg"] = daily["orders"].shift(1).rolling(7).mean()
    daily["pizzas_sold_7d_avg"] = daily["pizzas_sold"].shift(1).rolling(7).mean()
    daily = daily.dropna().reset_index(drop=True)
    return daily


def save_daily_sales_features() -> pd.DataFrame:
    DAILY_SALES_PATH.parent.mkdir(parents=True, exist_ok=True)
    daily = build_daily_sales_features()
    daily.to_csv(DAILY_SALES_PATH, index=False)
    return daily
