from matplotlib import pyplot as plt

def read_bots(filename: str) -> list:
    bots = []
    with open(filename) as file:
        for line in file:
            vals = line.strip().split(' ')
            p = [int(val) for val in vals[0].split('=')[1].split(',')]
            p.reverse()
            v = [int(val) for val in vals[1].split('=')[1].split(',')]
            v.reverse()
            bots.append([p,v])
    return bots

def update(bots) -> None:
    for i in range(len(bots)):
        bots[i][0][0] = bots[i][0][0] + bots[i][1][0]
        bots[i][0][1] = bots[i][0][1] + bots[i][1][1]

        if bots[i][0][0] < 0:
            bots[i][0][0] += HEIGHT
        elif bots[i][0][0] >= HEIGHT:
            bots[i][0][0] -= HEIGHT

        if bots[i][0][1] < 0:
            bots[i][0][1] += WIDTH
        elif bots[i][0][1] >= WIDTH:
            bots[i][0][1] -= WIDTH

def quad_product(bots, mid_row, mid_col):
    quads = [0,0,0,0]
    for bot in bots:
        if bot[0][0] > mid_row:
            if bot[0][1] > mid_col:
                quads[0] += 1
            if bot[0][1] < mid_col:
                quads[1] += 1
        if bot[0][0] < mid_row:
            if bot[0][1] < mid_col:
                quads[2] += 1
            if bot[0][1] > mid_col:
                quads[3] += 1

    prod = 1
    for quad in quads:
        prod *= quad
    return prod

def render(bots, out='scale') -> list:
    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    top = 0
    for bot in bots:
        grid[bot[0][0]][bot[0][1]] += 1
        if grid[bot[0][0]][bot[0][1]] > top:
            top = grid[bot[0][0]][bot[0][1]]

    if out == 'scale':
        scaled = [[val / top for val in row] for row in grid]
        return scaled
    if out == 'abs':
        return grid
    if out == 'rainbow':
        rainbow = []
        for row in range(len(grid)):
            rainbow.append([])
            for col in range(len(grid[row])):
                val = grid[row][col]
                if val == 0:
                    rainbow[row].append(0)
                else:
                    rainbow[row].append((row * WIDTH + col) / (HEIGHT * WIDTH))
        return rainbow


def view(grid, frame_delay=1, i=0) -> None:
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
        plt.imshow(grid, cmap='turbo')
        plt.title(f'Robot Bathroom Map #{i}')
        plt.pause(frame_delay)

WIDTH = 101
HEIGHT = 103
UPDATE_END = 15000
FILENAME = './Day14/input.txt'

bots = read_bots(FILENAME)

for _ in range(UPDATE_END):
    # grid = render(bots)
    # row_density = max([len(row) - row.count(0) for row in grid])
    if _ == 7383:
        view(render(bots, out="rainbow"),3,_)
    update(bots)
res = quad_product(bots, HEIGHT // 2, WIDTH // 2)
print(res)