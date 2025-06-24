#rute.py 
import math
from .config import GRID_HEIGHT, GRID_SIZE, GRID_WIDTH, STOP_DISTANCE_FROM_BALL
from .helperfunctions import compress_path, is_in_mid_region, nearest_safezone
from .navigation import drive_straight, forward_cm, turn
from .pathfinding import astar
from .safepoint import nearest_safepoint



def plan_path(grid, start, goal):
    path = astar(grid, start, goal)
    return path  # enten en liste eller None


def execute_path(robot, path, gyro, initial_angle=0.0, apply_early_stop=False):
    current_angle = initial_angle
    
    earlyStopPossible = False

    segments = compress_path(path)
    for i, (dx, dy, count) in enumerate(segments):
        target_angle = math.degrees(math.atan2(dy, dx))
        delta = (target_angle - current_angle + 180) % 360 - 180
       
        turn(robot, delta, gyro)
        current_angle = target_angle

        dist = count * GRID_SIZE
        if apply_early_stop and i == len(segments) - 1:
            #dist = max(dist - STOP_DISTANCE_FROM_BALL, 0)
            if dist > STOP_DISTANCE_FROM_BALL:
                dist = dist - STOP_DISTANCE_FROM_BALL
                earlyStopPossible = True
        drive_straight(robot, gyro, dist)
        
    return current_angle, earlyStopPossible

def rute(grid, robot_cell, ball_cell):

    # 1) Hvis bolden ligger i mid-region -> ekstra stop
    if is_in_mid_region(ball_cell):
        # 1a) Robot → nærmeste safezone
        safezone = nearest_safezone(ball_cell)
        path1 = plan_path(grid, robot_cell, safezone)
        if path1 is None:
            print("ADVARSEL: Ingen sti fra", robot_cell, "til", safezone)
            return None

        # 1b) Safezone → bold
        path2 = plan_path(grid, safezone, ball_cell)
        if path2 is None:
            print("ADVARSEL: Ingen sti fra", safezone, "til", ball_cell)
            return None

        # 1c) Bold → endeligt safepoint
        sp_cell = nearest_safepoint(ball_cell)
        path3 = plan_path(grid, ball_cell, sp_cell)
        if path3 is None:
            print("ADVARSEL: Ingen sti fra", ball_cell, "til", sp_cell)
            return None

        print("Robot:", robot_cell, "→ Interm:", safezone, "→ Bold:", ball_cell, "→ Safepoint:", sp_cell)
        print("plan1:", path1)
        print("plan2:", path2)
        print("plan3:", path3)
        return path1, path2, path3

    # 2) Almindelig case: Robot → Bold → Safepoint
    path1 = plan_path(grid, robot_cell, ball_cell)
    if path1 is None:
        print("ADVARSEL: Ingen sti fra", robot_cell, "til", ball_cell)
        return None

    sp_cell = nearest_safepoint(ball_cell)
    path2 = plan_path(grid, ball_cell, sp_cell)
    if path2 is None:
        print("ADVARSEL: Ingen sti fra", ball_cell, "til", sp_cell)
        return None

    print("Robot:", robot_cell, "→ Bold:", ball_cell, "→ Safepoint:", sp_cell)
    print("plan1:", path1)
    print("plan2:", path2)
    return path1, path2