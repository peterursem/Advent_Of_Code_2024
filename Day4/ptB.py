import re

SEARCH_TERM = "MAS"
FILENAME = "./Day4/input.txt"

def grid_from_file(fileName) -> list:
    with open(fileName) as file:
        return [line.strip() for line in file.readlines()]

def cell_in_bounds(grid, row: int, col: int):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def search_from_pos(row: int, col: int, grid: list):
    print(f"---- Searching at: R:{row}, C:{col} ----")
    found = 0
    for dr in (1,-1):
        for dc in (1,-1):
            search_row = row + (dr)
            search_col = col + (dc)

            opp_row = row + (dr * -1)
            opp_col = col + (dc * -1)

            if not cell_in_bounds(grid, search_row, search_col):
                continue
            if not cell_in_bounds(grid, opp_row, opp_col):
                continue

            search_val = grid[search_row][search_col]
            opp_val = grid[opp_row][opp_col]

            search = ""
            for i in range(len(SEARCH_TERM)):
                if i != int(len(SEARCH_TERM)/2):
                    search = search + SEARCH_TERM[i] 

            if (opp_val + search_val) == search:
                found += 1
                print(f"Found Match #{found}: {SEARCH_TERM}")

    if found == 2:
        print("Two matches found, completed cross")
        return True
    else:
        print("No cross found")
        return False

def map_middle_letter(grid) -> list:
    return [[e.start() for e in re.finditer(SEARCH_TERM[int(len(SEARCH_TERM)/2)], line)] for line in grid]

def main():
    grid = grid_from_file(FILENAME)
    start_map = map_middle_letter(grid)

    finds = 0
    for row in range(len(start_map)):
        for col in start_map[row]:
            if search_from_pos(row, col, grid):
                finds += 1
    print(finds)

main()