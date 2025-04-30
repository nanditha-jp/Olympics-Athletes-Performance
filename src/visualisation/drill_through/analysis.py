import os

from src.utils.logger import configure_logger
from src.utils.data_loader import load_and_merge_bios_results
from src.utils.filters import apply_filters

from src.visualisation.drill_through import DAX

# configure logger
logger = configure_logger("Drill Through", "drill_through.log")

# load data
data_path = os.path.join("data", "interim")

bios_col = ["athlete_id", "name", "noc", "born_year"]
merged, _, _ = load_and_merge_bios_results(data_path, logger, bios_cols=bios_col)
merged["age"] = merged["year"].astype(float) - merged["born_year"].astype(float)


def athlete_wise_medal_distribution(filters, top_n):
    df = apply_filters(merged, filters)
    # Filter only rows with medals
    medal_results = df[df["medal"].notna()]

    # Count medals per athlete
    medal_count = (
        medal_results.groupby(["athlete_id", "name"]).size().reset_index(name="medal")
    )
    # Sort
    medal_count = medal_count.sort_values(by="medal", ascending=False)
    # extract top_n
    medal_count = medal_count.head(top_n)

    return medal_count.rename(
        columns={"name": "Name", "medal": "Medals", "athlete_id": "Athlete ID"}
    )


def country_wise_medal_distribution(filters, top_n):
    df = apply_filters(merged, filters)
    # Filter only rows with medals
    medal_results = df[df["medal"].notna()]

    # Count medals per athlete
    medal_count = (
        medal_results.groupby(["noc", "country"]).size().reset_index(name="medal")
    )
    # Sort
    medal_count = medal_count.sort_values(by="medal", ascending=False)
    # extract top_n
    medal_count = medal_count.head(top_n)

    return medal_count.rename(
        columns={"noc": "NOC", "country": "Country", "medal": "Medals"}
    )


def drill_athlete(athlete_id):
    df = merged[merged["athlete_id"] == int(athlete_id)]
    return df


def drill_country(noc):
    df = merged[merged["noc"] == noc]
    return df


# Trend and distribution Analysis
def age_distribution_across_sports(filters, top_n):
    df = apply_filters(merged, filters)
    # Clean data: drop rows with missing sport, athlete_id or sex
    df = df.dropna(subset=["discipline", "age"])

    # Group by Discipline and calculate average age
    avg_age_by_sport = df.groupby("discipline")["age"].mean().reset_index()

    # Sort by average age
    avg_age_by_sport = avg_age_by_sport.sort_values(by="age", ascending=False)

    # Get top 10 sports by average age
    avg_age_by_sport = avg_age_by_sport.head(top_n)

    return avg_age_by_sport


def participation_trend_over_time(filters, past_n_years=10):
    df = merged.copy()
    # Filter for the past 10 years (e.g., from 2010 onward)
    if "year" in filters.keys():
        max_year = max(filters["year"])
    else:
        max_year = max(df["year"])
    filtered = df[df["year"].isin(range(max_year - past_n_years, max_year + 1))]

    # Group by year and count all athlete_id entries
    yearly_counts = filtered.groupby("year")["athlete_id"].count().reset_index()
    yearly_counts.columns = ["Year", "Athletes"]

    return yearly_counts


def sport_growth_participation(filters, top_n):
    df = apply_filters(merged, filters)

    df = (
        df.groupby("discipline")
        .apply(DAX.participation_growth_rate)
        .reset_index(name="participation_growth_rate")
    )

    df = df.sort_values(by="participation_growth_rate", ascending=False)

    if top_n is not None:
        return df.head(top_n)
    return df
