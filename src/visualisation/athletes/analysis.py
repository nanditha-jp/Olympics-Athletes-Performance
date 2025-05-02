import os
import requests

from src.utils.logger import configure_logger
from src.utils.geo import merge_lat_long
from src.utils.data_loader import load_and_merge_bios_results

from src.utils.filters import apply_filters

# configure logger
logger = configure_logger("Athletes", "athletes.log")

# load data
data_path = os.path.join("data", "interim")
merged, _, _ = load_and_merge_bios_results(data_path, logger)


def get_athlete_data(athlete_id):
    df = merged[merged["athlete_id"] == int(athlete_id)].copy()
    df = merge_lat_long(df, logger)
    return df


def get_athlete_image(athlete_id) -> str:

    url = f"https://d2a3o6pzho379u.cloudfront.net/{athlete_id}.jpg"
    response = requests.head(url, timeout=5)
    if response.status_code == 200 and "image" in response.headers.get(
        "Content-Type", ""
    ):
        return url
    return "https://cdn3d.iconscout.com/3d/premium/thumb/tennis-player-3d-icon-download-in-png-blend-fbx-gltf-file-formats--athlete-avatar-arhlete-avatars-pack-people-icons-8263140.png?f=webp"


def get_athlete_bio(df) -> dict:
    return {
        "Name": df["name"].unique()[0],
        "Full Name": df["full_name"].unique()[0],
        "NOC": df["noc"].unique()[0],
        "Sport": list(df["discipline"].unique()),
        "Years": list(df["year"].unique()),
        "Country": df["country"].unique()[0],
        "Sex": df["sex"].unique()[0],
        "Born Date": df["born_date"].unique()[0],
        "Born City": df["born_city"].unique()[0],
        "height": df["height"].unique()[0],
        "weight": df["weight"].unique()[0],
    }


def get_summary(df, filters):
    apply_filters(df, filters)

    medal_df = df[df["medal"].notna()]
    medal_df.fillna("", inplace=True)
    # Group by name, team, and noc; count each medal type
    medal_summary = (
        medal_df.groupby(["full_name", "team", "noc"])["medal"]
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Add total medals column
    medal_summary["Medals"] = medal_summary.sum(axis=1, numeric_only=True)

    # Rename for display
    medal_summary = medal_summary.rename(
        columns={"full_name": "Name", "team": "Team", "noc": "NOC"}
    )

    # Reorder columns (handle missing medal types gracefully)
    expected_cols = ["Name", "Team", "Gold", "Silver", "Bronze", "Medals", "NOC"]
    for col in ["Gold", "Silver", "Bronze"]:
        if col not in medal_summary.columns:
            medal_summary[col] = 0

    # Final ordering
    medal_summary = medal_summary[expected_cols]
    return medal_summary
