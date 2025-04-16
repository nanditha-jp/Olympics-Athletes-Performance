import plotly.express as px
from src.visualisation.compare import analysis
import folium

def plot_compare_countries_by_medal(filters, sport, country_a, country_b):
    countries_df = analysis.compare_countries_by_medal(filters, sport, country_a, country_b)

    # Plot
    fig = px.line(
        countries_df,
        x="year",
        y="medal",
        color="country",
        markers=True,
        title="Total Medals (Country Comparison) by Year and Country"
    )

    # Customize layout to match your image
    fig.update_layout(
        title_font=dict(size=18),
        legend_title_text='Country',
        xaxis_title="Year",
        yaxis_title="Total Medals",
        template="plotly_white"
    )
    return fig

def plot_compare_countries_by_athletes(filters, sport, country_a, country_b):
    countries_df = analysis.compare_countries_by_athletes(filters, sport, country_a, country_b)

    fig = px.pie(
        countries_df,
        names="country",
        values="athlete_id",
        title="Total Athletes (Country Comparison)",
        hole=0  # Set to >0 if you want a donut chart
    )

    # Customize layout
    fig.update_traces(textinfo='label+percent+value')
    fig.update_layout(
        title_font=dict(size=18),
        legend_title_text='Country',
        template="plotly_white"
    )
    return fig

def plot_medal_distribution_by_gender(filter):
    medal_counts = analysis.medal_distribution_by_gender(filter)

    # Plot
    fig = px.bar(
        medal_counts,
        x="sex",
        y="athlete_id",
        color="medal",
        title="Medal distribution by gender",
        text_auto=True
    )

    # Customize
    fig.update_layout(
        barmode="stack",
        xaxis_title="Sex",
        yaxis_title="Medals",
        title_font=dict(size=18),
        legend_title_text='Medal',
        template="plotly_white"
    )
    return fig

def plot_athlete_counts_by_country_map(filter):
    df = analysis.athlete_counts_by_country(filter)

    m = folium.Map(location=[20, 0], zoom_start=2)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=row["total_athletes"]*0.0015,  # scale radius
            popup=folium.Popup(f"NOC: {row['noc']}<br>Total Athletes: {row['total_athletes']}", max_width=200),
            color='blue',
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

    return m
