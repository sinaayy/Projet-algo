import pandas as pd

stations = pd.read_csv("stations.csv", sep=";", encoding="utf-8")

lignes = stations["ligne"].unique()

lignes_metro = []

for ligne in lignes:
    metro = {}
    
    with open(f"lignes_metro_stations_ids/metro_{ligne}.txt", "r", encoding="utf-8") as file:
        
        rows = list(map(lambda word: word.replace("\n", ""), file.readlines()))
    

    last_row = ""
    for row in rows:
            
        row_elements = row.split(";")
        last_row_elements = last_row.split(";")

        if len(last_row_elements) == len(row_elements):
            for i in range(len(row_elements)):
                metro[row_elements[i]] = last_row_elements[i]
        else:
            for i in range(len(row_elements)):
                metro[row_elements[i]] = ";".join(last_row_elements)
        last_row = row
        
    
    inverse_rows = rows[::-1]


    last_row = ""
    for row in inverse_rows:

        row_elements = row.split(";")
        last_row_elements = last_row.split(";")

        if len(last_row_elements) == len(row_elements):
            for i in range(len(row_elements)):
                add_char = ";" if metro[row_elements[i]] != "" and last_row_elements[i] != "" else ""
                metro[row_elements[i]] += add_char + last_row_elements[i]
        else:
            for i in range(len(row_elements)):
                add_char = ";" if metro[row_elements[i]] != "" and len(last_row_elements) != 0 else ""
                metro[row_elements[i]] += add_char + ";".join(last_row_elements)
        last_row = row 

    
    ligne_df = stations[stations["ligne"] == ligne]
    ligne_df["links"] = ligne_df["id"].astype(str).map(metro)
    lignes_metro.append(ligne_df)


stations = pd.concat(lignes_metro)
stations.to_csv("stations.csv", sep=";", encoding="utf-8", index=False)