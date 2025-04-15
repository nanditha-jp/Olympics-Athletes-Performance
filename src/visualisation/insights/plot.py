import plotly.express as px
from src.visualisation.insights import analysis

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
