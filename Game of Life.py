#Importing necessary libraries

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math
import random
import os 

#Declaring the variables required

dead_cells={}
resurrected_cells={}
resurrecting_pos=[]
random_dead_cells=[]

#Function to convert axial coordinates to screen coordinates

def axial_to_screen(q, r, hex_size):
    x_screen = hex_size* math.sqrt(3)*(q +r/2)
    y_screen = hex_size*3/2* r
    return x_screen, y_screen

#Function to generate grid based on screen coordinates

def screen_coordinate_grid(N, grid):
    screen_coord=[]
    size=2*N+1

    for row in range(size):
        row_size = size - abs(N - row)
        inner_row = [None] * row_size
        screen_coord.append(inner_row)

    for r in range(size):
        for q in range(size - abs(N-r)):
            screen_coord[r][q]=(axial_to_screen(grid[r][q][0][0], grid[r][q][0][1],10),grid[r][q][1])
            
    return screen_coord

#Functions to calculate corners of the hexagon 

def hex_corner(center, size, i):
    degree = (60 *i)+ 30
    radians = math.pi/180* degree
    return (center[0] +size*math.cos(radians),
            center[1] +size *math.sin(radians))

def calculate_hexagon_vertices(center, size):
    vertices = []
    for i in range(6):
        vertex = hex_corner(center, size,i)
        vertices.append(vertex)
    return vertices

#Function to plot the hexagon

def draw_hexagons(screen_centers, hex_size, generation):
    Folder="Frames"
    if not os.path.exists(Folder):
        os.makedirs(Folder)
    fig, ax = plt.subplots()
    i = 0
    background_color = "black"
    dead_cell="black"
    alive_cell=(57/255, 210/255, 20/255)
    for rows in screen_centers:
        for center in rows:
            vertices = calculate_hexagon_vertices(center[0], hex_size)
            if center[1] == 0:
                color = dead_cell
            elif center[1] == 1:
                color = alive_cell
            plt.gca().add_patch(Polygon(vertices, closed=True, fill=True, facecolor=color, edgecolor=(57/255, 210/255, 20/255)))
            i += 1
    plt.axis('equal')
    fig.patch.set_facecolor(background_color)
    plt.axis('off')
    plt.savefig(os.path.join(Folder, f"generation_{generation}.png"))
    plt.close()

#Function to implement rule number 7 (random dead cell resurrection)
def update_random_dead_cells(grid):
    global random_dead_cells
    random_dead_cells.clear()
    for row in grid:
        for cell in row:
            if not is_alive(cell[0]):
                random_dead_cells.append(cell[0])

def random_dead_cell_selection():
    global random_dead_cells
    return random.choice(random_dead_cells)


#Function to calculate the neighbours

def alive_neighbours(cell,grid):
    directions=[(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    count=0
    for direction in directions:
        coord=tuple(x + y for x, y in zip(cell, direction))
        for row in grid:
            for center in row:
                if center[0] == coord:
                    if center[1]==1:
                        count=count+1
                        
    return count

#Function to find if the cell is alive

def is_alive(cell):
    return cell[1]==1

#Function to check if the cell will be bnorn or not

def is_born(cell,grid):
    neighbours=alive_neighbours(cell[0],grid)
    return (not is_alive(cell)) and neighbours==3

#Function to set the next genration grid

def next_gen_grid(N, parent_grid,count):
    size=2*N+1
    new_grid = []
    global resurrecting_pos
    pos=None
    if (count%4==0):
        update_random_dead_cells(parent_grid)
        pos=random_dead_cell_selection()
    
    for row in range(size):
        row_size = size - abs(N - row)
        inner_row = [None] * row_size
        new_grid.append(inner_row)
        
    for r in range(size):
        for q in range(size - abs(N-r)):
            cell=parent_grid[r][q]
            if ((cell[0] in resurrecting_pos) or survives(cell, parent_grid) or is_born(cell, parent_grid) or (pos is not None and cell[0]==pos)):
                state=1
            else:
                state=0
            new_grid[r][q]=((q+(max(0,N-r)),r),state)
            
    return new_grid

#Function to set the initial state of the grid

def generate_grid(N):
    size = 2 * N + 1
    grid = []

    for row in range(size):
        row_size = size - abs(N - row)
        inner_row = [None] * row_size
        grid.append(inner_row)

    alive_count = 0  

    for r in range(size):
        for q in range(size -abs(N - r)):
            if alive_count < 15:
                alive = random.choice([True, False])
                if alive:
                    grid[r][q] = ((q +max(0, N-r), r), 1)
                    alive_count += 1
                else:
                    grid[r][q]= ((q + max(0, N-r), r), 0)
            else:
                grid[r][q] =((q + max(0, N-r), r), 0)
    return grid

#Function to check the survival condition

def survives(cell,grid):
    global dead_cells
    global resurrected_cells
    global resurrecting_pos
    neighbours=alive_neighbours(cell[0],grid)
    if is_alive(cell) and neighbours < 2:
        if ((cell[0] not in dead_cells) and (( cell[0] in resurrected_cells and resurrected_cells[cell[0]] != "UP") or cell[0] not in resurrected_cells)):
            dead_cells[cell[0]]=(0,"UP")
    elif is_alive(cell) and neighbours > 3:
        if ((cell[0] not in dead_cells) and (( cell[0] in resurrected_cells and resurrected_cells[cell[0]] != "OP") or cell[0] not in resurrected_cells)):
            dead_cells[cell[0]]=(0,"OP")

    state=is_alive(cell) and neighbours in [2,3]

    if is_alive(cell) and neighbours < 2:
        if ( ( cell[0] in resurrected_cells and resurrected_cells[cell[0]] == "UP")):
            state=1
    elif is_alive(cell) and neighbours > 3:
        if ( ( cell[0] in resurrected_cells and resurrected_cells[cell[0]] == "OP")):
            state=1
    return state

#Function taht updates the dying cell dictionary for every generations

def update_dying_cells():
    updated_dead_cells={}
    global dead_cells
    global resurrected_cells
    global resurrecting_pos
    resurrected_cells.clear()
    for cell, value in dead_cells.items():
        if(value[0]+1!=6): 
            updated_value = (value[0] + 1, value[1])
            updated_dead_cells[cell] = updated_value
        if(value[0]+1==6):
            if cell not in resurrected_cells:
                resurrected_cells[cell]=value
            else:
                del resurrected_cells[cell]
                resurrected_cells[cell]=value
            resurrecting_pos.append(cell)
    dead_cells=updated_dead_cells

#THE GAME
cell_nos=10 ##You can adjust the cell count here
hex_size=5
generations=20 ##You can adjust the genration numbers here
parent_grid=generate_grid(cell_nos)
screen_coord=screen_coordinate_grid(cell_nos, parent_grid)
draw_hexagons(screen_coord,10,0)
for i in range(1,generations+1):
    update_dying_cells()
    new_gen_grid=next_gen_grid(cell_nos,parent_grid,i)
    screen_coord_new_gen=screen_coordinate_grid(cell_nos, new_gen_grid)
    draw_hexagons(screen_coord_new_gen,10,i)
    parent_grid=new_gen_grid
print("All Frames Generated!!")


"""
The coordinate system employed in this implementation is based on the axial coordinate system for hexagonal grids, as detailed in the website "https://www.redblobgames.com/grids/hexagons/". 
The mathematical logic behind this implementation was derived from the explanations provided on the website, which elaborates on the relationship between axial coordinates and screen coordinates for rendering hexagons. 
"""