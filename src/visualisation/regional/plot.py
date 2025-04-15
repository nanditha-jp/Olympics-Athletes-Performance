import plotly.express as px
from src.visualisation.regional import analysis

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
