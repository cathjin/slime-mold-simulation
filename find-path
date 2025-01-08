import numpy as np
import matplotlib.pyplot as plt
import time
import math

grid = np.zeros((64,64),dtype = int)

colour_grid = np.zeros((64,64,3), dtype=int)
grid_size = 64
def display_grid(grid):
    plt.imshow(grid)
    plt.show(block=False)
    plt.pause(0.001)
    plt.clf()
    
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
def update_grid(grid):
    new_grid = np.copy(grid)
    for x in range(0,64):
        for y in range (0,64):
                if direct_neighbours(grid, x,y) >= 1 and grid[x,y] == 0:
                    new_grid[x,y] = max_direct_neighbours(grid, x,y) + 1
    return new_grid




destinations = [(40,40), (1,2), (60,15)]
paths =[[(32,32)],[(32,32)], [(32,32)]]


path_grid = np.zeros((64,64),dtype = int)

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

print(paths[1][0])
for i in range(0, len(destinations)):
    print(i)
    pathsx, pathsy = paths[i][0]
    grid = np.zeros((64,64),dtype = int)
    grid [pathsx, pathsy] = 1
    for j in range(0, 128):
        grid = update_grid(grid)
    paths[i] = find_path(grid, destinations[i], paths[i])

new_paths = []
for i in range(0, len(destinations)):
    for j in range(0, len(destinations)):
        if i != j:
            new_paths.insert(0,[destinations[j]])
    for k in range(0, len(destinations)-1):
        pathsx, pathsy = new_paths[k][0]
        grid = np.zeros((64,64),dtype = int)
        grid [pathsx, pathsy] = 1
        for j in range(0, 128):
            grid = update_grid(grid)
        new_paths[k] = find_path(grid, destinations[i], new_paths[k])
print (new_paths)

for i in range(0,50):
    for i in range(0, len(paths)):
        for x,y in paths[i]:
            path_grid[x,y] = 1
    display_grid(path_grid)

new_path_grid = np.zeros((64,64), dtype = int)
for i in range(0,50):
    for i in range(0, len(new_paths)):
        for x,y in new_paths[i]:
            new_path_grid[x,y] = 1
    display_grid(new_path_grid)