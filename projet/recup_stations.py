import pandas as pd

#https://data.iledefrance-mobilites.fr/explore/dataset/emplacement-des-gares-idf/export/?location=8,48.69899,2.33167&basemap=jawg.streets

link = "https://data.iledefrance-mobilites.fr/explore/dataset/emplacement-des-gares-idf/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"

stations = pd.read_csv(link, sep=";")

stations = stations[stations["metro"] == 1]
stations = stations[stations["idf"] == 1]

stations["id"] = range(stations.shape[0])

stations = stations[["id", "nom", "indice_lig", "termetro", "Geo Point"]]

stations.columns = ["id", "name", "ligne", "terminus", "coordinates"]

stations["coordinates"] = stations["coordinates"].apply(lambda coord: [float(c) for c in coord.split(",")])
stations["lat"] = stations["coordinates"].apply(lambda coord: coord[0])
stations["long"] = stations["coordinates"].apply(lambda coord: coord[1])
stations.drop("coordinates", axis=1, inplace=True)

stations["terminus"] = stations["terminus"].apply(lambda x: 0 if x == "0" else 1)

stations.sort_values(by="name", inplace=True)

stations.to_csv("stations.csv", sep=";", encoding="utf-8", index=False)