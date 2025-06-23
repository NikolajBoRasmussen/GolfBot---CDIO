#rute.py 
import math
from .config import GRID_HEIGHT, GRID_SIZE, GRID_WIDTH, STOP_DISTANCE_FROM_BALL
from .helperfunctions import compress_path
from .navigation import drive_straight, forward_cm, turn
from .pathfinding import astar
from .helperfunctions import cm_to_grid
from .safepoint import nearest_safepoint



def plan_path(grid, start, goal):
    path = astar(grid, start, goal)
    return path  # enten en liste eller None


def execute_path(robot, path, gyro, initial_angle=0.0, apply_early_stop=False):
    current_angle = initial_angle

    segments = compress_path(path)
    for i, (dx, dy, count) in enumerate(segments):
        target_angle = math.degrees(math.atan2(dy, dx))
        delta = (target_angle - current_angle + 180) % 360 - 180
       
        turn(robot, delta, gyro)
        current_angle = target_angle

        dist = count * GRID_SIZE
        print("dist før: ", dist)
        if apply_early_stop and i == len(segments) - 1:
            dist = max(dist - STOP_DISTANCE_FROM_BALL, 0)
            print("DIST: ", dist)
        drive_straight(robot, gyro, dist)
        
    return current_angle

# def execute_path(robot, path, gyro, initial_angle=0.0, apply_early_stop=False):
#     current_angle = initial_angle
#     segments = compress_path(path)
#     last_idx = len(segments) - 1

#     for i, (dx, dy, count) in enumerate(segments):
#         full_dist = count * GRID_SIZE

#         # Sidste segment med early-stop?
#         if apply_early_stop and i == last_idx:
#             drive_dist = full_dist - STOP_DISTANCE_FROM_BALL
#         else:
#             drive_dist = full_dist

#         # 1) Beregn og udfør altid rotation
#         target_angle = math.degrees(math.atan2(dy, dx))
#         delta = (target_angle - current_angle + 180) % 360 - 180
#         turn(robot, delta, gyro)
#         current_angle = target_angle

#         # 2) Hvis der er plads, kør – ellers spring kørsel over
#         if drive_dist > 0:
#             drive_straight(robot, gyro, drive_dist)
#         else:
#             # Sidste segment var for kort; vi har nu
#             # rotateret korrekt ind mod bolden, men kører ikke
#             break

#     return current_angle


def rute(grid, robot_cell, ball_cell):
    # 1) Fra robot til bold
    path1 = plan_path(grid, robot_cell, ball_cell)
    if path1 is None:
        print("ADVARSEL: Ingen sti fra", robot_cell, "til", ball_cell)
        return None, None, None

    # 2) Fra bold til safepoint
    sp_cell = nearest_safepoint(ball_cell)
    path2 = plan_path(grid, ball_cell, sp_cell)
    if path2 is None:
        print("ADVARSEL: Ingen sti fra", ball_cell, "til", sp_cell)
        return None, None, None

    # # 3) Fra safepoint tilbage til robot-start
    # path3 = plan_path(grid, sp_cell, robot_cell)
    # if path3 is None:
    #     print("ADVARSEL: Ingen sti fra", sp_cell, "til", robot_cell)
    #     return None, None, None

    # Debug-print af alle tre
    print("robot_cell:", robot_cell, "ball_cell:", ball_cell, "sp_cell:", sp_cell)
    print("plan1:", path1)
    print("plan2:", path2)
    #print("plan3:", path3)

    return path1, path2


# def rute(grid, robot_cell, ball_cell):
#     REQUIRED_CELLS = 20

#     best_path = None
#     best_dir  = None

#     for dir in [(1,0),(-1,0),(0,1),(0,-1)]:
#         approach = (ball_cell[0] - dir[0]*REQUIRED_CELLS,
#                     ball_cell[1] - dir[1]*REQUIRED_CELLS)
#         # tjek om approach er gyldig:
#         if not (0 <= approach[0] < GRID_WIDTH and 0 <= approach[1] < GRID_HEIGHT): 
#             continue
#         if grid[approach[1]][approach[0]] == 1:
#             continue

#         path = astar(grid, robot_cell, approach)
#         if not path:
#             continue

#         if best_path is None or len(path) < len(best_path):
#             best_path = path
#             best_dir  = dir

#     if best_path is None:
#         print("ADVARSEL: Ingen sti til en 15 cm offset ved bolden")
#         return None, None

#     # byg extra‐segmentet
#     extra = [
#       (best_path[-1][0] + best_dir[0]*i,
#        best_path[-1][1] + best_dir[1]*i)
#       for i in range(1, REQUIRED_CELLS+1)
#     ]
#     full_path = best_path + extra

#     # plan2 som før
#     sp_cell = nearest_safepoint(ball_cell)
#     path2   = astar(grid, ball_cell, sp_cell)
#     if path2 is None:
#         print("ADVARSEL: Ingen sti fra bold til safepoint")
#         return None, None

#     print("Rutens sidste segment er nu", REQUIRED_CELLS, "cm langt før 8 cm-stop.")
#     print("plan1:", full_path)
#     print("plan2:", path2)
#     return full_path, path2

    
