import math
from .config import GRID_SIZE, STOP_DISTANCE_FROM_BALL
from .helperfunctions import compress_path
from .navigation import drive_straight, forward_cm, turn
from .pathfinding import astar
from .helperfunctions import cm_to_grid
from .safepoint import nearest_safepoint



def plan_path(grid, start, goal):
    path = astar(grid, start, goal)
    if not path:
        raise RuntimeError("Ingen sti fundet ")
    return path


def execute_path(robot, path, gyro, initial_angle=0.0, apply_early_stop=True):
    current_angle = initial_angle

    segments = compress_path(path)
    for i, (dx, dy, count) in enumerate(segments):
        target_angle = math.degrees(math.atan2(dy, dx))
        delta = (target_angle - current_angle + 180) % 360 - 180
       
        turn(robot, delta, gyro)
        current_angle = target_angle

        dist = count * GRID_SIZE
        if apply_early_stop and i == len(segments) - 1:
            dist = max(dist - STOP_DISTANCE_FROM_BALL, 0)
            print("DIST: ", dist)
        drive_straight(robot, gyro, dist)
        
    return current_angle


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

    


    
