"""
Auto-converted from run_analysis.ipynb.
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
df = pd.read_csv("../data/processed/steam_games_processed.csv")


# --- Cell 4 ---
# Check how many free vs paid games we have
df["free_or_paid"].value_counts()


# --- Cell 5 ---
# Basic summary statistics for numeric columns
df[["recommendations", "price", "price_efficiency"]].describe()



def main() -> None:
    """Entry point for running as a script."""
    pass

if __name__ == "__main__":
    main()
