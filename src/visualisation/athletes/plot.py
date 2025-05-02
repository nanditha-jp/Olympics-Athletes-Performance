import folium
import plotly.express as px

from src.utils.filters import apply_filters


def plot_athlete_location(df):
    # Map
    m = folium.Map(
        location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=13
    )

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=7,  # scale radius
            popup=folium.Popup(
                f"NOC: {row['noc']}<br>Born region: {row['born_region']}<br> Born City: {row['born_city']}",
                max_width=200,
            ),
            color="blue",
            fill=True,
            fill_opacity=0.6,
        ).add_to(m)

    return m


def plot_medals_over_time(df, filters):
    df = apply_filters(df, filters)

    medal_df = df[df["medal"].notna()]

    # Map medals to scores
    medal_score = {"Bronze": 1, "Silver": 2, "Gold": 3}
    medal_df["medal_score"] = medal_df["medal"].map(medal_score)

    # Line chart: Medal score over years per event
    fig = px.line(
        medal_df,
        x="year",
        y="medal_score",
        color="event",
        markers=True,
        hover_data=["medal", "discipline"],
        title="🏅 Medal Score Over Time by Event",
    )

    fig.update_yaxes(
        tickvals=[1, 2, 3], ticktext=["Bronze", "Silver", "Gold"], title="Medal"
    )
    return fig


def plot_medal_breakdown(df, filters):
    df = apply_filters(df, filters)

    medal_df = df[df["medal"].notna()]
    # 4. Medal Breakdown
    medal_counts = medal_df["medal"].value_counts().reset_index()
    medal_counts.columns = ["medal", "count"]
    fig = px.pie(
        medal_counts, names="medal", values="count", title="Medal Type Breakdown"
    )
    return fig
