import streamlit as st
from streamlit_option_menu import option_menu

from utils import css

# Read from GET params
params = st.query_params
selected_page = params.get("page", "Home")


pages = ["Home", "Overview", "Insights"]
with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=pages,
        icons=["house", "bar-chart", "funnel"],
        styles=css.get_menu_style(),
        default_index=pages.index(selected_page)
    )


if page == "Overview":
    from webpages import overview
    overview.show()

elif page == "Insights":
    from webpages import insights
    insights.show()

elif page == "Home":
    st.header("Olympics Athlete Performance Analysis")
