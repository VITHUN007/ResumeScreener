from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )