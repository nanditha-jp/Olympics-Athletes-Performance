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

def get_testimonials_style():
    st.markdown("""
        <style>
        /* Wrapper container */
        .testimonials-container {
            overflow: hidden;
            position: relative;
            padding: 1rem 0;
            margin-top: 0.2rem;
        }

        /* Scrolling track */
        .testimonials-track {
            display: flex;
            gap: 1rem;
            animation: scroll 60s linear infinite;
            width: fit-content;
        }

        /* Card style (matches your feature-card theme) */
        .testimonial {
            flex: 0 0 auto;
            border: 1px solid #eee;
            border-radius: 12px;
            padding: 1rem;
            width: 280px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            transition: transform 0.2s;
            text-align: center;
        }
        .testimonial:hover {
            transform: translateY(-5px);
        }

        /* Pause on hover */
        .testimonials-container:hover .testimonials-track {
            animation-play-state: paused;
        }

        /* Smooth scrolling animation */
        @keyframes scroll {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        </style>
    """, unsafe_allow_html=True)
