# Project Name: Analyzing Player Activity and Recommendation Efficiency of Top Steam Games
# Group members: Jiahang Liu (student id: 7071108622) & Renjie Huang(students id: 1626544075)

# 
If any of the individual .py files fail to run, we’ve included a complete, end-to-end version of the project in src/510final_complete_project.ipynb.

## Project overview
This project collects a snapshot of **Steam Store “Top Sellers”** games and enriches each game with metadata from the **Steam Storefront API**.  
We then clean and merge the data, compute a simple “price efficiency” metric, run basic descriptive analysis, and generate visualizations.

**Core metric**
- `price_efficiency = recommendations / (price + 1)`  
  (The `+ 1` avoids division-by-zero for free games while keeping comparisons consistent.)

---

## Requirements
- Python **3.10+** recommended
- Internet access (data is collected live from Steam)
- Pip packages are listed in `requirements.txt`:

```txt
requests
beautifulsoup4
pandas
numpy
matplotlib
seaborn
```

---

## Installation
1) **Clone / download** this project folder.

2) (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

3) Install dependencies:

```bash
pip install -r requirements.txt
```

---

## How to run the code
This project is implemented in the Jupyter notebook:

- `510final+docstringtypehints.ipynb`

### Option A: Run in Jupyter Lab / Notebook
```bash
pip install jupyter
jupyter lab
```
Open `510final+docstringtypehints.ipynb`, then **Run All** (or run cells top-to-bottom).

### Option B: Run in VS Code
Open the notebook in VS Code and run cells in order with a Python interpreter that has the requirements installed.

---

## How to get the data
The notebook gathers data in **two steps**:

### 1) Scrape Steam “Top Sellers” search pages (HTML)
- Function: `scrape_steam_topsellers(n_pages=10)`
- Output: a DataFrame with at least:
  - `appid` (Steam app ID)
  - `name`
  - `search_price_raw` (price text shown on the page)

**Note:** This is scraping public HTML. Steam may change their page structure, which can break the scraper.

### 2) Query Steam Storefront API for each appid (JSON)
- Function: `fetch_storefront_info(appid)`
- Batched via: `fetch_storefront_for_df(df_search)`
- Output fields include:
  - `api_recommendations`
  - `api_is_free`
  - `api_price`
  - `api_currency`
  - `api_primary_genre`

**No API key is required** for the Storefront endpoint used in this project.

**Politeness / rate limiting**
- The notebook includes `time.sleep(...)` delays to reduce request load.

---

## How the data is cleaned (merge + cleaning steps)
After collection, the notebook performs these cleaning steps:

1) **Merge datasets**
- Merge search results (`df_search`) with API results (`df_store`) on `appid`.

2) **Drop unusable rows**
- Remove rows missing `api_recommendations` (these are not useful for the analysis).

3) **Rename columns for convenience**
- `api_recommendations → recommendations`
- `api_is_free → is_free`
- `api_price → price`
- `api_primary_genre → genre`

4) **Currency filtering**
- Keep **USD** entries (and allow missing currency for free games).

5) **Handle missing values**
- Fill missing `price` as `0.0`
- Fill missing `genre` as `"Unknown"`
- Fill missing `name` as `"Unknown title"` (rare)

6) **Create derived labels/metrics**
- `free_or_paid` label from `is_free`
- `price_efficiency = recommendations / (price + 1)`

7) **Optional plotting stabilizers**
For some plots, the notebook clips extreme values:
- Clip `price_efficiency` at the **99th percentile** for paid games to reduce the influence of extreme outliers.

---

## How to run the analysis
The analysis is descriptive and includes:
- Counts of **Free vs Paid** games
- Summary statistics (`describe()`) for:
  - `recommendations`, `price`, `price_efficiency`
- Comparisons of distributions across:
  - free vs paid
  - genres
  - price ranges (bins)

Because Steam Top Sellers changes frequently, results are **time-dependent** and may differ across runs.

---

## How to produce the visualizations
All visualizations are generated in the notebook using Matplotlib/Seaborn with `plt.show()`:

1) **Scatter:** `price` vs `recommendations` (paid games only)
2) **Boxplot:** `recommendations` by `free_or_paid` (Free vs Paid)
3) **Boxplot:** `price_efficiency` across top genres
4) **Histograms:** `price_efficiency` distributions by price bins
5) **Genre panels:** `price` vs `price_efficiency` (with a simple linear fit) by genre

If you want to **save** figures instead of showing them, replace `plt.show()` with:
```python
plt.savefig("outputs/figure_name.png", dpi=300, bbox_inches="tight")
```
(Ensure an `outputs/` folder exists.)

---

## Project structure
A minimal structure for submission:

```
.
├── 510final+docstringtypehints.ipynb
├── requirements.txt
└── README.md
```

(If you add saved outputs: `outputs/`)

---

## Notes / troubleshooting
- If requests are blocked or slow, try:
  - Running again later
  - Increasing delays (`time.sleep`)
  - Confirming you have a working internet connection
- If scraping returns empty results:
  - Steam page layout may have changed; inspect HTML and update selectors.

---

## Acknowledgements
- Data sources: Steam Store (Top Sellers) and Steam Storefront API.
