import numpy as np
import pandas as pd

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
            .pipe(remove_unnecessary_columns)
        )

        # save data
        data_path = os.path.join("data", "interim")
        utils.save_data(results, data_path, "results.csv", logger)

    except Exception as e:
        logger.error("Error cleaning athletes: %s", e)
