from src.pizza_sales.data import build_daily_sales_features, build_order_line_items, load_raw_tables
from src.pizza_sales.model import FEATURE_COLUMNS, TARGET, build_model


def test_real_dataset_loads():
    tables = load_raw_tables()
    assert tables["orders"].shape[0] > 20000
    assert tables["order_details"].shape[0] > 40000
    assert tables["pizzas"].shape[0] > 90


def test_daily_features_include_model_columns():
    daily = build_daily_sales_features()
    assert set(FEATURE_COLUMNS + [TARGET]).issubset(daily.columns)
    assert daily[TARGET].min() > 0


def test_model_fits_small_sample():
    daily = build_daily_sales_features().head(80)
    model = build_model()
    model.fit(daily[FEATURE_COLUMNS], daily[TARGET])
    predictions = model.predict(daily[FEATURE_COLUMNS].head(3))
    assert len(predictions) == 3


def test_order_line_items_have_revenue():
    line_items = build_order_line_items()
    assert "revenue" in line_items.columns
    assert line_items["revenue"].sum() > 0
