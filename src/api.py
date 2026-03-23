from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.loader import load_data
from src.analysis import (
    get_summary,
    get_top_products,
    get_regional_breakdown,
    get_monthly_trend,
    get_category_breakdown,
)
from src.forecast import train_forecast

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Sales Dashboard API",
    description="REST API powering the Real-Time Sales Dashboard project.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load once at startup
try:
    df = load_data()
except FileNotFoundError as e:
    raise RuntimeError(str(e))

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    """Health check."""
    return {"status": "ok", "message": "Sales Dashboard API is running."}


@app.get("/summary", tags=["Analytics"])
def summary():
    """Top-level KPIs: revenue, profit, orders, customers, margins."""
    return get_summary(df)


@app.get("/top-products", tags=["Analytics"])
def top_products(n: int = Query(default=10, ge=1, le=50)):
    """Top N products by total revenue."""
    return get_top_products(df, n)


@app.get("/regional-breakdown", tags=["Analytics"])
def regional_breakdown():
    """Revenue, profit, and order count broken down by region."""
    return get_regional_breakdown(df)


@app.get("/monthly-trend", tags=["Analytics"])
def monthly_trend():
    """Month-by-month revenue and profit trend."""
    return get_monthly_trend(df)


@app.get("/category-breakdown", tags=["Analytics"])
def category_breakdown():
    """Revenue and profit by product category."""
    return get_category_breakdown(df)


@app.get("/forecast", tags=["Forecasting"])
def forecast(days: int = Query(default=30, ge=7, le=90)):
    """
    Predict daily sales for the next N days (7–90).
    Returns: ds, yhat, yhat_lower, yhat_upper.
    """
    return train_forecast(df, days)
