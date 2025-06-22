from .config import GRID_HEIGHT, GRID_SIZE, GRID_WIDTH
# -*- coding: utf-8 -*-


def goalCellChecked(grid, raw_goal):
    x_goal, y_goal = raw_goal

    # Hvis den ønskede celle er blokeret
    if grid[y_goal][x_goal] == 1:
        # Scan mod venstre fra x_goal til 0 på samme række
        for x in range(x_goal, -1, -1):
            if grid[y_goal][x] == 0:
                adjusted = (x, y_goal)
                print("Warning: standard goal {} is blocked. Adjusted to {}.".format(raw_goal, adjusted))
                return adjusted

    # Returnér original, hvis den er fri
    return raw_goal
  
def     compress_path(path):

    if len(path) < 2:
        return []
    runs = []
    # Start første run
    prev = path[0]
    dx = path[1][0] - prev[0]
    dy = path[1][1] - prev[1]
    count = 1
    # Gennemløb resten to og to
    for (x0,y0),(x1,y1) in zip(path[1:], path[2:]):
        ndx, ndy = x1 - x0, y1 - y0
        if ndx == dx and ndy == dy:
            count += 1
        else:
            runs.append((dx, dy, count))
            dx, dy = ndx, ndy
            count  = 1
    runs.append((dx, dy, count))
    return runs


def cm_to_grid(coord_cm):

    x_cm, y_cm = coord_cm
    col = int(x_cm // GRID_SIZE)
    row = int(y_cm // GRID_SIZE)
    # Clamp til gyldigt område
    col = max(0, min(col, GRID_WIDTH - 1))
    row = max(0, min(row, GRID_HEIGHT - 1))
    return col, row

