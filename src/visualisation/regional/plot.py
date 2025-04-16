import plotly.express as px
from src.visualisation.regional import analysis
import folium
import branca.colormap as cm

def plot_region_sending_athletes_map(filter):
    df = analysis.region_sending_athletes(filter)

    m = folium.Map(location=[20, 0], zoom_start=2)

    # Create a custom gradient: Blue (low) to Red (high)
    colormap = cm.LinearColormap(
        colors=["blue", "lightblue", "yellow", "orange", "red"],
        vmin=df['total_athletes'].min(),
        vmax=df['total_athletes'].max(),
    )
    colormap.caption = 'Total Athletes by Country'
    colormap.add_to(m)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=row["total_athletes"]*0.0015,  # scale radius
            popup=folium.Popup(f"NOC: {row['noc']}<br>Total Athletes: {row['total_athletes']}", max_width=200),
            color=colormap(row["total_athletes"]),
            fill=True,
            fill_color=colormap(row["total_athletes"]),
            fill_opacity=0.6
        ).add_to(m)

    return m

def plot_country_sending_athletes(filters, top_n):
    df = analysis.country_sending_athletes(filters, top_n).iloc[::-1]

    # Plotly Express bar chart
    fig = px.bar(
        df,
        x='athlete_count',
        y='country',
        orientation='h',
        title='Region Sending the Most Athletes',
        labels={'athlete_count': 'Total Athletes', 'country': 'Region'},
        color_discrete_sequence=['dodgerblue']
    )

    fig.update_layout(title_x=0.5)
    return fig

def plot_gender_participation(filters):
    athlete_counts = analysis.gender_participation(filters)

    # Plotly Express bar chart
    fig = px.bar(
        athlete_counts,
        x='discipline',
        y='Count',
        color='sex',
        barmode='group',
        title='Number of Male and Female Athletes per Discipline',
        labels={'Count': 'Number of Athletes'}
    )

    fig.update_layout(xaxis_tickangle=-45, title_x=0.5)

    return fig
