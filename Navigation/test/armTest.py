from ev3dev2.motor import MediumMotor, OUTPUT_C, SpeedPercent
import time


# Fuldt udsving mellem top og bund
ARM_TRAVEL_DEGREES = 171
arm_motor = MediumMotor(OUTPUT_C)



def take_arm_down(speed_pct: int = 50):
    print("DEBUG: take_arm_down() kaldt")
    arm_motor.on_for_degrees(
        SpeedPercent(speed_pct),
        -ARM_TRAVEL_DEGREES,
        brake=True,
        block=True
    )
    print("DEBUG: take_arm_down() færdig")

def take_arm_up(speed_pct: int = 50):
    print("DEBUG: take_arm_up() kaldt")
    arm_motor.on_for_degrees(
        SpeedPercent(speed_pct),
        ARM_TRAVEL_DEGREES,
        brake=True,
        block=True
    )
    print("DEBUG: take_arm_up() færdig")

