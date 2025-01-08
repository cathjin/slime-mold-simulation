import numpy as np
import matplotlib.pyplot as plt
import time
import math
end = False
known_oats = []


def get_coordinates(string, array):
    for i in range(0, len(string)):
        if string[i] == "(" and string[i+2] == ",":
            x = int (string[i+1])
        elif string[i] == "(":
            x = int (string[i+1] + string [i+2])
        if string[i] == "," and string[i+2] == ")":
            y = int (string[i+1])
            array.append((x,y))
        elif string[i] == ",":
            y = int (string[i+1] + string[i+2])
            array.append((x,y))
    return array


oat_locations = input("Enter where you would like to place the oats in the form (a,b)(c,d)(e,f): ")
oat_locations_array = get_coordinates(oat_locations, [])


light_locations = input("Enter where you would like to place light sources in the form (a,b)(c,d)(e,f): ")
light_locations_array = get_coordinates(light_locations, [])

grid_size = 64
colour_grid = np.zeros((grid_size, grid_size, 3), dtype = int)
grid = np.zeros((grid_size,grid_size),dtype = int)
grid [32,32] = 1

destination = (2,2)
path = [(32,32)]
found = []

path_grid = np.zeros((grid_size,grid_size),dtype = int)

mold_grid = np.zeros((grid_size, grid_size), dtype = int)
mold_grid[32,32] = 1
mold_grid[31,32] = 1
mold_grid[31,31] = 1
mold_grid[32,31] = 1

path_found = np.zeros((grid_size, grid_size), dtype = int)
items_grid = np.zeros((grid_size, grid_size), dtype = int)


for x,y in oat_locations_array:
    colour_grid[x,y,0] = 255
    colour_grid[x,y,1] = 239  
    colour_grid[x,y,2] = 212
    items_grid[x,y] = 1
    
