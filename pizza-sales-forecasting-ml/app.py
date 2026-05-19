from __future__ import annotations

import json

import streamlit as st

from src.pizza_sales.config import METRICS_PATH, MODEL_PATH
from src.pizza_sales.predict import forecast_next_day


st.set_page_config(page_title="Pizza Sales Forecasting", layout="centered")

st.title("Pizza Sales Forecasting")
st.caption("Predict next-day revenue using the Maven Pizza Place Sales dataset.")

if not MODEL_PATH.exists():
    st.warning("Model artifact not found. Run `python -m src.pizza_sales.train` first.")
    st.stop()

expected_orders = st.number_input("Expected orders", min_value=1, max_value=300, value=60)
expected_pizzas = st.number_input("Expected pizzas sold", min_value=1, max_value=500, value=140)

if st.button("Forecast revenue", type="primary"):
    date, revenue = forecast_next_day(expected_orders=int(expected_orders), expected_pizzas_sold=int(expected_pizzas))
    st.metric(f"Predicted revenue for {date.date()}", f"${revenue:,.2f}")

if METRICS_PATH.exists():
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    st.subheader("Model metrics")
    st.json(metrics)
