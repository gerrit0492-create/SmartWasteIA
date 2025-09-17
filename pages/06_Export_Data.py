from __future__ import annotations
import streamlit as st, pandas as pd
from utils.config import DATA_DIR, ASSETS_DIR, get_secret
from utils import calc, sheets as gs

st.set_page_config(page_title="Data Export", page_icon="📤", layout="wide")
st.logo(str(ASSETS_DIR / "logo_cp.svg"))

st.title("📤 Data Export — Google Sheets & Power BI")

# Load BOM en referentiedata
try:
    bom = pd.read_csv(DATA_DIR / "bom_example.csv")
    materials = pd.read_csv(DATA_DIR / "materials.csv")
    machines = pd.read_csv(DATA_DIR / "machines.csv")
    labor = pd.read_csv(DATA_DIR / "labor.csv")
    logistics = pd.read_csv(DATA_DIR / "logistics.csv")
except FileNotFoundError:
    st.error("BOM of referentiedata niet gevonden. Zorg dat alles in de /data map staat.")
    st.stop()

# Kostenberekening uitvoeren
result = calc.compute_costs(bom, materials, machines, labor, logistics)

st.subheader("Kostenoverzicht")
st.dataframe(result, use_container_width=True)

st.download_button(
    label="⬇️ Download voor Power BI (CSV)",
    data=result.to_csv(index=False).encode("utf-8"),
    file_name="cost_data_powerbi.csv",
    mime="text/csv"
)

st.divider()
st.subheader("Exporteer naar Google Sheets")
sheet_id = st.text_input("Google Sheet ID", value=get_secret("sheets.price_history_sheet_id", ""))

if st.button("📤 Exporteer naar Google Sheets"):
    if not sheet_id:
        st.error("Voer een geldige Google Sheet ID in.")
    else:
        try:
            gs.write_sheet(result, sheet_id)
            st.success(f"Data succesvol geëxporteerd naar Google Sheets: {sheet_id}")
        except Exception as e:
            st.error(f"Export mislukt: {e}")
