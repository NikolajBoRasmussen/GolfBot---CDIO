import math
from .config import GRID_SIZE, ROBOT_START_POS, STOP_DISTANCE_FROM_BALL, START_POS_CM
from .helperfunctions import compress_path
from .navigation import drive_straight, forward_cm, turn
from .pathfinding import astar
from .helperfunctions import cm_to_grid
from .safepoint import nearest_safepoint


def get_positions(ball_coordinates_list):
  
    start_cm = ROBOT_START_POS

    xr, yr = start_cm
    nearest = min(
        ball_coordinates_list,
        key=lambda c: math.hypot(c[0] - xr, c[1] - yr)
    )
    
    start_cell = cm_to_grid(ROBOT_START_POS)
    ball_cell  = cm_to_grid(nearest)
    return start_cell, ball_cell


def plan_path(grid, start, goal):
    path = astar(grid, start, goal)
    if not path:
        raise RuntimeError("Ingen sti fundet ")
    return path


def execute_path(robot, path, gyro, initial_angle=0.0, apply_early_stop=False):
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
        drive_straight(robot, gyro, dist)
        
    return current_angle


def rute(grid, ball_coordinates_list):

    start_cell, ball_cell = get_positions(ball_coordinates_list)

    #-------path1: fra start → nærmeste bold
    path1 = plan_path(grid, start_cell, ball_cell)
    print("plan1", path1)
    #-------path2: fra bold → nærmeste safepoint
    sp_cell = nearest_safepoint(ball_cell)
    print("sp_cell: ", sp_cell)
    print("start_cell: ", start_cell)
    print("ball_cell: ", ball_cell)
    path2 = plan_path(grid, ball_cell, sp_cell)
    print("plan2", path2)

    #-------path3: fra safepoint → start
    path3 = plan_path(grid, sp_cell, start_cell)
    print("plan3", path3)
    return path1, path2, path3
    


    
