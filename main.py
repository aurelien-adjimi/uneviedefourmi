import os
from ants import Anthill

def main():
    nest_folder = 'Nest'
    files = [f for f in os.listdir(nest_folder) if f.startswith('fourmiliere_') and f.endswith('.txt')]
    print("Available anthills:")
    for file in files:
        print(f"- {file}")

    choice = input("Enter the name of the anthill file you want to solve: ")
    file_path = os.path.join(nest_folder, choice)

    if not os.path.exists(file_path):
        print("File not found. Please enter a valid file name.")
        return

    anthill = Anthill.from_file(file_path)
    if anthill is None:
        print("Failed to read the anthill from the file.")
        return

    ants = anthill.initialize_ants()
    if ants is None:
        return

    print("Starting to move ants to dormitory...")
    steps = anthill.move_ants_to_dormitory(ants)
    print(f"All ants reached the dormitory in {steps} steps.")

if __name__ == "__main__":
    main()
