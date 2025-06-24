# -*- coding: utf-8 -*-

from ev3dev2.motor import SpeedPercent
from ev3dev2.sound import Sound
from .navigation import drive_straight, forward_cm


# Lydenhed
sound = Sound()

ARM_TRAVEL_DEGREES = 171
TOLERANCE = 5  # i grader

def take_arm_down(arm_motor, speed_pct: int = 30):
    arm_motor.on_for_degrees(
        SpeedPercent(speed_pct),
        -ARM_TRAVEL_DEGREES,
        brake=True,
        block=True
    )

def take_arm_up(arm_motor, speed_pct: int = 30):

    arm_motor.on_for_degrees(
        SpeedPercent(speed_pct),
        ARM_TRAVEL_DEGREES,
        brake=True,
        block=True
    )



def go_back_fixedcm(robot, gyro, dist):
    #drive_straight(robot, gyro, -10, base_speed_percent= 50)
    forward_cm(robot, -dist)    # kører 3 cm baglæns


# 3) Kør 3 cm frem

def go_forward_fixedcm(robot, gyro, dist):
    drive_straight(robot, gyro, dist, base_speed_percent= 50)


def play_happy_sound():
    sound.beep()


def play_text(text):
    sound.speak(text)


def play_melody():
    notes = [(440, 200), (660, 200), (880, 400)]  # (Hz, ms)
    for freq, dur in notes:
        sound.tone([(freq, dur)])  

