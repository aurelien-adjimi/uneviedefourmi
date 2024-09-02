class Ant:
    def __init__(self, id):
        self.id = id
        self.position = 'V'  # Starting position

    def move_to(self, new_position):
        self.position = new_position

class Room:
    def __init__(self, name, capacity=0):
        self.name = name
        self.capacity = capacity
        self.ants = []

    def add_ant(self, ant):
        if self.capacity == 0 or len(self.ants) < self.capacity:
            self.ants.append(ant)
            return True
        return False

    def remove_ant(self, ant):
        if ant in self.ants:
            self.ants.remove(ant)
            return True
        return False

class Anthill:
    def __init__(self):
        self.rooms = {}
        self.tunnels = []
        self.num_ants = 0

    def add_room(self, name, capacity=0):
        self.rooms[name] = Room(name, capacity)

    def add_tunnel(self, room1, room2):
        self.tunnels.append((room1, room2))

    def set_num_ants(self, num):
        self.num_ants = num

    def move_ant(self, ant, from_room, to_room):
        if from_room not in self.rooms or to_room not in self.rooms:
            print(f"Error: Invalid room names: {from_room}, {to_room}")
            return False
        if self.rooms[from_room].remove_ant(ant) and self.rooms[to_room].add_ant(ant):
            ant.move_to(to_room)
            return True
        return False

    def initialize_ants(self):
        ants = [Ant(i) for i in range(self.num_ants)]
        for ant in ants:
            if not self.rooms['Sv'].add_ant(ant):
                print(f"Error: Not enough capacity in room 'Sv' for ant {ant.id}")
                return
            ant.move_to('Sv')
        return ants

    def move_ants_to_dormitory(self, ants):
        steps = 0
        while any(ant.position != 'Sd' for ant in ants):
            print(f"Step {steps}: Ant positions {[ant.position for ant in ants]}")
            for ant in ants:
                if ant.position == 'Sd':
                    continue
                current_room = ant.position
                moved = False
                # Try to find a valid tunnel
                for tunnel in self.tunnels:
                    if tunnel[0] == current_room:
                        next_room = tunnel[1]
                        if self.move_ant(ant, current_room, next_room):
                            print(f"Ant {ant.id} successfully moved from {current_room} to {next_room}")
                            moved = True
                            break
                if not moved:
                    print(f"Ant {ant.id} could not move from {current_room} - no valid tunnel found")
            steps += 1
        return steps

    @classmethod
    def from_file(cls, file_path):
        anthill = cls()
        anthill.add_room('Sv', 0)  # Ensure 'Sv' room is added with unlimited capacity
        anthill.add_room('Sd', 0)  # Ensure 'Sd' room is added with unlimited capacity
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                print("File read successfully.")
                for line in lines:
                    line = line.strip()
                    if line.startswith('f='):
                        num_ants = int(line.split('=')[1].strip())
                        anthill.set_num_ants(num_ants)
                        print(f"Number of ants: {num_ants}")
                    elif line.startswith('S') and ' - ' not in line:
                        if '{' in line and '}' in line:
                            name = line.split('{')[0].strip()
                            capacity = int(line.split('{')[1].split('}')[0].strip())
                        else:
                            name = line.strip()
                            capacity = 1  # Default capacity for rooms without specified capacity
                        if name not in ['Sv', 'Sd']:  # Avoid re-adding 'Sv' and 'Sd'
                            anthill.add_room(name, capacity)
                            print(f"Room added: {name} with capacity {capacity}")
                    elif ' - ' in line:
                        parts = line.split(' - ')
                        anthill.add_tunnel(parts[0].strip(), parts[1].strip())
                        print(f"Tunnel added between {parts[0].strip()} and {parts[1].strip()}")
            return anthill
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
