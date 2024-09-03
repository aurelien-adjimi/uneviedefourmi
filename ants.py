from collections import deque

class Fourmiliere:
    """
    Classe représentant une fourmilière.
    """
    def __init__(self, salles, tunnels, nb_fourmis, capacites):
        self.salles = salles
        self.tunnels = tunnels
        self.nb_fourmis = nb_fourmis
        self.capacites = capacites
        self.positions = {i: 'Sv' for i in range(nb_fourmis)}
        self.salles['Sv'] = nb_fourmis
        self.salles['Sd'] = 0
        self.historique = {i: ['Sv'] for i in range(nb_fourmis)}

    def deplacer_fourmis(self):
        """ 
        Déplace les fourmis d'une salle à une autre.
        """
        for fourmi in range(self.nb_fourmis):
            current_room = self.positions[fourmi]
            if current_room == 'Sd':
                continue
            for next_room in self.tunnels[current_room]:
                if self.peut_se_deplacer(next_room, fourmi):
                    self.positions[fourmi] = next_room
                    self.salles[current_room] -= 1
                    self.salles[next_room] += 1
                    self.historique[fourmi].append(next_room)
                    break

    def peut_se_deplacer(self, salle, fourmi):
        """
        Vérifie si une fourmi peut se déplacer dans une salle donnée.
        """
        if salle == 'Sd':
            return True
        if salle in self.historique[fourmi]:
            return False
        if self.salles[salle] >= self.capacites[salle]:
            return False
        if not self.est_sur_chemin_optimal(salle, fourmi):
            return False
        return True

    def est_sur_chemin_optimal(self, salle, fourmi):
        """
        Vérifie si une fourmi est sur le chemin optimal pour atteindre une salle donnée.
        """
        chemin_optimal = self.trouver_chemin_optimal(self.positions[fourmi], 'Sd')
        return salle in chemin_optimal

    def trouver_chemin_optimal(self, depart, arrivee):
        """
        Trouve le chemin optimal entre deux salles.
        """
        queue = deque([(depart, [depart])])
        visites = set()

        while queue:
            current, path = queue.popleft()
            if current == arrivee:
                return path
            if current not in visites:
                visites.add(current)
                for voisin in self.tunnels[current]:
                    if voisin not in visites:
                        queue.append((voisin, path + [voisin]))
        return []

    def toutes_fourmis_dans_dortoir(self):
        """
        Vérifie si toutes les fourmis sont dans le dortoir.
        """
        return self.salles['Sd'] == self.nb_fourmis

    def simuler(self):
        """"
        Simule le déplacement des fourmis jusqu'à ce que toutes les fourmis soient dans le dortoir.
        """
        etapes = 0
        while not self.toutes_fourmis_dans_dortoir():
            self.deplacer_fourmis()
            etapes += 1
            # print(f"Étape {etapes}: Positions des fourmis: {self.positions}")
            # print(f"Étape {etapes}: État des salles: {self.salles}")
        return etapes