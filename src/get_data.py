"""
Auto-converted from get_data.ipynb.
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
# Use a browser-like User-Agent to avoid being blocked by Steam
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


# --- Cell 5 ---
def scrape_steam_topsellers(n_pages: int = 10) -> pd.DataFrame:
    """
    Scrape the Steam Store 'Top Sellers' search pages.

    Parameters
    ----------
    n_pages : int, optional
        Number of pages to scrape (page=1, 2, ..., n_pages).
        Each page contains a list of top-selling games.

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per game and the following columns:
        - 'appid' : int
            Steam application ID of the game.
        - 'name' : str or None
            Game title as shown on the search page.
        - 'search_price_raw' : str
            Raw price text displayed on the search page
            (e.g., "Free To Play", "$29.99", "$59.99 $39.99").
    """
    rows = []

    for page in range(1, n_pages + 1):
        url = f"https://store.steampowered.com/search/?filter=topsellers&page={page}"
        print("Fetching:", url)

        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print("  -> Status code", resp.status_code, "- skipping this page.")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        # Each search result is an <a> tag with this class
        for a in soup.select("a.search_result_row"):
            appid = a.get("data-ds-appid")
            if not appid:   # bundles / ads etc.
                continue

            try:
                appid = int(appid)
            except ValueError:
                continue

            # Game title
            name_tag = a.find("span", class_="title")
            name = name_tag.get_text(strip=True) if name_tag else None

            # Raw price text shown on the search page (for reference only)
            price_tag = a.find("div", class_="search_price")
            price_text = price_tag.get_text(" ", strip=True) if price_tag else ""

            rows.append(
                {
                    "appid": appid,
                    "name": name,
                    "search_price_raw": price_text,
                }
            )
        time.sleep(1)

    df = pd.DataFrame(rows).drop_duplicates("appid")
    return df


# run scraper
df_search = scrape_steam_topsellers(n_pages=10)
print("Number of rows in df_search:", len(df_search))
df_search.head()


# --- Cell 7 ---
def fetch_storefront_info(appid: int, max_retries: int = 3) -> Optional[Dict[str, Any]]:
    """
    Fetch detailed game information from the Steam Storefront API
    for a single Steam appid.

    Parameters
    ----------
    appid : int
        Steam application ID to query.
    max_retries : int, optional
        Maximum number of retry attempts in case of network errors.

    Returns
    -------
    dict or None
        If successful, returns a dictionary with selected fields:
        - 'appid' : int
        - 'api_recommendations' : int or None
            Total number of recommendations (overall review count).
        - 'api_is_free' : bool
            Whether the game is free-to-play.
        - 'api_price' : float
            Final price in currency units (e.g., USD), 0.0 for free or missing.
        - 'api_currency' : str or None
            Currency code such as "USD", or None for free titles.
        - 'api_primary_genre' : str or None
            Description of the primary genre (first entry in the genre list).
        Returns None if the API call fails or the appid is not successful.
    """
    url = "https://store.steampowered.com/api/appdetails"
    params = {"appids": appid}

    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
            data_all = resp.json()
            data = data_all.get(str(appid), {})
            if not data.get("success", False):
                return None

            info = data.get("data", {})

            # Total recommendations (overall review count)
            rec = info.get("recommendations", {}).get("total", None)

            # Free or paid
            is_free = info.get("is_free", False)

            # Price in currency units (e.g., USD), usually given in cents
            price = 0.0
            currency = None
            if not is_free and "price_overview" in info:
                po = info["price_overview"]
                price = po.get("final", 0) / 100.0
                currency = po.get("currency")

            # Primary genre (first entry)
            genres = info.get("genres", [])
            primary_genre = genres[0]["description"] if genres else None

            return {
                "appid": appid,
                "api_recommendations": rec,
                "api_is_free": is_free,
                "api_price": price,
                "api_currency": currency,
                "api_primary_genre": primary_genre,
            }
        except Exception as e:
            print(f"Error fetching {appid} (attempt {attempt+1}):", e)
            time.sleep(2)

    return None


# --- Cell 9 ---
def fetch_storefront_for_df(df_search: pd.DataFrame) -> pd.DataFrame:
    """
    Fetch Steam Storefront API information for all appids contained
    in a search result DataFrame.

    Parameters
    ----------
    df_search : pandas.DataFrame
        DataFrame that must contain an 'appid' column with integer IDs
        (for example, the output of `scrape_steam_topsellers`).

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per appid and the following columns:
        - 'appid'
        - 'api_recommendations'
        - 'api_is_free'
        - 'api_price'
        - 'api_currency'
        - 'api_primary_genre'
        Only appids for which the API call succeeds are included.
    """
    records: list[Dict[str, Any]] = []
    appids = df_search["appid"].tolist()
    total = len(appids)

    for i, appid in enumerate(appids, start=1):
        print(f"[{i}/{total}] Fetching appid {appid}")
        info = fetch_storefront_info(appid)
        if info is not None:
            records.append(info)
        # Be polite
        time.sleep(0.5)

    return pd.DataFrame(records)


# run API collection
df_store = fetch_storefront_for_df(df_search)
print("Number of rows in df_store:", len(df_store))
df_store.head()


# --- Cell 11 ---
df_search.to_csv("data/raw/steam_topsellers_raw.csv", index=False)
df_store.to_csv("data/raw/steam_storefront_raw.csv", index=False)



def main() -> None:
    """Entry point for running as a script."""
    pass

if __name__ == "__main__":
    main()
