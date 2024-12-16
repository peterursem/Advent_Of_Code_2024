from matplotlib import pyplot as plt
import random

MIN_ALT = 0
MAX_ALT = 9
FRAME_DELAY = 0.3

class Mountain():
    def __init__(self, grid):
        self.grid = grid
        self.hikers = self.setup_hikers()
        self.summits = []
        self.trails = []

    def setup_hikers(self):
        hikers = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 0:
                    hikers.append(Hiker(self, {"row": row, "col": col}, {"row": row, "col": col}))
        return hikers
                    
    def in_bounds(self, position) -> bool:
        return 0 <= position["row"] < len(self.grid) and 0 <= position["col"] < len(self.grid[0])

    def get_alt(self, position):
        if not self.in_bounds(position):
            return None
        return self.grid[position["row"]][position["col"]]
    
    def update(self):
        for hiker in self.hikers:
            result = hiker.update()
            if result == 1:
                continue
            if self.get_alt(hiker.position) == 9:
                self.trails.append((hiker.origin, hiker.position))
                if not (hiker.origin, hiker.position) in self.summits:
                    self.summits.append((hiker.origin, hiker.position))
            self.hikers.remove(hiker)
        self.print_chars(gui=True, frame_delay=FRAME_DELAY)
    
    def loop(self):
        self.print_chars(gui=True, frame_delay=1)
        while len(self.hikers) != 0:
            self.update()        
    
    def print_chars(self, gui=False, text=False, frame_delay=0.0001):
        display = []
        for row in range(len(self.grid)):
            display.append([])
            for col in range(len(self.grid[row])):
                val = self.grid[row][col]

                if gui:
                    display[row].append((0.8, 0.4 + ((val+1)/(MAX_ALT+1))*0.6, 0.8))

                elif text:
                    char = val
                    if val == -1:
                        char = "*"

                    print(char, end="")
            if text:
                print("")

        for hiker in self.hikers:
            if text:
                print(hiker.position)
            if display[hiker.position["row"]][hiker.position["col"]] == (1,1,1):
                display[hiker.position["row"]][hiker.position["col"]] = hiker.colour
            else:
                display[hiker.position["row"]][hiker.position["col"]] = self.add_colour(hiker.colour, display[hiker.position["row"]][hiker.position["col"]])

        if gui:
            self.view(display, frame_delay=frame_delay)
        if text:
            print(f'\n{len(self.summits)} Points\n{len(self.trails)} Rating')
    
    def add_colour(self, base, adjustment):
        return (base[0] + adjustment[0], base[1] + adjustment[1], base[2] + adjustment[2])

    def view(self, grid, frame_delay=1) -> None:
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
        plt.title(f'Mountain | Score: {len(self.summits)} | Rating: {len(self.trails)}')
        plt.pause(frame_delay)
                


class Hiker():
    def __init__(self, mountain, position, origin):
        self.position = position
        self.altitude = mountain.get_alt(position)
        self.origin = origin
        self.mountain = mountain
        self.colour = (random.random() * 0.5, random.random()* 0.5, random.random() * 0.5)
    
    def update(self):
        if self.altitude == MAX_ALT:
            return 2

        possibilities = []
        
        for search_delta in ({"row": -1, "col": 0}, {"row": 1, "col": 0}, {"row": 0, "col": -1}, {"row": 0, "col": 1}):
            search_row = self.position["row"] + search_delta["row"]
            search_col = self.position["col"] + search_delta["col"]
            search_pos = {"row": search_row, "col": search_col}
            if self.mountain.get_alt(search_pos) == self.altitude + 1:
                possibilities.append(search_pos)
        
        if len(possibilities) == 0:
            return 0
        
        self.position = possibilities[0]
        self.altitude += 1
        if len(possibilities) > 1:
            for i in range(1, len(possibilities)): 
                self.mountain.hikers.append(Hiker(self.mountain, possibilities[i], self.origin))
        
        return 1
        
def read_file(filename):
    with open(filename) as file:
        return [line.strip() for line in file.readline()]

def lines_to_grid(file):
    grid = []
    for line_no in range(len(file)):
        grid.append([])
        for val in file[line_no]:
            if val == ".":
                val = "-1"
            grid[line_no].append(int(val))
    return grid

test_2 = [
    '...0...',
    '...1...',
    '...2...',
    '6543456',
    '7.....7',
    '8.....8',
    '9.....9'
]

test_3 = [
    "10..9..",
    "2...8..",
    "3...7..",
    "4567654",
    "...8..3",
    "...9..2",
    ".....01"
]

test_4 = [
    "..90..9",
    "...1.98",
    "...2..7",
    "6543456",
    "765.987",
    "876....",
    "987...."
]

test_36 = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732"
]

test_227 = [
    "012345",
    "123456",
    "234567",
    "345678",
    "4.6789",
    "56789."
]

file = []
with open('./Day10/input.txt') as file:
    file = [line.strip() for line in file.readlines()]

def main():
    mount = Mountain(lines_to_grid(file))
    mount.loop()

    score = {}
    for summit in mount.summits:
        if not f'{summit[0]["row"]}, {summit[0]["col"]}' in list(score.keys()):
            score[f'{summit[0]["row"]}, {summit[0]["col"]}'] = []
        score[f'{summit[0]["row"]}, {summit[0]["col"]}'].append(summit[1])

    rating = {}
    for trail in mount.trails:
        if not f'{trail[0]["row"]}, {trail[0]["col"]}' in list(rating.keys()):
            rating[f'{trail[0]["row"]}, {trail[0]["col"]}'] = []
        rating[f'{trail[0]["row"]}, {trail[0]["col"]}'].append(trail[1])

    for row in range(len(mount.grid)):
        for col in range(len(mount.grid[row])):
            if f'{row}, {col}' in list(score.keys()):
                print(f'* Trailhead ({row}, {col}) Score: {len(score[f"{row}, {col}"])}, Rating: {len(rating[f"{row}, {col}"])}, Peaks: {score[f"{row}, {col}"]}\n')

    mount.print_chars(text=True)

main()