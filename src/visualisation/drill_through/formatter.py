def add_athlete_link(row):
    row["Name"] = f'<a href="/?page=Drill%20Through&id={row["Athlete ID"]}">{row["Name"]}</a>'
    return row

def add_country_link(row):
    row["Country"] = f'<a href="/?page=Drill%20Through&noc={row["NOC"]}">{row["Country"]}</a>'
    return row
