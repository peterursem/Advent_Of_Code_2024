from matplotlib import pyplot as plt

class Garden:
    def __init__(self, filename):
        self.grid = []
        self.map_chars = []

        self.dY = [-1, 0, 1, 0]
        self.dX = [0, 1, 0, -1]
        
        with open(filename) as file:
            for line in file.readlines():
                self.width = len(line)
                for char in line.strip():
                    if not char in self.map_chars:
                        self.map_chars.append(char)
                    self.grid.append(self.map_chars.index(char))

        self.height = len(self.grid) // self.width
        self.regions = [-1 for _ in range(len(self.grid))]
        self.neighbour_grid = self.fences = [0 for _ in range(len(self.grid))]
        self.neighbour_grid = self.neighbour_search()
        self.fences = self.perimeter()
        self.region_fill()

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def xy_to_index(self, x, y):
        if self.in_bounds(x, y):
            return x + y * self.width
        return None
    
    def get_plant(self, x, y):
        index = self.xy_to_index(x, y)
        if index != None:
            return self.grid[index]
        return None
    
    def index_to_xy(self, index):
        return index % self.width, index // self.width
    
    def nearby_indices(self, index):
        positions = []
        x, y = self.index_to_xy(index)
        for search_delta in (-1, 0), (1, 0), (0, -1), (0, 1):
            search_x = x + search_delta[0]
            search_y = y + search_delta[1]
            search_index = self.xy_to_index(search_x, search_y)
            if search_index != None:
                positions.append(search_index)
        return positions

    def neighbours(self, index):        
        plant = self.grid[index]
        x, y = self.index_to_xy(index)
        valid_checks = []
        for search_index in self.nearby_indices(index):
            if self.grid[search_index] == plant:
                search_x, search_y = self.index_to_xy(search_index)
                valid_checks.append((search_x - x, search_y - y))
        return len(valid_checks)

    def neighbour_search(self):
        return [self.neighbours(index) for index in range(len(self.grid))]
    
    def perimeter(self):
        return [4 - count for count in self.neighbour_grid]
    
    def region_fill(self):
        for index in range(len(self.grid)):
            if self.regions[index] == -1:
                next_region = max(self.regions) + 1
                self.spread_region(index, self.grid[index], next_region)
    
    def spread_region(self, index, value, region):
        if self.grid[index] != value or self.regions[index] != -1:
            return
        #view(self, 0.0001)
        self.regions[index] = region
        for spread_index in self.nearby_indices(index):
            self.spread_region(spread_index, value, region)

    def output(self, keys, type="grid"):
        if "val" in keys:
            return self.print_grid(self.grid, type)
        if "neighbour" in keys:
            return self.print_grid(self.neighbour_grid, type)
        if "fence" in keys:
            return self.print_grid(self.fences, type)
        if "region" in keys:
            return self.print_grid(self.regions, type)
        if "side" in keys:
            return self.print_grid(self.sides, type)
    
    def print_grid(self, grid, type):
        out = []
        if type == "char":
            out = ""
        for y in range(self.height):
            if type == "char":
                out = out + f'\n'
            else:
                out.append([])
            for x in range(self.width):
                if type == "char":
                    out = out + f'{grid[self.xy_to_index(x, y)]}'
                else:
                    out[y].append(grid[self.xy_to_index(x, y)])
        return out
    
    def sides(self, index):
        x, y = self.index_to_xy(index)
        plant_sides = 0
        plant = self.get_plant(x, y)

        for i in range(4):
            # Calculate new row and column based on direction
            newY = y + self.dY[i]
            newX = x + self.dX[i]

            # Check if the new position is out of bounds or a different plant
            if not self.in_bounds(newX, newY) or self.get_plant(newX, newY) != plant:
                # 90 degree counter-clockwise direction check
                newX_90CC = x + self.dX[(i - 1) % 4]
                newY_90CC = y + self.dY[(i - 1) % 4]
                isBeginEdge = not self.in_bounds(newX_90CC, newY_90CC) or self.get_plant(newX_90CC, newY_90CC) != plant

                # Concave corner check
                newX_Corner = newX + self.dX[(i - 1) % 4]
                newY_Corner = newY + self.dY[(i - 1) % 4]
                isConcaveBeginEdge = self.in_bounds(newX_Corner, newY_Corner) and self.get_plant(newX_Corner, newY_Corner) == plant

                if isBeginEdge or isConcaveBeginEdge:
                    plant_sides += 1

        return plant_sides
    
    def region_prices(self):
        regions = []
        vertices = []
        price_total = 0
        bulk_total = 0
        for region in range(max(self.regions) + 1):
            regions.append(f'Region {region}| ')
            vertices.append([])
            regions[region] = regions[region] + f'Area: {self.regions.count(region)}, '
            perim = 0
            sides = 0
            for y in range(self.height):
                for x in range(self.width):
                    index = self.xy_to_index(x, y)
                    if self.regions[index] == region:
                        perim += self.fences[index]
                        sides += self.sides(index)
            regions[region] = regions[region] + f'Perimeter: {perim}, Price: {self.regions.count(region) * perim}, Bulk Price: {sides * self.regions.count(region)}'
            price_total += self.regions.count(region) * perim
            bulk_total += sides * self.regions.count(region)
        regions.append(f'Reg Price: {price_total}, Bulk Price: {bulk_total}')
        return regions

    def fence_total(self):
        return sum(self.fences)
    

def view(garden, frame_delay=1) -> None:
        """
        shows an image of the current state of the grid
        parameters:
            grid - list-of-lists representing the current grid. Inner lists use 0s to represent dead cells, and 1s to represent live ones
            frame_delay - the program will pause for this many seconds after displaying the image. 0.1s gives a pretty good animation effect
            step_number - the step number of the supplied grid (will be displayed above the image)
        """       


        grids = [garden.output("val"), garden.output("region"), garden.output("neighbour"), garden.output("fence")]

        # plot the grid

        plt.cla()

        #fig, axes = plt.subplots(2, 2, figsize=(10, 10))  # 2x2 layout
        titles = ['Values', 'Regions', 'Neighbours', 'Perimeter (Fences)']
        cmaps = ['turbo', 'turbo', 'viridis', 'viridis']

        for i, (grid, ax) in enumerate(zip(grids, axes.flat)):
            ax.imshow(grid, cmap=cmaps[i])
            ax.set_title(titles[i])
            ax.axis('off')  # Turn off the axes for a cleaner look

        plt.suptitle('Flower Fields', fontsize=16)  # Add a main title for the page
        plt.pause(frame_delay)

        return fig, axes
        
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
garden = Garden('./Day12/input.txt')

print(garden.map_chars)
print(garden.output("val", "char"))
print(garden.output("region", "char"))
print(garden.output("neighbour", "char"))
print(garden.output("fence", "char"))

for price in garden.region_prices():
    print(price)

if True:
    view(garden, 5)