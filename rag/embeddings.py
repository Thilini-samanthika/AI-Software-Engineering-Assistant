import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource(show_spinner="Loading embedding model...")
def _load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


embeddings = _load_embeddings()
