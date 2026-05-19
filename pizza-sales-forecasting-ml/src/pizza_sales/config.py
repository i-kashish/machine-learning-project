from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

MODEL_PATH = MODELS_DIR / "daily_revenue_model.joblib"
FEATURES_PATH = MODELS_DIR / "feature_columns.json"
METRICS_PATH = REPORTS_DIR / "metrics.json"
DAILY_SALES_PATH = DATA_DIR / "daily_sales_features.csv"