for x,y in light_locations_array:
    for i in range(-2, 2):
        for j in range(-2,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                colour_grid[x+i,y+j,0] = 255
    for i in range(-3,3):
        for j in range(-3,3):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                items_grid[x+i, y+j] = -1

items_grid[32,32] = 1
colour_grid[32,32,0] = 255

colour_grid[32,32,1] = 239

colour_grid[32,32,2] = 212

def display_grid(grid):
    plt.imshow(grid, cmap = "binary")
    plt.show(block=False)
    plt.pause(0.1)
    plt.clf()

def num_live_neighbours(x,y):
    sum = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if (i,j) != (0,0):
                    sum += mold_grid[x+i,y+j]
    return sum

def non_diagonal_num_live_neighbours(x,y):
    sum = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if (i,j) != (0,0) and (i==0 or j ==0):
                    sum += mold_grid[x+i,y+j]
    return sum

def list_live_neighbours(x,y):
    live_neighbours = []
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if (i,j) != (0,0) and (i==0 or j ==0):
                    live_neighbours.append(mold_grid[x+i,y+j])
    return live_neighbours

def diagonal_list_live_neighbours(x, y):
    live_neighbours = []
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if (i,j) != (0,0):
                    live_neighbours.append(mold_grid[x+i,y+j])
    return live_neighbours

def neighbours_found_oat(x,y,neighbours):
    new_weight = 1
    oat_found = False
    for neighbour in neighbours:
        if neighbour > new_weight:
            new_weight = neighbour
            oat_found = True
    if mold_grid[x,y] > new_weight:
        new_weight = min(mold_grid[x,y] + 0.5, 100)
        oat_found = True
    elif oat_found == True:
        new_weight = new_weight - 0.1
    return oat_found, new_weight
    
def update_grid(colour_grid, mold_grid):
    new_colour_grid = np.copy(colour_grid)
    new_mold_grid = np.copy(mold_grid)
    for i in range(0, mold_grid.shape[0]):
        for j in range(0, mold_grid.shape[1]):
            live_neighbours = num_live_neighbours(i,j)
            if mold_grid[i,j] == 0:
                if (live_neighbours >= 1) and items_grid[i][j] != -1:
                    new_mold_grid[i,j] = 1
                    if items_grid[i,j] == 0:
                        new_colour_grid[i,j, 0] = 237 * new_mold_grid[i,j] / 12
                        new_colour_grid[i,j, 1] = 224 * new_mold_grid[i,j] / 12
                        new_colour_grid[i,j, 2] = 36  * new_mold_grid[i,j] / 12
            if items_grid[i][j] == 1:
                if new_mold_grid[i,j] != 0 and not((i,j) in known_oats):
                    new_mold_grid[i,j] = mold_grid[i,j] + 15
                    path_found [i,j] = 1
                    known_oats.append((i,j))
            oat_found, new_weight = neighbours_found_oat(i,j,diagonal_list_live_neighbours(i,j))
            if oat_found == True and items_grid[i,j] != -1:
                new_mold_grid[i,j] = new_weight
                if items_grid[i,j] == 0:
                    new_colour_grid[i,j, 0] = min(255, 237 * new_mold_grid[i,j] / 12)
                    new_colour_grid[i,j, 1] = min(255, 224 * new_mold_grid[i,j] / 12)
                    new_colour_grid[i,j, 2] = min(255, 36  * new_mold_grid[i,j] / 12)
    return new_colour_grid, new_mold_grid


def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def optimize_routes(colour_grid, mold_grid, index):
    new_colour_grid = np.copy(colour_grid)
    new_mold_grid = np.copy(mold_grid)
    for a in range(1, len(known_oats)):
        path, found = find_path_wrapper(known_oats[a])
        print(path, found)
        for i in range(0, mold_grid.shape[0]):
            for j in range(0, mold_grid.shape[1]):
                if items_grid[i,j] != -1:
                    if items_grid[i,j] == 1: 
                        new_colour_grid[i,j,0] = min(255, 237 * new_mold_grid[i,j] / 12)
                        new_colour_grid[i,j,1] = min(255, 224 * new_mold_grid[i,j] / 12)
                        new_colour_grid[i,j,2] = min(255, 36  * new_mold_grid[i,j] / 12)
                    # elif mold_grid[i,j] != 0 and not(find_path(known_oats[a], (32,32))):
                    #     new_mold_grid[i,j] = 0
                    #     new_colour_grid[i,j,0] = 0
                    #     new_colour_grid[i,j,1] = 0
                    #     new_colour_grid[i,j,2] = 0
                    elif non_diagonal_num_live_neighbours(i,j) != 4 and found == True:
                        new_mold_grid[i,j] = mold_grid[i,j] - 0.01
                        new_colour_grid[i,j, 0] = min(255, 237 * new_mold_grid[i,j] / 12)
                        new_colour_grid[i,j, 1] = min(255, 224 * new_mold_grid[i,j] / 12)
                        new_colour_grid[i,j, 2] = min(255, 36  * new_mold_grid[i,j] / 12)
                    elif non_diagonal_num_live_neighbours == 4:
                        new_mold_grid[i,j] = mold_grid[i,j] + 0.02
                        new_colour_grid[i,j, 0] = min(255, 237 * new_mold_grid[i,j] / 12)
                        new_colour_grid[i,j, 1] = min(255, 224 * new_mold_grid[i,j] / 12)
                        new_colour_grid[i,j, 2] = min(255, 36  * new_mold_grid[i,j] / 12)
                    elif found == True:
                        new_mold_grid[i,j] = mold_grid[i,j] - 0.01
                        new_colour_grid[i,j, 0] = min(255, 237 * new_mold_grid[i,j] / 12)
                        new_colour_grid[i,j, 1] = min(255, 224 * new_mold_grid[i,j] / 12)
                        new_colour_grid[i,j, 2] = min(255, 36  * new_mold_grid[i,j] / 12)
                    if new_mold_grid[i,j] >= 0.1:
                        new_mold_grid[i,j] += 0.05
                    if items_grid[i,j] != 1 and mold_grid[i,j] <= 0.01 and found == True:
                        new_mold_grid[i,j] = 0
                        new_colour_grid[i,j,0] = 0
                        new_colour_grid[i,j,1] = 0
                        new_colour_grid[i,j,2] = 0
    return new_colour_grid, new_mold_grid, path

def new_optimize_routes(colour_grid, mold_grid, index):
    new_colour_grid = np.copy(colour_grid)
    new_mold_grid = np.copy(mold_grid)
    for a in range(1, len(known_oats)):
        path, found = find_path_wrapper(known_oats[a])
        print(path, found)
        for i in range(0, mold_grid.shape[0]):
            for j in range(0, mold_grid.shape[1]):
                if items_grid[i,j] != -1:
                    if items_grid[i,j] == 1: 
                        new_colour_grid[i,j,0] = min(255, 237 * new_mold_grid[i,j] / 12)
                        new_colour_grid[i,j,1] = min(255, 224 * new_mold_grid[i,j] / 12)
                        new_colour_grid[i,j,2] = min(255, 36  * new_mold_grid[i,j] / 12)
                    if (i,j) in path :
                        new_mold_grid[i,j] = mold_grid[i,j] + 0.1
                    else: 
                        new_mold_grid[i,j] = mold_grid[i,j] - 0.1
                    if items_grid[i,j] != 1 and mold_grid[i,j] <= 0.01 and found == True:
                        new_mold_grid[i,j] = 0
                        new_colour_grid[i,j,0] = 0
                        new_colour_grid[i,j,1] = 0
                        new_colour_grid[i,j,2] = 0
    return new_colour_grid, new_mold_grid, path

def direct_neighbours(x,y):
    sum = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if i == 0 or j == 0:
                    sum += grid[x+i,y+j]
    return sum
def max_direct_neighbours(x,y):
    max = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if i == 0 or j == 0:
                    if grid[x+i,y+j] > max:
                        max = grid[x+i, y+j]
    return max
def list_direct_neighbours(x,y):
    list = []
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if i == 0 or j == 0:
                    if grid[x+i, y+j] == grid[x,y] + 1:
                        list.append((x+i, y+j))
    return list
def update_new_grid(grid):
    new_grid = np.copy(grid)
    for x in range(0,grid_size):
        for y in range (0,grid_size):
                if direct_neighbours(x,y) >= 1 and grid[x,y] == 0:
                    new_grid[x,y] = max_direct_neighbours(x,y) + 1
    return new_grid
    
for i in range(0, 64):
    grid = update_new_grid(grid)

def neighbours_min_distance(x,y):
    neighbours = list_direct_neighbours(x,y)
    min_distance = grid_size**2
    closest_index = 0
    for i in range(0, len(neighbours)):
        if distance(destination, neighbours[i]) < min_distance:
            min_distance = distance(destination, neighbours[i])
            closest_index = i
    return closest_index

def find_path_wrapper(destination):
    found = False
    path = [(32,32)]
    path, found = find_path(destination, path, found, 0)
    return path, found

def find_path(destination,path, found, count):
    currentx, currenty = path[0]
    neighbours = list_direct_neighbours(currentx, currenty)
    if len(neighbours) > 0:
        closest_neighbour = neighbours[neighbours_min_distance(currentx,currenty)]
        if closest_neighbour == destination:
            path.insert(0,closest_neighbour)
            found = True
            return path, found
        else:
            path.insert(0,closest_neighbour)
            count+=1
            return find_path(destination, path, found, count)
    else:
        return [], False
             
        

def distance(point1, point2):
    x1,y1 = point1
    x2,y2 = point2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


# for i in range(0, 64):
#     for x,y in path:
#         path_grid[x,y] = 1
#     display_grid(path_grid)

# for i in range(0, 32):
#     display_grid(grid)
#     grid = update_new_grid(grid)

# find_path((5,5))
# for i in range(0, 64):
#     for x,y in path:
#         path_grid[x,y] = 1
#     display_grid(path_grid)
for i in range(0, 40):
    display_grid(colour_grid)
    colour_grid, mold_grid = update_grid(colour_grid, mold_grid)
for i in range(0, 2000):
    display_grid(colour_grid)
    time.sleep(0.1)
    for x,y in path:
        path_grid[x,y] = 1
    display_grid(path_grid)
    time.sleep(0.1)
    colour_grid, mold_grid,path = new_optimize_routes(colour_grid, mold_grid, i)
