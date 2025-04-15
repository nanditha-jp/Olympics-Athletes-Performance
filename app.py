import streamlit as st
from streamlit_option_menu import option_menu

from utils import css

# Read from GET params
params = st.query_params
selected_page = params.get("page", "Home")


pages = ["Home", "Overview", "Regional"]
with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=pages,
        icons=["house", "bar-chart", "globe"],
        styles=css.get_menu_style(),
        default_index=pages.index(selected_page)
    )


if page == "Overview":
    from webpages import overview
    overview.show()

elif page == "Regional":
    from webpages import regional
    regional.show()

elif page == "Home":
    st.header("Olympics Athlete Performance Analysis")
