from __future__ import annotations
import json
import pandas as pd

def _get_gspread_client():
    import gspread
    from google.oauth2.service_account import Credentials
    import streamlit as st
    info = st.secrets.get("gcp_service_account", {})
    if isinstance(info, str):
        info = json.loads(info)
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    return gspread.authorize(creds)

def read_sheet(sheet_id: str, worksheet: str | None = None) -> pd.DataFrame:
    gc = _get_gspread_client()
    sh = gc.open_by_key(sheet_id)
    ws = sh.worksheet(worksheet) if worksheet else sh.sheet1
    data = ws.get_all_records()
    return pd.DataFrame(data)

def write_sheet(df: pd.DataFrame, sheet_id: str, worksheet: str | None = None):
    gc = _get_gspread_client()
    sh = gc.open_by_key(sheet_id)
    ws = sh.worksheet(worksheet) if worksheet else sh.sheet1
    ws.clear()
    ws.update([df.columns.tolist()] + df.astype(str).values.tolist())
