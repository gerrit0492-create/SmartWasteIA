from __future__ import annotations
import os, json
from pathlib import Path

APP_NAME = "SmartWasteIA"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"

def get_secret(path: str, default=None):
    """Read nested secrets via dotted path, works with Streamlit or env fallbacks."""
    try:
        import streamlit as st
        node = st.secrets
        for part in path.split("."):
            node = node[part]
        return node
    except Exception:
        # fallback to environment variable with upper-case path
        env_key = path.replace(".", "_").upper()
        return os.environ.get(env_key, default)
