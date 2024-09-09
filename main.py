from ants import Anthill

def load_anthill(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    nb_ants = 0
    rooms = {}
    tunnels = []

    for line in lines: 
        line = line.strip()

        if line.startswith("f="):
            nb_ants = int(line.split('=')[1])
        elif line.startswith("S") and "-" not in line:
            if "{" in line:
                room, capacity = line.split("{")
                room = room.strip()
                capacity = int(capacity.split("}")[0].strip())
            else:
                room = line.strip()
                capacity = 1
            rooms[room] = capacity
        elif "-" in line:
            room1, room2 = line.split("-")
            tunnels.append((room1.strip(), room2.strip()))
    
    return nb_ants, rooms, tunnels

def main():
    filename = 'fourmiliere_quatre.txt'
    nb_ants, rooms, tunnels = load_anthill(filename)

    anthill = Anthill(rooms, tunnels)
    anthill.add_ants(nb_ants)
    anthill.move_ants()
    anthill.plot_graph()

if __name__ == "__main__":
    main()
