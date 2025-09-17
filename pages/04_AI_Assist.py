from __future__ import annotations
import streamlit as st
import pandas as pd
import os
import openai

# Config
st.set_page_config(page_title="AI Assist", page_icon="🤖", layout="wide")
st.title("🤖 AI Assist — Kostenreductie & Routing Advies")

# API key en model uit Streamlit Secrets
if "llm" in st.secrets:
    api_key = st.secrets["llm"]["api_key"]
    model = st.secrets["llm"].get("model", "gpt-4o")  # standaard gpt-4o
    openai.api_key = api_key
else:
    api_key = None
    model = None

# BOM inladen
DATA_DIR = "data"
try:
    bom = pd.read_csv(os.path.join(DATA_DIR, "bom_example.csv"))
except Exception:
    bom = pd.DataFrame()

st.write("AI-advies over de huidige BOM:")

# Knop voor AI advies
if st.button("💡 Genereer advies"):
    if api_key and model:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Je bent een AI-assistent voor kostenreductie en routingadvies."},
                    {"role": "user", "content": f"Geef kostenreductie-advies voor deze BOM:\n{bom.to_string(index=False)}"}
                ]
            )
            st.markdown(response.choices[0].message["content"])
        except Exception as e:
            st.error(f"Fout bij ophalen AI-advies: {e}")
    else:
        st.warning("Voeg je OpenAI API key en model toe in .streamlit/secrets.toml onder [llm].")
