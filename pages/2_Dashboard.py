import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Dashboard")

if "boms" in st.session_state and st.session_state["boms"]:
    for name, df in st.session_state["boms"].items():
        st.subheader(f"Dashboard voor {name}")

        # Tabel tonen
        st.dataframe(df)

        if "Qty" in df.columns:
            # Bar chart Qty per item
            fig = px.bar(df, x="Description", y="Qty", title="Aantal per onderdeel")
            st.plotly_chart(fig, use_container_width=True)

        if "Unit_Price_EUR" in df.columns and "Qty" in df.columns:
            df["Total_Cost"] = df["Unit_Price_EUR"] * df["Qty"]
            fig2 = px.pie(df, values="Total_Cost", names="Description", title="Kostenverdeling")
            st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Upload eerst een BOM via de 'BOM Upload' pagina.")
