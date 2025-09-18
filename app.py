import streamlit as st
import pandas as pd
from utils.config import get_text, get_current_theme, APP_NAME, LOGO_PATH

# Thema toepassen
theme = get_current_theme()
st.set_page_config(page_title=APP_NAME, page_icon="📦", layout="wide")

# Custom CSS voor professioneel design
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        .big-title {{
            font-size: 32px;
            color: {theme['accent']};
            font-weight: bold;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Header met logo en titel
col1, col2 = st.columns([1, 4])
with col1:
    st.image(LOGO_PATH, width=80)
with col2:
    st.markdown(f"<div class='big-title'>{get_text('home_title')}</div>", unsafe_allow_html=True)

st.markdown("---")

# Data inlezen
try:
    materials = pd.read_csv("data/materials.csv")
    machines = pd.read_csv("data/machines.csv")
    bom = pd.read_csv("data/bom_example.csv")
except FileNotFoundError:
    st.error("CSV-bestanden niet gevonden in de map 'data/'.")
    materials, machines, bom = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# KPI's tonen
if not materials.empty and not machines.empty and not bom.empty:
    st.subheader("📊 Datastatistieken")
    col1, col2, col3 = st.columns(3)
    col1.metric(get_text("data_sources") + " - Materialen", len(materials))
    col2.metric(get_text("data_sources") + " - Machines", len(machines))
    col3.metric(get_text("data_sources") + " - BOM", len(bom))
