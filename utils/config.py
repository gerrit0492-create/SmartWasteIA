import streamlit as st

# ------------------------------
# Teksten in meerdere talen
# ------------------------------
TEXTS = {
    "NL": {
        "settings": "Instellingen",
        "language": "Taal",
        "theme": "Thema",
        "sync_interval": "Sync-interval (minuten)",
        "success_update": "Instellingen bijgewerkt!",
        "dashboard": "Dashboard",
        "home_title": "BOM App v1.0",
        "data_sources": "Databestanden",
        "upload_bom": "Upload eerst een BOM via de 'BOM Upload'-pagina."
    },
    "EN": {
        "settings": "Settings",
        "language": "Language",
        "theme": "Theme",
        "sync_interval": "Sync interval (minutes)",
        "success_update": "Settings updated!",
        "dashboard": "Dashboard",
        "home_title": "BOM App v1.0",
        "data_sources": "Data Sources",
        "upload_bom": "Please upload a BOM file first via the 'BOM Upload' page."
    }
}

# ------------------------------
# Thema's
# ------------------------------
THEMES = {
    "Licht": {
        "background": "#FFFFFF",
        "text": "#000000",
        "accent": "#007BFF"
    },
    "Donker": {
        "background": "#1E1E1E",
        "text": "#FFFFFF",
        "accent": "#00BFFF"
    }
}

# ------------------------------
# Functie voor taalkeuze
# ------------------------------
def get_text(key: str) -> str:
    lang = st.session_state.get("language", "NL")
    return TEXTS.get(lang, TEXTS["NL"]).get(key, key)

# ------------------------------
# Functie voor huidig thema
# ------------------------------
def get_current_theme() -> dict:
    theme_name = st.session_state.get("theme", "Licht")
    return THEMES.get(theme_name, THEMES["Licht"])

# ------------------------------
# App instellingen
# ------------------------------
APP_NAME = "BOM App v1.0"
LOGO_PATH = "data/logo.png"  # Plaats hier een logo als je wilt

import base64
import streamlit as st

# Tekstlogo als fallback
def get_logo_base64():
    # Simpel tekstlogo
    logo_text = "BOM App v1.0"
    svg = f"""
    <svg width="200" height="60" xmlns="http://www.w3.org/2000/svg">
      <rect width="200" height="60" fill="#007BFF"/>
      <text x="100" y="35" font-size="20" text-anchor="middle" fill="white">{logo_text}</text>
    </svg>
    """
    return base64.b64encode(svg.encode("utf-8")).decode("utf-8")

# Functie om het logo te tonen
def show_logo():
    logo_base64 = get_logo_base64()
    logo_html = f'<img src="data:image/svg+xml;base64,{logo_base64}" width="200"/>'
    st.markdown(logo_html, unsafe_allow_html=True)

