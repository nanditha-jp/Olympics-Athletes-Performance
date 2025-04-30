import pandas as pd
import os
import logging

def load_data(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    try:
        logger.debug("Loading data from %s", file_path)
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error("Error loading data: %s", e)
        return pd.DataFrame()

def save_data(data: pd.DataFrame, data_path: str, file_name: str, logger: logging.Logger) -> None:
    try:
        logger.debug("Saving Data")
        os.makedirs(data_path, exist_ok=True)
        data.to_csv(os.path.join(data_path, file_name), index=False)
        logger.info("Data saved successfully")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
