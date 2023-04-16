## source : https://fr.wikipedia.org/wiki/Mod%C3%A8le:M%C3%A9tro_de_Paris/couleur_fond

metro_colors = {}

with open("metro_colors.txt", "r") as file:
    for row in file:
        metro, color = row.split()
        metro_colors[metro] = color