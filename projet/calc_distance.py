import pandas as pd
from datetime import timedelta
from geopy.distance import distance #télécharger cette librairie => pip install geopy

## Faire la distance entre les station du meme métro (en train)
## Faire la distance entre les stations qui ont le meme nom mais qui ne sont pas dans le même métro (à la marche)

MOY_SPEED_METRO = 21 #km/h
MOY_SPEED_WALK = 5 #km/h


stations = pd.read_csv("stations.csv", sep=";")

### Partie train dans les gares du même métro
times = {}
for i in range(stations.shape[0]):
    actual_station = stations.iloc[i]
    
    actual_id = actual_station.iloc[0]
    actual_coord = actual_station.iloc[-3:-1].to_list()
    
    linked_stations_ids = list(map(int, actual_station.iloc[-1].split(";")))

    for station_id in linked_stations_ids:
        station = stations[stations["id"] == station_id].iloc[0]

        coord = station.iloc[-3:-1].to_list()
        
        time = distance(actual_coord, coord).km / MOY_SPEED_METRO
        time = timedelta(hours=time).seconds
        
        times[(actual_id, station_id)] = time
    
    
### Pour ne pas surcharger la carte avec des directions inutiles (car les directions sont faites dans les deux sens)
direction_unique = []
for element in times.keys():
    if element[::-1] not in direction_unique:
        direction_unique.append(element)



stations_names_duplicated = stations[stations["name"].duplicated()]["name"].unique()


### Partie Marche entre les gares de même nom
times_walk = {}
for name in stations_names_duplicated:
    stations_names = stations[stations["name"] == name]

    for i in range(stations_names.shape[0]):
        
        station_one_id = stations_names.iloc[i, 0]
        coord_one = stations_names.iloc[i, -3:-1].to_list()

        for j in range(stations_names.shape[0]):
            if i != j:

                station_two_id = stations_names.iloc[j, 0]
                coord_two = stations_names.iloc[j, -3:-1].to_list()

                time = distance(coord_one, coord_two).km / MOY_SPEED_WALK
                time = timedelta(hours=time).seconds 

                times_walk[(station_one_id, station_two_id)] = time


### On combine dans le même dictionnaire les distances au dessus pour l'algo de plus court chemin
total_times = {}
total_times.update(times)
total_times.update(times_walk)


