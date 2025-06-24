#!/usr/bin/env pybricks-micropython
# -*- coding: utf-8 -*-

import time

from .helperfunctions import extract_entities, get_quadrant, get_stop_distance_from_ball, select_ball_sequence
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
    left  = LargeMotor(OUTPUT_A)
    right = LargeMotor(OUTPUT_D)
    arm   = MediumMotor(OUTPUT_C)
    arm.reset()
    robot = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, AXLE_TRACK)
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


def execute_ball_flow(ball, robot_cell, current_angle, robot, arm, gyro, infrared, grid):
    ball_cell = (ball["x"], ball["y"])
    paths = rute(grid, robot_cell, ball_cell)
    if not paths:
        print("Afbrudt: en eller flere ruter er None – ingen eksekvering.")
        return 0.0
    
    ball_quad = get_stop_distance_from_ball(ball_cell)
    

    # Håndter både 2-step og 3-step flows
    if len(paths) == 3:
        path_to_safezone, path_to_ball, path_to_safepoint = paths

        # a) Først til intermediate safezone
        current_angle, _ = execute_path(robot, path_to_safezone, gyro, initial_angle=current_angle)

        # b) Dernæst til bolden
        current_angle, earlyStopPossible = execute_path(robot, path_to_ball, gyro, initial_angle=current_angle, apply_early_stop=True)
    else:
        # Standard: direkte til bold
        path_to_ball, path_to_safepoint = paths
        current_angle, earlyStopPossible = execute_path(robot, path_to_ball, gyro, initial_angle=current_angle, apply_early_stop=True)

    # c) Fang bolden
    caught = captureBall(robot, arm, infrared, gyro, earlyStopPossible)
    current_angle = gyro.angle
    
    if not caught:
        face_angle(robot, gyro, target_angle=0.0)
        return 0.0

    # d) Aflever i safepoint
    current_angle, _ = execute_path(robot, path_to_safepoint, gyro, initial_angle=current_angle)
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
