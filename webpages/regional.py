import streamlit as st
from src.visualisation.regional import plot


def show():
    st.header("🔠 Regional and Category wise Analysis")
    st.markdown("---")

    st.markdown("### 🗺️ Region sending athletes")
    fig = plot.plot_country_sending_athletes({}, top_n=10)
    st.plotly_chart(fig, use_container_width=True)
