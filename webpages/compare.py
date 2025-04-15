import streamlit as st
from src.visualisation.compare import analysis, plot


def show():
    st.header("🌍 Comparative Analysis and Custom Visualizations")
    st.markdown("---")

    # Section: Top Countries by Medals
    st.markdown("### 🏅 Top 5 Countries Based on Medal Count")
    st.dataframe(analysis.countries_based_on_medals({}, top_n=5))

    # Section: Medal Distribution by Gender
    st.markdown("### 🚻 Medal Distribution by Gender")
    fig = plot.plot_medal_distribution_by_gender({})
    st.plotly_chart(fig, use_container_width=True)

    # Section: Sport Filter
    st.markdown("### 🎯 Compare Two Countries in a Selected Sport")
    selected_sports = st.multiselect("Select Sport(s)", analysis.get_unique("discipline"))
    if not selected_sports:
        selected_sports = analysis.get_unique("discipline")

    # Country selection
    col1, col2 = st.columns(2)
    countries = analysis.get_unique("country")
    with col1:
        country_a = st.selectbox("Select Country A", countries, key="country_a", index=countries.index("Greece"))
    with col2:
        country_b = st.selectbox("Select Country B", countries, key="country_b", index=countries.index("Canada"))

    # Comparison Plots
    st.markdown("#### 🥇 Medal Comparison")
    fig = plot.plot_compare_countries_by_medal({}, selected_sports, country_a, country_b)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 👥 Athlete Participation Comparison")
    fig = plot.plot_compare_countries_by_athletes({}, selected_sports, country_a, country_b)
    st.plotly_chart(fig, use_container_width=True)
