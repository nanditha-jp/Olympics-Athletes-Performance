import numpy as np
import pandas as pd

import os
import src.utils as utils

from src.visualisation.insights import DAX

# configure logger
logger = utils.configure_logger("Interactive Insights", "insights.log")

# load data
data_path = os.path.join("data", "interim")

bios = utils.load_data(os.path.join(data_path, "bios.csv"), logger)
results = utils.load_data(os.path.join(data_path, "results.csv"), logger)

# merge data
merged = results.merge(
    bios[["athlete_id", "noc", "sex", "name"]], on="athlete_id", how="left"
)

merged = merged.rename(columns={"noc_y": "country", "noc_x": "noc"})

# Utilities
def get_unique(column):
    if column in merged.columns:
        return sorted(merged[column].dropna().unique().tolist())
    else:
        return []

# Analysis fns
def participation_of_gender_over_time(filters):
    df = utils.apply_filters(merged, filters)

    # Group by Year and Sex to count athletes
    df_grouped = df.groupby(["year", "sex"])["athlete_id"].count().reset_index(name="Participants")

    return df_grouped

def athletes_by_total_medal_by_their_country_and_event(filters):
    df = utils.apply_filters(merged, filters)

    df = df[df['medal'].notnull()]
    # Group by Full name, born_country (or NOC), and Event to count medals
    grouped = df.groupby(['name', 'country', 'event']).size().reset_index(name='Medals')

    # Sort by Medals descending
    top_medalists = grouped.sort_values(by='Medals', ascending=False)
    return top_medalists

def medal_distribution(filters):
    df = utils.apply_filters(merged, filters)
    df = df.dropna(subset=["medal"])

    # Count medals
    medal_counts = df["medal"].value_counts().reset_index()
    medal_counts.columns = ["medal", "count"]

    return medal_counts

def merge_lat_long(df):
    noc_region_path = "https://raw.githubusercontent.com/prasertcbs/basic-dataset/refs/heads/master/noc_regions.csv"
    noc_region = utils.load_data(noc_region_path, logger)
    lat_long_path = "https://raw.githubusercontent.com/google/dspl/master/samples/google/canonical/countries.csv"
    lat_long = utils.load_data(lat_long_path, logger)

    lat_long = lat_long.merge(noc_region, left_on="name", right_on="region", how="inner")

    df = df.merge(lat_long, left_on="noc", right_on="NOC", how="left")
    return df

def performance_score_by_noc(filters):
    df = utils.apply_filters(merged, filters)
    df = merge_lat_long(df)
    df.dropna(subset=["latitude", "longitude"], inplace=True)

    # Basic grouped metrics
    grouped = df.groupby("noc").agg({
        "latitude": "mean",
        "longitude": "mean"
    }).reset_index()

    # Performance score separately using groupby + apply
    performance = df.groupby("noc").apply(DAX.performance_score).reset_index(name="Performance Score")

    # Merge them
    df = grouped.merge(performance, on="noc", how="left")
    return df
