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
    fichier_zero = 'Nest/fourmiliere_zero.txt'
    fichier_un = 'Nest/fourmiliere_un.txt'
    fichier_deux = 'Nest/fourmiliere_deux.txt'
    fichier_trois = 'Nest/fourmiliere_trois.txt'
    fichier_quatre = 'Nest/fourmiliere_quatre.txt'
    fichier_cinq = 'Nest/fourmiliere_cinq.txt'
    
    # ask user to choose a file using input
    fichier = input("Entrer le numéro du fichier de fourmilière à simuler (0, 1, 2, 3, 4, 5): ")
    if fichier == '0':
        fichier = fichier_zero
    elif fichier == '1':
        fichier = fichier_un
    elif fichier == '2':
        fichier = fichier_deux
    elif fichier == '3':
        fichier = fichier_trois
    elif fichier == '4':
        fichier = fichier_quatre
    elif fichier == '5':
        fichier = fichier_cinq

    nb_fourmis, salles, tunnels, capacites = lire_fichier_fourmiliere(fichier)


    # creation de graphique pour visualiser les salles, les tunnels et les fourmis
    G = nx.Graph()
    G.add_nodes_from(salles.keys())
    for salle, tunnel in tunnels.items():
        for t in tunnel:
            # add edge between salle and t with a arrow head
            G.add_edge(salle, t, color='black', arrowstyle='-|>', arrowsize=15)

    pos = {
        'Sv': (0, 1),
        'Sd': (1, 0),
    }

    pos.update(nx.spring_layout(G, seed=42))

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

    fourmiliere = Fourmiliere(salles, tunnels, nb_fourmis, capacites)
    etapes = fourmiliere.simuler()

    print(f"Nombre d'étapes pour que chaques fourmis arrive au dortoir: {etapes}")

        # simuler le déplacement des fourmis par étapes sur le graphiques
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