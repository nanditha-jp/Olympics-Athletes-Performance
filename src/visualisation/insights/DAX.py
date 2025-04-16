import pandas as pd

def performance_score(group: pd.DataFrame) -> float:
    total_athletes = group['athlete_id'].count()
    if total_athletes == 0:
        return 0.0
    medal_winners = group['medal'].notna().sum()
    return medal_winners / total_athletes * 100
