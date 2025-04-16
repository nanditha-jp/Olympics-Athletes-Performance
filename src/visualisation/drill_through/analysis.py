import numpy as np
import pandas as pd

import os
import src.utils as utils

from src.visualisation.drill_through import DAX

# configure logger
logger = utils.configure_logger("Drill Through", "drill_through.log")

# load data
data_path = os.path.join("data", "interim")

bios = utils.load_data(os.path.join(data_path, "bios.csv"), logger)
results = utils.load_data(os.path.join(data_path, "results.csv"), logger)

# merge data
merged = results.merge(
    bios[['athlete_id', 'name', "noc", "born_year"]], on="athlete_id", how="left"
)
merged["age"] = merged["year"].astype(float) - merged["born_year"].astype(float)

def athlete_wise_medal_distribution(filters, top_n):
    df = utils.apply_filters(merged, filters)
    # Filter only rows with medals
    medal_results = df[df['medal'].notna()]

    # Count medals per athlete
    medal_count = medal_results.groupby(['athlete_id', 'name']).size().reset_index(name='medal')
    # Sort
    medal_count = medal_count.sort_values(by='medal', ascending=False)
    # extract top_n
    medal_count = medal_count.head(top_n)

    return medal_count.rename(columns={"name": "Name", "medal": "Medals", "athlete_id": "Athlete ID"})

def country_wise_medal_distribution(filters, top_n):
    df = utils.apply_filters(merged, filters)
    # Filter only rows with medals
    medal_results = df[df['medal'].notna()]

    # Count medals per athlete
    medal_count = medal_results.groupby(["noc_x", "noc_y"]).size().reset_index(name='medal')
    # Sort
    medal_count = medal_count.sort_values(by='medal', ascending=False)
    # extract top_n
    medal_count = medal_count.head(top_n)

    return medal_count.rename(columns={"noc_x": "NOC", "noc_y": "Country", "medal": "Medals"})

def drill_athlete(athlete_id):
    df = results[results["athlete_id"] == int(athlete_id)]
    df = df.merge(bios, on="athlete_id", how="left")

    return df

def drill_country(noc):
    df = results[results["noc"] == noc]
    df = df.merge(bios, on="athlete_id", how="left")

    return df

# Trend and distribution Analysis
def age_distribution_across_sports(filters, top_n):
    df = utils.apply_filters(merged, filters)
    # Clean data: drop rows with missing sport, athlete_id or sex
    df = df.dropna(subset=["discipline", "age"])

    # Group by Discipline and calculate average age
    avg_age_by_sport = df.groupby('discipline')['age'].mean().reset_index()

    # Sort by average age
    avg_age_by_sport = avg_age_by_sport.sort_values(by='age', ascending=False)

    # Get top 10 sports by average age
    avg_age_by_sport = avg_age_by_sport.head(top_n)

    return avg_age_by_sport

def participation_trend_over_time(filters, past_n_years=10):
    df = results.copy()
    # Filter for the past 10 years (e.g., from 2010 onward)
    if "year" in filters.keys():
        max_year = max(filters["year"])
    else:
        max_year = max(df["year"])
    filtered = df[df['year'].isin(range(max_year - past_n_years, max_year + 1))]

    # Group by year and count all athlete_id entries
    yearly_counts = filtered.groupby('year')['athlete_id'].count().reset_index()
    yearly_counts.columns = ['Year', 'Athletes']

    return yearly_counts

def sport_growth_participation(filters, top_n):
    df = utils.apply_filters(merged, filters)

    df = df.groupby("discipline").apply(DAX.participation_growth_rate).reset_index(name="participation_growth_rate")

    df = df.sort_values(by="participation_growth_rate", ascending=False)

    if top_n is not None:
        return df.head(top_n)
    return df
