from ants import Fourmiliere, lire_fichier_fourmiliere, visualiser_deplacements

if __name__ == "__main__":
    fichier = input("Entrer le numéro du fichier de fourmilière à simuler (0, 1, 2, 3, 4, 5): ")
    fichiers = {
        '0': 'Nest/fourmiliere_zero.txt',
        '1': 'Nest/fourmiliere_un.txt',
        '2': 'Nest/fourmiliere_deux.txt',
        '3': 'Nest/fourmiliere_trois.txt',
        '4': 'Nest/fourmiliere_quatre.txt',
        '5': 'Nest/fourmiliere_cinq.txt'
    }
    fichier = fichiers.get(fichier, 'Nest/fourmiliere_zero.txt')

    nb_fourmis, salles, tunnels, capacites = lire_fichier_fourmiliere(fichier)

    fourmiliere = Fourmiliere(salles, tunnels, nb_fourmis, capacites)
    etapes = fourmiliere.simuler()

    print(f"Nombre d'étapes pour que chaque fourmi arrive au dortoir: {etapes}")

    # Visualiser les déplacements des fourmis
    visualiser_deplacements(fourmiliere)
