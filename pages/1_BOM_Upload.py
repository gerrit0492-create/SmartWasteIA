import streamlit as st
import pandas as pd
import os

st.title("BOM Upload")

# Session state voor meerdere BOM's
if "boms" not in st.session_state:
    st.session_state["boms"] = {}

uploaded = st.file_uploader("Upload een BOM (CSV)", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
    name = uploaded.name
    st.session_state["boms"][name] = df
    df.to_csv(f"data/{name}", index=False)
    st.success(f"BOM '{name}' succesvol geüpload!")
    st.dataframe(df)

if st.button("Voorbeeld BOM laden"):
    df = pd.read_csv("data/bom_example.csv")
    st.session_state["boms"]["voorbeeld_bom"] = df
    st.dataframe(df)

if st.button("Reset alle BOM's"):
    st.session_state["boms"] = {}
    st.success("Alle BOM's zijn verwijderd.")
