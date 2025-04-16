import streamlit as st
from src.models.groq import get_response

questions = [
    "Do the Olympics give a country economic Gains?",
    "What is the youngest/oldest medal winner?",
    "Which sports have gained or lost popularity?"
]

def show_buttons():
    button_query = None
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(questions[0]):
            button_query = questions[0]
    with col2:
        if st.button(questions[1]):
            button_query = questions[1]
    with col3:
        if st.button(questions[2]):
            button_query = questions[2]
    return button_query

def handle_query(query, selected_model):
    if query:
        st.markdown(f"#### {query}")
        response = get_response(query, selected_model)
        st.markdown(response)

def show():
    st.header("🤖 Ask the AI")
    st.markdown("---")

    # Select Model
    models = ["llama3-groq-70b-8192-tool-use-preview", "llama3-groq-8b-8192-tool-use-preview", "gemma2-9b-it", "gemma-7b-it", "llama-3.1-70b-versatile", "llama-3.1-8b-instant", "llama3-70b-8192", "llama3-8b-8192", "llama-guard-3-8b", "mixtral-8x7b-32768"]
    selected_model = st.sidebar.selectbox("Select Model", models, index=6)

    button_query = show_buttons()
    st.markdown("---")

    chat_query = st.chat_input("Ask me anything...")
    query = chat_query or button_query

    handle_query(query, selected_model)
