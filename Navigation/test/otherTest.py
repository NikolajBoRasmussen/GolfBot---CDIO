
import heapq
import math
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ..gridmap import add_border_obstacles, add_obstacles, create_empty_grid, print_grid

from ..config import GRID_HEIGHT, GRID_WIDTH, SAFEPOINTS

def build_grid(cross_pos):
    grid = create_empty_grid()
    grid = add_obstacles(grid, cross_pos)
    grid = add_border_obstacles(grid)
    print_grid(grid)
    

    print("Check (69,46):", grid[46][69])
    print("Check (84,61):", grid[61][84])
    print("Check (99,76):", grid[76][99])

    print("Check (68,46):", grid[46][68])
    print("Check (99,76):", grid[77][99])
    return grid



def runflow(tasks):

    cross, robot_from_pic, orange, white_list = extract_entities(tasks)

    robot_cell = (robot_from_pic["x"], robot_from_pic["y"])

    grid= build_grid((84,61))
    
    ball_sequence = select_ball_sequence(robot_from_pic, orange, white_list)

    # 3) Eksekver for hver bold
    current_angle = 0.0
    
    print("ball_sequence:", ball_sequence)
    for ball in ball_sequence:
        current_angle = execute_ball_flow(
            ball, robot_cell, grid
        )




tasks_with_orange = [
    {"name": "cross",  "x": 85,  "y": 60},
    {"name": "robot",  "x": 20,  "y": 20},
    {"name": "orange", "x": 88, "y": 60},
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

def select_ball_sequence(robot, orange, white_list):

    if orange is not None:
        return [orange]
    else:
        return [find_nearest_white(robot, white_list)]


def execute_ball_flow(ball, robot_cell, grid):

    print("VIRKER 5, execute_ball_flow")
    ball_cell = (ball["x"], ball["y"])
    pathToBall, pathToSafepoint, pathToStart = rute(grid, robot_cell, ball_cell)
    
    return 0.0  

def plan_path(grid, start, goal):
    path = astar(grid, start, goal)
    if not path:
        raise RuntimeError("Ingen sti fundet ")
    return path


def rute(grid, robot_cell, ball_cell):

    print("VIRKER 6, rute")
    # Path fra robot til bold
    path1 = plan_path(grid, robot_cell, ball_cell)

    # Find safepoint‐celle ud fra bold‐cellen
    sp_cell = nearest_safepoint(ball_cell)

    # Path fra bold til safepoint
    path2 = plan_path(grid, ball_cell, sp_cell)

    # Path fra safepoint tilbage til robot‐start
    path3 = plan_path(grid, sp_cell, robot_cell)

    # (valgfri debug-print)
    print("robot_cell:", robot_cell, 
          "ball_cell:", ball_cell, 
          "sp_cell:", sp_cell)
    print("plan1:", path1)
    print("plan2:", path2)
    print("plan3:", path3)

    return path1, path2, path3





# Liste over dine to safepoints i (col, row)-format


def nearest_safepoint(ball_cell, safepoints=SAFEPOINTS):
    """
    Returnerer den (col, row) fra safepoints-listen,
    der er tættest på ball_cell.
    """
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

runflow(tasks_with_orange)