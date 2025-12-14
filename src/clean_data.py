"""
Auto-converted from clean_data.ipynb.
This script was generated from notebook code cells.
"""

# --- Cell 1 ---
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import math

from typing import Optional, Dict, Any


# --- Cell 3 ---
df_search = pd.read_csv("../data/raw/steam_topsellers_raw.csv")
df_store  = pd.read_csv("../data/raw/steam_storefront_raw.csv")


# --- Cell 4 ---
# 1. Keep only appid + name from search results, then merge with API data
df_search_clean = df_search[["appid", "name"]].copy()
df = pd.merge(df_search_clean, df_store, on="appid", how="inner")

print("Rows after merge:", len(df))
df.head()


# --- Cell 5 ---
# 2. Drop rows without recommendation data (not useful for our analysis)
df = df.dropna(subset=["api_recommendations"])

# Convert recommendations to integer
df["api_recommendations"] = df["api_recommendations"].astype(int)

# 3. Rename columns for convenience
df = df.rename(
    columns={
        "api_recommendations": "recommendations",
        "api_is_free": "is_free",
        "api_price": "price",
        "api_primary_genre": "genre",
    }
)

# 4. Restrict to USD or missing currency (free games)
df = df[(df["api_currency"].isna()) | (df["api_currency"] == "USD")]

# 5. Handle missing values
df["price"] = df["price"].fillna(0.0)            # treat NaN price as 0 (free)
df["genre"] = df["genre"].fillna("Unknown")      # label missing genre as 'Unknown'
df["name"] = df["name"].fillna("Unknown title")  # just in case

# 6. Create a Free vs Paid label
df["free_or_paid"] = df["is_free"].map({True: "Free", False: "Paid"})

# 7. (Optional) Define a simple price-efficiency metric
#    This measures how many recommendations a game gets per dollar.
df["price_efficiency"] = df["recommendations"] / (df["price"] + 1)

print("Final number of rows:", len(df))
df.head()


# --- Cell 7 ---
import os
os.makedirs("data/processed", exist_ok=True)

df.to_csv("data/processed/steam_games_processed.csv", index=False)
print("Saved processed data to data/processed/steam_games_processed.csv")



def main() -> None:
    """Entry point for running as a script."""
    pass

if __name__ == "__main__":
    main()
