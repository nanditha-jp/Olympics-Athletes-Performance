import streamlit as st
from streamlit_option_menu import option_menu

from utils import css
from webpages import overview

# Read from GET params
params = st.query_params
selected_page = params.get("page", "Home")


pages = ["Home", "Overview"]
with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=pages,
        icons=["house", "bar-chart"],
        styles=css.get_menu_style(),
        default_index=pages.index(selected_page)
    )


if page == "Overview":
    overview.show()
elif page == "Home":
    st.header("Olympics Athlete Performance Analysis")
