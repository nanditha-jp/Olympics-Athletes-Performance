import streamlit as st
from src.visualisation.overview import plot, analysis

def show():

    st.header("🏅 Olympic Athlete Performance Dashboard")
    st.markdown("---")
    # Sidebar Filters
    st.sidebar.header("🔎 Filter Criteria")
    year_filter = st.sidebar.multiselect("Select Year(s)", analysis.get_unique(column="year"))

    # Metrics
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Athletes", analysis.get_total_athletes())
    col2.metric("Total Events", analysis.get_total_events())
    col3.metric("Average Height (cm)", round(analysis.get_avg_height(), 2))
    col4.metric("Average Age (years)", round(analysis.get_avg_age(), 2))


    # Visualizations
    st.markdown("### 🥇 Top Performing Countries")
    fig = plot.plot_top_countries(filters={"year": year_filter})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🏆 Medal Distribution")
    fig = plot.plot_medal_distribution(filters={"year": year_filter})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📈 Medal Trends Over Time")
    fig = plot.plot_medal_trend_over_time(filters={"year": year_filter})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🚻 Gender Distribution by Sport")
    fig = plot.plot_gender_distribution_across_sports(filters={"year": year_filter})
    st.plotly_chart(fig, use_container_width=True)
