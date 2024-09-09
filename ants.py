import networkx as nx
from collections import deque
import matplotlib.pyplot as plt

class Anthill:
    def __init__(self, rooms, tunnels):
        self.graph = nx.Graph()
        self.rooms = rooms
        self.tunnels = tunnels
        self.ants = deque()
        self.ant_positions = {} 
        self._initialize_graph()

# On ajoute les noeuds et leurs capacités
    def _initialize_graph(self):
        for room, capacity in self.rooms.items():
            self.graph.add_node(room, capacity=capacity)

# On ajoute les tunnels
        for tunnel in self.tunnels:
            self.graph.add_edge(*tunnel)

# On initialise et ajoute les fourmis à la fourmilière
    def add_ants(self, nb_ants):
        self.ants = deque([f"f{i+1}" for i in range(nb_ants)])
        self.ant_positions = {ant: 'Sv' for ant in self.ants}

    def move_ants(self):
        step = 1
        while any(pos != 'Sd' for pos in self.ant_positions.values()):
            print(f"+++ E{step} +++")
            step += 1
            
            moves = []
            moved_ants = []

            for ant, current_position in list(self.ant_positions.items()):
                if current_position == 'Sd':
                    continue

                for neighbor_room in self.graph.neighbors(current_position):
                    if self.graph.nodes[neighbor_room].get('capacity', 0) > 0:
                        moves.append(f"{ant} - {current_position} - {neighbor_room}")
                        self.graph.nodes[neighbor_room]['capacity'] -= 1

                        self.ant_positions[ant] = neighbor_room
                        moved_ants.append(ant)

                        if neighbor_room == 'Sd':
                            moved_ants.append(ant)
                            break
                        
                        break

            for _ in range(len(self.ants)):
                current_ant = self.ants.popleft()

                for neighbor_room in self.graph.neighbors('Sv'):
                    if self.graph.nodes[neighbor_room].get('capacity', 0) > 0:
                        moves.append(f"{current_ant} - Sv - {neighbor_room}")
                        self.graph.nodes[neighbor_room]['capacity'] -= 1
                        self.ant_positions[current_ant] = neighbor_room
                        moved_ants.append(current_ant)
                        break
                else:
                    self.ants.append(current_ant)
                    break

# On enlève les fourmis qui ont atteint le dortoir
            for ant in moved_ants:
                if self.ant_positions[ant] == 'Sd':
                    self.ants.remove(ant)

            for move in moves:
                print(move)

# On réinitialise la capacité des salles à la fin de chaque étape
            for room in self.graph.nodes:
                if room not in ['Sv', 'Sd']:
                    self.graph.nodes[room]['capacity'] = self.rooms.get(room, 1)

            print()

        print("Tout le monde est prêt à dormir")

    def plot_graph(self):
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)

        nx.draw_networkx_nodes(self.graph, pos, node_size=700, node_color='lightblue')
        nx.draw_networkx_edges(self.graph, pos, width=2)
        labels = {node: f"{node}\n({self.graph.nodes[node].get('capacity', 'N/A')})" for node in self.graph.nodes}
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=12, font_color='black')
        plt.title("Représentation de la fourmilière sous forme de graphe")
        plt.show()
