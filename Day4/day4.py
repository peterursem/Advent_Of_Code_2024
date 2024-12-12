import re

SEARCH_TERM = "XMAS"
FILENAME = "./Day4/input.txt"

def grid_from_file(fileName) -> list:
    with open(fileName) as file:
        return [line.strip() for line in file.readlines()]

def cell_in_bounds(grid, row: int, col: int):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def search_from_pos(row: int, col: int, grid: list):
    found = 0
    for dr in (1,0,-1):
        for dc in (1,0,-1):
            step = 1
            while step < len(SEARCH_TERM):
                search_row = row + dr * step
                search_col = col + dc * step

                if not cell_in_bounds(grid, search_row, search_col):
                    step = len(SEARCH_TERM) + 1
                    continue

                search_val = grid[search_row][search_col]

                if search_val != SEARCH_TERM[step]:
                    step = len(SEARCH_TERM) + 1
                    continue

                if step == len(SEARCH_TERM) - 1:
                    print(f"Found a match: {SEARCH_TERM} at Row: {row}, Col: {col}, with direction dR: {dr}, dC: {dc}")
                    found += 1
                
                step += 1

    return found

def map_first_letter(grid) -> list:
    return [[e.start() for e in re.finditer(SEARCH_TERM[0], line)] for line in grid]

def main():
    grid = grid_from_file(FILENAME)

    start_map = map_first_letter(grid)
    finds = 0
    for row in range(len(start_map)):
        for col in start_map[row]:
            finds += search_from_pos(row, col, grid)
    print(finds)

main()