import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import math
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, ROBOT_LENGTH, ROBOT_START_POS, ROBOT_WIDTH
from gridmap import create_empty_grid, add_obstacles, add_border_obstacles
from pathfinding import astar
from helperfunctions import goalCellChecked

def inflate_obstacles(grid, margin=1):
    # Udvider hver forhindringscelle med én celles margin
    new_grid = [row[:] for row in grid]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                for dy in range(-margin, margin+1):
                    for dx in range(-margin, margin+1):
                        ny, nx = y + dy, x + dx
                        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                            new_grid[ny][nx] = 1
    return new_grid

# 1) Byg grid og forhindringer
grid = create_empty_grid()
grid = add_obstacles(grid)
grid = inflate_obstacles(grid, margin=1)
grid = add_border_obstacles(grid)

# 2) Start og mål i gitter-indeks
start = (
    int(ROBOT_START_POS[0]),
    int(ROBOT_START_POS[1])
)
endGoal  = (17, 4) #TEST MED DENNE HVIS DU GERNE VIL PRØVE ANDET MÅL POSITION
#endGoal = (GRID_WIDTH - 1, START_POS_CM[1] // GRID_SIZE)
#goal = goal_cell(grid, endGoal)
goal= goalCellChecked(grid, (11, 1))

# 3) Find sti
path = astar(grid, start, goal)
if not path:
    print("❌ Ingen sti fundet!")
    exit(1)

# 4) Udskriv resultat
print("✅ Fundet sti (i gitterceller):", path)
print()

# 5) ASCII-visualisering
for y in range(GRID_HEIGHT):
    row = ""
    for x in range(GRID_WIDTH):
        if (x, y) == start:
            row += "S"   # start
        elif (x, y) == goal:
            row += "G"   # goal
        elif (x, y) in path:
            row += "·"   # sti
        elif grid[y][x] == 1:
            row += "■"   # forhindring
        else:
            row += " "   # frit
    print(row)
