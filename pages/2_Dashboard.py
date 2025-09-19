import streamlit as st
import pandas as pd
import os

st.title("📊 Dashboard – Kostenanalyse")

data_dir = "data"
materials_file = os.path.join(data_dir, "materials.csv")
machines_file = os.path.join(data_dir, "machines.csv")
bom_file = os.path.join(data_dir, "bom_example.csv")

if os.path.exists(materials_file) and os.path.exists(machines_file) and os.path.exists(bom_file):
    materials = pd.read_csv(materials_file)
    machines = pd.read_csv(machines_file)
    bom = pd.read_csv(bom_file)

    # Kostenberekening per onderdeel
    merged = bom.merge(materials, on="material_code", how="left")
    merged = merged.merge(machines, on="machine_code", how="left")

    merged["material_cost"] = merged["qty"] * merged["price_eur"]
    merged["machine_cost"] = (merged["process_time_min"] / 60) * merged["rate_eur_per_hour"]
    merged["co2_footprint"] = merged["qty"] * merged["co2_kg_per_unit"] + (merged["process_time_min"]/60)*merged["co2_kg_per_hour"]
    merged["total_cost"] = merged["material_cost"] + merged["machine_cost"]

    st.subheader("Overzicht per onderdeel")
    st.dataframe(merged[[
        "item_code","description","qty","material_cost","machine_cost","total_cost","co2_footprint"
    ]])

    # KPI's
    st.subheader("KPI's")
    st.metric("Totale materiaalkosten (€)", round(merged["material_cost"].sum(),2))
    st.metric("Totale machinekosten (€)", round(merged["machine_cost"].sum(),2))
    st.metric("Totale kosten (€)", round(merged["total_cost"].sum(),2))
    st.metric("Totale CO2 (kg)", round(merged["co2_footprint"].sum(),2))
else:
    st.warning("Materialen, machines of BOM ontbreken. Ga naar de uploadpagina.")