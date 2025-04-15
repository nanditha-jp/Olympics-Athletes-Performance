import streamlit as st
from src.visualisation.regional import plot, analysis


def show():
    st.header("🔠 Regional and Category wise Analysis")
    st.markdown("---")

    # Sidebar Filters
    st.sidebar.header("🔎 Filter Criteria")
    year_filter = st.sidebar.multiselect("Select Year(s)", analysis.get_unique(column="year"))
    country_filter = st.sidebar.multiselect("Select Country(s)", analysis.get_unique(column="country"))

    # Filters
    filters = {
        "year": year_filter if len(year_filter) > 0 else analysis.get_unique(column="year"),
        "country": country_filter if len(country_filter) > 0 else analysis.get_unique(column="country"),
    }

    st.markdown("### 🗺️ Region sending athletes")
    fig = plot.plot_country_sending_athletes(filters, top_n=10)
    st.plotly_chart(fig, use_container_width=True)


    st.markdown("### 👫 Gender Participation")
    fig = plot.plot_gender_participation(filters)
    st.plotly_chart(fig, use_container_width=True)
