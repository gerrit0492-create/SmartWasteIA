from __future__ import annotations
import streamlit as st
import pandas as pd
import os
import requests

# Config
st.set_page_config(page_title="AI Assist", page_icon="🤖", layout="wide")
st.title("🤖 AI Assist — Kostenreductie & Routing Advies (Volledig Gratis)")

# BOM inladen
DATA_DIR = "data"
try:
    bom = pd.read_csv(os.path.join(DATA_DIR, "bom_example.csv"))
except Exception:
    bom = pd.DataFrame()

st.write("AI-advies over de huidige BOM:")

# Gratis AI-endpoints
HF_API_URL_PRIMARY = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_API_URL_SECONDARY = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

# Demo-keys voor publieke modellen (niet beveiligd, alleen voor gratis tests)
HEADERS = {"Authorization": "Bearer hf_uJePzYSCIK_fake_demo_key"}

def query_huggingface(api_url, prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }
    try:
        response = requests.post(api_url, headers=HEADERS, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        return None
    except:
        return None

# Knop voor AI advies
if st.button("💡 Genereer advies"):
    prompt = f"Geef kostenreductie-advies voor deze BOM:\n{bom.to_string(index=False)}"

    # 1: Probeer primaire gratis AI
    ai_output = query_huggingface(HF_API_URL_PRIMARY, prompt)

    # 2: Fallback naar secundaire gratis AI als eerste faalt
    if ai_output is None:
        ai_output = query_huggingface(HF_API_URL_SECONDARY, prompt)

    # 3: Toon resultaat of foutmelding
    if ai_output:
        st.markdown(ai_output)
    else:
        st.error("Geen gratis AI-respons beschikbaar. Probeer later opnieuw.")
