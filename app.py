import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_URL = "http://localhost:8000"   # change to deployed URL after deploy

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Real-Time Sales Dashboard")
st.caption("Powered by FastAPI + Plotly + Streamlit")

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
@st.cache_data(ttl=60)
def fetch(endpoint: str) -> dict | list:
    resp = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
    resp.raise_for_status()
    return resp.json()

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
st.subheader("Key Metrics")
try:
    summary = fetch("/summary")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Revenue",    f"${summary['total_revenue']:,.0f}")
    c2.metric("Total Profit",     f"${summary['total_profit']:,.0f}")
    c3.metric("Total Orders",     f"{summary['total_orders']:,}")
    c4.metric("Avg Order Value",  f"${summary['avg_order_value']:,.2f}")
    c5.metric("Avg Profit Margin",f"{summary['avg_profit_margin']}%")
except Exception as e:
    st.error(f"Could not load summary: {e}")

st.divider()

# ---------------------------------------------------------------------------
# Monthly trend
# ---------------------------------------------------------------------------
st.subheader("Monthly Revenue & Profit Trend")
try:
    trend_data = fetch("/monthly-trend")
    trend_df   = pd.DataFrame(trend_data)
    fig_trend  = px.line(
        trend_df, x="Month", y=["revenue", "profit"],
        labels={"value": "USD", "variable": "Metric"},
        color_discrete_map={"revenue": "#636EFA", "profit": "#00CC96"},
    )
    fig_trend.update_layout(xaxis_tickangle=-45, legend_title="")
    st.plotly_chart(fig_trend, use_container_width=True)
except Exception as e:
    st.error(f"Could not load trend: {e}")

st.divider()

# ---------------------------------------------------------------------------
# Top products + Regional breakdown (side by side)
# ---------------------------------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 Products by Revenue")
    try:
        n = st.slider("Number of products", 5, 20, 10, key="top_n")
        products_df = pd.DataFrame(fetch(f"/top-products?n={n}"))
        fig_products = px.bar(
            products_df.sort_values("revenue"),
            x="revenue", y="Product Name",
            orientation="h",
            labels={"revenue": "Revenue (USD)"},
            color="revenue",
            color_continuous_scale="Blues",
        )
        fig_products.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig_products, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load products: {e}")

with col_right:
    st.subheader("Sales by Region")
    try:
        regional_df = pd.DataFrame(fetch("/regional-breakdown"))
        fig_pie = px.pie(
            regional_df, values="revenue", names="Region",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        st.dataframe(
            regional_df.rename(columns={"revenue":"Revenue","profit":"Profit","orders":"Orders"})
                       .set_index("Region")
                       .style.format({"Revenue": "${:,.0f}", "Profit": "${:,.0f}"}),
            use_container_width=True,
        )
    except Exception as e:
        st.error(f"Could not load regional data: {e}")

st.divider()

# ---------------------------------------------------------------------------
# Category breakdown
# ---------------------------------------------------------------------------
st.subheader("Revenue & Profit by Category")
try:
    cat_df   = pd.DataFrame(fetch("/category-breakdown"))
    fig_cat  = px.bar(
        cat_df, x="Category", y=["revenue", "profit"],
        barmode="group",
        labels={"value": "USD", "variable": "Metric"},
        color_discrete_map={"revenue": "#636EFA", "profit": "#00CC96"},
    )
    st.plotly_chart(fig_cat, use_container_width=True)
except Exception as e:
    st.error(f"Could not load category data: {e}")

st.divider()

# ---------------------------------------------------------------------------
# Forecast
# ---------------------------------------------------------------------------
st.subheader("Sales Forecast")
try:
    days        = st.slider("Forecast horizon (days)", 7, 90, 30)
    forecast_df = pd.DataFrame(fetch(f"/forecast?days={days}"))
    forecast_df["ds"] = pd.to_datetime(forecast_df["ds"])

    fig_fc = px.line(forecast_df, x="ds", y="yhat", labels={"ds": "Date", "yhat": "Predicted Sales (USD)"})
    fig_fc.add_scatter(
        x=forecast_df["ds"], y=forecast_df["yhat_upper"],
        mode="lines", line=dict(width=0), showlegend=False,
    )
    fig_fc.add_scatter(
        x=forecast_df["ds"], y=forecast_df["yhat_lower"],
        mode="lines", line=dict(width=0),
        fill="tonexty", fillcolor="rgba(99,110,250,0.15)",
        name="95% confidence",
    )
    st.plotly_chart(fig_fc, use_container_width=True)
except Exception as e:
    st.error(f"Could not load forecast: {e}")

st.divider()
st.caption("Project: Real-Time Sales Dashboard | Stack: FastAPI · pandas · scikit-learn · Streamlit · Plotly")
