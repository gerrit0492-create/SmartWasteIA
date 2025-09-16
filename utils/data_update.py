from __future__ import annotations
"""
Data updater: fetches latest materials prices (e.g., Outokumpu surcharge, LME proxy, supplier CSV)
and writes to /data/materials.csv or Google Sheets if configured.
This is a template; implement your real sources inside fetch_* functions.
"""
import os, csv, sys, time, json, datetime as dt
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
MATERIALS = DATA / "materials.csv"

def fetch_outokumpu_duplex_price() -> float | None:
    # Template scraper: please ensure legal compliance and robots.txt.
    try:
        url = "https://www.outokumpu.com/fi-fi/products/price-sheets"  # placeholder
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "html.parser")
        # TODO: parse the current surcharge. For now, return None to avoid false data.
        return None
    except Exception:
        return None

def fetch_generic_supplier_price(material_code: str) -> float | None:
    # Hook up to your supplier API or CSV here.
    return None

def run():
    df = pd.read_csv(MATERIALS)
    changed = False
    # Example: try to update duplex price if source == outokumpu
    for i, row in df.iterrows():
        if str(row.get("source","")).lower() == "outokumpu":
            price = fetch_outokumpu_duplex_price()
            if price:
                df.at[i, "eur_per_kg"] = price
                df.at[i, "last_update"] = dt.date.today().isoformat()
                changed = True
        else:
            # optionally update others via supplier hooks
            pass
    if changed:
        df.to_csv(MATERIALS, index=False)
        print("materials.csv updated.")
    else:
        print("No changes (template).")

if __name__ == "__main__":
    run()
