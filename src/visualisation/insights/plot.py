import plotly.express as px
from src.visualisation.insights import analysis
import folium

def plot_participation_of_gender_over_time(filters):
    df_grouped = analysis.participation_of_gender_over_time(filters)

    # Plot
    fig = px.line(
        df_grouped,
        x="year",
        y="Participants",
        color="sex",
        markers=True,
        title="Trend of participation by gender over time"
    )

    # Customize
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Participants",
        title_font=dict(size=18),
        legend_title_text="Sex",
        template="plotly_white"
    )
    return fig

def plot_medal_distribution(filters):
    medal_counts = analysis.medal_distribution(filters=filters)

    # Pie chart
    fig = px.pie(
        medal_counts,
        names="medal",
        values="count",
        color="medal",
        hole=0.3,
    )

    fig.update_traces(textinfo="percent", showlegend=False)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig


def plot_performance_score_by_noc_map(filters):
    df = analysis.performance_score_by_noc(filters)

    # Map
    m = folium.Map(location=[20, 0], zoom_start=2)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=row["Performance Score"]*0.0015,  # scale radius
            popup=folium.Popup(f"NOC: {row['noc']}<br>Total Athletes: {row['Performance Score']}", max_width=200),
            color='blue',
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

    return m
