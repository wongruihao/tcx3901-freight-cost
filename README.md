# TCX3901 — Freight Cost Prediction (Group 6, Wong Rui Hao)

Exploratory data analysis dashboard for the Freight Cost problem in TCX3901 Industrial Practice (AY2026/27). Predicts freight value for an order (regression) and flags orders where freight is disproportionately high relative to order value (classification).

Contents
- join_tables.py — joins the five Olist tables and aggregates to order level
- app.py — Streamlit dashboard (4 views: freight_share distribution, freight by category, weight vs freight, freight by route)
- chart.py - builds each individual chart for visualisation
- freight_cost_working_dataset.csv — the order-level dataset the dashboard reads
- requirements.txt — Python packages needed to run the app
