#!/usr/bin/env pybricks-micropython
# -*- coding: utf-8 -*-

import time
#from ascii_route_printer import print_full_route

from .ballHandling import captureBall, push_ball_to_goal
from .config import (
    AXLE_TRACK,
)
from .gridmap import create_empty_grid, add_obstacles, inflate_obstacles, add_border_obstacles, print_grid

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
    left  = LargeMotor(OUTPUT_A)
    right = LargeMotor(OUTPUT_B)
    arm   = MediumMotor(OUTPUT_C)
    arm.reset()
    robot = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3EducationSetTire, AXLE_TRACK)
    return robot, arm

def setup_sensors():
    gyro = GyroSensor(INPUT_1)
    gyro.reset()
    time.sleep(1)
    infrared = InfraredSensor(INPUT_3)
    return gyro, infrared

def build_grid():
    grid = create_empty_grid()
    grid = add_obstacles(grid)
    grid = inflate_obstacles(grid)
    grid = add_border_obstacles(grid)
    #print_grid(grid)
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

    print("VIRKER 5, execute_ball_flow")
    ball_cell = (ball["x"], ball["y"])
    pathToBall, pathToSafepoint, pathToStart = rute(grid, robot_cell, ball_cell)

    print("-> Henter", ball["name"], "på", ball_cell)
    current_angle = execute_path(robot, pathToBall, gyro, initial_angle=current_angle)

    caught = captureBall(robot, arm, infrared, gyro)
    current_angle = gyro.angle
    if not caught:

        back_path = list(reversed(pathToBall))
        current_angle = execute_path(robot, back_path, gyro, initial_angle=current_angle)
        face_angle(robot, gyro, target_angle=0.0)
        return 0.0  

    # d) Aflever i safepoint
    current_angle = execute_path(robot, pathToSafepoint, gyro, initial_angle=current_angle)
    push_ball_to_goal(robot, arm, gyro, pathToSafepoint)
    current_angle = gyro.angle

    # e) Tilbage til start
    current_angle = execute_path(robot, pathToStart, gyro, initial_angle=current_angle)
    face_angle(robot, gyro, target_angle=0.0)
    return 0.0  


def runflow(tasks):
    # 1) Hent cross/robot/orange/white

    #global robot, arm, gyro, infrared, grid
    print("VIRKER")
    robot, arm       = setup_motors()
    gyro, infrared   = setup_sensors()
    grid             = build_grid()
    print("VIRKER2")
    _, robot_from_pic, orange, white_list = extract_entities(tasks)

    print("VIRKEr3")
    robot_cell = (robot_from_pic["x"], robot_from_pic["y"])
    # 2) Vælg sekvens af bolde
    ball_sequence = select_ball_sequence(robot_from_pic, orange, white_list)
    print("VIRKER4")
    # 3) Eksekver for hver bold
    current_angle = 0.0
    print("ball_sequence:", ball_sequence)
    for ball in ball_sequence:
        current_angle = execute_ball_flow(
            ball, robot_cell, current_angle, robot, arm, gyro, infrared, grid
        )

    play_happy_sound()


tasks_with_orange = [
    {"name": "cross",  "x": 85,  "y": 60},
    {"name": "robot",  "x": 18,  "y": 16},
    {"name": "orange", "x": 140, "y": 30},
    [
        {"name": "white", "x": 20,  "y": 100},
        {"name": "white", "x": 160, "y": 80},
    ]
]

# if __name__ == "__main__":
#     robot, arm       = setup_motors()
#     gyro, infrared   = setup_sensors()
#     grid             = build_grid()



# balls_cm = [(90.0,10.0), (130.0,80.0), (170.0, 10.0)]

runflow(tasks_with_orange)
