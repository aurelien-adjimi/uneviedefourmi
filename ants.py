import numpy as np
import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import random

class Fourmiliere:
    def __init__(self, salles, tunnels, nb_fourmis, capacites):
        self.salles = salles
        self.nb_fourmis = nb_fourmis
        self.capacites = capacites
        self.positions = {i: 'Sv' for i in range(nb_fourmis)}
        self.salles['Sv'] = nb_fourmis
        self.salles['Sd'] = 0
        self.historique = {i: ['Sv'] for i in range(nb_fourmis)}
        self.etapes = []

        # Créer une matrice d'adjacence vide
        self.n = len(salles)
        self.salle_indices = {salle: i for i, salle in enumerate(salles.keys())}
        self.adjacence = np.zeros((self.n, self.n), dtype=int)
        
        # Remplir la matrice d'adjacence en fonction des tunnels
        for salle1, connexions in tunnels.items():
            for salle2 in connexions:
                i, j = self.salle_indices[salle1], self.salle_indices[salle2]
                self.adjacence[i][j] = 1  # matrice orientée

        # Créer un graphe à partir de la matrice d'adjacence
        self.graph = nx.from_numpy_array(self.adjacence, create_using=nx.DiGraph)
        self.mapping = {v: k for k, v in self.salle_indices.items()}
        self.graph = nx.relabel_nodes(self.graph, self.mapping)

        # Trouver tous les chemins possibles
        chemins_possibles = self.trouver_chemin_optimal('Sv', 'Sd')
        chemins_possibles.sort(key=len)  # Trier les chemins par longueur

        # Prioritize the direct path
        direct_path = [path for path in chemins_possibles if len(path) == 2]
        if direct_path:
            chemins_possibles = direct_path + [path for path in chemins_possibles if path not in direct_path]

        # Assigner un chemin à chaque fourmi
        self.chemins_assignes = {}
        for i in range(nb_fourmis):
            chemin = chemins_possibles[0]  # Always use the first (shortest) path
            self.chemins_assignes[i] = chemin

    def deplacer_fourmis(self):
        etape = {}
        for fourmi in range(self.nb_fourmis):
            current_room = self.positions[fourmi]
            if current_room == 'Sd':
                continue
            
            # Try paths in order of length until a valid move is found
            chemins = sorted(self.trouver_chemin_optimal(current_room, 'Sd'), key=len)
            moved = False
            for chemin in chemins:
                if len(chemin) > 1:
                    next_room = chemin[1]  # The next room in the path
                    if self.peut_se_deplacer(next_room, fourmi):
                        self.positions[fourmi] = next_room
                        self.salles[current_room] -= 1
                        self.salles[next_room] += 1
                        self.historique[fourmi].append(next_room)
                        etape[fourmi] = (current_room, next_room)
                        moved = True
                        break  # Move to the next ant once a valid move is found
            
            if not moved:
                self.recalculer_chemin(fourmi)
        
        self.etapes.append(etape)

    def peut_se_deplacer(self, salle, fourmi):
        if salle == 'Sd':
            return True
        if self.salles[salle] >= self.capacites[salle]:
            return False
        return True

    def recalculer_chemin(self, fourmi):
        current_room = self.positions[fourmi]
        new_paths = self.trouver_chemin_optimal(current_room, 'Sd')
        if new_paths:
            self.chemins_assignes[fourmi] = new_paths[0]  # Assign the shortest new path

    def trouver_chemin_optimal(self, depart, arrivee):
        try:
            chemins_possibles = list(nx.all_simple_paths(self.graph, source=depart, target=arrivee))
            return chemins_possibles
        except nx.NetworkXNoPath:
            return []

    def toutes_fourmis_dans_dortoir(self):
        return self.salles['Sd'] == self.nb_fourmis

    def simuler(self):
        etapes = 0
        dernière_position = {i: 'Sv' for i in range(self.nb_fourmis)}
        while not self.toutes_fourmis_dans_dortoir():
            self.deplacer_fourmis()
            etapes += 1
            print(f" +++ Étape {etapes}: +++ ")
            for fourmi in range(self.nb_fourmis):
                if self.positions[fourmi] == dernière_position[fourmi]:
                    continue
                if len(self.historique[fourmi]) > 1:
                    print(f"f{fourmi} - {self.historique[fourmi][-2]} - {self.historique[fourmi][-1]}")
                elif len(self.historique[fourmi]) == 1:
                    pass
                dernière_position[fourmi] = self.positions[fourmi]

        return etapes

    def simuler_deplacements(self):
        while not self.toutes_fourmis_dans_dortoir():
            self.deplacer_fourmis()

# The rest of your code (lire_fichier_fourmiliere and visualiser_deplacements functions) remains unchanged


def lire_fichier_fourmiliere(fichier):
    """
    Lit un fichier de fourmilière et retourne les informations nécessaires pour simuler le déplacement des fourmis.
    """
    with open(fichier, 'r') as f:
        lignes = f.readlines()

    nb_fourmis = int(lignes[0].strip().split('=')[1])
    salles = {'Sv': 0, 'Sd': 0}
    capacites = {'Sv': float('inf'), 'Sd': float('inf')}
    tunnels = {'Sv': [], 'Sd': []}
    i = 1

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

def visualiser_deplacements(simulation):
    """
    Visualise les déplacements des fourmis dans la fourmilière.
    """
    fig, ax = plt.subplots()
    
    # Créer un graphe basé sur la matrice d'adjacence
    G = nx.from_numpy_array(simulation.adjacence, create_using=nx.DiGraph)
    mapping = {v: k for k, v in simulation.salle_indices.items()}
    G = nx.relabel_nodes(G, mapping)
    
    pos = {
        'Sv': (0, 1),
        'Sd': (1, 0),
    }

    # Disposition des nœuds
    pos.update(nx.spring_layout(G, seed=42))

    color_map = []
    for node in G:
        if node == 'Sv':
            color_map.append('red')
        elif node == 'Sd':
            color_map.append('lightgreen')
        else:
            color_map.append('lightblue')
    
    simulation.simuler_deplacements()
    
    # Visualiser les déplacements
    for index, etape in enumerate(simulation.etapes):
        ax.clear()
        nx.draw(G, pos, with_labels=True, node_size=700, node_color=color_map, ax=ax)
    
        # Ajouter des annotations pour représenter les fourmis par F(n)
        for id_fourmi, (start, end) in etape.items():
            if start and end:
                # Calculer une position intermédiaire entre start et end pour placer l'annotation
                pos_start = pos[start]
                pos_end = pos[end]
                pos_mid = [(pos_start[0] + pos_end[0]) / 2, (pos_start[1] + pos_end[1]) / 2]
                
                # Placer l'annotation à mi-chemin
                ax.text(pos_mid[0], pos_mid[1], id_fourmi, fontsize=12, ha='center', va='center',
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
        
        plt.title(f"Étape {index + 1}")
        plt.pause(1)  # Pause pour montrer les étapes une par une

    plt.show()
