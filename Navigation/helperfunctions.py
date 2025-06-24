from .config import GRID_HEIGHT, GRID_SIZE, GRID_WIDTH, MID_REGION_X_MAX, MID_REGION_X_MIN, MID_REGION_Y_MAX, MID_REGION_Y_MIN, SAFEZONES
# -*- coding: utf-8 -*-
#helperfunctions.py 

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
  
def compress_path(path):

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


def extract_entities(tasks):

    cross       = tasks[0]
    robot_from_pic       = tasks[1]
    if len(tasks) == 4 and tasks[2]["name"] == "orange":
        orange = tasks[2]
        white_list = tasks[3]
    else:
        orange     = None
        white_list = tasks[2]
    return cross, robot_from_pic, orange, white_list


def find_nearest_white(robot, white_list):
    rx, ry = robot["x"], robot["y"]
    return min(
        white_list,
        key=lambda w: (w["x"]-rx)**2 + (w["y"]-ry)**2
    )

def select_ball_sequence(robot, orange, white_list, grid):

    def is_free(ball):
            x, y = ball["x"], ball["y"]
            if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
                return False
            return grid[y][x] == 0

    # Find og print hvide bolde, der frasorteres
    removed_whites = [w for w in white_list if not is_free(w)]
    for w in removed_whites:
        print("Filtered out white ball at (x={}, y={})".format(w['x'], w['y']))

    free_whites = [w for w in white_list if is_free(w)]

    if orange:
        if not is_free(orange):
            print("Filtered out orange ball at (x={}, y={})".format(orange['x'], orange['y']))
            orange = None
    else:
        orange = None

    if orange:
        return [orange]

    if not free_whites:
        return []

    nearest = find_nearest_white(robot, free_whites)
    return [nearest]



def print_grid_and_route(grid, path1, path2):


    marker = [[None]*GRID_WIDTH for _ in range(GRID_HEIGHT)]
    for idx, path in enumerate((path1, path2), start=1):
        if not path:
            continue
        for x,y in path:
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                marker[y][x] = str(idx)

    for y in range(GRID_HEIGHT-1, -1, -1):
        row = []
        for x in range(GRID_WIDTH):
            if marker[y][x]:
                row.append(marker[y][x])
            elif grid[y][x] == 1:
                row.append('#')
            else:
                row.append('.')
        print(''.join(row))



def is_in_mid_region(cell):
    x, y = cell
    return MID_REGION_X_MIN <= x <= MID_REGION_X_MAX and MID_REGION_Y_MIN <= y <= MID_REGION_Y_MAX
    


def nearest_safezone(cell):
    return min(
        SAFEZONES,
        key=lambda sz: (cell[0] - sz[0])**2 + (cell[1] - sz[1])**2
    )
