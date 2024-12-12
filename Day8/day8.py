from enum import Enum
from matplotlib import pyplot as plt
import random

class CELL(Enum):
    # NAME = CHAR, VALUE
    EMPTY = ".", 0
    TOWER = "T", 1
    ANTINODE = "#", -1
    def __init__(self, char, val):
        self.NAME = self.name
        self.VALUE = val
        self.CHAR = char
    
    @classmethod
    def _missing_(cls, query):
        for member in cls:
            if query in [member.CHAR, member.NAME]:
                return member
            if type(query) == str and not query in (cls.EMPTY.CHAR, cls.ANTINODE.CHAR):
                return cls.TOWER
        return cls.ANTINODE
            
class Grid:
    def __init__(self, filename):
        self.all_antinodes = []
        self.populate_from_file(filename)

    def in_bounds(self, position) -> bool:
        return 0 <= position["row"] < len(self.data) and 0 <= position["col"] < len(self.data[0])

    def get_char(self, position):
        if not self.in_bounds(position):
            return None
        return self.text[position["row"]][position["col"]]

    def get_cell(self, position):
        if not self.in_bounds(position):
            return None
        return self.data[position["row"]][position["col"]]
    
    def set_cell(self, position, value):
        if not self.in_bounds(position):
            return None
        
        if self.data[position["row"]][position["col"]] != value:
            self.data[position["row"]][position["col"]] = value
            return True
        else:
            return False
    
    def locate_tower(self):
        for row in range(len(self.data)):
            for col in range(len(self.data[row])):
                if CELL(self.data[row][col]) == CELL.TOWER:
                    char = self.data[row][col]
                    self.data[row][col] = CELL.TOWER.VALUE
                    return {"position": {"row": row, "col": col}, "char": char}
                
        return None
    
    def populate_from_file(self, filename):
        with open(filename) as file:
            self.text = [line.strip() for line in file.readlines()]
            self.data = [[char for char in row] for row in self.text]
            self.towers = {}

            tower_data = self.locate_tower()
            while tower_data:
                if list(self.towers.keys()).count(tower_data["char"]) == 0:
                    self.towers[tower_data["char"]] = []
                self.towers[tower_data["char"]].append(Tower(tower_data["position"], tower_data["char"]))
                tower_data = self.locate_tower()
            
            for char in self.towers:
                for tower in self.towers[char]:
                    tower.peers = [peer for peer in self.towers[char] if peer != tower]
                    tower.update_antinodes(self)
            
    def print_chars(self, gui=False, frame_delay=0.0001):
        colours = [((random.random()* 0.7) + 0.3 , (random.random()* 0.7) + 0.3 , (random.random()* 0.7) + 0.3 ) for _ in range(len(self.towers))]
        display = []
        for row in range(len(self.data)):
            display.append([])
            for col in range(len(self.data[row])):
                val = self.data[row][col]
                char = self.text[row][col]
                if CELL(char) == CELL.TOWER:
                    display[row].append(colours[list(self.towers.keys()).index(char)])
                else:
                    display[row].append((1,1,1))
                if val == CELL.ANTINODE.CHAR:
                    char = CELL.ANTINODE.CHAR
                print(char, end="")
            print("")

        self.view(display, frame_delay=0.75)
        for location in self.all_antinodes:
            if display[location["row"]][location["col"]] == (1,1,1):
                display[location["row"]][location["col"]] = ((location["row"] * location["col"]) / (len(display) * len(display[location["row"]])) * 0.8, location["col"] / len(display[location["row"]]) * 0.5, location["row"] / len(display) * 0.5)
            else:
                display[location["row"]][location["col"]] = self.adjust_colour(display[location["row"]][location["col"]], (0.9, 0.9, 0.9))
            if gui:
                self.view(display, frame_delay=frame_delay, antinodes=len(self.all_antinodes))

        print(f'\n{len(self.all_antinodes)} Anti-Nodes Found')
    
    def adjust_colour(self, base, adjustment):
        return (base[0] * adjustment[0], base[1] * adjustment[1], base[2] * adjustment[2])

    def view(self, grid, frame_delay=1, antinodes=0) -> None:
        """
        shows an image of the current state of the grid
        parameters:
            grid - list-of-lists representing the current grid. Inner lists use 0s to represent dead cells, and 1s to represent live ones
            frame_delay - the program will pause for this many seconds after displaying the image. 0.1s gives a pretty good animation effect
            step_number - the step number of the supplied grid (will be displayed above the image)
        """

        # check that the grid supplied is not empty
        if len(grid) == 0:
            raise Exception("grid is empty")

        # check that all rows contain the same number of cells
        row_lengths = set([len(row) for row in grid])
        if len(row_lengths) != 1:
            raise Exception(f"not all grid rows are the same length. Found lengths: {row_lengths}")

        # plot the grid
        plt.cla()
        plt.imshow(grid)
        plt.title(f'Anti-Nodes: {antinodes}')
        plt.pause(frame_delay)

class Tower:
    def __init__(self, position: dict, char: str):
        self.position = position
        self.char = char
    def update_antinodes(self, grid) -> list:
        for peer in self.peers:
            steps = 0
            while True:
                fore_position = self.antinode_position(self.tower_delta(peer, steps))
                back_position = self.antinode_position(self.tower_delta(peer, -steps))

                fore_val, back_val = self.verify_antinode(fore_position, grid), self.verify_antinode(back_position, grid)

                if fore_val == back_val == -1:
                    break

                steps += 1
    
    def verify_antinode(self, position, grid):
        grid_char = grid.get_char(position)
        if grid_char == None:
            return -1
        
        if not position in grid.all_antinodes:
            grid.all_antinodes.append(position)
            if CELL(grid_char).VALUE == 0:
                grid.set_cell(position, CELL.ANTINODE.CHAR)
            return 1

        return 0

    def tower_delta(self, peer, steps):
        return {"dR": (self.position["row"] - peer.position["row"]) * steps, "dC": (self.position["col"] - peer.position["col"]) * steps}
                
    def antinode_position(self, tower_delta):
        return {"row": self.position["row"] + tower_delta["dR"], "col": self.position["col"] + tower_delta["dC"]}


FILE = "./Day8/test.txt"

grid = Grid(FILE)

grid.print_chars(gui=True, frame_delay=0.1)