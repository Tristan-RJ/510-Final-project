from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
from .io import ensure_dir

def save_fig(out_path: str | Path, dpi: int = 300) -> None:
    """Save current matplotlib figure and close it."""
    out_path = Path(out_path)
    ensure_dir(out_path.parent)
    plt.savefig(out_path, dpi=dpi, bbox_inches='tight')
    plt.close()
