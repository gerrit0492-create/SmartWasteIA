import streamlit as st
import pandas as pd

# Pagina-instellingen
st.set_page_config(page_title="AI Assist", page_icon="🤖", layout="wide")
st.title("🤖 AI Assist — Kostenreductie & Routing Advies (Testmodus)")

# 1. Check of BOM in session_state aanwezig is
if "bom_df" not in st.session_state or st.session_state["bom_df"].empty:
    st.warning("⚠️ Geen BOM geladen. Ga eerst naar 'BOM Upload & Live Sync' om een BOM te uploaden.")
    st.stop()

# 2. Toon altijd de actuele BOM
st.success("✅ BOM succesvol ingeladen!")
st.dataframe(st.session_state["bom_df"])

# 3. AI-advies knop (nu alleen testmodus)
if st.button("💡 Genereer advies"):
    st.info("AI-functie staat nu in testmodus. Hier zou normaal het AI-antwoord komen.")
    # Voorbeeld: simulatie van AI-advies
    st.write("💡 **Simulatie-advies:** Overweeg materiaalreductie en procesoptimalisatie om kosten te verlagen.")

# 4. Toekomst: hier kan AI integratie komen
# ------------------------------------------------
# Bijv. OpenAI of Hugging Face API aanroepen met:
# - st.session_state["bom_df"] als input
# - Resultaat tonen in Streamlit
