# Pizza Sales Forecasting ML Project

Machine learning project that forecasts next-day pizza sales revenue using a real public pizza sales dataset. The project combines business analytics, feature engineering, model training, evaluation, and a small Streamlit app.

## Dataset

This project uses the public **Pizza Place Sales** dataset from Maven Analytics.

Source: [Maven Analytics Pizza Place Sales](https://mavenanalytics.io/data-playground/pizza-place-sales)

The dataset contains one year of sales from a fictitious pizza restaurant, including order date, order time, pizza quantity, pizza size, price, category, and ingredients.

Raw CSV files included in `data/`:

- `orders.csv`
- `order_details.csv`
- `pizzas.csv`
- `pizza_types.csv`
- `data_dictionary.csv`

## ML Problem

The project predicts **daily pizza sales revenue** from historical sales patterns.

The model uses features such as:

- Daily orders
- Pizzas sold
- Average pizza price
- Lunch and dinner order activity
- Day of week
- Month
- Weekend flag
- Revenue lag features
- Rolling 7-day sales averages

## Project Structure

```text
pizza-sales-forecasting-ml/
|-- app.py
|-- data/
|   |-- orders.csv
|   |-- order_details.csv
|   |-- pizzas.csv
|   |-- pizza_types.csv
|   |-- data_dictionary.csv
|-- models/
|-- reports/
|-- src/
|   |-- pizza_sales/
|       |-- config.py
|       |-- data.py
|       |-- eda.py
|       |-- model.py
|       |-- predict.py
|       |-- train.py
|-- tests/
|   |-- test_data_pipeline.py
|-- requirements.txt
|-- README.md
|-- LICENSE
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

## Run EDA Summary

```bash
python -m src.pizza_sales.eda
```

This creates:

- `reports/eda_summary.json`

## Train Model

```bash
python -m src.pizza_sales.train
```

This creates:

- `data/daily_sales_features.csv`
- `models/daily_revenue_model.joblib`
- `models/feature_columns.json`
- `reports/metrics.json`

## Make a Forecast

```bash
python -m src.pizza_sales.predict --expected-orders 70 --expected-pizzas-sold 165
```

Example output:

```text
Forecast date: 2016-01-01
Predicted revenue: $2,950.42
```

## Run Streamlit App

```bash
streamlit run app.py
```

## Run Tests

```bash
pytest
```

## Resume Bullet

Built an end-to-end pizza sales forecasting project using real Maven Analytics sales data, pandas, scikit-learn, and Streamlit, including data merging, feature engineering, time-based model validation, revenue forecasting, model persistence, automated tests, and an interactive demo app.

## Business Use Case

A pizza shop manager can use this project to estimate upcoming daily revenue, understand sales patterns, and plan staffing or ingredient inventory more efficiently.
