class Fourmiliere:
    def __init__(self, salles, tunnels, nb_fourmis, capacites):
        self.salles = salles
        self.tunnels = tunnels
        self.nb_fourmis = nb_fourmis
        self.capacites = capacites
        self.positions = {i: 'Sv' for i in range(nb_fourmis)}
        self.salles['Sv'] = nb_fourmis
        self.salles['Sd'] = 0
        self.historique = {i: ['Sv'] for i in range(nb_fourmis)}  # Historique des déplacements des fourmis

    def deplacer_fourmis(self):
        for fourmi in range(self.nb_fourmis):
            current_room = self.positions[fourmi]
            if current_room == 'Sd':
                continue
            for next_room in self.tunnels[current_room]:
                if self.peut_se_deplacer(next_room, fourmi):
                    self.positions[fourmi] = next_room
                    self.salles[current_room] -= 1
                    self.salles[next_room] += 1
                    self.historique[fourmi].append(next_room)  # Mettre à jour l'historique
                    break

    def peut_se_deplacer(self, salle, fourmi):
        # Le dortoir peut accueillir plusieurs fourmis
        if salle == 'Sd':
            return True
        # Une fourmi ne peut pas retourner dans une salle qu'elle a déjà quittée
        if salle in self.historique[fourmi]:
            return False
        # Vérifier la capacité de la salle
        if self.salles[salle] >= self.capacites[salle]:
            return False
        # Vérifier si la salle rapproche la fourmi du dortoir
        if not self.est_sur_chemin_optimal(salle, fourmi):
            return False
        return True

    def est_sur_chemin_optimal(self, salle, fourmi):
        # Déterminer si une salle est sur le chemin optimal vers le dortoir
        chemin_optimal = self.trouver_chemin_optimal(self.positions[fourmi], 'Sd')
        return salle in chemin_optimal

    def trouver_chemin_optimal(self, depart, arrivee):
        # Utiliser un algorithme de recherche en largeur pour trouver le chemin optimal
        from collections import deque

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
        return self.salles['Sd'] == self.nb_fourmis

    def simuler(self):
        etapes = 0
        while not self.toutes_fourmis_dans_dortoir():
            self.deplacer_fourmis()
            etapes += 1
            # Debug: Afficher l'état de la simulation à chaque étape
            print(f"Étape {etapes}: Positions des fourmis: {self.positions}")
            print(f"Étape {etapes}: État des salles: {self.salles}")
        return etapes