from __future__ import annotations
import streamlit as st, pandas as pd
from utils.config import DATA_DIR, ASSETS_DIR
from utils import sheets as gs
from utils.data_update import run as run_update

st.set_page_config(page_title="Data Sources", page_icon="🌐", layout="wide")
st.logo(str(ASSETS_DIR / "logo_cp.svg"))

st.title("🌐 Data Sources & Sync")
st.write("Beheer materiaal-, machine-, en arbeidsdata. Sync met Google Sheets of update via scrapers/APIs.")

materials = pd.read_csv(DATA_DIR / "materials.csv")
machines = pd.read_csv(DATA_DIR / "machines.csv")
labor = pd.read_csv(DATA_DIR / "labor.csv")

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Materials")
    st.dataframe(materials, use_container_width=True)
with col2:
    st.subheader("Machines")
    st.dataframe(machines, use_container_width=True)
with col3:
    st.subheader("Labor")
    st.dataframe(labor, use_container_width=True)

st.divider()
st.subheader("🔄 Update actuele prijzen")
if st.button("Fetch latest (template)"):
    try:
        run_update()
        st.success("Update script uitgevoerd. Check materials.csv.")
    except Exception as e:
        st.error(f"Update failed: {e}")

st.divider()
st.subheader("🧩 Google Sheets Sync")
sid_m = st.text_input("Materials Sheet ID", value="")
if st.button("⬆️ Push materials -> Google Sheets"):
    try:
        gs.write_sheet(materials, sid_m or st.secrets["sheets"]["materials_sheet_id"])
        st.success("Materials geschreven naar Sheets.")
    except Exception as e:
        st.error(f"Schrijven mislukt: {e}")
