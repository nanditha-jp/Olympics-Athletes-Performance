import streamlit as st
from utils import testimonials

def feature_card(emoji: str, title: str, description: str):
    """Create a feature card component"""
    return f"""
    <div class="feature-card">
        <div style="font-size: 2rem;">{emoji}</div>
        <h5>{title}</h5>
        <p>{description}</p>
    </div>
    """

def show():
    st.header("Olympics 🏃 Athlete Performance Analysis")
    st.markdown("###### Interactive Dashboard for Analyzing Olympic Athlete Performance Trends")

    st.info("""⚠️ **Disclaimer:**  
    This project is for educational and analytical purposes, using data scraped from https://www.olympedia.org/athletes/.""")

    st.markdown("---")
    st.markdown("### ✨ Main Features")
    with st.container():
        cols = st.columns(3)
        features = [
            ("🤖", "LLM-Powered Q&A Assistant", "Integrated a Large Language Model (LLM) to answer user queries about Olympic data in natural language."),
            ("📊", "Interactive Visual Analytics", "Dynamic, user-friendly Streamlit dashboard with rich visualizations for exploring trends in athlete performance."),
            ("🔥", "Modular Code Architecture", "Clean, maintainable project structure with separate modules for data ingestion, preprocessing, and visualization."),
        ]
        for col, feature in zip(cols, features):
            with col:
                st.markdown(feature_card(*feature), unsafe_allow_html=True)
    
    st.text("")
    st.text("")
    
    testimonials.show_testimonials()

    st.text("")
    st.text("")

    st.markdown("### 🧭 How to Use This Dashboard")
    st.markdown("""
    - Navigate between pages from the sidebar.
    - Use filters to explore specific countries, sports, or years.
    - Try the LLM Q&A Assistant for instant answers about the data.
    """)

    st.markdown("---")
    st.markdown("""<div style="text-align: center; margin-top: 1rem; color: #666; font-size: 0.9em;">
        🔒 Data used for educational purposes only</div>""", 
        unsafe_allow_html=True)
