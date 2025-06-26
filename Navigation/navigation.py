# navigation.py
# -*- coding: utf-8 -*-

import time
from ev3dev2.motor import SpeedDPS, SpeedRPM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.motor import SpeedPercent
from ev3dev2.motor import SpeedDPS
from .gyroSensor import face_angle



def turn(robot, angle: float, gyro,
         coarse_speed_dps: int = 50,
         tolerance: float = 0.1,
         kp: float = 0.7):


    start = gyro.angle
    target = start + angle

    robot.turn_degrees(
        SpeedDPS(coarse_speed_dps),
        angle,
        brake=True,  
        block=True
    )

    face_angle(robot, gyro,
               target_angle=target,
               tolerance=tolerance,
               kp=kp)

####----------chat------------
       # 2) Finjustering i loop
    while True:
        # Beregn fejl og udfør proportional fin-vending
        current = gyro.angle
        error   = target - current

        # Hvis inden for tolerance, stop motorer og bryd loop
        if abs(error) <= tolerance:
            robot.off(brake=True)
            break

        # P-kontroller: hastighed proportional med fejl
        speed = kp * error
        speed = max(min(speed, 100), -100)

        # Kør motorerne mod hinanden for at dreje ind
        robot.on(SpeedPercent(speed), SpeedPercent(-speed))
        time.sleep(0.01)

        # (valgfrit) print status for debug
        print("🔄 Korrektion: fejl = {:.2f}° – gyro = {:.2f}°".format(error, current))

####----------chat------------

    end = gyro.angle
    actual = end - start
    print("⚙️  Målt rotation: {:.1f}° (mål: {:.1f}°) – Total gyro‐vinkel nu: {:.1f}°"
          .format(actual, angle, end))
    


def forward_cm(robot, dist_cm, speed=200, brake=True):
   
    dist_mm = int(dist_cm * 10)
    wheel   = EV3EducationSetTire()
    rpm     = speed / wheel.circumference_mm * 60
    robot.on_for_distance(SpeedRPM(rpm),
                          dist_mm,
                          brake=brake,
                          block=True)
    

def raise_arm(arm, angle_deg: int = 90, speed_rpm: int = 50): 
    arm.on_for_degrees(SpeedRPM(speed_rpm), angle_deg, brake=True, block=True)

def lower_arm(arm, angle_deg: int = 90, speed_rpm: int = 50):
       arm.on_for_degrees(SpeedRPM(speed_rpm), -angle_deg, brake=True, block=True)
    
    
wheel = EV3EducationSetTire()
WHEEL_CIRCUMFERENCE_MM = wheel.circumference_mm

def drive_straight(robot, gyro, dist_cm,
                   base_speed_percent: int = 40,
                   kp: float = 1.2):

    # Omregn til mm
    dist_mm = dist_cm * 10
    # Hvor mange grader motorerne skal dreje samlet set?
    rotations_needed = dist_mm / WHEEL_CIRCUMFERENCE_MM 
    degrees_needed   = rotations_needed * 360            

    # Reset tacho‐tællere
    robot.left_motor.reset()
    robot.right_motor.reset()
    time.sleep(0.1)

    # Gem start‐heading
    target_heading = gyro.angle

    # Kør indtil gennemsnitlig tacho ≥ mål
    while True:
        left_deg  = abs(robot.left_motor.position)  
        right_deg = abs(robot.right_motor.position)
        avg_deg   = (left_deg + right_deg) / 2

        if avg_deg >= degrees_needed:
            break

        # Regn gyro‐fejl og korrektion
        error      = target_heading - gyro.angle
        correction = kp * error

        # Beregn motorhastigheder
        left_speed  = base_speed_percent + correction
        right_speed = base_speed_percent - correction

        # Clamp til valid range
        left_speed  = max(min(left_speed,  100), -100)
        right_speed = max(min(right_speed, 100), -100)

        # Send kommando til motorerne
        robot.on(SpeedPercent(left_speed),
                 SpeedPercent(right_speed))

        time.sleep(0.01)

    # Stop og hold position
    robot.off(brake=True)