# -*- coding: utf-8 -*-

import time
from .config import ANGLE_TOLERANCE, DRIVE_BACK_FROM_BALL, DRIVE_TO_BALL, SAFEPOINT_BIG, SAFEPOINT_SMALL, STOP_DISTANCE_FROM_BALL
from .gyroSensor import face_angle, face_opposite
from .infraredSensor import isBallVeryClose
from .navigation import drive_straight, lower_arm, raise_arm, turn
from .robotActions import go_back_fixedcm, go_forward_fixedcm, play_happy_sound, play_text, take_arm_down, take_arm_up

def captureBall(robot, arm_motor, infrared, gyro):

    time.sleep(2)
    if isBallVeryClose(infrared):
       take_arm_down(arm_motor)
       time.sleep(0.5)
       go_forward_fixedcm(robot, gyro, STOP_DISTANCE_FROM_BALL)
       return True

    applied_angle = 0
    for angle in (ANGLE_TOLERANCE, -2*ANGLE_TOLERANCE, ANGLE_TOLERANCE):
        turn(robot, angle, gyro)        # relativ drejning
        applied_angle += angle          # akkumuler
        time.sleep(1)
        if isBallVeryClose(infrared):
            # 3) Bold fundet! Vend tilbage til start-retning
            turn(robot, -applied_angle, gyro)
            play_text("Yes")
            take_arm_down(arm_motor)
            go_forward_fixedcm(robot, gyro, STOP_DISTANCE_FROM_BALL)
            return True

    turn(robot, -applied_angle, gyro)
    go_forward_fixedcm(robot, gyro, STOP_DISTANCE_FROM_BALL)
    # play_text("No ball")
    return False



def push_ball_to_goal(robot, arm_motor, gyro, path_to_safepoint,tolerance: float = 1.0, kp: float = 0.8):
    # Hent det sidste safepoint
    target_sp = path_to_safepoint[-1]
    
    # # # Drej til korrekt heading
    if target_sp == SAFEPOINT_BIG:
        # Vend 180 grader væk fra start
        face_opposite(robot, gyro)
    else:
        face_angle(robot, gyro, target_angle=0.0)
     
    time.sleep(1)
    take_arm_up(arm_motor)
    time.sleep(0.5)

    go_back_fixedcm(robot, gyro, DRIVE_BACK_FROM_BALL)
    go_forward_fixedcm(robot, gyro, DRIVE_TO_BALL)
    time.sleep(1)
    go_back_fixedcm(robot, gyro, DRIVE_TO_BALL-DRIVE_BACK_FROM_BALL)
    
    return True





