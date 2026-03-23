import pandas as pd
from typing import Any


def get_summary(df: pd.DataFrame) -> dict[str, Any]:
    """High-level KPIs for the /summary endpoint."""
    return {
        "total_revenue":    round(float(df["Sales"].sum()), 2),
        "total_profit":     round(float(df["Profit"].sum()), 2),
        "total_orders":     int(df["Order ID"].nunique()),
        "total_customers":  int(df["Customer ID"].nunique()),
        "avg_order_value":  round(float(df["Sales"].mean()), 2),
        "avg_profit_margin":round(float(df["Profit Margin"].mean() * 100), 2),
        "top_category":     str(df.groupby("Category")["Sales"].sum().idxmax()),
        "top_region":       str(df.groupby("Region")["Sales"].sum().idxmax()),
    }


def get_top_products(df: pd.DataFrame, n: int = 10) -> list[dict]:
    """Top N products by total revenue."""
    return (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
        .rename(columns={"Sales": "revenue"})
        .round(2)
        .to_dict(orient="records")
    )


def get_regional_breakdown(df: pd.DataFrame) -> list[dict]:
    """Sales and profit breakdown by region."""
    return (
        df.groupby("Region")
        .agg(revenue=("Sales", "sum"), profit=("Profit", "sum"), orders=("Order ID", "nunique"))
        .reset_index()
        .round(2)
        .to_dict(orient="records")
    )


def get_monthly_trend(df: pd.DataFrame) -> list[dict]:
    """Monthly revenue trend for the line chart."""
    trend = (
        df.groupby("Month")
        .agg(revenue=("Sales", "sum"), profit=("Profit", "sum"))
        .reset_index()
        .sort_values("Month")
        .round(2)
    )
    return trend.to_dict(orient="records")


def get_category_breakdown(df: pd.DataFrame) -> list[dict]:
    """Revenue and profit by product category."""
    return (
        df.groupby("Category")
        .agg(revenue=("Sales", "sum"), profit=("Profit", "sum"))
        .reset_index()
        .round(2)
        .to_dict(orient="records")
    )
