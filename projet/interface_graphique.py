import streamlit as st # pip install streamlit
import folium # pip install folium
from streamlit_folium import folium_static

import pandas as pd

st.set_page_config(page_title="Metro stations", page_icon="🚃", layout="wide", initial_sidebar_state="auto")

from metro_colors import metro_colors
from calc_distance import direction_unique
from graphes import graphe, shortest_path


PARIS_COORDINATES = [48.856614, 2.3522219]


stations = pd.read_csv("stations.csv", sep=";")

st.title("Metro Stations 🚃")

## Partie pour afficher les différents noms de métro possible sur l'interface graphique
stations_names = stations["name"].unique().tolist()

st.subheader("*Trouver un itinéraire*")

col1, col2 = st.columns(2)

start_station_name = col1.selectbox(label="Station de départ", options = [None] + stations_names)
end_station_name = col2.selectbox(label="Station d'arrivée", options = [None] + stations_names)


## La carte du métro parisien
map = folium.Map(location=PARIS_COORDINATES, zoom_start=12)


## Lorsque des noms valides sont séléctionnés on affiche le chemin le plus court
if start_station_name and end_station_name and start_station_name != end_station_name:

    start_station = stations[stations["name"] == start_station_name].iloc[0]
    end_station = stations[stations["name"] == end_station_name].iloc[0]

    start_loc = start_station.iloc[-3:-1].to_list()
    end_loc = end_station.iloc[-3:-1].to_list()

    folium.Marker(location=start_loc, popup="Vous êtes ici").add_to(map)
    folium.Marker(location=end_loc, popup="Vous êtes arrivé").add_to(map)

    start_id = start_station.iloc[0]
    end_id = end_station.iloc[0]

    path, distance = shortest_path(graphe, start_id, end_id)

    st.write("**Itinéraire**")
    st.write(f"Vous partez de {start_station_name}")
    begin = start_station_name

    for i in range(len(path) - 1):

        mid_start_station_id = path[i]
        mid_end_station_id = path[i+1]

        mid_start_station = stations[stations["id"] == mid_start_station_id].iloc[0]
        mid_end_station = stations[stations["id"] == mid_end_station_id].iloc[0]

        mid_start_station_name = mid_start_station["name"] 
        mid_end_station_name = mid_end_station["name"]

        mid_start_loc = mid_start_station.iloc[-3:-1].to_list()
        mid_end_loc = mid_end_station.iloc[-3:-1].to_list()

        metro = mid_start_station.loc["ligne"]
        metro_color = metro_colors[metro] 

        if mid_start_station_name == mid_end_station_name:
            st.write(f"Prenez le métro {metro} de {begin} à {mid_start_station_name}")
            st.write(f"Marchez du métro {mid_start_station['ligne']} au métro {mid_end_station['ligne']}")
            begin = mid_end_station_name

            folium.PolyLine([mid_start_loc, mid_end_loc], color="black", popup="walk").add_to(map)

        else:
            folium.PolyLine([mid_start_loc, mid_end_loc], color=metro_color, popup=f"Metro_{metro}").add_to(map)

    st.write(f"Prenez le métro {metro} de {begin} à {end_station_name}")
    st.write(f"Arrivée à {end_station_name} en {int(round(distance/60, 0))} min")

## Sinon on affiche la carte du métro parisien
else:

    for id_one, id_two in direction_unique:

        station_one = stations[stations["id"] == id_one].iloc[0]
        station_two = stations[stations["id"] == id_two].iloc[0]

        coord_one = station_one.iloc[-3:-1].to_list()
        coord_two = station_two.iloc[-3:-1].to_list()

        metro = station_one.loc["ligne"]
        metro_color = metro_colors[metro]

        folium.PolyLine([coord_one, coord_two], color=metro_color, popup=f"Metro_{metro}").add_to(map)

        term_one = station_one.loc["terminus"]
        term_two = station_two.loc["terminus"]

        if term_one == 1:
            folium.CircleMarker(coord_one, radius=20, color=metro_color, popup=station_one.loc["name"], fill=True).add_to(map)
    
        if term_two == 1:
            folium.CircleMarker(coord_two, radius=20, color=metro_color, popup=station_two.loc["name"], fill=True).add_to(map)


folium_static(map, width=1530, height=700)