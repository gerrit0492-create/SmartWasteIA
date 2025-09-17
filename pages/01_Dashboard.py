from __future__ import annotations
import streamlit as st, pandas as pd
from pathlib import Path
from utils import calc
from utils.config import DATA_DIR, ASSETS_DIR

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.logo(str(ASSETS_DIR / "logo_cp.svg"))

st.title("📊 Dashboard")

@st.cache_data
def load_df(path: Path): return pd.read_csv(path)

materials = load_df(DATA_DIR / "materials.csv")
machines = load_df(DATA_DIR / "machines.csv")
labor = load_df(DATA_DIR / "labor.csv")
logistics = load_df(DATA_DIR / "logistics.csv")
bom = load_df(DATA_DIR / "bom_example.csv")

res = calc.compute_costs(bom, materials, machines, labor, logistics)
st.dataframe(res, use_container_width=True)
