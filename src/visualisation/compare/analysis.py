import numpy as np
import pandas as pd

import os
import src.utils as utils

# configure logger
logger = utils.configure_logger("Comparative Analysis", "compare.log")

# load data
data_path = os.path.join("data", "interim")

bios = utils.load_data(os.path.join(data_path, "bios.csv"), logger)
results = utils.load_data(os.path.join(data_path, "results.csv"), logger)

# merge data
merged = results.merge(
    bios[["athlete_id", "born_year", "sex", "noc"]], on="athlete_id", how="left"
)
merged = merged.rename(columns={"noc_y": "country", "noc_x": "noc"})

def get_unique(column):
    if column in merged.columns:
        return sorted(merged[column].dropna().unique().tolist())
    else:
        return []

# Analysis
def countries_based_on_medals(filters, top_n):
    df = utils.apply_filters(merged, filters)
    df = df.dropna(subset=["medal", "country"])
    top_countries = df.groupby("country")["medal"].count().reset_index().sort_values("medal", ascending=False).rename(columns={"medal": "Medals", "country": "Country"})
    if top_n is not None:
        return top_countries.head(top_n)
    return top_countries

def compare_countries_by_medal(filters, sport, country_a, country_b):
    df = utils.apply_filters(merged, filters)
    
    df = df[df["discipline"].isin(sport)]
    df = df[df["country"].isin([country_a, country_b])]

    countries_df = df.groupby(["country", "year"])["medal"].count().reset_index()

    return countries_df

def compare_countries_by_athletes(filters, sport, country_a, country_b):
    df = utils.apply_filters(merged, filters)
    
    df = df[df["discipline"].isin(sport)]
    df = df[df["country"].isin([country_a, country_b])]

    countries_df = df.groupby(["country", "year"])["athlete_id"].count().reset_index()

    return countries_df

def medal_distribution_by_gender(filters):
    df = utils.apply_filters(merged, filters)
    df = df.dropna(subset=["medal", "sex"])

    medal_counts = df.groupby(["medal", "sex"])["athlete_id"].count().reset_index()

    return medal_counts
