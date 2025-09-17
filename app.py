from __future__ import annotations
import streamlit as st
import pandas as pd
from pathlib import Path
from utils import calc
from utils.config import APP_NAME, DATA_DIR, ASSETS_DIR

st.set_page_config(page_title=f"{APP_NAME} • Dashboard", page_icon="📊", layout="wide")
st.logo(str(ASSETS_DIR / "logo_cp.svg"))
st.title("📊 SmartWasteIA — Dashboard")
st.caption("Live-sync costing with AI assist • EUR")

@st.cache_data
def load_df(path: Path):
    return pd.read_csv(path)

materials = load_df(DATA_DIR / "materials.csv")
machines = load_df(DATA_DIR / "machines.csv")
labor = load_df(DATA_DIR / "labor.csv")
logistics = load_df(DATA_DIR / "logistics.csv")
bom = load_df(DATA_DIR / "bom_example.csv")

res = calc.compute_costs(bom, materials, machines, labor, logistics)
sumx = calc.summarize(res)

c1,c2,c3,c4,c5,c6,c7,c8 = st.columns(8)
c1.metric("Lines", sumx["lines"])
c2.metric("Qty total", f"{sumx['qty_total']:.0f}")
c3.metric("Material €", f"{sumx.get('material_cost',0):.2f}")
c4.metric("Machine €", f"{sumx.get('machine_cost',0):.2f}")
c5.metric("Labor €", f"{sumx.get('labor_cost',0):.2f}")
c6.metric("Consumables €", f"{sumx.get('consumables_cost',0):.2f}")
c7.metric("Logistics €", f"{sumx.get('logistics_cost',0):.2f}")
c8.metric("Grand total €", f"{sumx.get('grand_total',0):.2f}")

st.divider()
st.subheader("BOM result")
st.dataframe(res, use_container_width=True)

st.page_link("pages/02_BOM_Upload.py", label="➡️ BOM Upload", icon="📤")
st.page_link("pages/03_Data_Sources.py", label="📡 Data Sources", icon="🌐")
st.page_link("pages/04_AI_Assist.py", label="🤖 AI Assist", icon="✨")
st.page_link("pages/06_Export_Data.py", label="📤 Export Data", icon="📈")
st.page_link("pages/05_Settings.py", label="⚙️ Settings", icon="🧩")
