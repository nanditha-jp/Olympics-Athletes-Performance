import numpy as np
import pandas as pd

import os
import src.utils as utils
from src.visualisation.overview import DAX

# configure logger
logger = utils.configure_logger("Visualisation", "overview_dax.log")

# load data
data_path = os.path.join("data", "interim")

bios = utils.load_data(os.path.join(data_path, "bios.csv"), logger)
results = utils.load_data(os.path.join(data_path, "results.csv"), logger)

# merge data
results = results.merge(
    bios[["athlete_id", "born_year", "sex", "height"]], on="athlete_id", how="left"
)
results["age"] = results["year"].astype(float) - results["born_year"].astype(float)


# Utilities
def get_unique(column):
    if column in results.columns:
        return sorted(results[column].dropna().unique().tolist())
    elif column in bios.columns:
        return sorted(bios[column].dropna().unique().tolist())
    else:
        return []


def apply_filters(df, filters):
    for column, values in filters.items():
        if column in df.columns:
            df = df[df[column].isin(values)]
    return df


# load metrics
def get_total_athletes(filters):
    df = apply_filters(results, filters)
    return DAX.total_athletes(df)


def get_total_events(filters):
    df = apply_filters(results, filters)
    return DAX.total_events(df)


def get_avg_height(filters):
    df = apply_filters(results, filters)
    return DAX.avg_height(df)


def get_avg_age(filters):
    df = apply_filters(results, filters)
    return DAX.avg_age(df)


# Analysis fns
def top_performing_countries(filters, top_n=10):
    df = apply_filters(results, filters)

    top_countries = (
        df.groupby("noc")["medal"]
        .count()
        .reset_index()
        .sort_values("medal", ascending=False)
        .head(top_n)
    )
    return top_countries


def medal_distribution(filters):
    df = apply_filters(results, filters)
    df = df.dropna(subset=["medal"])

    # Count medals
    medal_counts = df["medal"].value_counts().reset_index()
    medal_counts.columns = ["medal", "count"]

    return medal_counts


def medal_trend_over_time(filters):
    df = apply_filters(results, filters)
    df = df.dropna(subset=["medal"])
    # Group by year
    yearly_counts = df.groupby("year").size().reset_index(name="medal_count")

    return yearly_counts


def gender_distribution_across_sports(filters, top_n=10):
    df = apply_filters(results, filters)
    # Clean data: drop rows with missing sport, athlete_id or sex
    df = df.dropna(subset=["discipline", "athlete_id", "sex"])

    # Count athletes by sport and sex
    athlete_counts = (
        df.groupby(["discipline", "sex"])["athlete_id"].nunique().reset_index()
    )

    # Get top 10 sports by total athletes
    top_sports = (
        athlete_counts.groupby("discipline")["athlete_id"]
        .sum()
        .nlargest(top_n)
        .index.tolist()
    )

    # Filter to top 10 sports
    athlete_counts = athlete_counts[athlete_counts["discipline"].isin(top_sports)]

    # Sort sports by total athletes (for consistent order)
    sport_order = (
        athlete_counts.groupby("discipline")["athlete_id"]
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )
    athlete_counts["discipline"] = pd.Categorical(
        athlete_counts["discipline"], categories=sport_order, ordered=True
    )
    return athlete_counts
