#!/usr/bin/env pybricks-micropython
# -*- coding: utf-8 -*-

import time
#from ascii_route_printer import print_full_route

from .ballHandling import captureBall, push_ball_to_goal
from .config import (
    AXLE_TRACK,
    GRID_HEIGHT,
    GRID_WIDTH,
)
from .gridmap import create_empty_grid, add_obstacles, add_border_obstacles, print_grid

from .gyroSensor import face_angle
from .rute import execute_path, rute
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.sensor import INPUT_3, INPUT_1

from ev3dev2.sensor.lego import GyroSensor
from .robotActions import play_happy_sound
from ev3dev2.motor import (
    LargeMotor,
    OUTPUT_A,
    OUTPUT_B,
    MediumMotor,
    OUTPUT_C,
    MoveDifferential,
)
from ev3dev2.wheel import EV3EducationSetTire


def setup_motors():
    left  = LargeMotor(OUTPUT_B)
    right = LargeMotor(OUTPUT_A)
    arm   = MediumMotor(OUTPUT_C)
    arm.reset()
    robot = MoveDifferential(OUTPUT_B, OUTPUT_A, EV3EducationSetTire, AXLE_TRACK)
    return robot, arm

def setup_sensors():
    gyro = GyroSensor(INPUT_1)
    gyro.reset()
    time.sleep(1)
    infrared = InfraredSensor(INPUT_3)
    return gyro, infrared

def build_grid(cross_pos):
    grid = create_empty_grid()
    grid = add_obstacles(grid, cross_pos)
    grid = add_border_obstacles(grid)
    
    #print_grid(grid)
    print("Check (69,46):", grid[46][69])
    print("Check (84,61):", grid[61][84])
    print("Check (99,76):", grid[76][99])
    # Udenfor boks bør printe 0:
    print("Check (68,46):", grid[46][68])
    print("Check (99,77):", grid[77][99])
    return grid




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


def execute_ball_flow(ball, robot_cell, current_angle, robot, arm, gyro, infrared, grid):


    ball_cell = (ball["x"], ball["y"])
    pathToBall, pathToSafepoint = rute(grid, robot_cell, ball_cell)

    print_grid_and_route(grid, pathToBall, pathToSafepoint)
    # if not pathToBall or not pathToSafepoint or not pathToStart:
    #     print("Afbrudt: en eller flere ruter er None – ingen eksekvering.")
    #     return 0.0  

    print("-> Henter", ball["name"], "på", ball_cell)
    current_angle = execute_path(robot, pathToBall, gyro, initial_angle=current_angle, apply_early_stop=True)

    caught = captureBall(robot, arm, infrared, gyro)
    current_angle = gyro.angle
    if not caught:

        # back_path = list(reversed(pathToBall))
        # current_angle = execute_path(robot, back_path, gyro, initial_angle=current_angle)
        face_angle(robot, gyro, target_angle=0.0)
        return 0.0  

    # d) Aflever i safepoint
    current_angle = execute_path(robot, pathToSafepoint, gyro, initial_angle=current_angle)
    push_ball_to_goal(robot, arm, gyro, pathToSafepoint)
    
    #bliver ved safepoint, men roter til vinkel 0
    face_angle(robot, gyro, target_angle=0.0)
    
    # current_angle = gyro.angle
    # # e) Tilbage til start
    # current_angle = execute_path(robot, pathToStart, gyro, initial_angle=current_angle)
    # face_angle(robot, gyro, target_angle=0.0)
   
    return 0.0  


def runflow(tasks):

    cross, robot_from_pic, orange, white_list = extract_entities(tasks)
    cross_pos = (cross["x"], cross["y"])
    robot_cell = (robot_from_pic["x"], robot_from_pic["y"])

    print("VIRKER")
    robot, arm       = setup_motors()
    gyro, infrared   = setup_sensors()
    grid             = build_grid(cross_pos)
    
    ball_sequence = select_ball_sequence(robot_from_pic, orange, white_list)

    # 3) Eksekver for hver bold
    current_angle = 0.0
    
    print("ball_sequence:", ball_sequence)
    for ball in ball_sequence:
        current_angle = execute_ball_flow(
            ball, robot_cell, current_angle, robot, arm, gyro, infrared, grid
        )

    play_happy_sound()



# tasks_with_orange = [
#     {"name": "cross",  "x": 85,  "y": 60},
#     {"name": "robot",  "x": 20,  "y": 20},
#     {"name": "orange", "x": 140, "y": 30},
#     [
#         {"name": "white", "x": 20,  "y": 100},
#         {"name": "white", "x": 160, "y": 80},
#     ]
# ]

# # if __name__ == "__main__":
# #     robot, arm       = setup_motors()
# #     gyro, infrared   = setup_sensors()
# #     grid             = build_grid()



# # # balls_cm = [(90.0,10.0), (130.0,80.0), (170.0, 10.0)]

# runflow(tasks_with_orange)


def print_grid_and_route(grid, path1, path2):

    # Byg marker-tabel
    marker = [[None]*GRID_WIDTH for _ in range(GRID_HEIGHT)]
    for idx, path in enumerate((path1, path2), start=1):
        if not path:
            continue
        for x,y in path:
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                marker[y][x] = str(idx)

    # Print øverst til nederst
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
