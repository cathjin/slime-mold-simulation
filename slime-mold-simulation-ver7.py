import numpy as np
import matplotlib.pyplot as plt
import time
import math

known_oats = []
all_paths = []
all_paths_points = []


grid_size = 64
mold_grid = np.zeros((grid_size, grid_size), dtype = int)
colour_grid = np.zeros((grid_size, grid_size, 3), dtype = int)
grid = np.zeros((grid_size,grid_size),dtype = int)
path_grid = np.zeros((grid_size,grid_size),dtype = int)
path_found = np.zeros((grid_size, grid_size), dtype = int)
items_grid = np.zeros((grid_size, grid_size), dtype = int)

mold_grid[32,32] = 1
mold_grid[31,32] = 1
mold_grid[31,31] = 1
mold_grid[32,31] = 1

items_grid[32,32] = 1
colour_grid[32,32,0] = 255
colour_grid[32,32,1] = 239
colour_grid[32,32,2] = 212

explored_all = False
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

for x,y in oat_locations_array:
    colour_grid[x,y,0] = 255
    colour_grid[x,y,1] = 239  
    colour_grid[x,y,2] = 212
    items_grid[x,y] = 1

light_locations = input("Enter where you would like to place light sources in the form (a,b)(c,d)(e,f): ")
light_locations_array = get_coordinates(light_locations, [])

for x,y in light_locations_array:
    for i in range(-2, 2):
        for j in range(-2,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                colour_grid[x+i,y+j,0] = 255
    for i in range(-3,3):
        for j in range(-3,3):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                items_grid[x+i, y+j] = -1

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

def direct_num_live_neighbours(x,y):
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

def max_direct_neighbours(x,y):
    max = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if i == 0 or j == 0:
                    if grid[x+i,y+j] > max:
                        max = grid[x+i, y+j]

def neighbours_found_oat(x,y,neighbours, grid, neighbours_coord, path_points):
    new_weight = 1
    oat_found = False
    for i in range(0, len(neighbours)):
        if neighbours_coord[i] in path_points:
            if neighbours[i] > new_weight:
                new_weight = neighbours[i]
                oat_found = True
        else:
            if neighbours[i] > new_weight:
                new_weight = neighbours[i] - 0.5
                oat_found = True
    if grid[x,y] > new_weight:
        new_weight = min(grid[x,y] + 0.5, 100)
        oat_found = True
    elif oat_found == True:
        new_weight = new_weight - 0.1
    return oat_found, new_weight
    
def update_grid(colour_grid, mold_grid, index):
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
                    known_oats.insert(0,(i,j))
                    find_path_wrapper(known_oats[0],[(32,32)])
            oat_found, new_weight = neighbours_found_oat(i,j,diagonal_list_live_neighbours(i,j), new_mold_grid, new_list_direct_neighbours(i,j), all_paths_points)
            if oat_found == True and items_grid[i,j] != -1 and index <= 40:
                new_mold_grid[i,j] = new_weight
                if items_grid[i,j] == 0:
                    new_colour_grid[i,j, 0] = min(255, 237 * new_mold_grid[i,j] / 12)
                    new_colour_grid[i,j, 1] = min(255, 224 * new_mold_grid[i,j] / 12)
                    new_colour_grid[i,j, 2] = min(255, 36  * new_mold_grid[i,j] / 12)
            if (i,j) in all_paths_points:
                new_mold_grid[i,j] = min(new_mold_grid[i,j] + 1, 50)
            elif all_paths_points != [] and index >= 32:
                new_mold_grid[i,j] = max(new_mold_grid[i,j] - 1, 0)
    return new_colour_grid, new_mold_grid


def direct_neighbours(grid, x,y):
    sum = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if i == 0 or j == 0:
                    sum += grid[x+i,y+j]
    return sum
def max_direct_neighbours(grid, x,y):
    max = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if i == 0 or j == 0:
                    if grid[x+i,y+j] > max:
                        max = grid[x+i, y+j]
    return max
def list_direct_neighbours(grid, x,y):
    list = []
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                if i == 0 or j == 0:
                    if grid[x+i, y+j] == grid[x,y] + 1:
                        list.append((x+i, y+j))
    return list
def new_list_direct_neighbours(x,y):
    list = []
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and x+i < grid_size and y+j >= 0 and y+j < grid_size:
                        list.append((x+i, y+j))
    return list
def new_update_grid(grid):
    new_grid = np.copy(grid)
    for x in range(0,64):
        for y in range (0,64):
                if direct_neighbours(grid, x,y) >= 1 and grid[x,y] == 0:
                    new_grid[x,y] = max_direct_neighbours(grid, x,y) + 1
    return new_grid

def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def update_number_grid(grid):
    new_grid = np.copy(grid)
    for x in range(0,grid_size):
        for y in range (0,grid_size):
                if direct_num_live_neighbours(x,y) >= 1 and grid[x,y] == 0:
                    new_grid[x,y] = max_direct_neighbours(x,y) + 1
    return new_grid
def neighbours_min_distance(grid, x,y, destination):
    neighbours = list_direct_neighbours(grid, x,y)
    min_distance = grid_size**2
    closest_index = 0
    for i in range(0, len(neighbours)):
        if distance(destination, neighbours[i]) < min_distance:
            min_distance = distance(destination, neighbours[i])
            closest_index = i
    return closest_index
found = False

def find_path_wrapper(destination, paths):
    pathsx, pathsy = paths[0]
    grid = np.zeros((64,64),dtype = int)
    grid [pathsx, pathsy] = 1
    for j in range(0, 128):
        grid = new_update_grid(grid)
    path = find_path(grid, destination,[(32,32)])
    for x,y in path:
        path_grid[x,y] = 1
    if path != []:
        all_paths.insert(0, path)
        all_paths_points.extend(path)
def find_path(grid, destination, path):
    currentx, currenty = path[0]
    neighbours = list_direct_neighbours(grid, currentx, currenty)
    if len(neighbours) > 0:
        closest_neighbour = neighbours[neighbours_min_distance(grid, currentx,currenty, destination)]
        if closest_neighbour == destination:
            path.insert(0,closest_neighbour)
            print("success")
            return path
        else:
            path.insert(0,closest_neighbour)
            return find_path(grid, destination, path)
    else:
        print("fail")
        return []
        

def distance(point1, point2):
    x1,y1 = point1
    x2,y2 = point2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

for i in range(0, 200):
    if mold_grid[0,0] != 0:
        explored_all = True
    display_grid(colour_grid)
    colour_grid, mold_grid = update_grid(colour_grid, mold_grid, i)