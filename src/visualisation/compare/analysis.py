import os

from src.utils.logger import configure_logger
from src.utils.data_loader import load_and_merge_bios_results
from src.utils.filters import apply_filters
from src.utils.geo import merge_lat_long

# configure logger
logger = configure_logger("Comparative Analysis", "compare.log")

# load data
data_path = os.path.join("data", "interim")

bios_col = ["athlete_id", "born_year", "sex", "noc"]
merged, _, _ = load_and_merge_bios_results(data_path, logger, bios_cols=bios_col)


def get_unique(column):
    if column in merged.columns:
        return sorted(merged[column].dropna().unique().tolist())
    else:
        return []


# Analysis
def countries_based_on_medals(filters, top_n):
    df = apply_filters(merged, filters)
    df = df.dropna(subset=["medal", "country"])
    top_countries = (
        df.groupby("country")["medal"]
        .count()
        .reset_index()
        .sort_values("medal", ascending=False)
        .rename(columns={"medal": "Medals", "country": "Country"})
    )
    if top_n is not None:
        return top_countries.head(top_n)
    return top_countries


def compare_countries_by_medal(filters, sport, country_a, country_b):
    df = apply_filters(merged, filters)

    df = df[df["discipline"].isin(sport)]
    df = df[df["country"].isin([country_a, country_b])]

    countries_df = df.groupby(["country", "year"])["medal"].count().reset_index()

    return countries_df


def compare_countries_by_athletes(filters, sport, country_a, country_b):
    df = apply_filters(merged, filters)

    df = df[df["discipline"].isin(sport)]
    df = df[df["country"].isin([country_a, country_b])]

    countries_df = df.groupby(["country", "year"])["athlete_id"].count().reset_index()

    return countries_df


def medal_distribution_by_gender(filters):
    df = apply_filters(merged, filters)
    df = df.dropna(subset=["medal", "sex"])

    medal_counts = df.groupby(["medal", "sex"])["athlete_id"].count().reset_index()

    return medal_counts


def athlete_counts_by_country(filters):
    df = apply_filters(merged, filters)
    df = merge_lat_long(df, logger)

    df.dropna(subset=["latitude", "longitude"], inplace=True)

    grouped = (
        df.groupby("noc")
        .agg({"athlete_id": "count", "latitude": "mean", "longitude": "mean"})
        .reset_index()
    )

    grouped.rename(columns={"athlete_id": "total_athletes"}, inplace=True)
    return grouped
