import pandas as pd
import os

def load_data(path: str = "data/superstore.csv") -> pd.DataFrame:
    """
    Load and clean the Superstore sales dataset.
    Download from: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
    Save as data/superstore.csv
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at '{path}'.\n"
            "Download from: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final\n"
            "and save it as data/superstore.csv"
        )

    df = pd.read_csv(path, encoding="latin-1")

    # Parse dates
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=False)
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=False)

    # Drop rows missing critical fields
    df.dropna(subset=["Sales", "Order Date", "Product Name", "Region"], inplace=True)

    # Derived columns
    df["Year"]  = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Profit Margin"] = (df["Profit"] / df["Sales"].replace(0, float("nan"))).fillna(0)

    return df
