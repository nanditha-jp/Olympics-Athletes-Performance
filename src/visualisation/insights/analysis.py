import os

from src.utils.logger import configure_logger
from src.utils.data_loader import load_and_merge_bios_results
from src.utils.filters import apply_filters
from src.utils.geo import merge_lat_long

from src.visualisation.insights import DAX

# configure logger
logger = configure_logger("Interactive Insights", "insights.log")

# load data
data_path = os.path.join("data", "interim")
bios_cols = ["athlete_id", "noc", "sex", "name"]
merged, _, _ = load_and_merge_bios_results(data_path, logger, bios_cols=bios_cols)


# Utilities
def get_unique(column):
    if column in merged.columns:
        return sorted(merged[column].dropna().unique().tolist())
    else:
        return []


# Analysis fns
def participation_of_gender_over_time(filters):
    df = apply_filters(merged, filters)

    # Group by Year and Sex to count athletes
    df_grouped = (
        df.groupby(["year", "sex"])["athlete_id"]
        .count()
        .reset_index(name="Participants")
    )

    return df_grouped


def athletes_by_total_medal_by_their_country_and_event(filters):
    df = apply_filters(merged, filters)

    df = df[df["medal"].notnull()]
    # Group by Full name, born_country (or NOC), and Event to count medals
    grouped = df.groupby(["name", "country", "event"]).size().reset_index(name="Medals")

    # Sort by Medals descending
    top_medalists = grouped.sort_values(by="Medals", ascending=False)
    return top_medalists


def medal_distribution(filters):
    df = apply_filters(merged, filters)
    df = df.dropna(subset=["medal"])

    # Count medals
    medal_counts = df["medal"].value_counts().reset_index()
    medal_counts.columns = ["medal", "count"]

    return medal_counts


def performance_score_by_noc(filters):
    df = apply_filters(merged, filters)
    df = merge_lat_long(df, logger)
    df.dropna(subset=["latitude", "longitude"], inplace=True)

    # Basic grouped metrics
    grouped = (
        df.groupby("noc").agg({"latitude": "mean", "longitude": "mean"}).reset_index()
    )

    # Performance score separately using groupby + apply
    performance = (
        df.groupby("noc")
        .apply(DAX.performance_score)
        .reset_index(name="Performance Score")
    )

    # Merge them
    df = grouped.merge(performance, on="noc", how="left")
    return df
