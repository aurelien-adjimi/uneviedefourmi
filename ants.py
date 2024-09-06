from collections import deque
import networkx as nx
import random
import matplotlib.pyplot as plt

class Fourmiliere:
    def __init__(self, salles, tunnels, nb_fourmis, capacites):
        self.salles = salles
        self.tunnels = tunnels
        self.nb_fourmis = nb_fourmis
        self.capacites = capacites
        self.positions = {i: 'Sv' for i in range(nb_fourmis)}
        self.salles['Sv'] = nb_fourmis
        self.salles['Sd'] = 0
        self.historique = {i: ['Sv'] for i in range(nb_fourmis)}
        self.etapes = []
        self.graph = nx.Graph()
        for salle, tunnel in tunnels.items():
            for t in tunnel:
                self.graph.add_edge(salle, t)
        
        # Stocker tous les chemins optimaux
        self.chemins_optimaux = self.trouver_chemin_optimal('Sv', 'Sd')
        
        # Assigner un chemin à chaque fourmi
        self.chemins_assignes = {i: self.chemins_optimaux[i % len(self.chemins_optimaux)] for i in range(nb_fourmis)}

    def deplacer_fourmis(self):
        """
        Déplace les fourmis en suivant leur chemin assigné.
        """
        etape = {}
        for fourmi in range(self.nb_fourmis):
            current_room = self.positions[fourmi]
            if current_room == 'Sd':
                continue
            # Récupérer le chemin assigné à la fourmi
            chemin = self.chemins_assignes[fourmi]
            
            # Trouver la prochaine salle sur le chemin
            if current_room in chemin:
                next_room_index = chemin.index(current_room) + 1
                if next_room_index < len(chemin):
                    next_room = chemin[next_room_index]
                    # Vérifier que la salle peut accueillir la fourmi
                    if self.peut_se_deplacer(next_room, fourmi):
                        self.positions[fourmi] = next_room
                        self.salles[current_room] -= 1
                        self.salles[next_room] += 1
                        self.historique[fourmi].append(next_room)
                        etape[fourmi] = (current_room, next_room)
        self.etapes.append(etape)

    def peut_se_deplacer(self, salle, fourmi):
        """
        Vérifie si une fourmi peut se déplacer dans une salle donnée.
        """
        if salle == 'Sd':
            return True
        if self.salles[salle] >= self.capacites[salle]:
            return False
        return True

    def trouver_chemin_optimal(self, depart, arrivee):
        """
        Trouve tous les chemins possibles entre deux salles.
        Utilise nx.all_simple_paths pour trouver tous les chemins simples entre deux nœuds.
        """
        try:
            chemins_possibles = list(nx.all_simple_paths(self.graph, source=depart, target=arrivee))
            return chemins_possibles
        except nx.NetworkXNoPath:
            return []

    def toutes_fourmis_dans_dortoir(self):
        """
        Vérifie si toutes les fourmis sont dans le dortoir.
        """
        return self.salles['Sd'] == self.nb_fourmis

    def simuler(self):
        """
        Simule le déplacement des fourmis jusqu'à ce que toutes les fourmis soient dans le dortoir.
        """
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
        """
        Simule les déplacements des fourmis et stocke les étapes.
        """
        while not self.toutes_fourmis_dans_dortoir():
            self.deplacer_fourmis()


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
    
    G = nx.Graph()
    G.add_nodes_from(simulation.salles.keys())
    for salle, tunnel in simulation.tunnels.items():
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
            color_map.append('red')
        elif node == 'Sd':
            color_map.append('lightgreen')
        else:
            color_map.append('lightblue')
    
    simulation.simuler_deplacements()
    
    # Visualiser les déplacements
    for index, etape in enumerate(simulation.etapes):
        ax.clear()
        nx.draw(simulation.graph, pos, with_labels=True, node_size=700, node_color=color_map, ax=ax)
    
        
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
