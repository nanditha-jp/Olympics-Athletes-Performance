import pandas as pd

def participation_growth_rate(df: pd.DataFrame) -> float:
    # Make sure year column is numeric
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    
    # Drop missing year rows
    df = df.dropna(subset=["year"])
    
    min_year = df["year"].min()
    max_year = df["year"].max()

    # Count of athletes in min and max year
    old_count = df[df["year"] == min_year]["athlete_id"].nunique()
    new_count = df[df["year"] == max_year]["athlete_id"].nunique()

    if old_count == 0:
        return 0.0

    growth_rate = (new_count - old_count) / old_count
    return growth_rate
