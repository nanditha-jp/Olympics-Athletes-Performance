import streamlit as st
from streamlit_option_menu import option_menu

from utils import css

# Read from GET params
params = st.query_params
selected_page = params.get("page", "Home")
selected_athlete = params.get("id", None)
selected_country = params.get("noc", None)


pages = ["Home", "Overview", "Drill Through"]
with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=pages,
        icons=["house", "bar-chart", "layers"],
        styles=css.get_menu_style(),
        default_index=pages.index(selected_page)
    )


if page == "Overview":
    from webpages import overview
    overview.show()

elif page == "Drill Through":
    from webpages import drill_through
    if selected_athlete:
        drill_through.drill_athlete(selected_athlete)
    elif selected_country:
        drill_through.drill_country(selected_country)
    else:
        drill_through.show()

elif page == "Home":
    st.header("Olympics Athlete Performance Analysis")
