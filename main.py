from ants import Fourmiliere

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

    print(f"Nombre de fourmis: {nb_fourmis}")
    print(f"Salles: {salles}")
    print(f"Capacités: {capacites}")
    print(f"Tunnels: {tunnels}")

    fourmiliere = Fourmiliere(salles, tunnels, nb_fourmis, capacites)
    etapes = fourmiliere.simuler()

    print(f"Nombre d'étapes pour que toutes les fourmis atteignent le dortoir: {etapes}")
