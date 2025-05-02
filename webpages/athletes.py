import streamlit as st
from streamlit_folium import st_folium
from src.visualisation.athletes import plot, analysis


def show(athlete_id):
    # Load athlete data
    df = analysis.get_athlete_data(athlete_id)
    bio = analysis.get_athlete_bio(df)

    # Title and Divider
    st.markdown(f"## 🏊‍♂️ {bio['Name']} Performance Explorer")
    st.markdown("---")

    # Sidebar Filters
    st.sidebar.header("🔎 Filter Criteria")
    selected_sports = st.sidebar.multiselect("Select Sport(s)", bio["Sport"])
    selected_medals = st.sidebar.multiselect(
        "Select Medal(s)", df["medal"].dropna().unique()
    )
    selected_years = st.sidebar.multiselect("Select Year(s)", bio["Years"])

    # Set filter defaults if none selected
    filters = {
        "discipline": selected_sports or bio["Sport"],
        "medal": selected_medals or df["medal"].dropna().unique(),
        "year": selected_years or bio["Years"],
    }

    # Athlete Profile Section
    col1, col2 = st.columns(2)
    with col1:
        try:
            st.image(analysis.get_athlete_image(athlete_id))
        except Exception as e:
            st.warning("No image available for this athlete")

    with col2:
        st.markdown("#### Summary")
        for key, value in bio.items():
            if key not in ["Name", "Sport", "Years"]:
                st.markdown(f"*{key}:* {value}")

    # Visualizations
    st.markdown("### 🏅 Medals Over Time")
    st.plotly_chart(plot.plot_medals_over_time(df, filters), use_container_width=True)

    st.markdown("### 🥇 Medal Breakdown")
    st.plotly_chart(plot.plot_medal_breakdown(df, filters), use_container_width=True)

    # Medal Summary Table
    st.markdown("### 🎖️ Medal Summary")
    st.dataframe(analysis.get_summary(df, filters))

    # Location Map
    st.markdown("---")
    st.markdown(f"### 🗺️ {bio['Name']}'s Location Map")

    if df["latitude"].isna().any():
        st.warning("No location data available for this athlete")
    else:
        st_folium(plot.plot_athlete_location(df), width=1000, height=500)
