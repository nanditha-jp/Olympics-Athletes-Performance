import streamlit as st

def get_menu_style():
    return {
        "container": {
            "padding": "0!important",
            "background-color": "#f5f6fa"
        },
        "icon": {
            "color": "black",
            "font-size": "16px"
        },
        "nav-link": {
            "font-size": "14px",
            "font-weight": "normal",  # removed extra semicolon
            "color": "#2c3e50"
        },
        "nav-link-selected": {
            "background-color": "#ff4b4b",
            "color": "white",
            "font-weight": "normal",
            "border-radius": "8px"
        }
    }

def inject_css():
    """Inject all custom CSS styles"""
    st.markdown("""
    <style>
    
    /* Feature Cards */
    .feature-card {
        padding: 1rem;
        height: 18rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border: 1px solid #eee;
        transition: transform 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    /* Metric Boxes */
    .metric-box {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)
