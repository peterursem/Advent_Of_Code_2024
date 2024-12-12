from enum import Enum
from matplotlib import pyplot as plt

class CELL(Enum):
    # STATE = CHAR, VALUE
    EMPTY = ["."], 0, 0
    OBSTRUCTION = ["#"], -1, -1
    GUARD = ["X","O","^","v","<",">"], 1, 2
    LOOP = ["*"], 3, 4
    def __init__(self, char, val, alt_val):
        self.STATE = self.name
        self.VALUE = val
        self.CHAR = char
        self.ALT = alt_val
    
    @classmethod
    def _missing_(cls, query):
        for member in cls:
            if query in member.CHAR + [member.VALUE, member.ALT, member.STATE]:
                return member

class HEADING(Enum):
    UP = "^", {"dR": -1,"dC": 0}, 0, "dR"
    RIGHT = ">", {"dR": 0,"dC": 1}, 1, "dC"
    DOWN = "v", {"dR": 1,"dC": 0}, 2, "dR"
    LEFT = "<", {"dR": 0,"dC": -1}, 3, "dC"

    def __init__(self, char, delta, order, axis):
        self.NAME = self.name
        self.CHAR = char
        self.DELTA = delta
        self.ORDER = order
        self.AXIS = axis
        if self.ORDER < 3:
            self.NEXT = order + 1
        else:
            self.NEXT = 0

    @classmethod
    def _missing_(cls, query):
        for member in cls:
            if query in (member.NAME, member.CHAR, member.DELTA, member.ORDER):
                return member

class Grid:
    def __init__(self, filename):
        self.populate_from_file(filename)

    def in_bounds(self, position) -> bool:
        return 0 <= position["row"] <= len(grid.data) - 1 and 0 <= position["col"] <= len(grid.data[0]) - 1

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
    
    def locate_guard(self):
        for row in range(len(self.text)):
            for col in range(len(self.text[row])):
                if CELL(self.text[row][col]).STATE == "GUARD":
                    return {"position": {"row": row, "col": col}, "char": self.text[row][col]}
    
    def populate_from_file(self, filename):
        with open(filename) as file:
            self.text = [line.strip() for line in file.readlines()]
            self.data = [[CELL(char).VALUE for char in row] for row in self.text]
            self.height = len(self.data)
            self.width = len(self.data[0])

            guard_data = self.locate_guard()
            self.guard = Guard(guard_data["position"], guard_data["char"])
    
    def print_chars(self):
        for line in self.data:
            for val in line:
                char = CELL(val).CHAR[0]
                if val == CELL.GUARD.ALT:
                    char = CELL.GUARD.CHAR[1]
                print(char, end="")
            print("")
    
    def view(self, frame_delay: float, step_number: int, unique_spaces, loops) -> None:
        """
        shows an image of the current state of the grid
        parameters:
            grid - list-of-lists representing the current grid. Inner lists use 0s to represent dead cells, and 1s to represent live ones
            frame_delay - the program will pause for this many seconds after displaying the image. 0.1s gives a pretty good animation effect
            step_number - the step number of the supplied grid (will be displayed above the image)
        """

        grid = self.data

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
        plt.title(f'Step: #{step_number} | Unique Spaces: {unique_spaces} | Loops {loops}')
        plt.pause(frame_delay)

class Guard:
    def __init__(self, position: dict, char: str):
        self.unique_spaces = 1
        self.position = position
        self.heading = HEADING(char)
        self.turns = []


    def loop(self, grid, obstruction_location = None, display=False, i=1, frame_time=0.0001, loop_no=0):
        if obstruction_location:
            grid.set_cell(obstruction_location, CELL.OBSTRUCTION.VALUE)

        visited = []
        update = self.update(grid)
        visited.append(update["space"])

        while (update["status"] == 1):
            if display:
                grid.view(frame_time, i, self.unique_spaces, loop_no)
            update = self.update(grid)
            if update["space"] and visited.count(update["space"]) == 0:
                visited.append(update["space"])
            if update["loop"]:
                return loop_no + 1
            i+=1
        return visited

    def update(self, grid):
        nextpos = self.next_position(self.position, self.heading)
        obstacle = grid.get_cell(nextpos)

        set = CELL.GUARD.VALUE
        space = self.position
        
        if obstacle == None:
            return {"status": 0, "space": space, "loop": False}

        if obstacle == CELL.OBSTRUCTION.VALUE:
            self.turns.append((self.position, self.heading))
            self.turn()
        elif obstacle == CELL.EMPTY.VALUE or obstacle == CELL.LOOP.VALUE:
            if grid.set_cell(nextpos, set):
                space = self.position
                self.unique_spaces += 1
            self.position = nextpos
        elif obstacle == CELL.GUARD.VALUE or obstacle == CELL.GUARD.ALT:
            self.position = nextpos
        
        if self.turns.count((self.position, self.heading)) == 1:
                return {"status": 0, "space": None, "loop": True}
        
        return {"status": 1, "space": space, "loop": False}
                
    def next_position(self, position, heading):
        return {"row": position["row"] + heading.DELTA["dR"], "col": position["col"] + heading.DELTA["dC"]}
    
    def turn(self):
        self.heading = HEADING(self.heading.NEXT)

DISPLAY = True
FRAME_TIME = 0.001
FILE = "./Day6/testgrid.txt"

grid = Grid(FILE)
visited = grid.guard.loop(grid, display=DISPLAY, frame_time=FRAME_TIME)
loop_num = 0

for position in visited:
    grid = Grid(FILE)
    out = grid.guard.loop(grid, obstruction_location=position, display=DISPLAY, frame_time=FRAME_TIME, loop_no=loop_num)
    if type(out) == int:
        loop_num = out

grid.print_chars()

print(f'{grid.guard.unique_spaces} Unique spaces occupied \n{loop_num} Loops')
