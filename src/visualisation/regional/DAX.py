import pandas as pd

def medal_efficiency_ratio(df: pd.DataFrame) -> float:
    # Count number of rows with a non-empty medal
    medalists = df[df['medal'].notna() & (df['medal'] != '')].shape[0]

    # Count distinct athletes (by ID)
    total_athletes = df['athlete_id'].nunique()

    # Avoid divide-by-zero
    if total_athletes == 0:
        return 0.0

    return medalists / total_athletes

def sport_medal_percentage(df: pd.DataFrame) -> float:
    # Filter for non-empty medal and non-empty sport
    sport_medals = df[
        df['medal'].notna() & (df['medal'] != '') &
        df['discipline'].notna() & (df['discipline'] != '')
    ].shape[0]

    return sport_medals
