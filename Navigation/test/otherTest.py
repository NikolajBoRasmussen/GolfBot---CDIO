
import heapq
import math
import sys
import os

from ..helperfunctions import compress_path, print_grid_and_route


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ..gridmap import add_border_obstacles, add_obstacles, create_empty_grid, print_grid

from ..config import GRID_HEIGHT, GRID_WIDTH, MIN_SEGMENT_CM, SAFEPOINTS, STOP_DISTANCE_FROM_BALL

def build_grid(cross_pos):
    grid = create_empty_grid()
    grid = add_obstacles(grid, cross_pos)
    grid = add_border_obstacles(grid)
    print_grid(grid)
    return grid



def runflow(tasks):

    cross, robot_from_pic, orange, white_list = extract_entities(tasks)

    robot_cell = (robot_from_pic["x"], robot_from_pic["y"])

    grid= build_grid((84,61))
    
    ball_sequence = select_ball_sequence(robot_from_pic, orange, white_list, grid)

    # 3) Eksekver for hver bold
    current_angle = 0.0
    
    print("ball_sequence:", ball_sequence)
    for ball in ball_sequence:
        current_angle = execute_ball_flow(
            ball, robot_cell, grid
        )


tasks_with_orange = [
    {"name": "cross",  "x": 85,  "y": 60},
    {"name": "robot",  "x": 30,  "y": 30},
    {"name": "orange", "x": 30, "y": 40},
    [
        {"name": "white", "x": 20,  "y": 100},
        {"name": "white", "x": 160, "y": 80},
    ]
]

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

    free_whites = [w for w in white_list if is_free(w)]

    # Tjek orange
    orange_free = (orange if (orange and is_free(orange)) else None)

    if orange_free:
        return [orange_free]
    else:
        if not free_whites:
            return []
        return [find_nearest_white(robot, free_whites)]
    


def execute_ball_flow(ball, robot_cell, grid):

    ball_cell = (ball["x"], ball["y"])
    pathToBall, pathToSafepoint = rute(grid, robot_cell, ball_cell)
    print_grid_and_route(grid, pathToBall, pathToSafepoint)
    
    return 0.0  


def plan_path(grid, start, goal):
    path = astar(grid, start, goal)
    if not path:
        raise RuntimeError("Ingen sti fundet ")
    return path


# def rute(grid, robot_cell, ball_cell):

#     print("VIRKER 6, rute")
#     # Path fra robot til bold
#     path1 = plan_path(grid, robot_cell, ball_cell)

#     # Find safepoint‐celle ud fra bold‐cellen
#     sp_cell = nearest_safepoint(ball_cell)

#     # Path fra bold til safepoint
#     path2 = plan_path(grid, ball_cell, sp_cell)

#     # (valgfri debug-print)
#     print("robot_cell:", robot_cell, 
#           "ball_cell:", ball_cell, 
#           "sp_cell:", sp_cell)
#     print("plan1:", path1)
#     print("plan2:", path2)

#     return path1, path2


def rute(grid, robot_cell, ball_cell):
    REQUIRED_CELLS = 15  # 15 cm / 1 cm pr. celle

    best_path = None
    best_dir  = None

    for dir in [(1,0),(-1,0),(0,1),(0,-1)]:
        approach = (ball_cell[0] - dir[0]*REQUIRED_CELLS,
                    ball_cell[1] - dir[1]*REQUIRED_CELLS)
        # tjek om approach er gyldig:
        if not (0 <= approach[0] < GRID_WIDTH and 0 <= approach[1] < GRID_HEIGHT): 
            continue
        if grid[approach[1]][approach[0]] == 1:
            continue

        path = astar(grid, robot_cell, approach)
        if not path:
            continue

        # ondt: du kunne tjekke segment‐retningen her, men lad os forudsætte A* følger korteste
        # og at du bare vælger den med mindste total‐længde:
        if best_path is None or len(path) < len(best_path):
            best_path = path
            best_dir  = dir

    if best_path is None:
        print("ADVARSEL: Ingen sti til en 15 cm offset ved bolden")
        return None, None

    # byg extra‐segmentet
    extra = [
      (best_path[-1][0] + best_dir[0]*i,
       best_path[-1][1] + best_dir[1]*i)
      for i in range(1, REQUIRED_CELLS+1)
    ]
    full_path = best_path + extra

    # plan2 som før
    sp_cell = nearest_safepoint(ball_cell)
    path2   = astar(grid, ball_cell, sp_cell)
    if path2 is None:
        print("ADVARSEL: Ingen sti fra bold til safepoint")
        return None, None

    print("Rutens sidste segment er nu", REQUIRED_CELLS, "cm langt før 8 cm-stop.")
    print("plan1:", full_path)
    print("plan2:", path2)
    return full_path, path2

