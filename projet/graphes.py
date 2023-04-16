from calc_distance import total_times

### Vérifier que le graphe est connexe

## Pour cela il faut que peu importe le sommet sur lequel on commence à parcourir le graphe
## tous les points doivent être accessibles

## Le graphe qui nous interesse est celui avec toutes les distances (marche et métro)


## On crée le graphe avec un dictionnaire qui associe à chaque id tous les ids auquel il est connecté
all_links = total_times.keys()
graphe = {}
for id_one, id_two in all_links:
    if id_one not in graphe:
        graphe[id_one] = []
    
    graphe[id_one].append(id_two)


## Permet de parcourir le graphe en partant d'un certain sommet
def bfs(graphe, s):
    
    visited = {s:None}
    queue = [s]

    while queue:
        u = queue.pop(0)
        for v in graphe[u]:
            if v in visited: 
                continue
            visited[v] = u
            queue.append(v)
    return visited


## Si on peut accéder à tous les points du graphe en partant de n'importe quel sommet alors le graphe est connexe
def est_connexe(graphe):
    for s in graphe.keys():
        if len(bfs(graphe, s)) != len(graphe):
            return False
    return True

#print(est_connexe(graphe))


## Algorithme de dijsktra que l'on va utiliser pour trouver les plus courts chemins
def dijsktra(graphe, s):
    T = {s}
    V = graphe.keys()
    distances = {i:100000 for i in range(len(graphe))}
    peres = {i:None for i in range(len(graphe))}
    distances[s] = 0

    for sommet in V - T:
        if (s, sommet) in total_times.keys():
            distances[sommet] = total_times[(s, sommet)]
            peres[sommet] = s
    
    sommet_prec = s

    while T != V: # le graphe doit être connexe pour que cela fonctionne
        min = 100000
        for sommet in V - T:
            if distances[sommet] < min:
                sommet_prec = sommet
                min = distances[sommet]

        T.add(sommet_prec)
        
        for k in V - T:
            if (sommet_prec, k) in total_times.keys():
                d = min + total_times[(sommet_prec, k)]
                if distances[k] > d:
                    distances[k] = d
                    peres[k] = sommet_prec
        
    return distances, peres


## Grace au résultat retourné par l'algorithme de dijsktra on peut retrouver le chemin le plus court entre deux sommets
def shortest_path(graphe, start, end):
    distances, peres = dijsktra(graphe, start)
    path = [end]
    last = end
    while last != start:
        path.append(peres[last])
        last = peres[last]

    path = path[::-1]

    return path, distances[end]
    # return les ids du chemin le plus court + le temps en secondes


#print(shortest_path(graphe, 0, 100))


### Quelques liens pour comprendre les graphes

## https://math.univ-lyon1.fr/irem/Formation_ISN/formation_parcours_graphes/largeur/3_python1.html
## http://www.monlyceenumerique.fr/nsi_terminale/sd/sd5_graphe.php
## https://iut-info.univ-reims.fr/users/blanchard/ISN20181218/les-graphes-from-scratch.html#implementation-simple
