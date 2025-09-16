from __future__ import annotations
import streamlit as st, pandas as pd
from utils.config import DATA_DIR, ASSETS_DIR
from utils.ai import advise_cost_reduction

st.set_page_config(page_title="AI Assist", page_icon="🤖", layout="wide")
st.logo(str(ASSETS_DIR / "logo_cp.svg"))
st.title("🤖 AI Assist — Cost Reduction & Routing Hints")

try:
    bom = pd.read_csv(DATA_DIR / "bom_example.csv")
except Exception:
    bom = pd.DataFrame()

st.write("AI-advies over de huidige BOM.")
if st.button("🔎 Genereer advies"):
    out = advise_cost_reduction(bom, pd.read_csv(DATA_DIR / "materials.csv"))
    st.markdown(out)
else:
    st.caption("Voeg je OpenAI API-key toe in `.streamlit/secrets.toml` onder [llm] om dit te activeren.")
