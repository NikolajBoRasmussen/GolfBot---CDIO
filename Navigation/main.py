#!/usr/bin/env pybricks-micropython
# -*- coding: utf-8 -*-

import time

from .helperfunctions import extract_entities, select_ball_sequence
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
    OUTPUT_D,
    MediumMotor,
    OUTPUT_C,
    MoveDifferential,
)
from ev3dev2.wheel import EV3EducationSetTire


def setup_motors():
    left  = LargeMotor(OUTPUT_D)
    right = LargeMotor(OUTPUT_A)
    arm   = MediumMotor(OUTPUT_C)
    arm.reset()
    robot = MoveDifferential(OUTPUT_D, OUTPUT_A, EV3EducationSetTire, AXLE_TRACK)
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
    return grid


# def execute_ball_flow(ball, robot_cell, current_angle, robot, arm, gyro, infrared, grid):


#     ball_cell = (ball["x"], ball["y"])
#     pathToBall, pathToSafepoint = rute(grid, robot_cell, ball_cell)

#     print_grid_and_route(grid, pathToBall, pathToSafepoint)
#     if not pathToBall or not pathToSafepoint:
#         print("Afbrudt: en eller flere ruter er None – ingen eksekvering.")
#         return 0.0  

#     print("-> Henter", ball["name"], "på", ball_cell)
#     current_angle = execute_path(robot, pathToBall, gyro, initial_angle=current_angle, apply_early_stop=True)

#     caught = captureBall(robot, arm, infrared, gyro)
#     current_angle = gyro.angle
#     if not caught:
#         # back_path = list(reversed(pathToBall))
#         # current_angle = execute_path(robot, back_path, gyro, initial_angle=current_angle)
#         face_angle(robot, gyro, target_angle=0.0)
#         return 0.0  

#     # d) Aflever i safepoint
#     current_angle = execute_path(robot, pathToSafepoint, gyro, initial_angle=current_angle)
#     push_ball_to_goal(robot, arm, gyro, pathToSafepoint)
    
#     #bliver ved safepoint, men roter til vinkel 0
#     face_angle(robot, gyro, target_angle=0.0)
    
#     # current_angle = gyro.angle
#     # # e) Tilbage til start
#     # current_angle = execute_path(robot, pathToStart, gyro, initial_angle=current_angle)
#     # face_angle(robot, gyro, target_angle=0.0)
   
#     return 0.0  

def execute_ball_flow(ball, robot_cell, current_angle, robot, arm, gyro, infrared, grid):
    ball_cell = (ball["x"], ball["y"])
    paths = rute(grid, robot_cell, ball_cell)
    if not paths:
        print("Afbrudt: en eller flere ruter er None – ingen eksekvering.")
        return 0.0

    # Håndter både 2-step og 3-step flows
    if len(paths) == 3:
        path_to_safezone, path_to_ball, path_to_safepoint = paths

        # a) Først til intermediate safezone
        current_angle = execute_path(robot, path_to_safezone, gyro, initial_angle=current_angle)

        # b) Dernæst til bolden
        current_angle = execute_path(robot, path_to_ball, gyro, initial_angle=current_angle, apply_early_stop=True)
    else:
        # Standard: direkte til bold
        path_to_ball, path_to_safepoint = paths
        current_angle = execute_path(robot, path_to_ball, gyro, initial_angle=current_angle, apply_early_stop=True)

    # c) Fang bolden
    caught = captureBall(robot, arm, infrared, gyro)
    current_angle = gyro.angle
    
    if not caught:
        face_angle(robot, gyro, target_angle=0.0)
        return 0.0

    # d) Aflever i safepoint
    current_angle = execute_path(robot, path_to_safepoint, gyro, initial_angle=current_angle)
    push_ball_to_goal(robot, arm, gyro, path_to_safepoint)
    face_angle(robot, gyro, target_angle=0.0)

    return 0.0

def runflow(tasks):

    cross, robot_from_pic, orange, white_list = extract_entities(tasks)
    cross_pos = (cross["x"], cross["y"])
    robot_cell = (robot_from_pic["x"], robot_from_pic["y"])

    robot, arm       = setup_motors()
    gyro, infrared   = setup_sensors()
    grid             = build_grid(cross_pos)
    
    ball_sequence = select_ball_sequence(robot_from_pic, orange, white_list, grid)

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

# runflow(tasks_with_orange)
