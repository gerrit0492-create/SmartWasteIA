from __future__ import annotations
import streamlit as st
import pandas as pd
import os

# Configuratie
st.set_page_config(page_title="AI Assist", page_icon="🤖", layout="wide")
st.title("🤖 AI Assist — Kostenreductie & Routing Advies (Testmodus)")

# BOM inladen
DATA_DIR = "data"
try:
    bom = pd.read_csv(os.path.join(DATA_DIR, "bom_example.csv"))
except Exception:
    bom = pd.DataFrame()

st.write("AI-advies over de huidige BOM (nu zonder AI, alleen voor testen):")

# Knop voor testmodus
if st.button("💡 Genereer advies"):
    st.info("AI-functie staat uit in testmodus. Hier zou normaal het AI-antwoord komen.")
    if bom.empty:
        st.warning("BOM-bestand is leeg of niet gevonden.")
    else:
        st.success("BOM is succesvol ingeladen!")
        st.dataframe(bom)
