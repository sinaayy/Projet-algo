## Permet d'enregistrer les différentes stations de chaque métro
## pour les remettre dans l'ordre à la main

import pandas as pd

# source : https://www.ratp.fr/plans-lignes/metro/14

datas = pd.read_csv("stations.csv", sep=";")

lignes = datas["ligne"].unique()

for ligne in lignes:
    stations = datas[datas["ligne"] == ligne]["name"].to_list()
    with open(f"lignes/metro_{ligne}.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(stations))