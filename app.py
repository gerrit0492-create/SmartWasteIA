import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Maakindustrie Cost App", layout="wide")

st.title("💰 Maakindustrie Cost Engineer App")
st.write("Welkom! Gebruik het menu links om een BOM te uploaden en kosten te analyseren.")

# Check of data aanwezig is
data_dir = "data"
materials_file = os.path.join(data_dir, "materials.csv")
machines_file = os.path.join(data_dir, "machines.csv")
bom_file = os.path.join(data_dir, "bom_example.csv")

if os.path.exists(materials_file) and os.path.exists(machines_file) and os.path.exists(bom_file):
    materials = pd.read_csv(materials_file)
    machines = pd.read_csv(machines_file)
    bom = pd.read_csv(bom_file)

    st.metric("Aantal Materialen", len(materials))
    st.metric("Aantal Machines", len(machines))
    st.metric("Voorbeeld BOM-regels", len(bom))
else:
    st.warning("Data ontbreekt. Zorg dat materials.csv, machines.csv en bom_example.csv in de /data map staan.")