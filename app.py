import streamlit as st
import pandas as pd
from utils.config import show_logo, get_text

# ------------------------------
# Pagina configuratie
# ------------------------------
st.set_page_config(
    page_title="BOM App v1.0",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# Logo en titel
# ------------------------------
show_logo()
st.title(get_text("home_title"))

st.markdown("---")

# ------------------------------
# Data laden
# ------------------------------
def load_data():
    try:
        materials = pd.read_csv("data/materials.csv")
    except:
        materials = pd.DataFrame()

    try:
        machines = pd.read_csv("data/machines.csv")
    except:
        machines = pd.DataFrame()

    try:
        bom = pd.read_csv("data/bom_example.csv")
    except:
        bom = pd.DataFrame()

    return materials, machines, bom


materials, machines, bom = load_data()

# ------------------------------
# KPI's tonen
# ------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Materialen", len(materials))
col2.metric("Machines", len(machines))
col3.metric("BOM regels", len(bom))

st.markdown("---")

# ------------------------------
# Data previews
# ------------------------------
st.subheader(get_text("data_sources"))

with st.expander("Materialen bekijken"):
    if not materials.empty:
        st.dataframe(materials)
    else:
        st.info("Geen materialen gevonden.")

with st.expander("Machines bekijken"):
    if not machines.empty:
        st.dataframe(machines)
    else:
        st.info("Geen machines gevonden.")

with st.expander("BOM voorbeeld bekijken"):
    if not bom.empty:
        st.dataframe(bom)
    else:
        st.info("Geen BOM voorbeeld gevonden.")

