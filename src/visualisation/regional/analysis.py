import numpy as np
import pandas as pd

import os
import src.utils as utils

from src.visualisation.regional import DAX

# configure logger
logger = utils.configure_logger("Visualisation", "regional.log")

# load data
data_path = os.path.join("data", "interim")

bios = utils.load_data(os.path.join(data_path, "bios.csv"), logger)
results = utils.load_data(os.path.join(data_path, "results.csv"), logger)

# merge data
merged = results.merge(
    bios[["athlete_id", "noc", "sex"]], on="athlete_id", how="left"
)
merged = merged.rename(columns={"noc_y": "country", "noc_x": "noc"})

# Utilities
def get_unique(column):
    if column in merged.columns:
        return sorted(merged[column].dropna().unique().tolist())
    else:
        return []

def merge_lat_long(df):
    noc_region_path = "https://raw.githubusercontent.com/prasertcbs/basic-dataset/refs/heads/master/noc_regions.csv"
    noc_region = utils.load_data(noc_region_path, logger)
    lat_long_path = "https://raw.githubusercontent.com/google/dspl/master/samples/google/canonical/countries.csv"
    lat_long = utils.load_data(lat_long_path, logger)

    lat_long = lat_long.merge(noc_region, left_on="name", right_on="region", how="inner")

    df = df.merge(lat_long, left_on="noc", right_on="NOC", how="left")
    return df


def country_sending_athletes(filters, top_n):
    df = utils.apply_filters(merged, filters)
    df = df.dropna(subset=["country"])

    country_sending_athletes = df.groupby("country").size().reset_index(name="athlete_count")

    if top_n is not None:
        country_sending_athletes = country_sending_athletes.sort_values("athlete_count", ascending=False)
        return country_sending_athletes.head(top_n)

    return country_sending_athletes

def region_sending_athletes(filters):
    df = utils.apply_filters(merged, filters)
    df = merge_lat_long(df)
    df.dropna(subset=["latitude", "longitude"], inplace=True)

    region_sending_athletes = df.groupby("noc").agg({
        "athlete_id": "count",
        "latitude": "mean",
        "longitude": "mean"
    }).reset_index()
    
    region_sending_athletes.rename(columns={"athlete_id": "total_athletes"}, inplace=True)

    return region_sending_athletes

def gender_participation(filters):
    df = utils.apply_filters(merged, filters)

    # Count of athletes by Discipline and Sex
    athlete_counts = (
        df.groupby(['discipline', 'sex'])['athlete_id']
        .nunique()
        .reset_index(name='Count')
    )

    return athlete_counts

def medal_efficiency_ratio(filters):
    df = utils.apply_filters(merged, filters)
    
    grouped = df.groupby("noc").apply(DAX.medal_efficiency_ratio).reset_index(name="medal_efficiency_ratio")

    noc_region_path = "https://raw.githubusercontent.com/prasertcbs/basic-dataset/refs/heads/master/noc_regions.csv"
    noc_region = utils.load_data(noc_region_path, logger)

    df = grouped.merge(noc_region, left_on="noc", right_on="NOC", how="left")
    df = df.sort_values(by="medal_efficiency_ratio", ascending=False)

    return df[["region", "medal_efficiency_ratio"]].rename(columns={
        "region": "Country",
        "medal_efficiency_ratio": "Medal Efficiency Ratio"
    })

def sport_medal_percentage(filters, top_n):
    df = utils.apply_filters(merged, filters)
    total_medals = df[df['medal'].notna() & (df['medal'] != '')].shape[0]

    df = df.groupby("discipline").apply(lambda x: DAX.sport_medal_percentage(x) / total_medals).reset_index(name="sport_performance_ratio")

    if top_n is not None:
        df = df.sort_values(by="sport_performance_ratio", ascending=False)
        return df.head(top_n)

    return df
