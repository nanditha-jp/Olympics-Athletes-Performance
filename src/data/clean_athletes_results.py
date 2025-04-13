import numpy as np
import pandas as pd

import re
import os
import src.utils as utils

# configure logger
logger = utils.configure_logger("Cleaning Athletes Results", "clean_results.log")

def clean_game_column(data: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.debug("Cleaning game column")
        df = data.copy()

        df["year"] = df["Games"].str.split().str.get(0).str.extract(r'(\d{4})')[0]
        df["type"] = df["Games"].str.split().str.get(1)

        df["year"] = df["year"].astype(int)

        return df

    except Exception as e:
        logger.error("Error cleaning game column: %s", e)
        return pd.DataFrame()

def remove_unnecessary_columns(data: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.debug("Removing unnecessary columns")
        df = data.copy()
        columns_to_remove = ["Games", "Nationality", "Unnamed: 7"]
        return df.drop(columns=columns_to_remove)

    except Exception as e:
        logger.error("Error removing unnecessary columns: %s", e)
        return pd.DataFrame()

def extract_postions(data: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.debug("Extracting positions")
        df = data.copy()

        def parse_position(pos_val):
            if pd.isna(pos_val):
                return None

            if isinstance(pos_val, (int, float)):
                return float(pos_val)

            pos_str = str(pos_val).strip()

            # These are status codes, not positions
            if re.match(r'(?i)^\s*(DNS|DNF|DSQ|RET|WD|AC)', pos_str):
                return None

            # Remove '=' if it's used to indicate tied positions like '=81'
            pos_str = pos_str.lstrip('=').strip()

            # Extract leading number only (to avoid grabbing lane/heat numbers)
            match = re.match(r'^(\d+)', pos_str)
            if match:
                return float(match.group(1))

            return None
        
        df["Pos"] = df["Pos"].apply(parse_position)

        return df

    except Exception as e:
        logger.error("Error extracting positions: %s", e)
        return pd.DataFrame()

def rename_and_reorder(data: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.debug("Renaming and reordering columns")
        df = data.copy()

        df = df.rename(columns={
            "Pos": "pos",
            "NOC": "noc",
            "Event": "event",
            "Discipline": "discipline",
            "Team": "team",
            "As": "as",
            "Medal": "medal"
        })

        columns_ordered = ['athlete_id', 'noc', 'year', 'type', 'discipline', 'event', 'team', 'as','pos', 'medal']

        return df[columns_ordered]

    except Exception as e:
        logger.error("Error renaming and reordering columns: %s", e)
        return pd.DataFrame()


if __name__ == "__main__":

    try:
        # load data
        data_path = os.path.join("data", "raw")
        file_path = os.path.join(data_path, "results.csv")

        results = utils.load_data(file_path, logger)
        if results.empty:
            raise ValueError("Data is empty")

        # clean data pipeline
        results = (
            results.pipe(clean_game_column)
            .pipe(extract_postions)
            .pipe(remove_unnecessary_columns)
            .pipe(rename_and_reorder)
        )

        # save data
        data_path = os.path.join("data", "interim")
        utils.save_data(results, data_path, "results.csv", logger)

    except Exception as e:
        logger.error("Error cleaning athletes: %s", e)
