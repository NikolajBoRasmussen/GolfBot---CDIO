#!/usr/bin/env pybricks-micropython
# -*- coding: utf-8 -*-

import math
import time
from ascii_route_printer import print_full_route

from ballHandling import captureBall, push_ball_to_goal
from config import (
    GRID_SIZE,
    ROBOT_START_POS,
    START_POS_CM,
    STOP_DISTANCE_FROM_BALL,
    AXLE_TRACK,
)
from gridmap import create_empty_grid, add_obstacles, inflate_obstacles
from gyroSensor import face_angle
from rute import execute_path, rute
from safepoint import SAFEPOINTS, nearest_safepoint
from pathfinding import astar
from helperfunctions import compress_path
from navigation import lower_arm, turn, forward_cm

from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.sensor import INPUT_3, INPUT_1
from infraredSensor import isBallVeryClose

from ev3dev2.sensor.lego import GyroSensor
from robotActions import take_arm_down, take_arm_up, play_happy_sound
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
    drive = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3EducationSetTire, AXLE_TRACK)
    return drive, arm

def setup_Sensors():
    gyro = GyroSensor(INPUT_1)
    gyro.reset()
    time.sleep(1)
    infrared = InfraredSensor(INPUT_3)
    return gyro, infrared

def build_grid(margin=1):
    grid = create_empty_grid()
    grid = add_obstacles(grid)
    grid = inflate_obstacles(grid, margin=margin)
    return grid

def runflow(ball_coordinates_list):
    robot, arm   = setup_motors()
    grid         = build_grid()
    gyro, infrared = setup_Sensors()

    # Vi antager, at robotten altid starter mod nord (0)
    current_angle = 0.0

    for ball_cm in ball_coordinates_list:
        # 1) Planer stier for denne bold
        pathToBall, pathToSafepoint, pathToStart = rute(grid, [ball_cm])
        print_full_route(grid, [pathToBall, pathToSafepoint, pathToStart])

        # 2) Koer til bold
        print("-> Henter bold paa", ball_cm)
        current_angle = execute_path(robot, pathToBall, gyro, initial_angle=current_angle)

        # 3) Fang bolden
        caught = captureBall(robot, arm, infrared, gyro)
        current_angle = gyro.angle
        if not caught:
            back_path = list(reversed(pathToBall))
            current_angle = execute_path(robot, back_path, gyro, initial_angle=current_angle)
            face_angle(robot, gyro, target_angle=0.0)
            # Nulstil vinklen efter vendingen til nord
            current_angle = 0.0
            continue

        # 4) Koer til safepoint og aflever
        current_angle = execute_path(robot, pathToSafepoint, gyro, initial_angle=current_angle)
        push_ball_to_goal(robot, arm, gyro, pathToSafepoint)
        current_angle = gyro.angle

        # 5) Retur til start
        current_angle = execute_path(robot, pathToStart, gyro, initial_angle=current_angle)
        face_angle(robot, gyro, target_angle=0.0)
        # Her nulstiller vi endelig vinklen til 0 grader, saa naeste bold altid starter mod nord
        current_angle = 0.0

    # Naar alle bolde er faerdige, spil glad lyd
    play_happy_sound()


# Test: to identiske boldpositioner
balls_cm = [
    (90.0, 10.0),
    (130.0,80.0),
]

runflow(balls_cm)
