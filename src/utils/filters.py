def apply_filters(df, filters):
    for column, values in filters.items():
        if column in df.columns:
            df = df[df[column].isin(values)]
    return df
