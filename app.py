import streamlit as st
from streamlit_option_menu import option_menu

from utils import css
from webpages import overview

with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=["Home", "Overview"],
        icons=["home", "overview"],
        styles=css.get_menu_style()
    )


if page == "Overview":
    overview.show()
elif page == "Home":
    st.header("Olympics Athlete Performance Analysis")
