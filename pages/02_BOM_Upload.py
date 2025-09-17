import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="BOM Upload & Live Sync", page_icon="📦", layout="wide")
st.title("📦 BOM Upload & Live Sync")

DATA_DIR = "data"
BOM_FILE = os.path.join(DATA_DIR, "bom_example.csv")

# Kolommen die minimaal verwacht worden
REQUIRED_COLUMNS = [
    "item_code", "description", "qty", "unit", "material_code",
    "unit_price_eur", "machine_code", "process_time_min_machine",
    "machine_time_est_min", "machine_setup_min", "labor_grade", "markup_pct"
]

# Standaardwaarden voor ontbrekende kolommen
DEFAULT_VALUES = {
    "process_time_min_machine": 0,
    "machine_time_est_min": 0,
    "machine_setup_min": 0,
    "markup_pct": 0,
    "unit_price_eur": 0,
    "qty": 1
}

def load_bom(file_path):
    try:
        df = pd.read_csv(file_path, encoding="utf-8", sep=",")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="latin1", sep=",")  # fallback voor speciale tekens

    # Ontbrekende kolommen toevoegen met defaultwaarden
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = DEFAULT_VALUES.get(col, "")

    return df[REQUIRED_COLUMNS]

# Upload via Streamlit
uploaded_file = st.file_uploader("Upload je BOM (CSV)", type=["csv"])

if uploaded_file:
    bom_df = load_bom(uploaded_file)
    st.success("BOM succesvol ingeladen!")
    st.dataframe(bom_df)
else:
    # Testbestand gebruiken als er geen upload is
    if os.path.exists(BOM_FILE):
        bom_df = load_bom(BOM_FILE)
        st.info("Voorbeeld-BOM geladen (geen upload).")
        st.dataframe(bom_df)
    else:
        st.warning("Nog geen BOM geladen. Upload een bestand of voeg bom_example.csv toe.")
