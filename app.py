import streamlit as st
import pandas as pd

st.set_page_config(page_title="BOM App", layout="wide")
st.title("BOM App v1.0")

st.markdown("""
Welkom bij de **BOM App**!  
Gebruik het menu links om een BOM te uploaden of het dashboard te bekijken.
""")

# Data inlezen ter controle
materials = pd.read_csv("data/materials.csv")
machines = pd.read_csv("data/machines.csv")
bom = pd.read_csv("data/bom_example.csv")

st.subheader("Databestanden")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Materialen", len(materials))
with col2:
    st.metric("Machines", len(machines))
with col3:
    st.metric("BOM Items", len(bom))
