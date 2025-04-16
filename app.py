import streamlit as st
from streamlit_option_menu import option_menu

from utils import css

# Read from GET params
params = st.query_params
selected_page = params.get("page", "Home")
selected_athlete = params.get("id", None)
selected_country = params.get("noc", None)


pages = ["Home", "Overview", "Regional", "Drill Through", "Insights", "Compare", "Ask the AI"]
with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=pages,
        icons=["house", "bar-chart", "globe", "layers", "funnel", "graph-up", "robot"],
        styles=css.get_menu_style(),
        default_index=pages.index(selected_page)
    )


if page == "Overview":
    from webpages import overview
    overview.show()

elif page == "Regional":
    from webpages import regional
    regional.show()

elif page == "Drill Through":
    from webpages import drill_through
    if selected_athlete:
        drill_through.drill_athlete(selected_athlete)
    elif selected_country:
        drill_through.drill_country(selected_country)
    else:
        drill_through.show()

elif page == "Insights":
    from webpages import insights
    insights.show()

elif page == "Compare":
    from webpages import compare
    compare.show()

elif page == "Ask the AI":
    from webpages import assistant
    assistant.show()

elif page == "Home":
    st.header("Olympics Athlete Performance Analysis")
