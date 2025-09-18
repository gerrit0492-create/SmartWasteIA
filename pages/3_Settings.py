import streamlit as st
from utils.config import get_text, THEMES

# -------------------------
# Pagina configuratie
# -------------------------
st.set_page_config(page_title=get_text("settings"), page_icon="⚙️", layout="wide")

# -------------------------
# Initialisatie van sessievariabelen
# -------------------------
if "language" not in st.session_state:
    st.session_state["language"] = "NL"

if "theme" not in st.session_state:
    st.session_state["theme"] = "Licht"

if "sync_interval" not in st.session_state:
    st.session_state["sync_interval"] = 15  # minuten

# -------------------------
# Pagina titel
# -------------------------
st.title(f"⚙️ {get_text('settings')}")
st.markdown("Configureer de taal, het thema en automatische updates.")

# -------------------------
# Layout in 3 kolommen
# -------------------------
col1, col2, col3 = st.columns(3)

# --- Taalkeuze ---
with col1:
    st.subheader(get_text("language"))
    language = st.radio(
        get_text("language"),
        ["NL", "EN"],
        index=0 if st.session_state["language"] == "NL" else 1,
        label_visibility="collapsed"
    )
    st.session_state["language"] = language

# --- Thema ---
with col2:
    st.subheader(get_text("theme"))
    theme = st.radio(
        get_text("theme"),
        ["Licht", "Donker"],
        index=0 if st.session_state["theme"] == "Licht" else 1,
        label_visibility="collapsed"
    )
    st.session_state["theme"] = theme

# --- Sync-interval ---
with col3:
    st.subheader(get_text("sync_interval"))
    sync_interval = st.slider(
        get_text("sync_interval"),
        min_value=5,
        max_value=60,
        step=5,
        value=st.session_state["sync_interval"],
        label_visibility="collapsed"
    )
    st.session_state["sync_interval"] = sync_interval

# -------------------------
# Huidige instellingen tonen
# -------------------------
st.markdown("---")
st.markdown("### Huidige instellingen")
st.info(f"""
- **{get_text('language')}**: {st.session_state['language']}
- **{get_text('theme')}**: {st.session_state['theme']}
- **{get_text('sync_interval')}**: {st.session_state['sync_interval']} min
""")

st.success(get_text("success_update"))

# -------------------------
# Thema kleuren ophalen en toepassen
# -------------------------
theme_colors = THEMES.get(st.session_state["theme"], THEMES["Licht"])
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {theme_colors['background']};
            color: {theme_colors['text']};
        }}
        .stSlider > div > div {{
            color: {theme_colors['accent']};
        }}
    </style>
    """,
    unsafe_allow_html=True
)
