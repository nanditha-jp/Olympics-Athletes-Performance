import os
from .io import load_data

def load_and_merge_bios_results(data_path, logger, bios_cols=None, results_cols=None):
    bios = load_data(os.path.join(data_path, "bios.csv"), logger)
    results = load_data(os.path.join(data_path, "results.csv"), logger)

    if bios_cols is None:
        bios_cols = bios.columns
    if results_cols is None:
        results_cols = results.columns

    bios_filtered = bios[bios_cols]
    results_filtered = results[results_cols]

    merged = results_filtered.merge(bios_filtered, on="athlete_id", how="left")

    if "noc_x" in merged.columns and "noc_y" in merged.columns:
        merged = merged.rename(columns={"noc_y": "country", "noc_x": "noc"})

    return merged, bios, results
