from __future__ import annotations
import streamlit as st
import pandas as pd
import sys, os

# Voeg projectroot toe aan sys.path zodat utils altijd gevonden wordt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.ai import advise_cost_reduction
from utils.config import DATA_DIR, ASSETS_DIR

# Pagina-instellingen
st.set_page_config(page_title="AI Assist", page_icon="🤖", layout="wide")
st.logo(str(ASSETS_DIR / "logo_cp.svg"))

st.title("🤖 AI Assist — Kostenreductie & Routing Advies")

# Probeer BOM in te lezen
try:
    bom = pd.read_csv(DATA_DIR / "bom_example.csv")
except FileNotFoundError:
    st.error("BOM-bestand niet gevonden. Upload eerst een BOM via 'BOM Upload'.")
    bom = pd.DataFrame()

# Check of er een API-key beschikbaar is
api_key = None
try:
    if "llm" in st.secrets and "api_key" in st.secrets["llm"]:
        api_key = st.secrets["llm"]["api_key"]
except Exception:
    pass

# UI met fallback voor ontbrekende API-key of BOM
if api_key:
    if st.button("🔎 Genereer advies"):
        if len(bom) == 0:
            st.warning("Geen BOM-gegevens beschikbaar. Upload eerst een BOM.")
        else:
            st.info("AI genereert advies… even geduld.")
            out = advise_cost_reduction(bom, pd.read_csv(DATA_DIR / "materials.csv"))
            st.markdown(out)
    else:
        st.caption("Klik op 'Genereer advies' om AI-ideeën te krijgen.")
else:
    st.warning("Geen API-key gevonden. Voeg je OpenAI API-key toe in `.streamlit/secrets.toml` onder [llm].")

