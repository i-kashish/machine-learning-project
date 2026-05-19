from __future__ import annotations

import argparse
from datetime import timedelta

import joblib
import pandas as pd

from .config import MODEL_PATH
from .data import build_daily_sales_features
from .model import FEATURE_COLUMNS


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Run `python -m src.pizza_sales.train` first.")
    return joblib.load(MODEL_PATH)


def build_next_day_features(
    expected_orders: int | None = None,
    expected_pizzas_sold: int | None = None,
) -> pd.DataFrame:
    daily = build_daily_sales_features()
    latest = daily.iloc[-1].copy()
    next_date = pd.to_datetime(latest["date"]) + timedelta(days=1)

    latest["date"] = next_date
    latest["day_of_week"] = next_date.dayofweek
    latest["month"] = next_date.month
    latest["day_of_month"] = next_date.day
    latest["is_weekend"] = int(next_date.dayofweek in [5, 6])

    if expected_orders is not None:
        latest["orders"] = expected_orders
    if expected_pizzas_sold is not None:
        latest["pizzas_sold"] = expected_pizzas_sold

    latest["avg_order_value"] = latest["revenue_lag_1"] / max(latest["orders_lag_1"], 1)
    return pd.DataFrame([latest])


def forecast_next_day(expected_orders: int | None = None, expected_pizzas_sold: int | None = None) -> tuple[pd.Timestamp, float]:
    model = load_model()
    features = build_next_day_features(expected_orders, expected_pizzas_sold)
    prediction = float(model.predict(features[FEATURE_COLUMNS])[0])
    return pd.to_datetime(features.iloc[0]["date"]), prediction


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Forecast next-day pizza sales revenue.")
    parser.add_argument("--expected-orders", type=int, default=None)
    parser.add_argument("--expected-pizzas-sold", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    date, revenue = forecast_next_day(args.expected_orders, args.expected_pizzas_sold)
    print(f"Forecast date: {date.date()}")
    print(f"Predicted revenue: ${revenue:,.2f}")


if __name__ == "__main__":
    main()