# Liste over dine to safepoints i (col, row)-format


def nearest_safepoint(ball_cell, safepoints=SAFEPOINTS):

    distances = []
    for sp in safepoints:
        dx = sp[0] - ball_cell[0]
        dy = sp[1] - ball_cell[1]
        distances.append((math.hypot(dx, dy), sp))
    _, nearest = min(distances, key=lambda t: t[0])
    return (int(nearest[0]), int(nearest[1]))


def heuristic(a, b):
    # Manhattan‐afstand
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    
    # print("GRID I ASTAR")
    # for y in range(len(grid)-1, -1, -1):        # udskriv fra top til bund
    #     row = grid[y]
    #     line = ''.join('#' if cell else '.' for cell in row)
    #     print(line)

    # Min‐heap: hvert entry er (f_score, x, y)
    open_heap = []
    # G-scores for hver koord
    g_score = { start: 0 }
    # Parent‐pege for path‐rekonstruktion
    came_from = {}
    
    # Hæld start ind i heap med f = h(start)
    heapq.heappush(open_heap, (heuristic(start, goal), start))
    
    while open_heap:
        f, current = heapq.heappop(open_heap)
        if current == goal:
            # Byg path tilbage til start
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            return path[::-1]
        
        x, y = current
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT):
                continue
            if grid[ny][nx] == 1:
                continue
            
            neighbor = (nx, ny)
            tentative_g = g_score[current] + 1
            
            # Hvis vi fandt en bedre g-score for neighbor:
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f_score, neighbor))
    
    # Ingen sti fundet
    return None


def check_last_segment(path):
    """
    Returnerer antallet af celler i det sidste segment af den komprimerede path.
    """
    # compact path til segmenter (dx, dy, count)
    diffs = [(path[i+1][0] - path[i][0], path[i+1][1] - path[i][1])
             for i in range(len(path) - 1)]
    segments = []
    i = 0
    while i < len(diffs):
        dx, dy = diffs[i]
        cnt = 1
        i += 1
        while i < len(diffs) and diffs[i] == (dx, dy):
            cnt += 1
            i += 1
        segments.append((dx, dy, cnt))
    if not segments:
        return 0
    # Antal celler i det sidste segment
    return segments[-1][2]

#TODO: prøv at teste med STOP_DISTANCE_FROM_BALL+7 eller sådan noget
def astar_with_min_last_segment(grid, start, goal, min_seg_cells=STOP_DISTANCE_FROM_BALL+7):
    """
    Finder en sti hvor sidste segment har mindst min_seg_cells celler.
    Ellers prøver den buffermål min_seg_cells væk fra goal i fire retninger.
    """
    # 1) Prøv direkte
    path = astar(grid, start, goal)
    if path and check_last_segment(path) >= min_seg_cells:
        return path

    gx, gy = goal
    # 2) Prøv buffermål
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        bx = gx - dx * min_seg_cells
        by = gy - dy * min_seg_cells
        if not (0 <= bx < GRID_WIDTH and 0 <= by < GRID_HEIGHT):
            continue
        if grid[by][bx] == 1:
            continue
        buf_path = astar(grid, start, (bx, by))
        if buf_path and check_last_segment(buf_path) >= min_seg_cells:
            return buf_path

    # 3) Fald tilbage
    return path
runflow(tasks_with_orange)