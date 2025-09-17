from __future__ import annotations
import streamlit as st
import pandas as pd
import os
from openai import OpenAI, APIError

# Config
st.set_page_config(page_title="AI Assist", page_icon="🤖", layout="wide")
st.title("🤖 AI Assist — Kostenreductie & Routing Advies (OpenAI versie)")

# BOM inladen
DATA_DIR = "data"
try:
    bom = pd.read_csv(os.path.join(DATA_DIR, "bom_example.csv"))
except Exception:
    bom = pd.DataFrame()

st.write("AI-advies over de huidige BOM:")

# OpenAI API-key ophalen
OPENAI_KEY = st.secrets.get("openai", {}).get("api_key", None)
if not OPENAI_KEY:
    st.error("Geen OpenAI API key gevonden in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=OPENAI_KEY)

# Modellen in volgorde van voorkeur
MODELS = ["gpt-4o", "gpt-3.5-turbo"]

def query_openai(prompt: str):
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Je bent een AI-assistent voor kostenreductie en routingadvies."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content, model
        except APIError as e:
            st.warning(f"Model {model} gaf een fout: {e}")
    return None, None

# Knop voor advies
if st.button("💡 Genereer advies"):
    prompt = f"Geef kostenreductie-advies voor deze BOM:\n{bom.to_string(index=False)}"
    ai_output, used_model = query_openai(prompt)

    if ai_output:
        st.success(f"Antwoord van model: {used_model}")
        st.markdown(ai_output)
    else:
        st.error("Geen antwoord ontvangen van OpenAI. Controleer API-sleutel of gebruikslimieten.")
