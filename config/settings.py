import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()
api_key = st.secrets("GEMINI_API_KEY")

if not api_key:
    st.error("Please set GEMINI_API_KEY in your .env file.")
    st.stop()

os.environ["GEMINI_API_KEY"] = api_key