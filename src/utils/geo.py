from .io import load_data

def merge_lat_long(df, logger):
    noc_region_path = "https://raw.githubusercontent.com/prasertcbs/basic-dataset/refs/heads/master/noc_regions.csv"
    lat_long_path = "https://raw.githubusercontent.com/google/dspl/master/samples/google/canonical/countries.csv"

    noc_region = load_data(noc_region_path, logger)
    lat_long = load_data(lat_long_path, logger)

    lat_long = lat_long.merge(noc_region, left_on="name", right_on="region", how="inner")
    df = df.merge(lat_long, left_on="noc", right_on="NOC", how="left")
    return df
