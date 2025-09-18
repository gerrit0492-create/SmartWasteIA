import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import get_text, get_current_theme

# Thema toepassen
theme = get_current_theme()

st.title(f"📊 {get_text('dashboard')}")

if "boms" in st.session_state and st.session_state["boms"]:
    for name, df in st.session_state["boms"].items():
        st.subheader(f"{get_text('dashboard')} - {name}")

        # Dataframe tonen
        st.dataframe(df)

        if "Qty" in df.columns:
            fig = px.bar(df, x="Description", y="Qty", title="Aantal per onderdeel",
                         template="plotly_dark" if st.session_state["theme"] == "Donker" else "plotly")
            st.plotly_chart(fig, use_container_width=True)

        if "Unit_Price_EUR" in df.columns and "Qty" in df.columns:
            df["Total_Cost"] = df["Unit_Price_EUR"] * df["Qty"]
            fig2 = px.pie(df, values="Total_Cost", names="Description",
                          title="Kostenverdeling",
                          template="plotly_dark" if st.session_state["theme"] == "Donker" else "plotly")
            st.plotly_chart(fig2, use_container_width=True)
else:
    st.info(get_text("upload_bom"))
