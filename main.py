from ants import Fourmiliere
import networkx as nx
import matplotlib.pyplot as plt
import random

def lire_fichier_fourmiliere(fichier):
    """
    Lit un fichier de fourmilière et retourne les informations nécessaires pour simuler le déplacement des fourmis.
    """
    with open(fichier, 'r') as f:
        lignes = f.readlines()

    """
    Exemple de fichier de fourmilière:
    """
    nb_fourmis = int(lignes[0].strip().split('=')[1])
    salles = {'Sv': 0, 'Sd': 0}
    capacites = {'Sv': float('inf'), 'Sd': float('inf')}
    tunnels = {'Sv': [], 'Sd': []}
    i = 1

    """
    Exemple de fichier de fourmilière:
    """
    while i < len(lignes) and '-' not in lignes[i]:
        ligne = lignes[i].strip()
        if '{' in ligne:
            salle, capacite = ligne.split('{')
            salle = salle.strip()
            capacite = int(capacite.strip(' }'))
        else:
            salle = ligne
            capacite = 1
        salles[salle] = 0
        capacites[salle] = capacite
        tunnels[salle] = []
        i += 1

    while i < len(lignes):
        salle1, salle2 = lignes[i].strip().split(' - ')
        tunnels[salle1].append(salle2)
        tunnels[salle2].append(salle1)
        i += 1

    return nb_fourmis, salles, tunnels, capacites

if __name__ == "__main__":
    fichier = 'Nest/fourmiliere_cinq.txt'
    nb_fourmis, salles, tunnels, capacites = lire_fichier_fourmiliere(fichier)

    # print(f"Nombre de fourmis: {nb_fourmis}")
    # print(f"Salles: {salles}")
    # print(f"Capacités: {capacites}")
    # print(f"Tunnels: {tunnels}")

    fourmiliere = Fourmiliere(salles, tunnels, nb_fourmis, capacites)
    etapes = fourmiliere.simuler()


    # creation de graphique pour visualiser les salles, les tunnels et les fourmis
    G = nx.Graph()
    G.add_nodes_from(salles.keys())
    for salle, tunnel in tunnels.items():
        for t in tunnel:
            G.add_edge(salle, t)

    pos = {
        'Sv': (0, 1),
        'Sd': (1, 0),
    }

    pos.update(nx.spring_layout(G, seed=404))

    color_map = []
    for node in G:
        if node == 'Sv':
            color_map.append('green')
        elif node == 'Sd':
            color_map.append('orange')
        else:
            color_map.append('skyblue')

    nx.draw(G, pos, node_size=1000, node_color=color_map, with_labels=True, font_weight='bold')

    plt.show()

    # # simuler le déplacement des fourmis par étapes sur le graphiques
    # for etape in range(etapes):
    #     plt.clf()
    #     # pour chaques fourmis ajouter un point rouge à bord noir et numéro blanc sur la salle dans laquelle elle se trouve
    #     # les faires se déplacer dans l'ordres par étapes et par salles
    #     for fourmi, position in fourmiliere.positions.items():
    #         x, y = pos[position]
    #         plt.plot(x, y, 'ro', markersize=20, markeredgewidth=2)
    #         plt.text(x, y, fourmi, color='white', fontsize=12, ha='center', va='center')
    #     plt.title(f"Étape {etape + 1}")
    #     plt.pause(1)
    #     fourmiliere.deplacer_fourmis()

    # print(f"Nombre d'étapes pour que toutes les fourmis atteignent le dortoir: {etapes}")

    # plt.show()