import numpy as np
import pandas as pd

# DAX
def total_athletes(df: pd.DataFrame) -> int:
    return len(df['athlete_id'].unique())

def total_events(df: pd.DataFrame) -> int:
    return len(df['event'].unique())

def avg_height(df: pd.DataFrame) -> float:
    return df['height'].mean()

def avg_age(df: pd.DataFrame) -> float:
    return df['age'].mean()
