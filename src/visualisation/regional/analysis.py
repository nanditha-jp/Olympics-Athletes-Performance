import numpy as np
import pandas as pd

import os
import src.utils as utils

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


def country_sending_athletes(filters, top_n):
    df = utils.apply_filters(merged, filters)
    df = df.rename(columns={"noc_y": "country", "noc_x": "noc"})
    df = df.dropna(subset=["country"])

    country_sending_athletes = df.groupby("country").size().reset_index(name="athlete_count")

    if top_n is not None:
        country_sending_athletes = country_sending_athletes.sort_values("athlete_count", ascending=False)
        return country_sending_athletes.head(top_n)

    return country_sending_athletes
