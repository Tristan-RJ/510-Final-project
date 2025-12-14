from __future__ import annotations
from pathlib import Path
import pandas as pd

def ensure_dir(path: str | Path) -> Path:
    """Create directory if needed and return Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def read_csv(path: str | Path) -> pd.DataFrame:
    """Read CSV into DataFrame."""
    return pd.read_csv(path)

def write_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Write DataFrame to CSV (no index)."""
    p = Path(path)
    ensure_dir(p.parent)
    df.to_csv(p, index=False)
