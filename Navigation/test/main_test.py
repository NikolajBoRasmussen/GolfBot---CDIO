# # main_test.py

import math
import time
from config import ROBOT_START_POS
from config import AXLE_TRACK, GRID_SIZE, START_POS_CM
from gridmap import create_empty_grid, add_obstacles, inflate_obstacles
from Navigation.test.perception import closest_ball

from safepoint import SAFEPOINTS, nearest_safepoint
from pathfinding import astar
from helperfunctions import compress_path, cm_to_grid
# ← Tilføj 'robot' her:
from navigation import forward_cm, raise_arm, lower_arm, turn
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, MoveDifferential
# --- Nyt: opret EV3‐robotten her ---
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire

# Opret robot‐instans til navigation
robot = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3EducationSetTire, AXLE_TRACK)

# --- Byg gridet med inflation af obstacles ---
grid = inflate_obstacles(add_obstacles(create_empty_grid()))


# --- 2) Perception ---
robot_cm = START_POS_CM
balls_cm = [ (50.0,20.0), (150.0,90.0), (130.0,80.0), (200.0,10.0) ]
idx, ball_cm, dist_cm = closest_ball(robot_cm, balls_cm)
start_cell = cm_to_grid(robot_cm)
ball_cell  = cm_to_grid(ball_cm)

# --- 3) Planlæg sti til bold ---
path1 = astar(grid, start_cell, ball_cell)
if not path1:
    raise RuntimeError("Ingen sti til bold fundet")

# --- 4) Kør sti til bold med debug-prints ---
print("=== Kør sti til bold ===")
raise_arm(180, 30)

current_angle = 0.0
print("DEBUG: Starter med current_angle = 0.0° (øst)")

for dx, dy, count in compress_path(path1):
    # Absolut ønsket heading:
    target_angle = math.degrees(math.atan2(dy, dx))
    # Relativ drejning:
    delta = target_angle - current_angle
    # Normaliser til interval [-180, +180]
    delta = (delta + 180) % 360 - 180

    # Debug-udskrift:
    print("DEBUG: dx={0}, dy={1} → target={2:.1f}°, current={3:.1f}°, delta={4:.1f}°".format(
        dx, dy, target_angle, current_angle, delta
    ))

    # Udfør drejning + kørsel
    turn(robot, delta)
    current_angle = target_angle

    dist = count * GRID_SIZE
    forward_cm(robot, dist)
    print("DEBUG: Kørte {0} celler → {1:.1f} cm".format(count, dist))

lower_arm(180, 30)

# --- 5) Planlæg sti til safepoint ---
sp    = nearest_safepoint(ball_cell, SAFEPOINTS)
path2 = astar(grid, ball_cell, sp)
if not path2:
    raise RuntimeError("Ingen sti til safepoint fundet")

# --- 6) Kør sti til safepoint med debug-prints ---
print("=== Kør sti til safepoint ===")
# current_angle er stadig vinklen fra afslutningen af bold-loopen

for dx, dy, count in compress_path(path2):
    target_angle = math.degrees(math.atan2(dy, dx))
    delta = target_angle - current_angle
    delta = (delta + 180) % 360 - 180

    print("DEBUG: dx={0}, dy={1} → target={2:.1f}°, current={3:.1f}°, delta={4:.1f}°".format(
        dx, dy, target_angle, current_angle, delta
    ))

    turn(robot, delta)
    current_angle = target_angle

    dist = count * GRID_SIZE
    forward_cm(robot, dist)
    print("DEBUG: Kørte {0} celler → {1:.1f} cm".format(count, dist))

print("=== Flow complete ===")