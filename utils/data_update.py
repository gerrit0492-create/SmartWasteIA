from __future__ import annotations
"""
Template updater: plug real sources (e.g., Outokumpu surcharge pages, supplier CSV/API).
"""
import datetime as dt, pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
MATERIALS = DATA / "materials.csv"

def run():
    df = pd.read_csv(MATERIALS)
    # Example: trivial update of last_update timestamp (replace with your logic)
    df["last_update"] = dt.date.today().isoformat()
    df.to_csv(MATERIALS, index=False)
    print("materials.csv timestamps refreshed")

if __name__ == "__main__":
    run()
