import streamlit as st

from src.visualisation.drill_through import analysis, plot
from src.visualisation.overview.analysis import get_unique
from src.visualisation.drill_through.formatter import add_athlete_link, add_country_link

from . import athletes

def show():
    st.header("🔍 Drill Through Dashboard")
    st.markdown("---")

    # Sidebar Filters
    st.sidebar.header("🔎 Filter Criteria")
    year_filter = st.sidebar.multiselect("Select Year(s)", get_unique(column="year"))

    # Filters
    filters = {
        "year": year_filter if len(year_filter) > 0 else get_unique(column="year"),
    }

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏅 Athletes by Medal Count")
        df_athletes = analysis.athlete_wise_medal_distribution(filters, top_n=10)
        df_athletes = df_athletes.apply(add_athlete_link, axis=1)
        st.markdown(df_athletes[["Name", "Medals"]].to_html(escape=False, index=False), unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🏅 Countries by Medal Count")
        df_countries = analysis.country_wise_medal_distribution(filters, top_n=10)
        df_countries = df_countries.apply(add_country_link, axis=1)
        st.markdown(df_countries[["Country", "Medals"]].to_html(escape=False, index=False), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📊 Age Distribution of Athletes Across Sports")
    fig = plot.plot_age_distribution_across_sports(filters)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📈 Participation Trends Over the Years")
    fig = plot.plot_participation_trend_over_time(filters)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📈 Sport with Highest growth in participation")
    fig = plot.plot_sport_growth_participation(filters, top_n=12)
    st.plotly_chart(fig, use_container_width=True)


# Drill Through
def drill_athlete(id):
    athletes.show(id)

def drill_country(noc):
    st.markdown(f"### 🌍 Country Detail: {noc}")
    st.dataframe(analysis.drill_country(noc))
