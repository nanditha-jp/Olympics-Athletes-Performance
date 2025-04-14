import streamlit as st
from streamlit_option_menu import option_menu

from utils import css


with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=["Home"],
        icons=["home"],
        styles=css.get_menu_style()
    )


if page == "Home":
    st.header("Olympics Athlete Performance Analysis")
