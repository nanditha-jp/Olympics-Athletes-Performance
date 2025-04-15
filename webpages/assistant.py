import streamlit as st
from src.models.groq import get_response

def show():
    st.header("🤖 Ask the AI")
    st.markdown("---")

    # Select Model
    models = ["llama3-groq-70b-8192-tool-use-preview", "llama3-groq-8b-8192-tool-use-preview", "gemma2-9b-it", "gemma-7b-it", "llama-3.1-70b-versatile", "llama-3.1-8b-instant", "llama3-70b-8192", "llama3-8b-8192", "llama-guard-3-8b", "mixtral-8x7b-32768"]
    selected_model = st.sidebar.selectbox("Select Model", models, index=6)

    query = st.chat_input("Ask me anything...")
    if query is not None:
        st.markdown(f"##### Query: {query}")
        st.markdown(get_response(query, selected_model))
