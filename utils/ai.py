from __future__ import annotations
import os
from typing import List, Dict
import pandas as pd

def _get_llm_params():
    try:
        import streamlit as st
        llm = st.secrets.get("llm", {})
        provider = llm.get("provider","openai")
        api_key = llm.get("api_key","")
        model = llm.get("model","gpt-4o-mini")
        return provider, api_key, model
    except Exception:
        return "openai", os.getenv("OPENAI_API_KEY",""), "gpt-4o-mini"

def advise_cost_reduction(bom_df: pd.DataFrame, materials_df: pd.DataFrame) -> str:
    provider, api_key, model = _get_llm_params()
    if not api_key:
        return "LLM disabled (no API key). Add an API key in secrets to enable AI suggestions."
    prompt = (
        "You are a manufacturing cost engineer. Analyze the following BOM rows and suggest 7 concrete cost reduction ideas. "
        "Consider material substitutions, process changes (laser/waterjet/plasma; bending simplifications), batch sizing, DFMA, and routing. "
        "Return concise bullet points with quantifiable impact (% or €/part). CSV of BOM below:\n\n"
        + bom_df.to_csv(index=False)
    )
    try:
        if provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role":"system","content":"Be precise and pragmatic. Use EUR."},
                          {"role":"user","content":prompt}],
                temperature=0.2,
            )
            return resp.choices[0].message.content
        else:
            return "LLM provider not implemented yet: {}".format(provider)
    except Exception as e:
        return f"LLM error: {e}"
