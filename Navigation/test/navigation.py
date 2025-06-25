import math
import time

from config import ROBOT_START_POS, AXLE_TRACK, GRID_SIZE, START_POS_CM
from gridmap import create_empty_grid, add_obstacles, inflate_obstacles
from Navigation.test.perception import closest_ball
from safepoint import SAFEPOINTS, nearest_safepoint
from pathfinding import astar
from helperfunctions import compress_path, cm_to_grid
from navigation import forward_cm, raise_arm, lower_arm, turn
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire


def setup_robot():
    """Initialize and return the EV3 robot instance."""
    return MoveDifferential(OUTPUT_A, OUTPUT_B, EV3EducationSetTire, AXLE_TRACK)


def build_grid():
    """Create and return a grid map with inflated obstacles."""
    grid = create_empty_grid()
    grid = add_obstacles(grid)
    grid = inflate_obstacles(grid)
    return grid


def get_positions(robot_cm, balls_cm):
    """
    Determine the closest ball to the robot and convert positions to grid cells.

    Returns:
        start_cell: tuple[int, int]
        ball_cell: tuple[int, int]
        robot_cell: tuple[int, int]
    """

    _, ball_cm, _ = closest_ball(robot_cm, balls_cm)
    start_cell = cm_to_grid(robot_cm)
    ball_cell = cm_to_grid(ball_cm)
    return start_cell, ball_cell


def plan_path(grid, start, goal):
    """Plan a path using A* and raise an error if no path is found."""
    path = astar(grid, start, goal)
    if not path:
        raise RuntimeError(f"Ingen sti fundet fra {start} til {goal}")
    return path


def execute_path(robot, path, initial_angle=0.0, arm_action=None):
    """
    Execute a path: optionally raise/lower arm, then navigate with debug prints.

    Args:
        robot: The robot instance for navigation.
        path: List of cells from astar.
        initial_angle: Starting heading in degrees (0° = east).
        arm_action: 'raise' or 'lower' or None.

    Returns:
        current_angle: The robot's ending heading in degrees.
    """
    if arm_action == 'raise':
        raise_arm(180, 30)
    elif arm_action == 'lower':
        lower_arm(180, 30)

    print(f"=== Executing path: arm_action={arm_action}, starting angle={initial_angle:.1f}° ===")
    current_angle = initial_angle

    for dx, dy, count in compress_path(path):
        target_angle = math.degrees(math.atan2(dy, dx))
        delta = (target_angle - current_angle + 180) % 360 - 180

        print(
            f"DEBUG: dx={dx}, dy={dy} → target={target_angle:.1f}°, "
            f"current={current_angle:.1f}°, delta={delta:.1f}°"
        )

        turn(robot, delta)
        current_angle = target_angle

        distance = count * GRID_SIZE
        forward_cm(robot, distance)
        print(f"DEBUG: Moved {count} cells → {distance:.1f} cm")

    if arm_action == 'lower':
        lower_arm(180, 30)
    elif arm_action == 'raise':
        raise_arm(180, 30)

    return current_angle


def main():
    # --- Initialization ---
    robot = setup_robot()
    grid = build_grid()

    # --- Perception ---
    robot_cm = START_POS_CM
    balls_cm = [(50.0,20.0), (150.0,90.0), (130.0,80.0), (200.0,10.0)]
    start_cell, ball_cell = get_positions(robot_cm, balls_cm)

    # --- Path 1: Start → Ball ---
    path1 = plan_path(grid, start_cell, ball_cell)
    angle_after_path1 = execute_path(robot, path1, initial_angle=0.0, arm_action='raise')

    # --- Path 2: Ball → Safepoint ---
    sp_cell = nearest_safepoint(ball_cell)
    path2 = plan_path(grid, ball_cell, sp_cell)
    angle_after_path2 = execute_path(robot, path2, initial_angle=angle_after_path1)

    # --- Path 3: Safepoint → Start ---
    path3 = plan_path(grid, sp_cell, start_cell)
    _ = execute_path(robot, path3, initial_angle=angle_after_path2)

    print("=== Flow complete ===")


if __name__ == '__main__':
    main()
