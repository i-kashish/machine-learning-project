from __future__ import annotations

from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


TARGET = "revenue"
FEATURE_COLUMNS = [
    "pizzas_sold",
    "orders",
    "avg_pizza_price",
    "unique_pizza_types",
    "lunch_orders",
    "dinner_orders",
    "day_of_week",
    "month",
    "day_of_month",
    "is_weekend",
    "avg_order_value",
    "revenue_lag_1",
    "orders_lag_1",
    "revenue_lag_7",
    "orders_lag_7",
    "revenue_lag_14",
    "orders_lag_14",
    "revenue_7d_avg",
    "orders_7d_avg",
    "pizzas_sold_7d_avg",
]


def build_model() -> Pipeline:
    """Build a daily revenue forecasting model."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=250,
                    min_samples_leaf=3,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )
