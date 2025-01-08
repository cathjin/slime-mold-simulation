import numpy as np
import matplotlib.pyplot as plt

grid_size = int(input("How big do you want the grid to be? "))
grid = np.zeros((grid_size, grid_size), dtype=int)

def display_grid(grid):
    plt.imshow(grid, cmap="binary")
    plt.show(block=False)
    plt.pause(0.1)
    plt.clf()

def update_grid(grid, stay_live, become_live):
    new_grid = np.copy(grid)
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            live_neighbors = (
                grid[i - 1, j - 1]
                + grid[i - 1, j]
                + grid[i - 1, j + 1]
                + grid[i, j - 1]
                + grid[i, j + 1]
                + grid[i + 1, j - 1]
                + grid[i + 1, j]
                + grid[i + 1, j + 1]
            )
            if grid[i, j] == 1:  
                if live_neighbors != stay_live:
                    new_grid[i, j] = 0  
            else:  
                if live_neighbors == become_live:
                    new_grid[i, j] = 1  
    return new_grid

# Initialize grid with a random state

stay_live = int(input("How many neighbours should a cell have to remain alive? "))
become_live = int(input("How many neighbours should a cell have to come to life? "))
done = False
while done == False:
    start_live = (input("Enter the coordinates in the format 'x,y' for the cells you would like to start live. \n If you are done, please enter 'done'. \n If you would like it to be randomized, please enter 'random'"))
    if start_live == "random":
        grid = np.random.choice([0,1], size = (grid_size, grid_size))
        done = True
        break
    if start_live == "done":
        done = True
        break
    start_live_x = int(start_live[0])
    start_live_y = int(start_live[2])
    grid[start_live_x, start_live_y] = 1
    
end = True
while end == True:  # Number of iterations
    display_grid(grid)
    grid = update_grid(grid, stay_live, become_live)