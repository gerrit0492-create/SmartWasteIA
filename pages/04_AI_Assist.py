from __future__ import annotations
import streamlit as st
import pandas as pd
import os
import requests

# Config
st.set_page_config(page_title="AI Assist", page_icon="🤖", layout="wide")
st.title("🤖 AI Assist — Kostenreductie & Routing Advies (Gratis AI)")

# BOM inladen
DATA_DIR = "data"
try:
    bom = pd.read_csv(os.path.join(DATA_DIR, "bom_example.csv"))
except Exception:
    bom = pd.DataFrame()

st.write("AI-advies over de huidige BOM:")

# Modellen en token
PRIMARY_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
SECONDARY_MODEL = "HuggingFaceH4/zephyr-7b-beta"
HF_TOKEN = st.secrets.get("huggingface", {}).get("token", None)

if not HF_TOKEN:
    st.error("Geen Hugging Face token gevonden in Streamlit Secrets.")
    st.stop()

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_model(model_name: str, prompt: str):
    """Vraag AI-advies op voor een model."""
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200, "temperature": 0.7}}
    try:
        response = requests.post(api_url, headers=HEADERS, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            return f"Fout {response.status_code} van {model_name}: {response.text}"
    except Exception as e:
        return f"Verbindingsfout met {model_name}: {e}"

# Knop voor AI-advies
if st.button("💡 Genereer advies"):
    prompt = f"Geef kostenreductie-advies voor deze BOM:\n{bom.to_string(index=False)}"

    # Eerst primaire model proberen
    ai_output = query_model(PRIMARY_MODEL, prompt)

    # Als primaire model faalt, fallback naar secundaire model
    if not ai_output or ai_output.startswith("Fout"):
        ai_output = query_model(SECONDARY_MODEL, prompt)

    # Resultaat tonen
    if ai_output and not ai_output.startswith("Fout"):
        st.success(f"Model: {PRIMARY_MODEL if 'Fout' not in ai_output else SECONDARY_MODEL}")
        st.markdown(ai_output)
    else:
        st.error(f"Geen bruikbaar antwoord van AI. Laatste fout: {ai_output}")

