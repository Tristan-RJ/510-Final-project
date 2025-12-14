"""
Auto-converted from Visualization.ipynb.
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
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("../data/processed/steam_games_processed.csv")

# 1) Scatter plot: price vs recommendations (paid games only)
df_paid = df[df["free_or_paid"] == "Paid"].copy()

plt.figure(figsize=(6, 4))
sns.scatterplot(data=df_paid, x="price", y="recommendations")
plt.xlabel("Price (USD)")
plt.ylabel("Total recommendations")
plt.title("Price vs. recommendations (paid games)")
plt.tight_layout()
plt.show()


# --- Cell 4 ---
# 2) Boxplot: Free vs Paid recommendations
plt.figure(figsize=(5, 4))
sns.boxplot(data=df, x="free_or_paid", y="recommendations")
plt.xlabel("")
plt.ylabel("Total recommendations")
plt.title("Recommendations: Free vs. Paid games")
plt.tight_layout()
plt.show()


# --- Cell 5 ---
# 3) Boxplot: price_efficiency by genre
top_genres = df["genre"].value_counts().head(5).index
df_top_genres = df[df["genre"].isin(top_genres)].copy()

plt.figure(figsize=(8, 4))
sns.boxplot(data=df_top_genres, x="genre", y="price_efficiency")
plt.xlabel("Genre")
plt.ylabel("Price efficiency (recommendations per dollar)")
plt.title("Price efficiency by genre (top 5 genres)")
plt.tight_layout()
plt.show()


# --- Cell 6 ---
# Histogram: Distribution of efficiency values to illustrate how recommendation behavior varies across games prices.
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["price_efficiency"] = pd.to_numeric(df["price_efficiency"], errors="coerce")
df_paid = df[df["price"] > 0].copy()
pe_99 = df_paid["price_efficiency"].quantile(0.99)
df_paid["price_efficiency_clipped"] = df_paid["price_efficiency"].clip(upper=pe_99)

# Define price bins
bins = [0, 5, 10, 20, 40, 1000]
labels = ["$0-5", "$5-10", "$10-20", "$20-40", "$40+"]

df_paid["price_bin"] = pd.cut(
    df_paid["price"],
    bins=bins,
    labels=labels,
    right=False
)

# Grid setup
n = len(labels)
ncols = 3
nrows = math.ceil(n / ncols)

fig, axes = plt.subplots(nrows, ncols, figsize=(12, 3.2 * nrows), sharex=True, sharey=True)
axes = axes.flatten()

for i, label in enumerate(labels):
    ax = axes[i]
    sub = df_paid[df_paid["price_bin"] == label]
    ax.hist(sub["price_efficiency_clipped"].dropna(), bins=20)
    ax.set_title(f"{label} (n={len(sub)})")
    ax.set_xlabel("Price efficiency")
    ax.set_ylabel("Count")

# Hide unused axes
for j in range(i + 1, len(axes)):
    axes[j].axis("off")

fig.suptitle("Price efficiency distributions by price ranges", y=1.02, fontsize=12)
plt.tight_layout()
plt.show()


print("This figure presents a set of histograms showing the distribution of price efficiency across five price ranges: $0–5, $5–10, $10–20, $20–40, and $40+. Sample sizes are meaningful in most bins (n=9, 18, 42, 44, 25), which provides a reasonable basis for comparing distributional patterns across pricing tiers. The purpose of this analysis is to evaluate whether recommendation behavior (as summarized by price efficiency) varies systematically with price, and to identify whether lower- or higher-priced games tend to deliver greater “recommendation impact per dollar.")
print("Strong right-skew across all price categories Across every price band, the histograms show highly right-skewed distributions. The mass of observations clusters near low price efficiency values, while a small subset of games exhibits very large efficiency. This pattern indicates that most games generate modest recommendation efficiency, while a limited number of titles produce exceptionally high performance relative to price. The presence of extreme values suggests that price efficiency is likely influenced by game-specific factors such as franchise popularity.")
print("The persistent right-skew across every tier indicates that price alone is insufficient to explain recommendation efficiency. While there may be mild differences in tail behavior across categories, the overall structure suggests that game quality, community effects, and genre-specific dynamics likely drive variation more strongly than price.")


# --- Cell 7 ---
# Price vs efficiency by genre (scatter + simple linear fit) Plot the relationship between prices and recommendation efficiency in different genre to see whether recommendation efficiency is positively related to prices across different genres.
top_genres = df_paid["genre"].value_counts().head(6).index
df_g = df_paid[df_paid["genre"].isin(top_genres)].copy()

n = len(top_genres)
ncols = 3
nrows = math.ceil(n / ncols)

fig, axes = plt.subplots(nrows, ncols, figsize=(12, 3.4 * nrows), sharey=True)
axes = axes.flatten()

for i, genre in enumerate(top_genres):
    ax = axes[i]
    sub = df_g[df_g["genre"] == genre].dropna(subset=["price", "price_efficiency_clipped"])

    # Scatter
    ax.scatter(sub["price"], sub["price_efficiency_clipped"], s=12, alpha=0.6)

    # Simple linear fit line (only if enough points)
    if len(sub) >= 2:
        x = sub["price"].to_numpy()
        y = sub["price_efficiency_clipped"].to_numpy()

        # Fit
        slope, intercept = np.polyfit(x, y, 1)

        xs = np.linspace(x.min(), x.max(), 50)
        ys = intercept + slope * xs
        ax.plot(xs, ys)

        ax.text(
            0.05, 0.95,
            f"slope={slope:.3f}",
            transform=ax.transAxes,
            va="top"
        )

    ax.set_title(f"{genre} (n={len(sub)})")
    ax.set_xlabel("Price ($)")
    ax.set_ylabel("Price efficiency")

# Hide unused axes
for j in range(i + 1, len(axes)):
    axes[j].axis("off")

fig.suptitle("Price vs. price efficiency by genre (paid games)", y=1.02, fontsize=12)
plt.tight_layout()
plt.show()
print("In smaller genres—Simulation (n=10), Indie (n=8), RPG (n=8), Adventure (n=8), and Casual (n=7)—the fitted lines suggest heterogeneous relationships. Indie, RPG, and Casual appear to show relatively steep negative slopes, while Adventure shows a mild positive slope. However, given the limited observations, these slopes may be sensitive to a few influential points and should be interpreted cautiously.")
print("Overall, this figure provides evidence that higher prices are associated with higher price efficiency across genres. Instead, the dominant pattern suggests that higher-priced titles tend to yield lower recommendations per dollar")



def main() -> None:
    """Entry point for running as a script."""
    pass

if __name__ == "__main__":
    main()
