from __future__ import annotations

import json

import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from .config import FEATURES_PATH, METRICS_PATH, MODEL_PATH, MODELS_DIR, REPORTS_DIR
from .data import save_daily_sales_features
from .model import FEATURE_COLUMNS, TARGET, build_model


def train_model() -> dict[str, float]:
    """Train model with a time-based split and save artifacts."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    daily = save_daily_sales_features()
    split_index = int(len(daily) * 0.8)
    train_df = daily.iloc[:split_index]
    test_df = daily.iloc[split_index:]

    model = build_model()
    model.fit(train_df[FEATURE_COLUMNS], train_df[TARGET])
    predictions = model.predict(test_df[FEATURE_COLUMNS])

    mae = mean_absolute_error(test_df[TARGET], predictions)
    rmse = np.sqrt(mean_squared_error(test_df[TARGET], predictions))
    r2 = r2_score(test_df[TARGET], predictions)

    metrics = {
        "rows_used": int(len(daily)),
        "train_days": int(len(train_df)),
        "test_days": int(len(test_df)),
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2),
        "r2": round(float(r2), 4),
        "average_daily_revenue": round(float(daily[TARGET].mean()), 2),
    }

    joblib.dump(model, MODEL_PATH)
    FEATURES_PATH.write_text(json.dumps(FEATURE_COLUMNS, indent=2), encoding="utf-8")
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    metrics = train_model()
    print("Pizza sales forecasting model trained successfully.")
    print(f"Saved model: {MODEL_PATH}")
    print(f"Saved metrics: {METRICS_PATH}")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
