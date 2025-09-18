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
