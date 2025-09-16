from __future__ import annotations
import streamlit as st, pandas as pd, io, time
from utils.config import DATA_DIR, ASSETS_DIR, get_secret
from utils import calc
from utils import sheets as gs

st.set_page_config(page_title="BOM Upload", page_icon="📤", layout="wide")
st.logo(str(ASSETS_DIR / "logo_cp.svg"))
st.title("📤 BOM Upload & Live Sync")

tab1, tab2 = st.tabs(["Upload CSV", "Google Sheets Live"])

with tab1:
    st.write("Upload een CSV met minimaal de kolommen: item_code, description, qty, unit, material_code, unit_price_eur, machine_code, process_time_min_machine, labor_grade, process_time_min_labor, markup_pct.")
    f = st.file_uploader("Kies CSV", type=["csv"])
    if f:
        df = pd.read_csv(f)
        st.dataframe(df.head(100), use_container_width=True)
        st.session_state["bom_df"] = df

with tab2:
    sid = st.text_input("Google Sheet ID", value=get_secret("sheets.bom_sheet_id",""))
    ws = st.text_input("Worksheet (tab) naam, leeg = eerste", value="")
    auto = st.toggle("Auto-refresh elke 30s", value=True)
    if st.button("🔄 Lees nu"):
        try:
            df = gs.read_sheet(sid, worksheet=ws or None)
            st.session_state["bom_df"] = df
            st.success(f"Ingeladen: {len(df)} rijen")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Kon sheet niet lezen: {e}")
    if auto and sid:
        st.caption("Auto-refresh actief.")
        st.experimental_data_editor  # no-op to keep session alive
        st.autorefresh = st.experimental_rerun

st.divider()

if "bom_df" in st.session_state:
    # Load refs
    mats = pd.read_csv(DATA_DIR / "materials.csv")
    macs = pd.read_csv(DATA_DIR / "machines.csv")
    lab = pd.read_csv(DATA_DIR / "labor.csv")
    logi = pd.read_csv(DATA_DIR / "logistics.csv")
    out = calc.compute_costs(st.session_state["bom_df"], mats, macs, lab, logi)
    st.subheader("Resultaat")
    st.dataframe(out, use_container_width=True)
    st.download_button("⬇️ Exporteer resultaat (CSV)", data=out.to_csv(index=False).encode("utf-8"),
                       file_name="bom_costed.csv", mime="text/csv")
else:
    st.info("Nog geen BOM geladen.")
