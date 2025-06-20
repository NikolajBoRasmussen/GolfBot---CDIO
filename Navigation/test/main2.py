#!/usr/bin/env pybricks-micropython
import math
import time
from config import GRID_SIZE, ROBOT_START_POS, START_POS_CM, STOP_DISTANCE_FROM_BALL, WHEEL_DIAMETER, AXLE_TRACK, GRID_WIDTH
from gridmap import create_empty_grid, add_obstacles, inflate_obstacles
from infraredSensor import isBallVeryClose
from pathfinding import astar
from navigation import turn, forward_cm
from helperfunctions import compress_path, goalCellChecked
from gyroSensor import face_angle, face_opposite, turn_and_report
from robotActions import go_back_3cm, go_forward_3cm, play_happy_sound, play_melody, play_text, take_arm_down, take_arm_up    

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B  # Tacho-motorer og portkonstanter :contentReference[oaicite:0]{index=0}
from ev3dev2.wheel import EV3EducationSetTire            # Standard-hjul for Education Set :contentReference[oaicite:1]{index=1}
from ev3dev2.motor import MoveDifferential
from ev3dev2.motor import MediumMotor, OUTPUT_C

#from ultrasonicSensor import isBallClose


# Opsætning af motorer
left  = LargeMotor(OUTPUT_A)
right = LargeMotor(OUTPUT_B)
# Arm motor på port C
arm_motor = MediumMotor(OUTPUT_C)
arm_motor.reset()        

wheel_diameter = WHEEL_DIAMETER
axle_track     = AXLE_TRACK

robot = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3EducationSetTire, axle_track)


# Byg grid og find sti
grid = create_empty_grid()
grid = add_obstacles(grid)
grid = inflate_obstacles(grid, margin=1)

start_cell = (
    int(ROBOT_START_POS[0]),
    int(ROBOT_START_POS[1])
)  
goalCellChecked = goalCellChecked(grid, (11,1))

path = astar(grid, start_cell, goalCellChecked) #returnere liste med de celler robotten må køre i
if not path:
    raise RuntimeError("Ingen sti fundet – tjek forhindringer og margin!")

# Initier navigation
# current_angle track­er, hvilken retning robotten peger (0° = øst).
# prev_cm er den fysiske (cm) position, vi senest befandt os i — her midten af startcellen.

runs = compress_path(path)
current_angle = 0
prev_cm = ((start_cell[0]*GRID_SIZE + GRID_SIZE/2),
           (start_cell[1]*GRID_SIZE + GRID_SIZE/2))


# Kør langs stien
"""
Compute
    tx, ty: centrum af den næste celle i centimeter.

    dx, dy: forskellen fra forrige position (prev_cm).

Drej
    atan2(dy, dx) giver vinklen mod det punkt.

    pivot(...) drejer på stedet uden stop-og-start-hak.

Frem
    Afstanden i cm (dist_cm) omregnes i forward_cm() til mm, køres kontinuerligt, indtil den er nået.

Opdater
    prev_cm sættes til den position, du netop har kørt til, så næste loop-trin beregner forskellen fra dér.
"""

for i, (dx, dy, count) in enumerate(runs):
    target_ang = math.degrees(math.atan2(dy, dx))
    
    print("target_ang - current_angle ", target_ang - current_angle)
    #turn(robot, target_ang - current_angle)
    current_angle = target_ang

    # 2) Kør direkte 'count' celler i træk
    dist_cm = count * GRID_SIZE
    if i == len(runs) - 1:
        dist_cm = max(dist_cm - STOP_DISTANCE_FROM_BALL, 0)

    #forward_cm(robot, dist_cm)
   # turn(robot, 180)
 
   # forward_cm(robot, dist_cm)
    # #take_arm_down(arm_motor)
    # time.sleep(1)
    # pivot(robot, 90)
    # time.sleep(1)
    # take_arm_up(arm_motor)
    # go_back_3cm(robot)
    # go_forward_3cm(robot)

    # Opdater prev_cm (valgfrit cell_to_cm kun til debugging)
    prev_cm = (prev_cm[0] + dx*dist_cm, prev_cm[1] + dy*dist_cm)

 
#take_arm_up(arm_motor)
#turn_and_report(robot, 180)


# if isBallClose():
#     print("🚫 Objekt for tæt på!")
# else:
#     print("✅ Frit foran.")


#infrarød
if isBallVeryClose():
    print("🔴 Bold (eller andet objekt) er meget tæt på!")
else:
    print("🟢 Ingen objekt lige foran.")


play_happy_sound()
#play_melody()
#play_text()
print("Robotten har fuldført ruten.")

