# check_secret.py
import os
import streamlit as st

def get_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.environ.get("GROQ_API_KEY")

print("GROQ key loaded:", bool(get_key()))
