import plotly.express as px
from src.visualisation.overview import analysis


def plot_top_countries(filters):
    top_countries = analysis.top_performing_countries(filters=filters, top_n=10)

    fig = px.bar(
        top_countries,
        x="medal",
        y="noc",
        orientation="h",
        title="Top Performing Countries by Medal Count",
        labels={"noc": "Country (NOC)", "medal": "Number of Medals"},
        color="medal",
        color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    return fig


def plot_medal_distribution(filters):
    medal_counts = analysis.medal_distribution(filters=filters)
    color_map = {"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"}

    # Pie chart
    fig = px.pie(
        medal_counts,
        names="medal",
        values="count",
        color="medal",
        color_discrete_map=color_map,
        hole=0.3,
    )

    fig.update_traces(textinfo="percent", showlegend=False)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig


def plot_medal_trend_over_time(filters):
    yearly_counts = analysis.medal_trend_over_time(filters=filters)
    # Plot
    fig = px.line(
        yearly_counts,
        x="year",
        y="medal_count",
        title="Medal Trends Over Time",
        labels={"year": "Year", "medal_count": "Number of Medals"},
    )

    fig.update_traces(line=dict(width=3), mode="lines+markers")
    fig.update_layout(
        title_font=dict(size=20, family="Arial", color="black"),
        xaxis=dict(tickformat="d"),  # No comma formatting for years
        yaxis=dict(tickformat=",d"),  # Use '1K', '2K' etc.
        margin=dict(l=40, r=10, t=40, b=40),
        height=350,
    )
    return fig


def plot_gender_distribution_across_sports(filters):
    athlete_counts = analysis.gender_distribution_across_sports(
        filters=filters, top_n=10
    )
    # Plot
    fig = px.bar(
        athlete_counts,
        x="discipline",
        y="athlete_id",
        color="sex",
        title="Gender distribution across sports",
        labels={"athlete_id": "Number of athletes", "sport": "Sport", "sex": "Sex"},
        color_discrete_map={"Female": "#66c2ff", "Male": "#001f77"},
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        legend_title="Sex",
        height=400,
        margin=dict(t=40, b=40, l=20, r=10),
    )
    return fig
