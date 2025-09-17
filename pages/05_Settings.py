from __future__ import annotations
import streamlit as st
from utils.config import ASSETS_DIR

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
st.logo(str(ASSETS_DIR / "logo_cp.svg"))
st.title("⚙️ Settings")

st.markdown(
"""
**Secrets configureren (Streamlit Cloud):**
1. Ga naar je app ➜ **Settings** ➜ **Secrets**.
2. Kopieer de inhoud uit `.streamlit/secrets.toml` (template) en vul je eigen waarden in.
3. Sla op en trigger een redeploy (of push naar GitHub).

**Google Sheets**:
- Gebruik een **Service Account** met toegang tot de target-spreadsheets (deel de Sheet met het SA e-mailadres).

**LLM (OpenAI)**:
- Vul `[llm] api_key` in de secrets in om AI-advies te activeren.
"""
)
