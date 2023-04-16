import pandas as pd

stations = pd.read_csv("stations.csv", sep=";", encoding="utf-8")

lignes = stations["ligne"].unique()

for ligne in lignes:
    
    with open(f"lignes_metro/metro_{ligne}.txt", "r", encoding="utf-8") as file:
        
        rows = list(map(lambda word: word.replace("\n", ""), file.readlines()))

    ligne_df = stations[stations["ligne"] == ligne]

    new_rows = []
    for row in rows:
        new_row = ""
        for name in row.split(";"):
            id_of_name = ligne_df[ligne_df["name"] == name].iloc[0, 0]
            if new_row:
                new_row += ";" + str(id_of_name)
            else:
                new_row = str(id_of_name)
        new_rows.append(new_row)

    with open(f"lignes_metro_stations_ids/metro_{ligne}.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(new_rows))

