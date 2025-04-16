import streamlit as st
from src.visualisation.insights import plot, analysis
from streamlit_folium import st_folium


def show():
    st.header("🔍 Interactive Insights and Filtering System")
    st.markdown("---")

    # Sidebar Filters
    st.sidebar.header("🔎 Filter Criteria")
    country_filter = st.sidebar.multiselect("Select Country(s)", analysis.get_unique(column="country"))
    sex_filter = st.sidebar.multiselect("Select Gender", analysis.get_unique(column="sex"))
    sport_filter = st.sidebar.multiselect("Select Sport(s)", analysis.get_unique(column="discipline"))
    medal_filter = st.sidebar.multiselect("Select Medal(s)", analysis.get_unique(column="medal"))
    year_filter = st.sidebar.multiselect("Select Year(s)", analysis.get_unique(column="year"))

    # Applied Filters
    filters = {
        "country": country_filter or analysis.get_unique(column="country"),
        "sex": sex_filter or analysis.get_unique(column="sex"),
        "discipline": sport_filter or analysis.get_unique(column="discipline"),
        "medal": medal_filter or analysis.get_unique(column="medal"),
        "year": year_filter or analysis.get_unique(column="year"),
    }

    # Trend Visualization
    st.markdown("### 📈 Participation Trends by Gender Over Time")
    fig = plot.plot_participation_of_gender_over_time(filters)
    st.plotly_chart(fig, use_container_width=True)

    # Top Athletes Table
    st.markdown("### 🏅 Top Athletes by Total Medals Won")
    st.markdown("List may include more than 10 due to tied medal counts.")
    df = analysis.athletes_by_total_medal_by_their_country_and_event(filters)
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("### 📝 Performance Score of NOC's in the World Map")
    folium_map = plot.plot_performance_score_by_noc_map({})
    st_folium(folium_map, width=1000, height=500)

    # Medal Distribution Chart
    st.markdown("### 🥇 Medal Distribution")
    fig = plot.plot_medal_distribution(filters)
    st.plotly_chart(fig, use_container_width=True)
