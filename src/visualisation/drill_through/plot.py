import plotly.express as px

from src.visualisation.drill_through import analysis

def plot_age_distribution_across_sports(filters, top_n=10):
    avg_age_by_sport = analysis.age_distribution_across_sports(filters=filters, top_n=top_n)

    # Plot using Plotly Express
    fig = px.bar(avg_age_by_sport, x='discipline', y='age',
                title='Age distribution of athletes across different sports',
                labels={'age': 'Average of Age', 'Discipline': 'Sport'},
                color_discrete_sequence=['dodgerblue'])

    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_participation_trend_over_time(filters, past_n_years=10):
    yearly_counts = analysis.participation_trend_over_time(filters=filters, past_n_years=past_n_years)

    # Plot the line chart
    fig = px.line(yearly_counts, x='Year', y='Athletes',
                title='Participation trends for the past 10 years.',
                markers=True)

    # Styling
    fig.update_traces(line=dict(color='dodgerblue', width=3))
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Athletes',
        yaxis_tickformat=','
    )
    return fig
