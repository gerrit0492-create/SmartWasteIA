from __future__ import annotations
import streamlit as st
import pandas as pd
import os
import requests

# Configuratie
st.set_page_config(page_title="AI Assist", page_icon="🤖", layout="wide")
st.title("🤖 AI Assist — Kostenreductie & Routing Advies (Gratis AI + Fallback)")

# BOM inladen
DATA_DIR = "data"
try:
    bom = pd.read_csv(os.path.join(DATA_DIR, "bom_example.csv"))
except Exception:
    bom = pd.DataFrame()

st.write("AI-advies over de huidige BOM:")

# Modellen in volgorde van gebruik
MODELS = [
    "mistralai/Mistral-7B-Instruct-v0.2",
    "tiiuae/falcon-7b-instruct",
    "bigscience/bloomz-560m"
]

# Hugging Face Token ophalen
HF_TOKEN = st.secrets.get("huggingface", {}).get("token", None)
if not HF_TOKEN:
    st.error("Geen Hugging Face token gevonden in Streamlit Secrets.")
    st.stop()

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_model(model_name: str, prompt: str):
    """Vraag AI-advies op via Hugging Face."""
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200, "temperature": 0.7}}
    try:
        response = requests.post(api_url, headers=HEADERS, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()[0]["generated_text"], None
        else:
            return None, f"Fout {response.status_code} van {model_name}: {response.text}"
    except Exception as e:
        return None, f"Verbindingsfout met {model_name}: {e}"

# Knop voor AI-advies
if st.button("💡 Genereer advies"):
    prompt = f"Geef kostenreductie-advies voor deze BOM:\n{bom.to_string(index=False)}"

    ai_output = None
    last_error = None
    used_model = None

    # Probeer modellen in volgorde
    for model in MODELS:
        st.info(f"Probeer model: {model}")
        ai_output, error = query_model(model, prompt)
        if ai_output:
            used_model = model
            break
        last_error = error

    # Resultaat tonen
    if ai_output:
        st.success(f"Antwoord van model: {used_model}")
        st.markdown(ai_output)
    else:
        st.error(f"Geen bruikbaar antwoord ontvangen. Laatste fout: {last_error}")
