import numpy as np
import pandas as pd

import os

from src.utils.logger import configure_logger
from src.utils import io


# configure logger
logger = configure_logger("Cleaning Athletes Bio", "clean_bios.log")


def clean_name(data: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.debug("Cleaning name")
        df = data.copy()
        df["name"] = df["Used name"].str.replace("•", " ")
        return df
    except Exception as e:
        logger.error("Error cleaning name: %s", e)
        return pd.DataFrame()


def extract_height_weight(data: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.debug("Extracting height and weight")
        df = data.copy()

        # Split the Measurements column into height & weight columns
        df[["height_cm", "weight_kg"]] = df["Measurements"].str.split("/", expand=True)

        # Get rid of " cm" and the " kg" from our new columns
        df["height_cm"] = pd.to_numeric(
            df["height_cm"].str.strip(" cm"), errors="coerce"
        )
        df["weight_kg"] = pd.to_numeric(
            df["weight_kg"].str.strip(" kg"), errors="coerce"
        )

        return df

    except Exception as e:
        logger.error("Error extracting height and weight: %s", e)
        return pd.DataFrame()


def extract_born_details(data: pd.DataFrame) -> pd.DataFrame:
    try:
        df = data.copy()

        logger.debug("Extracting born date, year..")
        # Parse out dates from 'Born' and 'Died' columns
        date_pattern = r"(\d+ \w+ \d{4}|\d{4})"
        df["born_date"] = df["Born"].str.extract(date_pattern)
        df["born_year"] = df["Born"].str.extract(r"(\d{4})")

        df["born_date"] = pd.to_datetime(
            df["born_date"], format="mixed", errors="coerce"
        )
        df["born_year"] = pd.to_numeric(df["born_year"])

        logger.debug("Extracting born location")
        location_pattern = r"in ([\w\s()-]+), ([\w\s-]+) \((\w+)\)"
        df[["born_city", "born_region", "born_country"]] = df["Born"].str.extract(
            location_pattern, expand=True
        )

        return df

    except Exception as e:
        logger.error("Error extracting born details: %s", e)
        return pd.DataFrame()


def filter_columns(data: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.debug("Filtering columns")
        df = data.copy()
        columns_to_remove = [
            "Roles",
            "Used name",
            "Measurements",
            "Born",
            "Died",
            "Affiliations",
            "Nick/petnames",
            "Title(s)",
            "Other names",
            "Nationality",
            "Original name",
            "Name order",
        ]

        return df.drop(columns=columns_to_remove)

    except Exception as e:
        logger.error("Error filtering columns: %s", e)
        return pd.DataFrame()


def rename_and_reorder(data: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.debug("Renaming and reordering columns")
        df = data.copy()

        df = df.rename(
            columns={
                "Full name": "full_name",
                "Sex": "sex",
                "height_cm": "height",
                "weight_kg": "weight",
                "NOC": "noc",
            }
        )

        columns_ordered = [
            "athlete_id",
            "full_name",
            "name",
            "sex",
            "born_date",
            "born_year",
            "born_city",
            "born_region",
            "born_country",
            "height",
            "weight",
            "noc",
        ]

        return df[columns_ordered]

    except Exception as e:
        logger.error("Error renaming and reordering columns: %s", e)
        return pd.DataFrame()


if __name__ == "__main__":

    try:
        # load data
        data_path = os.path.join("data", "raw")
        file_path = os.path.join(data_path, "bios.csv")

        bios = io.load_data(file_path, logger)
        if bios.empty:
            raise ValueError("Data is empty")

        # clean data pipeline
        bios = (
            bios.pipe(clean_name)
            .pipe(extract_height_weight)
            .pipe(extract_born_details)
            .pipe(filter_columns)
            .pipe(rename_and_reorder)
        )

        # save data
        data_path = os.path.join("data", "interim")
        io.save_data(bios, data_path, "bios.csv", logger)

    except Exception as e:
        logger.error("Error cleaning athletes: %s", e)
