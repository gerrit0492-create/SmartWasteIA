import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="BOM Upload & Live Sync", page_icon="📦", layout="wide")
st.title("📦 BOM Upload & Live Sync")

DATA_DIR = "data"
BOM_PATH = os.path.join(DATA_DIR, "bom_last.csv")

# Als er nog geen BOM in session_state zit → leeg DataFrame maken
if "bom_df" not in st.session_state:
    if os.path.exists(BOM_PATH):
        st.session_state["bom_df"] = pd.read_csv(BOM_PATH)
        st.info("📂 BOM geladen vanuit bestand (bom_last.csv).")
    else:
        st.session_state["bom_df"] = pd.DataFrame()

# Upload veld
uploaded_file = st.file_uploader("Upload je BOM (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state["bom_df"] = df
    df.to_csv(BOM_PATH, index=False)  # <-- Direct opslaan naar bestand
    st.success("✅ BOM succesvol ingeladen en opgeslagen!")
    st.dataframe(df)

# Toon huidige BOM als die bestaat
if not st.session_state["bom_df"].empty:
    st.subheader("📋 Huidige BOM")
    st.dataframe(st.session_state["bom_df"])

