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

mold_grid = np.zeros((grid_size, grid_size), dtype = int)
mold_grid[32,32] = 1
mold_grid[31,32] = 1
mold_grid[31,31] = 1
mold_grid[32,31] = 1

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
colour_grid[31,32,0] = 237
colour_grid[31,31,0] = 237
colour_grid[32,31,0] = 237

colour_grid[32,32,1] = 239
colour_grid[31,32,1] = 224
colour_grid[31,31,1] = 224
colour_grid[32,31,1] = 224

colour_grid[32,32,2] = 212
colour_grid[31,32,2] = 36
colour_grid[31,31,2] = 36
colour_grid[32,31,2] = 36

def display_grid(grid):
    plt.imshow(grid)
    plt.show(block=False)
    plt.pause(0.1)
    plt.clf()

def num_live_neighbours(x,y):
    if x == grid_size - 1 and y == grid_size - 1:
        live_neighbours = (
                    mold_grid [x - 1, y] 
                    + mold_grid[x, y - 1]
                    + mold_grid [x - 1, y - 1] 
                    )
    elif x == grid_size - 1:
        live_neighbours = (
                    mold_grid [x - 1, y] 
                    + mold_grid[x, y+ 1] 
                    + mold_grid[x, y - 1]
                    + mold_grid [x - 1, y - 1] 
                    + mold_grid[x-1, y+1]
                    )
    elif y == grid_size - 1:
        live_neighbours = (
                mold_grid[x + 1,y] 
                + mold_grid [x - 1, y] 
                + mold_grid[x, y - 1]
                + mold_grid [x - 1, y - 1] 
                + mold_grid[x+1, y - 1]
                )
    else:
        live_neighbours = (
                mold_grid[x + 1,y] 
                + mold_grid [x - 1, y] 
                + mold_grid[x, y + 1] 
                + mold_grid[x, y - 1]
                + mold_grid [x - 1, y - 1] 
                + mold_grid[x+1, y + 1] 
                + mold_grid[x+1, y - 1]
                + mold_grid[x-1, y+1]
                )
    return live_neighbours

def non_diagonal_num_live_neighbours(x,y):
    if x == grid_size - 1 and y == grid_size - 1:
        live_neighbours = (
                    mold_grid [x - 1, y] 
                    + mold_grid[x, y - 1]
                    )
    elif x == grid_size - 1:
        live_neighbours = (
                    mold_grid [x - 1, y] 
                    + mold_grid[x, y+ 1] 
                    + mold_grid[x, y - 1]
                    )
    elif y == grid_size - 1:
        live_neighbours = (
                mold_grid[x + 1,y] 
                + mold_grid [x - 1, y] 
                + mold_grid[x, y - 1]
                )
    else:
        live_neighbours = (
                mold_grid[x + 1,y] 
                + mold_grid [x - 1, y] 
                + mold_grid[x, y + 1] 
                + mold_grid[x, y - 1]
                )
    return live_neighbours

def update_grid(colour_grid, mold_grid):
    new_colour_grid = np.copy(colour_grid)
    new_mold_grid = np.copy(mold_grid)
    for i in range(0, mold_grid.shape[0]):
        for j in range(0, mold_grid.shape[1]):
            non_diagonal_live_neighbours = non_diagonal_num_live_neighbours(i,j)
            live_neighbours = num_live_neighbours(i,j)
            if mold_grid[i,j] == 0:
                if (non_diagonal_live_neighbours == 2 or non_diagonal_live_neighbours == 1) and items_grid[i][j] != -1:
                    new_mold_grid[i,j] = 1
                    if items_grid[i][j] == 1:
                        if new_mold_grid[i,j] == 1 and not((i,j) in known_oats) and (i,j) != (32,32):
                            known_oats.append((i,j))
                    else:
                        new_colour_grid[i,j, 0] = 237
                        new_colour_grid[i,j, 1] = 224
                        new_colour_grid[i,j, 2] = 36
    return new_colour_grid, new_mold_grid

def optimize_routes(colour_grid, mold_grid, index):
    new_colour_grid = np.copy(colour_grid)
    new_mold_grid = np.copy(mold_grid)
    for a in range(0, len(known_oats)):
        oatx,oaty = known_oats[a]
        for i in range(0, mold_grid.shape[0]):
            for j in range(0, mold_grid.shape[1]):
                if items_grid[i,j] != -1:
                    if items_grid[i,j] == 1: 
                        new_colour_grid[i,j, 0] = 255
                        new_colour_grid[i,j, 1] = 239
                        new_colour_grid[i,j, 2] = 212
                    elif mold_grid[i,j] == 1 and (distance (oatx, oaty, i, j) > distance (oatx,oaty,32,32) or distance (i,j,32,32) > distance (32, 32,oatx,oaty)
                    or distance(oatx,oaty,i,j) + distance(32,32, i,j) > distance (oatx,oaty,32,32) + 10):
                        new_mold_grid[i,j] = 0
                        new_colour_grid[i,j,0] = 0
                        new_colour_grid[i,j,1] = 0
                        new_colour_grid[i,j,2] = 0
                    if items_grid[i,j] != 1 and (non_diagonal_num_live_neighbours(i,j) <= 1 or (num_live_neighbours(i,j) == 8 and index >= 1)):
                        new_mold_grid[i,j] = 0
                        new_colour_grid[i,j,0] = 0
                        new_colour_grid[i,j,1] = 0
                        new_colour_grid[i,j,2] = 0
                
    return new_colour_grid, new_mold_grid

def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)





for i in range(0, 64):
    display_grid(colour_grid)
    colour_grid, mold_grid = update_grid(colour_grid, mold_grid)
print(mold_grid)

for i in range(0, 32):
    display_grid(colour_grid)
    time.sleep(1)
    display_grid(mold_grid)
    time.sleep(1)
    colour_grid, mold_grid = optimize_routes(colour_grid, mold_grid, i)
    


    
