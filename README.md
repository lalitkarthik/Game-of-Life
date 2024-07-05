# Game of Life

This project implements a variant of Conway's Game of Life on a hexagonal grid. The game uses hand-coded rules and functions to simulate generations of cell states, rendering each generation as an image.

## Project Structure

The system consists of the following main components:

1. **Grid Generation and Initialization**: Functions to generate and initialize a hexagonal grid with random initial cell states.
2. **State Update Functions**: Functions to update cell states based on the rules of the game.
3. **Visualization**: Functions to visualize the hexagonal grid using Matplotlib.

## Components

- **Python 3.x**
- **Jupyter Notebook**
- **Matplotlib**
- **Math**
- **Random**
- **OS**

## How It Works

### Grid Generation

The grid is generated using axial coordinates for hexagonal grids. The initial state of the grid is randomly assigned, with a certain number of cells set to alive.

### State Update Functions

The state of each cell is updated based on the number of alive neighbors it has. The rules are:
- A living cell with fewer than 2 or more than 3 neighbors dies.
- A dead cell with exactly 3 neighbors becomes alive.
- Additionally, a random dead cell is resurrected every 4th generation.

### Visualization

Each generation of the grid is visualized as an image using Matplotlib. The hexagons are drawn based on their screen coordinates calculated from their axial coordinates.

