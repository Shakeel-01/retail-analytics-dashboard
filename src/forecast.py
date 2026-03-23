import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def train_forecast(df: pd.DataFrame, periods: int = 30) -> list[dict]:
    """
    Forecast daily sales for the next `periods` days using linear regression
    on date ordinals + 7-day rolling average as a feature.

    Uses sklearn so there are no heavy optional dependencies.
    Swap for Prophet if you want seasonality decomposition:

        from prophet import Prophet
        daily = df.groupby("Order Date")["Sales"].sum().reset_index()
        daily.columns = ["ds", "y"]
        m = Prophet(); m.fit(daily)
        future = m.make_future_dataframe(periods=periods)
        fc = m.predict(future)
        return fc[["ds","yhat","yhat_lower","yhat_upper"]].tail(periods).to_dict(orient="records")
    """
    daily = (
        df.groupby("Order Date")["Sales"]
        .sum()
        .reset_index()
        .rename(columns={"Order Date": "ds", "Sales": "y"})
        .sort_values("ds")
    )

    daily["ordinal"]    = daily["ds"].map(pd.Timestamp.toordinal)
    daily["rolling7"]   = daily["y"].rolling(7, min_periods=1).mean()

    X = daily[["ordinal", "rolling7"]].values
    y = daily["y"].values

    model = LinearRegression()
    model.fit(X, y)

    last_date    = daily["ds"].max()
    last_rolling = float(daily["rolling7"].iloc[-1])
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=periods)

    results = []
    rolling_val = last_rolling
    for d in future_dates:
        ordinal = d.toordinal()
        yhat    = float(model.predict([[ordinal, rolling_val]])[0])
        yhat    = max(0.0, yhat)            # sales can't be negative
        std     = float(np.std(y - model.predict(X)))
        results.append({
            "ds":         d.strftime("%Y-%m-%d"),
            "yhat":       round(yhat, 2),
            "yhat_lower": round(max(0.0, yhat - 1.96 * std), 2),
            "yhat_upper": round(yhat + 1.96 * std, 2),
        })
        rolling_val = (rolling_val * 6 + yhat) / 7   # update rolling estimate

    return results
