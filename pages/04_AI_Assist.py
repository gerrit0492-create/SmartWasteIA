from __future__ import annotations
import streamlit as st
import pandas as pd
import os
import requests

# Configuratie
st.set_page_config(page_title="AI Assist", page_icon="🤖", layout="wide")
st.title("🤖 AI Assist — Kostenreductie & Routing Advies (Gratis AI)")

# BOM inladen
DATA_DIR = "data"
try:
    bom = pd.read_csv(os.path.join(DATA_DIR, "bom_example.csv"))
except Exception:
    bom = pd.DataFrame()

st.write("AI-advies over de huidige BOM:")

# Hugging Face API-config met veilige token uit Streamlit Secrets
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_TOKEN = st.secrets["huggingface"]["token"] if "huggingface" in st.secrets else None
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def get_hf_response(prompt: str):
    """Vraag AI-advies op via Hugging Face."""
    if not HF_TOKEN:
        return "Geen Hugging Face token gevonden in Streamlit Secrets."
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }
    try:
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            return f"Fout van Hugging Face: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Verbindingsfout: {e}"

# Knop voor AI-advies
if st.button("💡 Genereer advies"):
    prompt = f"Geef kostenreductie-advies voor deze BOM:\n{bom.to_string(index=False)}"
    ai_output = get_hf_response(prompt)

    if ai_output:
        st.markdown(ai_output)
    else:
        st.error("Geen AI-respons ontvangen. Probeer het later opnieuw.")
